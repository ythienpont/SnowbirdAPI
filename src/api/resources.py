from flask_restful import Resource
from flask import request
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


class ContinentResource(Resource):
    def get(self, continent_name):
        try:
            countries = countries_by_continent(continent_name)
            return {"continent": continent_name, "countries": countries}, 200
        except ValueError as e:
            return {"message": str(e)}, 404


class CountryResource(Resource):
    def get(self, country_name):
        try:
            info = country_info(country_name)
            return info, 200
        except Exception:
            return {"message": "Country not found or has no data"}, 404


class TemperatureResource(Resource):
    def get(self, country_name):
        days = request.args.get("days", default=1, type=int)

        try:
            if days == 1:
                forecasts = [
                    temperature(country_name)
                ]  # Ensuring single day temp is also returned as a list
            else:
                forecasts = forecast(country_name, days)
            return {"forecasts": forecasts}, 200
        except Exception as e:
            return {"message": str(e)}, 404


class FavoriteResource(Resource):
    def get(self):
        """Get all favorite countries."""
        return {"favorites": favorites()}, 200

    def post(self, country_name):
        """Favorite a country."""
        if favorite(country_name):
            return {"message": f"{country_name} has been added to favorites"}, 200
        else:
            return {"message": "Country not found or already favorited"}, 404

    def delete(self, country_name):
        """Unfavorite a country."""
        if unfavorite(country_name):
            return {"message": f"{country_name} has been removed from favorites"}, 200
        else:
            return {"message": "Country not found or not in favorites"}, 404
