import src.utils as utils
from src.Classifier import Classifier
from src.Classifier import  Type
import pickle
import json

class SentimentSpectrum(object):
    def __init__(self, build_new=False):
        """Represents a spectrum of Tweets from most negative to most positive on a specific topic.
        :param build_new boolean whether to retrain and pickle a classifier before loading it."""
        if build_new:
            self.build_classifier()
        with open(utils.MODEL_PATH, "rb") as file:
            self.classifier = pickle.load(file)

        self.spectrum = []
        self.neg_count = 0
        self.pos_count = 0

    def build_classifier(self):
        """Create a new classifier and pickle it."""
        dataset = utils.load_anonymized_sentiment_tweets(small=False)
        classifier = Classifier(unigrams=True, bigrams=True, classifier_type=Type.NB)
        classifier.train_and_pickle(dataset)

    def create_spectrum(self, tweets):
        """Classify tweets and sort them in order of their sentiment increasing in positivity.
        Use the probability percentage as indication of how strongly positive or negative a tweet is and use it to order
        them.
        :param set of unlabelled strings
        """
        prediction_probabilities = self.classifier.predict_proba(tweets)
        sentiments = self.classifier.predict(tweets)
        confidences = [max(probs) for probs in prediction_probabilities]
        negatives = [[conf, tweet] for sent, tweet, conf in zip(sentiments, tweets, confidences) if sent == 0]
        positives = [[conf, tweet] for sent, tweet, conf in zip(sentiments, tweets, confidences) if sent == 1]
        negatives_sorted = [tweet for _, tweet in sorted(negatives, reverse=True)]
        positives_sorted = [tweet for _, tweet in sorted(positives)]
        self.spectrum = negatives_sorted + positives_sorted
        self.neg_count = len(negatives_sorted)
        self.pos_count = len(positives_sorted)

    def get_alternatives(self, tweet, skip):
        """Returns a set of 5 tweets from across the spectrum around a tweet.
        The passed tweet needs to first be found on the spectrum determined by its classification confidence. The
        alternative tweets are chosen by sampling the spectrum at even intervals. The skip works as an offset so that
        similarily distant but different tweets are chosen.
        :param tweet text for which alternatives are found.
        :param skip number of tweets to skip when searching (offset)
        :return 5 alternative tweets.
        """
        tweet_sent = self.classifier.predict([tweet])
        tweet_prob = max(self.classifier.predict_proba([tweet])[0])
        total = len(self.spectrum)
        if tweet_sent == 0:
            tweet_prob = 1 - tweet_prob
            index = int(self.neg_count * tweet_prob)
        else:
            index = int(self.neg_count + self.pos_count * tweet_prob)
        step = total // 5
        offset = skip // 5
        indecies = [((index + i*step) + offset) % total for i in range(0, 5)]
        alternatives = [self.spectrum[i] for i in indecies]
        return alternatives

    def get_json_arguments(self):
        """Creates arguments for the debate and prepares them for sending with HTTP.
        9 positive and negative tweets are chosen from across their spectrum and their neighboring tweets are taken as
        supporting messages. Put into the Argument class format, the same used on the client side, the arguments are
        then JSON serialised.
        :return json list of argument objects 9 negative followed by 9 positive.
        """
        class Argument:
            def __init__(self, t, sup, neg):
                self.tweet = t
                self.support = sup
                self.negative = neg

        arguments = []
        # Assume that one argument consists of one main tweet and 3 supporting tweets = 4
        max_argument_count = min(self.pos_count // 4, self.neg_count // 4, 9)
        neg_main_indecies = [(self.neg_count // max_argument_count) * i for i in range(0, max_argument_count)]
        neg_support_indecies = [(index + i) for index in neg_main_indecies for i in range(1, 4)]
        pos_main_indecies = [self.neg_count + (self.pos_count // max_argument_count) * i for i in range(0, max_argument_count)]
        pos_support_indecies = [(index + i) for index in pos_main_indecies for i in range(1, 4)]

        for i, index in enumerate(neg_main_indecies):
            sup = []
            for sup_number in range(0, 3):
                sup_index = neg_support_indecies[sup_number + 3*i]
                sup.append(self.spectrum[sup_index])
            arguments.append(Argument(self.spectrum[index], sup, True))
        for i, index in enumerate(pos_main_indecies):
            sup = []
            for sup_number in range(0, 3):
                sup_index = pos_support_indecies[sup_number + 3*i]
                sup.append(self.spectrum[sup_index])
            arguments.append(Argument(self.spectrum[index], sup, False))
        # First element of the list is the number of arguments being sent.
        return json.dumps([arg.__dict__ for arg in arguments])
