import argparse
import random

from utils import handle_datasets
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
    handle_datasets.save_results(json_data, filename)
    return "All good"


@app.route('/random/<string:topic>', methods=['GET'])
def get_random_tweet(topic):
    """Passes a random tweet not on topic."""
    topic_list = ["Trump", "NRA", "Obamacare", "Miley Cyrus", "Antivax",
                  "Immigration", "Israel", "Video game violence", "Voting age"]
    random_topic = random.choice(topic_list)
    while random_topic == topic:
        random_topic = random.choice(topic_list)

    dataset = handle_datasets.get_dataset(random_topic)
    spectrum = SentimentSpectrum()
    spectrum.create_spectrum(dataset)
    return spectrum.get_random_argument()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the server for the user study")
    parser.add_argument("--study", "-s", action="store", help="Study number.")
    args = parser.parse_args()
    handle_datasets.study_number = int(args.study)
    app.run()
