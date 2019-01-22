import os

from src import utils
from src.SentimentSpectrum import SentimentSpectrum

from flask import Flask, json
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

in_making = False

@app.route('/spectrum/<string:topic>')
def get_spectrum(topic):
    """Responds to topic requests with a json list of argument objects for a given topic."""
    spectrum = SentimentSpectrum()
    dataset = utils.get_dataset(topic)
    spectrum.create_spectrum(dataset)
    return spectrum.get_json_arguments()


if __name__ == "__main__":
    output = get_spectrum("trump")
    print(output)
