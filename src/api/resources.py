from flask_restx import Namespace, Resource, fields
from urllib.parse import urlencode
from flask import request
from .models import register_models
from .utils import (
    countries_by_continent,
    country_info,
    forecast,
    temperature,
    forecast,
    favorites,
    favorite,
    unfavorite,
)

# Register the models
api_namespace = Namespace("Api", description="All API operations")
models = register_models(api_namespace)
continent_model = models["continent_model"]
country_model = models["country_model"]
favorite_model = models["favorite_model"]
forecast_model = models["forecast_model"]
temperature_model = models["temperature_model"]

# Each resource calls a method from utils. A 404 is returned at any error


@api_namespace.route("/continents/<string:continent_name>")
class ContinentResource(Resource):
    @api_namespace.response(200, "Success", models["continent_model"])
    @api_namespace.response(404, "Continent not found")
    def get(self, continent_name):
        """Retrieve all countries inside a continent"""
        try:
            countries = countries_by_continent(continent_name)
            return {"continent": continent_name, "countries": countries}, 200
        except ValueError as e:
            api_namespace.abort(404, e.__str__())


@api_namespace.route("/countries/<string:country_name>")
class CountryResource(Resource):
    @api_namespace.response(
        200,
        "Successful retrieval of country information",
        model=country_model,
    )
    @api_namespace.response(404, "Country not found")
    def get(self, country_name):
        """Retrieve information of a specific country"""
        try:
            info = country_info(country_name)
            return info, 200
        except Exception:
            api_namespace.abort(404, "Country not found or has no data")


@api_namespace.route("/countries/<string:country_name>/temperature")
class TemperatureResource(Resource):
    @api_namespace.response(200, "Success", temperature_model)
    @api_namespace.response(404, "No temperature data found")
    def get(self, country_name):
        """Retrieve the temperature from the capital city"""
        try:
            temp = temperature(country_name)
            return {"temperature": temp}, 200
        except Exception as e:
            api_namespace.abort(404, e.__str__())


@api_namespace.route("/countries/<string:country_name>/forecast")
class ForecastResource(Resource):
    @api_namespace.param(
        "days", "Number of days to forecast (between 1 and 5)", _in="query"
    )
    @api_namespace.response(200, "Success", forecast_model)
    @api_namespace.response(400, "Invalid number of days")
    @api_namespace.response(404, "No forecast available")
    def get(self, country_name):
        """Get a graph with forecast information for next n days"""
        days = request.args.get("days", default=1, type=int)
        if days < 1 or days > 5:
            api_namespace.abort(
                400,
                "Days must be greater than or equal to 1 and less than or equal to 5",
            )
        try:
            forecasts = forecast(country_name, days)
            labels = [f["time"] for f in forecasts]
            temps = [f["temperature"] for f in forecasts]

            # Create the request for QuickChart
            chart_config = {
                "type": "line",
                "data": {
                    "labels": labels,
                    "datasets": [
                        {
                            "label": f"3-Hourly Temperature Forecast for {days} Day(s)",
                            "data": temps,
                            "fill": 0,
                            "borderColor": "rgb(75, 192, 192)",
                            "tension": 0.1,
                        }
                    ],
                },
                "options": {
                    "title": {
                        "display": 1,
                        "text": f"Temperature Forecast for {country_name.title()}",
                    }
                },
            }

            chart_url = (
                f"https://quickchart.io/chart?c={urlencode({'c': str(chart_config)})}"
            )

            return {"forecast_url": chart_url}, 200
        except Exception as e:
            api_namespace.abort(404, e.__str__())


@api_namespace.route("/favorites")
class FavoriteListResource(Resource):
    @api_namespace.response(200, "List of favorites", [favorite_model])
    def get(self):
        """Retrieve a list of all favorite countries."""
        return {"favorites": favorites()}, 200


@api_namespace.route("/favorites/<string:country_name>")
class FavoriteResource(Resource):
    @api_namespace.expect(favorite_model)
    @api_namespace.response(200, "Country favorited")
    @api_namespace.response(404, "Country not found or already favorited")
    def post(self, country_name):
        """Add a country to favorites."""
        if favorite(country_name):
            return {"message": f"{country_name} has been added to favorites"}, 200
        else:
            api_namespace.abort(404, "Country not found or already favorited")

    @api_namespace.response(200, "Country unfavorited")
    @api_namespace.response(404, "Country not found or not in favorites")
    def delete(self, country_name):
        """Remove a country from favorites."""
        if unfavorite(country_name):
            return {"message": f"{country_name} has been removed from favorites"}, 200
        else:
            api_namespace.abort(404, "Country not found or not in favorites")
