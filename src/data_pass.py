from src import utils
from src.SentimentSpectrum import SentimentSpectrum

import sys

if __name__ == "__main__":
    topic = sys.argv[1]
    spectrum = SentimentSpectrum()
    dataset = utils.get_dataset(topic)
    spectrum.create_spectrum(dataset)
    output = ""
    for s in spectrum.spectrum:
        output += s + " "
    print(output)
    # spectrum.write_to_json()
