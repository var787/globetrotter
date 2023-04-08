# Globetrotter

Globetrotter is a Flask web application that allows users to get information about a location by entering its address. The app retrieves the city, state, and country name from the address and uses various APIs to get additional information about the location, such as its history, current weather, and a map of the location.

Requirements
Globetrotter requires the following:

Python 3.6+
Flask 2.0.1
requests 2.25.1
The following API keys are also required:

Google Maps Geocoding API key
OpenWeatherMap API key
Setup
Clone the repository:

bash
Copy code
git clone <https://github.com/your-username/globetrotter.git>
Install the required packages:

bash
Copy code
pip install -r requirements.txt
Set the API keys as environment variables:

bash
Copy code
`export GOOGLE_MAPS_API_KEY=<your-google-maps-api-key>`
`export OPEN_WEATHER_MAP_API_KEY=<your-openweathermap-api-key>`
Start the Flask server:

bash
Copy code
flask run
Open the app in your web browser at <http://localhost:5000>
