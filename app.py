
import streamlit as st

st.title("🌍 GuidrGo AI Travel Assistant")

start_city = st.selectbox(
    "Starting City",
    [
        "Lahore",
        "Islamabad",
        "Karachi",
        "Peshawar"
    ]
)

destination = st.selectbox(
    "Destination",
    [
        "Murree",
        "Naran",
        "Hunza",
        "Skardu",
        "Swat"
    ]
)

days = st.slider("Number of Days",1,14,3)

travel_type = st.selectbox(
    "Travel Type",
    ["Family","Luxury","Adventure","Honeymoon","Solo"]
)

if st.button("Generate Travel Report"):

    st.success(
    f"Generating trip from {start_city} to {destination}"
)
    st.subheader("🌦 Weather Analysis")
    st.write("Condition: Sunny")
    st.write("Temperature: 25°C")
    st.write("Risk Level: Low")

    st.subheader("🏨 Recommended Hotel")
    st.write("Grand Taj Hotel")
    st.write("Rating: 4.4/5")

    st.subheader("🚗 Traffic Analysis")
    st.write("Traffic Risk: Medium")

    st.subheader("🗺 Suggested Itinerary")

    if destination == "Murree":

    st.write("Day 1: Mall Road")
    st.write("Day 2: Patriata")
    st.write("Day 3: Kashmir Point")

elif destination == "Naran":

    st.write("Day 1: Lake Saif ul Malook")
    st.write("Day 2: Babusar Top")
    st.write("Day 3: Kunhar River")

elif destination == "Hunza":

    st.write("Day 1: Baltit Fort")
    st.write("Day 2: Attabad Lake")
    st.write("Day 3: Eagle Nest")

elif destination == "Skardu":

    st.write("Day 1: Shangrila Resort")
    st.write("Day 2: Upper Kachura Lake")
    st.write("Day 3: Deosai Plains")

elif destination == "Swat":

    st.write("Day 1: Mingora")
    st.write("Day 2: Malam Jabba")
    st.write("Day 3: Kalam Valley")
