import argparse
import unittest
from flask import Flask
from flask_restx import Api
from src.api.resources import api_namespace
from src.api.utils import set_api_key


class APITestCase(unittest.TestCase):
    def setUp(self):
        # Reading the API key from a file
        with open("api_key", "r") as file:
            api_key = (
                file.read().strip()
            )  # .strip() to remove any surrounding whitespace/newlines

        if not api_key:
            raise ValueError("API key not found in file")
        set_api_key(api_key)
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_namespace(api_namespace, path="/api")
        self.client = self.app.test_client()

    def test_continent_endpoint(self):
        response = self.client.get("/api/continents/Europe")
        self.assertEqual(response.status_code, 200)

    def test_country_endpoint(self):
        response = self.client.get("/api/countries/Belgium")
        self.assertEqual(response.status_code, 200)

    def test_temperature_endpoint(self):
        response = self.client.get("/api/countries/Belgium/temperature")
        self.assertEqual(response.status_code, 200)

    def test_temperature_invalid_country(self):
        response = self.client.get("/api/countries/ChakaMaka/temperature")
        self.assertEqual(response.status_code, 404)

    def test_forecast_endpoint(self):
        response = self.client.get("/api/countries/Belgium/forecast")
        self.assertEqual(response.status_code, 200)

    def test_forecast_invalid_country(self):
        response = self.client.get("/api/countries/ChakaMaka/forecast")
        self.assertEqual(response.status_code, 404)

    def test_forecast_with_days_endpoint(self):
        response = self.client.get("/api/countries/Belgium/forecast?days=3")
        self.assertEqual(response.status_code, 200)

    def test_forecast_with_invalid_days_smaller(self):
        response = self.client.get("/api/countries/Belgium/forecast?days=0")
        self.assertEqual(response.status_code, 400)

    def test_forecast_with_invalid_days_larger(self):
        response = self.client.get("/api/countries/Belgium/forecast?days=6")
        self.assertEqual(response.status_code, 400)

    def test_forecast_with_edge_day_one(self):
        response = self.client.get("/api/countries/Belgium/forecast?days=1")
        self.assertEqual(response.status_code, 200)

    def test_forecast_with_edge_day_five(self):
        response = self.client.get("/api/countries/Belgium/forecast?days=5")
        self.assertEqual(response.status_code, 200)

    def test_forecast_without_args(self):
        response = self.client.get("/api/countries/Belgium/forecast")
        self.assertEqual(response.status_code, 200)

    def test_favorite_post_endpoint(self):
        response = self.client.post("/api/favorites/Belgium")
        self.assertEqual(response.status_code, 200)

    def test_favorite_get_endpoint(self):
        response = self.client.get("/api/favorites")
        self.assertEqual(response.status_code, 200)

    def test_favorite_delete_endpoint(self):
        # Posting a favorite first to ensure it exists for deletion
        self.client.post("/api/favorites/Belgium")
        response = self.client.delete("/api/favorites/Belgium")
        self.assertEqual(response.status_code, 200)

    def test_favorite_delete_not_found(self):
        # Posting a favorite first to ensure it exists for deletion
        response = self.client.delete("/api/favorites/Belgium")
        self.assertEqual(response.status_code, 404)

    def test_country_not_found(self):
        response = self.client.get("/api/countries/ChakaMaka")
        self.assertEqual(response.status_code, 404)

    def test_continent_not_found(self):
        response = self.client.get("/api/continents/Atlantis")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
