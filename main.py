from fastapi import FastAPI
import googlemaps
import os

app = FastAPI()

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

gmaps = googlemaps.Client(key=API_KEY)

@app.get("/")
def home():
    return {
        "message": "GuidrGo Backend Running"
    }

@app.get("/hotels/{city}")
def get_hotels(city: str):

    places = gmaps.places(
        query=f"best hotels in {city} Pakistan"
    )

    hotels = []

    for place in places["results"][:5]:
        hotels.append({
            "name": place["name"],
            "rating": place.get("rating", "N/A")
        })

    return hotels


@app.get("/attractions/{city}")
def get_attractions(city: str):

    places = gmaps.places(
        query=f"tourist attractions in {city} Pakistan"
    )

    attractions = []

    for place in places["results"][:10]:
        attractions.append(
            place["name"]
        )

    return attractions
