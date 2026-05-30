from fastapi import FastAPI
import googlemaps
import os

app = FastAPI()

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

gmaps = googlemaps.Client(key=API_KEY)


@app.get("/")
def home():
    return {
        "message": "GuidrGo AI Backend Running"
    }


@app.get("/travel/{city}")
def get_travel_data(city: str):

    hotels = []
    attractions = []

    try:
        hotel_results = gmaps.places(
            query=f"best hotels in {city} Pakistan"
        )

        for place in hotel_results["results"][:5]:
            hotels.append({
                "name": place["name"],
                "rating": place.get("rating", "N/A")
            })

    except:
        hotels = []

    try:
        attraction_results = gmaps.places(
            query=f"tourist attractions in {city} Pakistan"
        )

        for place in attraction_results["results"][:10]:
            attractions.append(place["name"])

    except:
        attractions = []

    return {
        "city": city,
        "hotels": hotels,
        "attractions": attractions
    }
