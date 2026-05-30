from fastapi import FastAPI
import googlemaps
import requests
import os

app = FastAPI()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)


def get_weather(city):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"

        response = requests.get(url)
        data = response.json()

        return {
            "temperature": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "humidity": data["current"]["humidity"],
            "wind_kph": data["current"]["wind_kph"]
        }

    except Exception as e:
        return {
            "error": str(e)
        }


@app.get("/")
def home():
    return {
        "message": "GuidrGo AI Backend Running"
    }


@app.get("/debug")
def debug():
    return {
        "weather_key_exists": WEATHER_API_KEY is not None,
        "google_key_exists": GOOGLE_MAPS_API_KEY is not None
    }


@app.get("/travel/{city}")
def get_travel_data(city: str):

    hotels = []
    attractions = []

    try:
        hotel_results = gmaps.places(
            query=f"best hotels in {city} Pakistan"
        )

        for hotel in hotel_results["results"][:5]:
            hotels.append({
                "name": hotel["name"],
                "rating": hotel.get("rating")
            })

    except:
        pass

    try:
        attraction_results = gmaps.places(
            query=f"tourist attractions in {city} Pakistan"
        )

        for attraction in attraction_results["results"][:10]:
            attractions.append(
                attraction["name"]
            )

    except:
        pass

    weather = get_weather(city)

    return {
        "city": city,
        "weather": weather,
        "hotels": hotels,
        "attractions": attractions
    }
