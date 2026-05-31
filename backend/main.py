from fastapi import FastAPI
import googlemaps
import requests
import os
from textblob import TextBlob

app = FastAPI()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)


# ==========================
# WEATHER
# ==========================
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


# ==========================
# NLP SENTIMENT ANALYSIS
# ==========================
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
        "score": round(score, 2)
    }


# ==========================
# REVIEW ANALYSIS
# ==========================
def analyze_hotel_reviews():

    reviews = [
        "Amazing hotel and staff",
        "Rooms were dirty and uncomfortable",
        "Excellent experience and location",
        "Bad service and rude staff",
        "Loved the food and hospitality",
        "Terrible management",
        "Very clean and peaceful place"
    ]

    analyzed_reviews = []

    for review in reviews:

        sentiment = analyze_sentiment(review)

        analyzed_reviews.append({
            "review": review,
            "sentiment": sentiment["label"],
            "score": sentiment["score"]
        })

    return analyzed_reviews


# ==========================
# TRAVEL SCORE
# ==========================
def calculate_travel_score(weather, hotels, attractions):

    score = 5

    try:

        if weather.get("temperature", 0) < 35:
            score += 2

        score += min(len(attractions) / 2, 2)

        if hotels:

            ratings = [
                h["rating"]
                for h in hotels
                if h["rating"] is not None
            ]

            if ratings:
                score += sum(ratings) / len(ratings) / 5

    except:
        pass

    return round(min(score, 10), 1)


# ==========================
# AI TRIP PLANNER
# ==========================
def generate_trip_plan(city):

    return {
        "day_1": [
            f"Explore famous attractions in {city}",
            "Visit local market"
        ],

        "day_2": [
            "Visit top tourist spots",
            "Enjoy local cuisine"
        ],

        "day_3": [
            "Photography and sightseeing",
            "Shopping and souvenirs"
        ]
    }


# ==========================
# HOME
# ==========================
@app.get("/")
def home():
    return {
        "message": "GuidrGo AI Backend Running"
    }


# ==========================
# DEBUG
# ==========================
@app.get("/debug")
def debug():

    return {
        "weather_key_exists": WEATHER_API_KEY is not None,
        "google_key_exists": GOOGLE_MAPS_API_KEY is not None
    }


# ==========================
# SENTIMENT API
# ==========================
@app.get("/sentiment/{text}")
def sentiment(text: str):

    return analyze_sentiment(text)


# ==========================
# REVIEW API
# ==========================
@app.get("/reviews")
def reviews():

    return analyze_hotel_reviews()


# ==========================
# TRAVEL API
# ==========================
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

    risk = "Low Risk"

    try:

        if weather["temperature"] > 40:
            risk = "High Risk"

        elif weather["wind_kph"] > 30:
            risk = "Medium Risk"

    except:
        pass

    travel_score = calculate_travel_score(
        weather,
        hotels,
        attractions
    )

    trip_plan = generate_trip_plan(city)

    return {
        "city": city,
        "weather": weather,
        "risk_analysis": risk,
        "travel_score": travel_score,
        "hotels": hotels,
        "attractions": attractions,
        "reviews": analyze_hotel_reviews(),
        "trip_plan": trip_plan
    }
