import unittest
from flask import Flask
from flask_restful import Api
from src.api.resources import (
    ContinentResource,
    CountryResource,
    TemperatureResource,
    FavoriteResource,
)


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(ContinentResource, "/continent/<string:continent_name>")
        self.api.add_resource(CountryResource, "/country/<string:country_name>")
        self.api.add_resource(TemperatureResource, "/temperature/<string:country_name>")
        self.api.add_resource(
            FavoriteResource, "/favorites/<string:country_name>", "/favorites"
        )
        self.client = self.app.test_client()

    def test_continent_endpoint(self):
        response = self.client.get("/continent/Europe")
        self.assertEqual(response.status_code, 200)

    def test_country_endpoint(self):
        response = self.client.get("/country/USA")
        self.assertEqual(response.status_code, 200)

    def test_temperature_endpoint(self):
        response = self.client.get("/temperature/USA")
        self.assertEqual(response.status_code, 200)

    def test_temperature_with_days_endpoint(self):
        response = self.client.get("/temperature/USA?days=3")
        self.assertEqual(response.status_code, 200)

    def test_favorite_post_endpoint(self):
        response = self.client.post("/favorites/USA")
        self.assertEqual(response.status_code, 200)

    def test_favorite_get_endpoint(self):
        response = self.client.get("/favorites")
        self.assertEqual(response.status_code, 200)

    def test_favorite_delete_endpoint(self):
        self.client.post("/favorites/USA")
        response = self.client.delete("/favorites/USA")
        self.assertEqual(response.status_code, 200)

    def test_country_not_found(self):
        response = self.client.get("/country/ChakaMaka")
        self.assertEqual(response.status_code, 404)

    def test_continent_not_found(self):
        response = self.client.get("/continent/Atlantis")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
