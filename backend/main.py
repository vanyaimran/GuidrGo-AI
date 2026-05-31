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
def analyze_hotel_reviews(city):

    analyzed_reviews = []

    try:

        hotel_results = gmaps.places(
            query=f"best hotels in {city} Pakistan"
        )

        if not hotel_results["results"]:
            return []

        place_id = hotel_results["results"][0]["place_id"]

        details = gmaps.place(
            place_id=place_id,
            fields=["reviews"]
        )

        google_reviews = details["result"].get(
            "reviews",
            []
        )

        for review in google_reviews:

            text = review.get("text", "")

            sentiment = analyze_sentiment(text)

            analyzed_reviews.append({
                "review": text,
                "sentiment": sentiment["label"],
                "score": sentiment["score"]
            })

    except Exception as e:

        analyzed_reviews.append({
            "review": str(e),
            "sentiment": "Error",
            "score": 0
        })

    return analyzed_reviews
    # ==========================
# LIVE GOOGLE REVIEWS
# ==========================
def get_live_reviews(place_id):

    try:

        details = gmaps.place(
            place_id=place_id,
            fields=["reviews"]
        )

        reviews = []

        for review in details["result"].get("reviews", []):

            text = review.get("text", "")

            sentiment = analyze_sentiment(text)

            reviews.append({
                "review": text,
                "sentiment": sentiment["label"],
                "score": sentiment["score"]
            })

        return reviews

    except Exception as e:

        print(e)

        return []


@app.get("/reviews/{city}")
def reviews(city: str):
    return analyze_hotel_reviews(city)

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
# TEST LIVE REVIEWS
# ==========================
@app.get("/test-reviews/{city}")
def test_reviews(city: str):

    try:

        hotels = gmaps.places(
            query=f"best hotels in {city} Pakistan"
        )

        first_hotel = hotels["results"][0]

        place_id = first_hotel["place_id"]

        return get_live_reviews(place_id)

    except Exception as e:

        return {
            "error": str(e)
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

    # ==========================
# SMART HOTEL RECOMMENDER
# ==========================
@app.get("/recommend/{city}/{preference}")
def recommend_hotel(city: str, preference: str):

   @app.get("/recommend/{city}/{preference}")
def recommend_hotel(city: str, preference: str):

    try:

        results = gmaps.places(
            query=f"{preference} hotels in {city} Pakistan"
        )

        hotels = results.get("results", [])

        if not hotels:

            return {
                "recommended_hotel": "No hotel found",
                "reviews": []
            }

        best_hotel = hotels[0]

        return {
            "recommended_hotel": best_hotel["name"],
            "reviews": [
                f"Rating: {best_hotel.get('rating', 'N/A')}",
                f"Recommended for: {preference}"
            ]
        }

    except Exception as e:

        return {
            "recommended_hotel": "Error",
            "reviews": [str(e)]
        }

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
       "reviews": analyze_hotel_reviews(city),
        "trip_plan": trip_plan
    }
