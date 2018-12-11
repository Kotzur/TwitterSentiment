from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

from src import utils
from enum import Enum

import pickle


class Type(Enum):
    BOW = 0
    NB = 1
    SVM = 2


def train_bow(train_set):
    positive_tweet_words = [word for line in train_set for word in utils.tokenize(line[0]) if line[1] == 1]
    negative_tweet_words = [word for line in train_set for word in utils.tokenize(line[0]) if line[1] == 0]
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
    predictions = []
    for review, sentiment in test:
        score = 0
        tokens = utils.tokenize(review)
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
        self.type = classifier_type     # Classifier type (NB or SVM).
        self.calibrating = calibrating  # Test settings on validation set.
        self.unigrams = unigrams        # Use unigrams as features.
        self.bigrams = bigrams          # Use bigrams as features.
        self.presence = presence        # Use presence (binary) or frequency as feature count.

    def train_classifier(self, train_set):
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
                                 ('clf', clf)])
            pipeline.fit([t[0] for t in train_set], [t[1] for t in train_set])
            return pipeline

    def predict(self, classifier, test):
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
        if not (self.unigrams or self.bigrams):
            print("At least one ngram option must be chosen. Unigrams will be used as default.")

        folds = utils.round_robin_split(dataset)
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
        return actual, predictions

    def train_and_pickle(self, dataset):
        classifier = self.train_classifier(dataset)
        with open(utils.MODEL_PATH, "wb") as file:
            pickle.dump(classifier, file)
