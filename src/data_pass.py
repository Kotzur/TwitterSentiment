import handle_datasets
from sentiment_spectrum import SentimentSpectrum

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

in_making = False


@app.route('/spectrum/<string:topic>')
def get_spectrum(topic):
    """Responds to topic requests with a json list of argument objects for a given topic."""
    spectrum = SentimentSpectrum()
    dataset = handle_datasets.get_dataset(topic)
    spectrum.create_spectrum(dataset)
    return spectrum.get_json_arguments()
# Check if using the tflrd gives better resurts


if __name__ == "__main__":
    app.run()
