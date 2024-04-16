import requests

API_URL = "http://localhost:5000/api"


def get_countries_by_continent(continent_name):
    response = requests.get(f"{API_URL}/continents/{continent_name}")
    response.raise_for_status()
    return response.json()


def get_country_info(country_name):
    API_URL = (
        "http://localhost:5000/api"  # This should be replaced with your actual API URL
    )
    try:
        response = requests.get(f"{API_URL}/countries/{country_name}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def get_temperature(country_name):
    response = requests.get(f"{API_URL}/countries/{country_name}/temperature")
    response.raise_for_status()
    return response.json()


def favorite_country(country_name):
    response = requests.post(f"{API_URL}/favorites/{country_name}")
    if response.status_code == 200:
        print(f"{country_name} has been added to favorites")
    else:
        print(f"Error favoriting {country_name}")


def unfavorite_country(country_name):
    response = requests.delete(f"{API_URL}/favorites/{country_name}")
    if response.status_code == 200:
        print(f"{country_name} has been removed from favorites")
    else:
        print(f"Error unfavoriting {country_name}")


def list_favorites():
    response = requests.get(f"{API_URL}/favorites")
    response.raise_for_status()
    return response.json()


def get_forecast(country_name, days):
    response = requests.get(f"{API_URL}/countries/{country_name}/forecast?days={days}")
    response.raise_for_status()
    return response.json()


def main():
    south_american_countries = get_countries_by_continent("South America")["countries"]

    warmest_country = None
    highest_temp = -float("inf")

    for country in south_american_countries:
        temp_info = get_temperature(country)
        if temp_info["temperature"] > highest_temp:
            highest_temp = temp_info["temperature"]
            warmest_country = country

    if warmest_country is None:
        raise Exception("No warmest country found")

    print(
        f"The warmest country in South America is currently {warmest_country} with a temperature of {highest_temp}°C."
    )

    # Fetch and print information about Venezuela in a descriptive format
    country_data = get_country_info(warmest_country)
    if country_data:
        print(
            f"{warmest_country.title()} ({country_data['latitude']} lat., {country_data['longitude']} long.) is a country with a population of {country_data['population']} and an area of {country_data['area']}. The capital is {country_data['capital']}."
        )
    else:
        print("Failed to retrieve data.")

    favorite_country(warmest_country)
    print(f"Favorites: {list_favorites()['favorites']}")
    unfavorite_country(warmest_country)
    print(f"Favorites: {list_favorites()['favorites']}")

    forecast_data = get_forecast(warmest_country, 4)
    forecast_url = forecast_data["forecast_url"]
    print(forecast_url)


if __name__ == "__main__":
    main()
