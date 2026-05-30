import streamlit as st
import googlemaps

# ==========================
# GOOGLE MAPS
# ==========================

API_KEY = "AIzaSyArdcZwlR4JZ4cWnxsA0SQOwIH-8-7GeUs"

gmaps = googlemaps.Client(key=API_KEY)

# ==========================
# FUNCTIONS
# ==========================

def get_hotels(city):

    try:
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

    except:
        return []


def get_attractions(city):

    try:
        places = gmaps.places(
            query=f"tourist attractions in {city} Pakistan"
        )

        attractions = []

        for place in places["results"][:10]:
            attractions.append(place["name"])

        return attractions

    except:
        return []


# ==========================
# PAGE
# ==========================

st.set_page_config(
    page_title="GuidrGo AI",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 GuidrGo AI Travel Assistant")

# ==========================
# INPUTS
# ==========================

start_city = st.selectbox(
    "Starting City",
    [
        "Lahore",
        "Islamabad",
        "Karachi",
        "Peshawar",
        "Quetta"
    ]
)

destination = st.selectbox(
    "Destination",
    [
        "Murree",
        "Naran",
        "Hunza",
        "Skardu",
        "Swat",
        "Islamabad",
        "Lahore",
        "Karachi",
        "Peshawar",
        "Quetta",
        "Gilgit",
        "Fairy Meadows",
        "Neelum Valley",
        "Chitral",
        "Gwadar"
    ]
)

days = st.slider(
    "Number of Days",
    1,
    14,
    3
)

travel_type = st.selectbox(
    "Travel Type",
    [
        "Family",
        "Luxury",
        "Adventure",
        "Honeymoon",
        "Solo"
    ]
)

# ==========================
# REPORT
# ==========================

if st.button("Generate Travel Report"):

    st.success(
        f"Generating trip from {start_city} to {destination}"
    )

    # WEATHER
    st.subheader("🌦 Weather Analysis")

    st.write("Weather API will be connected in Phase 2")

    # HOTELS

    st.subheader("🏨 Recommended Hotels")

    hotels = get_hotels(destination)

    if hotels:

        for hotel in hotels:

            st.write(
                f"⭐ {hotel['name']} | Rating: {hotel['rating']}"
            )

    else:

        st.write("No hotel data found")

    # TRAFFIC

    st.subheader("🚗 Traffic Analysis")

    st.write("Google Maps Route API coming in Phase 2")

    # ITINERARY

    st.subheader("🗺 Suggested Attractions")

    attractions = get_attractions(destination)

    if attractions:

        for i, attraction in enumerate(attractions, start=1):

            st.write(
                f"Day {i}: {attraction}"
            )

    else:

        st.write("No attractions found")




   
       
        
