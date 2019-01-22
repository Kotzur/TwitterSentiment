from src.SentimentSpectrum import SentimentSpectrum
import src.utils as utils


class Cli(object):
    def __init__(self):
        """The command line interface."""
        self.central = ""
        self.tweets = []
        self.spectrum = SentimentSpectrum()
        self.topic = ""

    def init_prompt(self):
        """Prompts to choose a new topic."""
        self.topic = input("Enter topic:")
        self.central = input("Enter a tweet you agree with.")
        dataset = utils.get_dataset(self.topic)
        self.spectrum.create_spectrum(dataset)
        self.print_alternative_views()

    def prompt(self):
        """Prompts with interaction options."""
        print()
        print("Enter 'M' to display more.")
        print("Enter Tweet number to explore it.")
        print("Enter a new Tweet you want to explore.")
        print("Enter 'N' to change a topic.")
        print("Enter 0 to exit.")
        return input()

    def print_alternative_views(self, skip=0):
        """Prints views alternative to the central one.
        :param skip number of alternative views already printed."""
        print("Alternative views:")
        alternatives = self.spectrum.get_alternatives(self.central, skip)
        for i, alter in enumerate(alternatives):
            print(f"{i + skip}. {alter}")

    def get_tweet(self, index):
        """Returns a tweet with index from alternative tweets printed."""
        return self.tweets[index]

    def set_central(self, tweet):
        """Changes the central tweet to a passed one."""
        self.central = tweet
        print(f'The new central tweet is "{self.central}".')
