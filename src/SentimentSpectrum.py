import src.utils as utils
from src.Classifier import Classifier
from src.Classifier import  Type
import pickle

class SentimentSpectrum(object):
    def __init__(self, build_new=False):
        if build_new:
            self.build_classifier()
        with open(utils.MODEL_PATH, "rb") as file:
            self.classifier = pickle.load(file)

        self.spectrum = []
        self.neg_count = 0
        self.pos_count = 0

    def build_classifier(self):
        dataset = utils.load_anonymized_sentiment_tweets(small=False)
        classifier = Classifier(unigrams=True, bigrams=True, classifier_type=Type.NB)
        classifier.train_and_pickle(dataset)

    def create_spectrum(self, tweets):
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
