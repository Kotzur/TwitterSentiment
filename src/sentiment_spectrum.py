import random

import handle_datasets
from classifier import Classifier
from classifier import Type
import pickle
import json
import math


class Argument:
    def __init__(self, t, sup, neg, prob, word_probs):
        self.tweet = t
        self.support = sup
        self.negative = neg
        self.class_prob = prob
        self.word_probs = word_probs


class SentimentSpectrum(object):
    def __init__(self, build_new=False, word_probs=True):
        """Represents a spectrum of Tweets from most negative to most positive on a specific topic.
        :param build_new boolean whether to retrain and pickle a classifier before loading it."""
        self.word_probs = word_probs
        if build_new:
            self.build_classifier()

        with open(handle_datasets.MODEL_PATH, "rb") as file:
            self.classifier = pickle.load(file)

        # Spectrum from most prob negative to most prob positive arguments.
        self.spectrum = []
        # All negative arguments from the most to least probable.
        self.negative = []
        # All positive arguments from the most to lest probable.
        self.positive = []

    def build_classifier(self):
        """Create a new classifier and pickle it."""
        dataset = handle_datasets.load_anonymized_sentiment_tweets(small=False)
        classifier = Classifier(unigrams=True, bigrams=False, classifier_type=Type.NB)
        classifier.train_and_pickle(dataset)

    def create_spectrum(self, tweets):
        """Classify tweets and sort them in order of their sentiment increasing in positivity.
        Use the probability percentage as indication of how strongly positive or negative a tweet is and use it to order
        them.
        :param tweets set of unlabelled strings
        """
        prediction_probabilities = self.classifier.predict_proba(tweets)
        sentiments = self.classifier.predict(tweets)
        confidences = [max(probs) for probs in prediction_probabilities]
        negatives = []
        positives = []
        for sent, tweet, conf in zip(sentiments, tweets, confidences):
            if sent == 0:
                word_probs = self.get_word_probabilities(tweet, True)
                new_tweet = Argument(t=tweet, sup=[], neg=True, prob=conf, word_probs=word_probs)
                negatives.append(new_tweet)
            else:
                word_probs = self.get_word_probabilities(tweet, False)
                new_tweet = Argument(t=tweet, sup=[], neg=False, prob=round(conf, 5), word_probs=word_probs)
                positives.append(new_tweet)

        # Sort the lists of tweets accord to their confidence values.
        negatives.sort(key=lambda x: x.class_prob, reverse=True)
        positives.sort(key=lambda x: x.class_prob)

        self.spectrum = negatives + positives
        self.negative = negatives
        positives.reverse()
        self.positive = positives

    def get_word_probabilities(self, tweet, sentiment):
        feature_log_probs = self.classifier.named_steps["clf"].feature_log_prob_
        vocabulary_mapping = self.classifier.named_steps["vect"].vocabulary_

        word_probs = {}
        for word in tweet.split():
            if word in vocabulary_mapping:
                word_probs[word] = round(math.exp(
                    feature_log_probs[0 if sentiment is True else 1][vocabulary_mapping[word]]), 5)
            else:
                # Because of Laplace smoothing, unknown words are given 1/N prob where N is the number of words the
                # classifier trained on.
                word_probs[word] = 1 / len(feature_log_probs)
        return word_probs

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
            index = int(len(self.negative) * tweet_prob)
        else:
            index = int(len(self.spectrum) * tweet_prob)
        step = total // 5
        offset = skip // 5
        indecies = [((index + i*step) + offset) % total for i in range(0, 5)]
        alternatives = [self.spectrum[i].tweet for i in indecies]
        return alternatives

    def get_json_arguments(self):
        """Creates arguments for the debate and prepares them for sending with HTTP.
        9 positive and negative tweets are chosen from across their spectrum and their neighboring tweets are taken as
        supporting messages. Put into the Argument class format, the same used on the client side, the arguments are
        then JSON serialised.
        :return json list of argument objects 9 negative followed by 9 positive.
        """
        max_argument_count = min(len(self.positive) // 4, len(self.negative) // 4, 9)

        main_indecies = [4 * i for i in range(0, max_argument_count)]

        arguments = self.assign_supporting_arguments(main_indecies)

        return json.dumps([arg.__dict__ for arg in arguments])

    def get_random_argument(self):
        rand_arg = random.choice(self.positive + self.negative)
        if rand_arg in self.positive:
            index = self.positive.index(rand_arg)
            arg_list = self.positive
        else:
            index = self.negative.index(rand_arg)
            arg_list = self.negative
        sup = []
        for sup_number in range(1, 4):
            if index + sup_number >= len(arg_list):
                print("Length", len(arg_list))
                print("INdex", index)
                print("supnumber", sup_number)
                sup.append(arg_list[len(arg_list) - sup_number - 1].tweet)
            else:
                sup.append(arg_list[index + sup_number].tweet)
        rand_arg.support = sup
        return json.dumps(rand_arg.__dict__)

    def assign_supporting_arguments(self, main_indecies):
        arguments = []
        for argument_list in [self.negative, self.positive]:
            for i, index in enumerate(main_indecies):
                sup = []
                for sup_number in range(1, 4):
                    sup.append(argument_list[index + sup_number].tweet)
                main_arg = argument_list[index]
                main_arg.support = sup
                arguments.append(main_arg)
        return arguments
