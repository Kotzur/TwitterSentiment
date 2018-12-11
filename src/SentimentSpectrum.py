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

    def build_classifier(self):
        dataset = utils.load_anonymized_sentiment_tweets(small=False)
        classifier = Classifier(unigrams=True, bigrams=True, classifier_type=Type.NB)
        classifier.train_and_pickle(dataset)

    def create_spectrum(self, tweets):
        prediction_probabilities = self.classifier.predict_proba(tweets)
        sentiments = self.classifier.predict(tweets)
        confidences = [max(probs) for probs in prediction_probabilities]
        for sent, review, conf in zip(sentiments, tweets, confidences):
            print("Sent:", sent, conf, "Review:", review)
        negatives = [[conf, tweet] for sent, tweet, conf in zip(sentiments, tweets, confidences) if sent == 0]
        positives = [[conf, tweet] for sent, tweet, conf in zip(sentiments, tweets, confidences) if sent == 1]
        negatives_sorted = [tweet for _, tweet in sorted(negatives, reverse=True)]
        positives_sorted = [tweet for _, tweet in sorted(positives)]
        return negatives_sorted + positives_sorted


spectrum = SentimentSpectrum()
airline_data = utils.load_airline_tweets()
print(len(airline_data))
airline_tweets = [tweet for tweet, _ in airline_data[:10]]
print(spectrum.create_spectrum(airline_tweets))
