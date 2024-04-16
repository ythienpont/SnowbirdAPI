import requests

favorite_countries = set()
API_KEY = None


def set_api_key(key: str):
    global API_KEY
    API_KEY = key


# Returns a list of all continents in a format compatible with the REST Countries API.
def continents():
    return ["Asia", "Africa", "North America", "South America", "Europe"]


# Fetches countries from a specified continent (region) using the REST Countries API.
def countries_by_continent(continent_name: str) -> list:
    # Capitalize the first letter of each word to match the API's naming convention
    continent_name = continent_name.title()

    # Check if the provided continent name is valid
    if continent_name not in continents():
        valid_continents = ", ".join(continents())
        raise ValueError(
            f"Invalid continent: {continent_name}. Valid continents are: {valid_continents}"
        )

    # Construct the URL for the API request by appending the continent name to the base region URL.
    REGION_URL = f"https://restcountries.com/v3.1/region/{continent_name}"
    try:
        response = requests.get(
            REGION_URL
        )  # Send a GET request to the constructed URL.
        response.raise_for_status()  # If the response status code indicates an error, raise HTTPError.
        data = response.json()  # Parse the JSON response into a Python dictionary

        # Extract the common name of each country from the response data and compile a list of these names.
        countries = [country["name"]["common"] for country in data]

        return countries  # Return the list of country names.
    except requests.exceptions.HTTPError as http_err:
        raise Exception(f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise Exception(f"An error occurred: {err}")


def country_info(country_name: str) -> dict:
    # Capitalize the first letter of each word to match the API's naming convention
    country_name = country_name.title()

    # Construct the URL for the API request by appending the continent name to the base region URL.
    COUNTRY_URL = f"https://restcountries.com/v3.1/name/{country_name}"
    try:
        response = requests.get(
            COUNTRY_URL
        )  # Send a GET request to the constructed URL.
        response.raise_for_status()  # If the response status code indicates an error, raise HTTPError.
        data = response.json()[0]  # Parse the JSON response into a Python dictionary

        # A country can have multiple capitals (e.g South Africa), return the first if it exists, default to "Unknown"
        capital = (
            data.get("capital", ["Unknown"])[0] if data.get("capital") else "Unknown"
        )
        # Get relevant fields from data, default to "Unknown"
        population = data.get("population", "Unknown")
        area = data.get("area", "Unknown")

        latlng = data.get("latlng", ["Unknown", "Unknown"])

        if latlng and len(latlng) == 2:
            latitude, longitude = latlng
        else:
            latitude, longitude = ("Unknown", "Unknown")

        return {
            "name": country_name,
            "capital": capital,
            "population": population,
            "area": area,
            "latitude": latitude,
            "longitude": longitude,
        }  # Return the relevant country info as dictionary
    except requests.exceptions.HTTPError as http_err:
        raise Exception(f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise Exception(f"An error occurred: {err}")


def temperature(country_name: str) -> float:
    country_details = country_info(country_name)
    lat = country_details["latitude"]
    lon = country_details["longitude"]

    global API_KEY
    URL = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    response = requests.get(URL)
    response.raise_for_status()  # This will raise an exception for HTTP errors

    data = response.json()
    temperature = data["main"]["temp"]

    return temperature


def forecast(country_name: str, days: int) -> list:
    country_details = country_info(country_name)
    lat = country_details["latitude"]
    lon = country_details["longitude"]

    global API_KEY
    URL = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    response = requests.get(URL)
    response.raise_for_status()  # This will raise an exception for HTTP errors

    data = response.json()
    # Calculate how many 3-hour intervals are there in `n` days
    forecast_limit = 8 * days  # there are 8 intervals of 3 hours in one day

    forecasts = []
    for i in range(min(forecast_limit, len(data["list"]))):
        forecast_entry = data["list"][i]
        forecasts.append(
            {
                "time": forecast_entry["dt_txt"],
                "temperature": forecast_entry["main"]["temp"],
            }
        )

    return forecasts


def favorite(country_name: str) -> bool:
    """Mark a country as a favorite."""
    global favorite_countries
    country_details = country_info(country_name)
    if country_details:
        favorite_countries.add(country_name.title())
        return True
    return False


def unfavorite(country_name: str) -> bool:
    """Remove a country from favorites."""
    global favorite_countries
    if country_name in favorite_countries:
        favorite_countries.remove(country_name.title())
        return True
    return False


def favorites() -> list:
    """List all favorited countries."""
    global favorite_countries
    return list(favorite_countries)
