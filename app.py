import os
import re

import requests
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
OPEN_WEATHER_MAP_API_KEY = os.getenv("OPEN_WEATHER_MAP_API_KEY")


def get_state_history(state):
    # Get the content of the state's Wikipedia page (lead section only)
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&titles={state}&explaintext=1&exintro=1" # noqa
    headers = {"User-Agent": "FlaskMapApp/1.0"}
    response = requests.get(url, headers=headers)
    data = response.json()
    page = next(iter(data["query"]["pages"].values()))
    state_text = page["extract"]

    # Extract the first 200 words of plain text from the state's Wikipedia page
    words = state_text.split()
    truncated_text = " ".join(words[:200])

    # Truncate at a period punctuation mark
    last_period = truncated_text.rfind(".")
    if last_period != -1:
        truncated_text = truncated_text[: last_period + 1]

    return truncated_text


def get_weather_data(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPEN_WEATHER_MAP_API_KEY}&units=imperial" # noqa
    response = requests.get(url)
    data = response.json()
    print(data)
    return data["weather"][0]["description"], data["main"]["temp"]


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        address = request.form["address"]
        return redirect(url_for("location", address=address))
    return render_template("home.html")


@app.route("/location/<address>")
def location(address):
    # Get city, state, and country name from the address
    parts = address.split(",")
    city = parts[-3].strip()
    state = None
    country = parts[-1].strip()

    # Fetch full state name from Google Maps Geocoding API
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_MAPS_API_KEY}" # noqa
    geocode_response = requests.get(geocode_url)
    geocode_data = geocode_response.json()
    address_components = geocode_data["results"][0]["address_components"]
    for component in address_components:
        if "administrative_area_level_1" in component["types"]:
            state = component["long_name"]
            break

    if state is None:
        # If state was not found in the address components, try to find it in the formatted address # noqa
        formatted_address = geocode_data["results"][0]["formatted_address"]
        state_regex = r",\s*([A-Za-z ]+?)(?:,|\s)\s*[A-Z]{2}\s*"
        state_match = re.search(state_regex, formatted_address)
        if state_match:
            state = state_match.group(1)

    if state is None:
        # If state still cannot be found, return an error page
        return render_template(
            "location_error.html", message="Could not find state in address."
        )  # noqa

    # Fetch city facts from Wikipedia
    state_history = get_state_history(state)

    # Fetch location coordinates
    location = geocode_data["results"][0]["geometry"]["location"]
    lat, lon = location["lat"], location["lng"]

    # Fetch current weather
    weather_description, current_temperature = get_weather_data(lat, lon)

    return render_template(
        "location.html",
        address=address,
        city=city,
        state=state,
        country=country,
        state_history=state_history,
        weather_description=weather_description,
        current_temperature=current_temperature,
    )


if __name__ == "__main__":
    app.run(debug=True)
