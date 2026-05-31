from fastapi import FastAPI
import googlemaps
import requests
import os
from textblob import TextBlob

app = FastAPI()

# API KEYS
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Google Maps Client
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)


# -----------------------------
# WEATHER FUNCTION
# -----------------------------
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


# -----------------------------
# SENTIMENT ANALYSIS
# -----------------------------
def analyze_sentiment(text):

    analysis = TextBlob(text)
    score = analysis.sentiment.polarity

    if score > 0:
        label = "Positive"
    elif score < 0:
        label = "Negative"
    else:
        label = "Neutral"

    return {
        "label": label,
        "score": score
    }


# -----------------------------
# HOME
# -----------------------------
@app.get("/")
def home():
    return {
        "message": "GuidrGo AI Backend Running"
    }


# -----------------------------
# DEBUG
# -----------------------------
@app.get("/debug")
def debug():
    return {
        "weather_key_exists": WEATHER_API_KEY is not None,
        "google_key_exists": GOOGLE_MAPS_API_KEY is not None
    }


# -----------------------------
# SENTIMENT API
# -----------------------------
@app.get("/sentiment/{text}")
def sentiment(text: str):
    return analyze_sentiment(text)


# -----------------------------
# TRAVEL API
# -----------------------------
@app.get("/travel/{city}")
def get_travel_data(city: str):

    hotels = []
    attractions = []

    # HOTELS
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

    # ATTRACTIONS
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

    # WEATHER
    weather = get_weather(city)

    # RISK ANALYSIS
    risk = "Low Risk"

    if weather and "temperature" in weather:

        if weather["temperature"] > 40:
            risk = "High Heat Risk"

        elif weather["wind_kph"] > 30:
            risk = "Medium Weather Risk"

    return {
        "city": city,
        "weather": weather,
        "risk_analysis": risk,
        "hotels": hotels,
        "attractions": attractions
    }
