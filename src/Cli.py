import sys

from src.SentimentSpectrum import SentimentSpectrum
import src.utils as utils


class Cli(object):
    def __init__(self):
        self.central = ""
        self.tweets = []
        self.spectrum = SentimentSpectrum()
        self.topic = ""

    def init_prompt(self):
        self.topic = input("Enter topic:")
        self.central = input("Enter a tweet you agree with.")
        dataset = utils.get_dataset(self.topic)
        self.spectrum.create_spectrum(dataset)
        self.print_alternative_views()

    def prompt(self):
        print()
        print("Enter 'M' to display more.")
        print("Enter Tweet number to explore it.")
        print("Enter a new Tweet you want to explore.")
        print("Enter 'N' to change a topic.")
        print("Enter 0 to exit.")
        return input()

    def print_alternative_views(self, skip=0):
        print("Alternative views:")
        alternatives = self.spectrum.get_alternatives(self.central, skip)
        for i, alter in enumerate(alternatives):
            print(f"{i + skip}. {alter}")

    def get_tweet(self, index):
        return self.tweets[index]

    def set_central(self, tweet):
        self.central = tweet
        print(f'The new central tweet is "{self.central}".')