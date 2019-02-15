from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

import handle_datasets
from enum import Enum

import pickle


class Type(Enum):
    """Type enum for classifiers available."""
    BOW = 0
    NB = 1
    SVM = 2


def train_bow(train_set):
    """Bag of Words training algorithm.
    Count the number of occurences of words in both contexts and create a dictionary which gives the word polarity. It's
    calculated by adding on positive words and subtracting on negative. Positive scores are thus positive words and vice
    versa for negative.
    :param train_set dataset which the words are counted from.
    :return dictionary of words mapping to sentiment score.
    """
    positive_tweet_words = [word for line in train_set for word in handle_datasets.tokenize(line[0]) if line[1] == 1]
    negative_tweet_words = [word for line in train_set for word in handle_datasets.tokenize(line[0]) if line[1] == 0]
    word_sentiment_count = {}
    for word in positive_tweet_words:
        if word in word_sentiment_count.keys():
            curr_count = word_sentiment_count[word]
        else:
            curr_count = 0
        word_sentiment_count.update({word: curr_count + 1})
    for word in negative_tweet_words:
        if word in word_sentiment_count.keys():
            curr_count = word_sentiment_count[word]
        else:
            curr_count = 0
        word_sentiment_count.update({word: curr_count - 1})
    return word_sentiment_count


def predict_bow(word_count, test):
    """Predict sentiment for a test dataset using a BoW dictionary.
    The passed in dictionary is created with the BoW training algorithm and determines the polarity of words. For each
    test text, all words are looked up in the dictionary and for those present the score is modified by adding or
    subtracting 1. If the text's final score i 0 or more, it's considered positive.
    :param word_count dictionary of words to sentiment scores giving their polarities.
    :param test dataset tested on.
    :return tuple of real classes and predicted classes of the test dataset.
    """
    predictions = []
    for review, sentiment in test:
        score = 0
        tokens = handle_datasets.tokenize(review)
        for token in tokens:
            if token in word_count.keys():
                score += word_count[token]
        if score >= 0:
            predictions.append(1)
        else:
            predictions.append(0)
    return [t[1] for t in test], predictions


class Classifier:
    def __init__(self, classifier_type=Type.NB, unigrams=True, bigrams=False, presence=True, calibrating=False):
        """Represents any type of sentiment classifier with configurable settings.
        The classifier type is one of the Type class enums. For each, the type of tokens considered and the way of counting
        and testing them can be modified.
        :param classifier_type Type enum specifying what type of classifier this is.
        :param unigrams boolean whether unigrams should be counted.
        :param bigrams boolean whether bigrams should be counted.
        :param presence boolean whether frequency or the binary presence is counted.
        :param calibrating boolean whether thsi is meant to be tested on a validation set or not.
        """
        self.type = classifier_type     # Classifier type (NB or SVM).
        self.calibrating = calibrating  # Test settings on validation set.
        self.unigrams = unigrams        # Use unigrams as features.
        self.bigrams = bigrams          # Use bigrams as features.
        self.presence = presence        # Use presence (binary) or frequency as feature count.

    def train_classifier(self, train_set):
        """Train the classifier.
        Either call the train_bow method or create a pipeline with a CountVectorizer and an sklearn model to fit.
        :param train_set dataset for training
        :return model for later classification; In case of BoW, it's a dictionary; Otherwise it's a pipeline.
        """
        if self.type == Type.BOW:
            return train_bow(train_set)
        else:
            min_ngram = 1 if self.unigrams else 2
            max_ngram = 2 if self.bigrams else 1
            feature_extractor = CountVectorizer(binary=self.presence,
                                                ngram_range=(min_ngram, max_ngram))
            # Alpha is 1 for Laplace smoothing.
            # Linear kernel gives best results for this type of classification.
            # Need to specify gamma because it will soon be depreciated and otherwise it throws warnings.
            clf = SVC(gamma='auto', kernel='linear') if self.type == Type.SVM else MultinomialNB(alpha=1)
            pipeline = Pipeline([('vect', feature_extractor),
                                 ('tfidf', TfidfTransformer()),
                                 ('clf', clf)])
            pipeline.fit([t[0] for t in train_set], [t[1] for t in train_set])
            return pipeline

    def predict(self, classifier, test):
        """Predict the dataset using the classfier to evaluate it.
        :param classifier Classifier used for prediction
        :param test dataset use for evaluation
        :return real classes and predicted classes for the test dataset.
        """
        if self.type == Type.BOW:
            actual, predictions = predict_bow(classifier, test)
        else:
            predictions = []
            actual = []
            pred = classifier.predict([t[0] for t in test])
            for p, t in zip(pred, test):
                predictions.append(p)
                actual.append(t[1])
        return actual, predictions

    def classify(self, dataset):
        """Handle the dataset and use it for evaluating the classifier with either 10-fold cross-validation or the
        validation set.
        :param dataset collection of tuples (tweet text, sentiment 0 or 1).
        :return tuple of collections of real classes and prediction classes for the dataset
        """
        if not (self.unigrams or self.bigrams):
            print("At least one ngram option must be chosen. Unigrams will be used as default.")

        folds = handle_datasets.round_robin_split(dataset)
        predictions = []
        actual = []
        print(self.type)

        if self.calibrating:
            train_list = folds[1:]
            train = [item for sublist in train_list for item in sublist]
            test = folds[0]
            classifier = self.train_classifier(train)
            actual, predictions = self.predict(classifier, test)
        else:
            folds = folds[1:]
            for fold_ind in range(len(folds)):
                print("*", end=" ", flush=True)
                train_lists = folds[:fold_ind] + folds[fold_ind + 1:]
                train = [item for sublist in train_lists for item in sublist]
                test = folds[fold_ind]
                classifier = self.train_classifier(train)
                act, pred = self.predict(classifier, test)
                actual.extend(act)
                predictions.extend(pred)
        print("\n")
        return actual, predictions

    def train_and_pickle(self, dataset):
        """Train the classifier with a dataset and pickle it for reuse.
        :param dataset collection of tuples (tweet text, sentiment 0 or 1).
        """
        classifier = self.train_classifier(dataset)
        with open(handle_datasets.MODEL_PATH, "wb") as file:
            pickle.dump(classifier, file)
