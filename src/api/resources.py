from flask_restful import Resource
from .utils import countries_by_continent, country_info, temperature


class ContinentResource(Resource):
    def get(self, continent_name):
        countries = countries_by_continent(continent_name)
        if countries:
            return {"continent": continent_name, "countries": countries}, 200
        else:
            return {"message": "Continent not found or has no countries"}, 404


class CountryResource(Resource):
    def get(self, country_name):
        info = country_info(country_name)
        if info:
            return info, 200
        else:
            return {"message": "Country not found or has no data"}, 404


class TemperatureResource(Resource):
    def get(self, country_name):
        temp = temperature(country_name)
        if temp:
            return {"temperature": temp}, 200
        else:
            return {"message": "Country not found or has no data"}, 404
