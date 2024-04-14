from flask import Flask
from flask_restful import Api

from src.api.resources import (
    ContinentResource,
    CountryResource,
    TemperatureResource,
    FavoriteResource,
)

app = Flask(__name__)
api = Api(app)

api.add_resource(ContinentResource, "/countries/<string:continent_name>")
api.add_resource(CountryResource, "/country/<string:country_name>")
api.add_resource(TemperatureResource, "/temperature/<string:country_name>")
api.add_resource(FavoriteResource, "/favorites", "/favorites/<string:country_name>")

if __name__ == "__main__":
    app.run(debug=True)
