
import streamlit as st

st.set_page_config(
    page_title="GuidrGo AI",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 GuidrGo AI Travel Assistant")

city = st.text_input("Destination")

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

if st.button("Generate Travel Report"):

    weather = get_weather(city)

    st.subheader("🌦 Weather")

    st.write("Condition:", weather["condition"])
    st.write("Temperature:", weather["temperature"], "°C")
    st.write("Humidity:", weather["humidity"], "%")
    st.write("Wind:", weather["wind"], "km/h")

    top_hotel = df_final.iloc[0]

    st.subheader("🏨 Recommended Hotel")

    st.write("Hotel:", top_hotel["Hotel"])
    st.write("Rating:", top_hotel["Google Rating"])
    st.write("AI Score:", top_hotel["Final AI Score"])
    st.write("Risk Score:", top_hotel["Risk Score"])

    traffic = traffic_risk(
        "Islamabad",
        city
    )

    st.subheader("🚗 Traffic Analysis")

    st.write("Traffic Risk:", traffic)

    st.subheader("🗺 Travel Itinerary")

    if city.lower() in ITINERARY_DATA:

        for day, activities in ITINERARY_DATA[city.lower()].items():

            st.markdown(f"### {day}")

            for activity in activities:

                st.write("✓", activity)
