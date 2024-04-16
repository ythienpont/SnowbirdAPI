import argparse
from flask import Flask
from flask_restx import Api
from src.api.resources import api_namespace
from src.api.utils import set_api_key

parser = argparse.ArgumentParser(description="Start Flask application.")
parser.add_argument("--api-key", type=str, required=True, help="OpenWeatherMap API key")
args = parser.parse_args()
set_api_key(args.api_key)

app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="SnowbirdAPI",
    description="An API for sunseekers",
)

api.add_namespace(api_namespace, path="/api")

if __name__ == "__main__":
    app.run(debug=True)
