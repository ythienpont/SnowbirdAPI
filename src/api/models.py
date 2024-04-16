from flask_restx import fields

from src.api.utils import forecast


# The models used for Swagger's API documentation
def register_models(api_namespace):
    continent_model = api_namespace.model(
        "Continents",
        {
            "continent": fields.String(
                required=True, description="The name of the continent"
            ),
            "countries": fields.List(
                fields.String, description="List of countries in the continent"
            ),
        },
    )

    country_model = api_namespace.model(
        "Countries",
        {
            "name": fields.String(
                required=True, description="The name of the country", example="Belgium"
            ),
            "capital": fields.String(description="Capital city", example="Brussels"),
            "population": fields.Integer(
                description="Population count", example=11555997
            ),
            "area": fields.Integer(description="Area of the country", example=30528),
            "latitude": fields.Float(description="Latitude", example=50.83333333),
            "longitude": fields.Float(description="Longitude", example=4),
        },
    )

    temperature_model = api_namespace.model(
        "Temperature",
        {"temperature": fields.Float(description="Current temperature in Celsius")},
    )

    forecast_model = api_namespace.model(
        "Forecast",
        {"forecast_url": fields.String(description="Url to the generated graph")},
    )

    favorite_model = api_namespace.model(
        "Favorites",
        {"country": fields.String(required=True, description="The country favorited")},
    )

    return {
        "continent_model": continent_model,
        "country_model": country_model,
        "favorite_model": favorite_model,
        "forecast_model": forecast_model,
        "temperature_model": temperature_model,
    }
