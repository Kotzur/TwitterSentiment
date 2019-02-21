import json
import os

import handle_datasets
from sentiment_spectrum import SentimentSpectrum

from flask import Flask
from flask import request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)


@app.route('/spectrum/<string:topic>', methods=['GET'])
def get_spectrum(topic):
    """Responds to topic requests with a json list of argument objects for a given topic."""
    spectrum = SentimentSpectrum()
    dataset = handle_datasets.get_dataset(topic)
    spectrum.create_spectrum(dataset)
    return spectrum.get_json_arguments()


@app.route('/results/<string:filename>', methods=['POST'])
def dump_results(filename):
    """Writes details of arguments from a complete session."""
    json_data = request.form
    with open(os.path.join(handle_datasets.DATA_DIR, filename), "w+") as file:
        json.dump(json_data, file)
    return "All good"


if __name__ == "__main__":
    app.run()
