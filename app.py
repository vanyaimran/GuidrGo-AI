
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

days = st.slider("Number of Days",1,14,3)

travel_type = st.selectbox(
    "Travel Type",
    ["Family","Luxury","Adventure","Honeymoon","Solo"]
)

if st.button("Generate Travel Report"):

   st.success(
    f"Generating trip from {start_city} to {destination}"
)

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
    elif destination == "Islamabad":
    st.write("Day 1: Faisal Mosque")
    st.write("Day 2: Daman-e-Koh")
    st.write("Day 3: Pakistan Monument")

    elif destination == "Lahore":
    st.write("Day 1: Badshahi Mosque")
    st.write("Day 2: Lahore Fort")
    st.write("Day 3: Food Street")

    elif destination == "Karachi":
    st.write("Day 1: Clifton Beach")
    st.write("Day 2: Mohatta Palace")
    st.write("Day 3: Port Grand")

    elif destination == "Peshawar":
    st.write("Day 1: Qissa Khwani Bazaar")
    st.write("Day 2: Bala Hisar Fort")
    st.write("Day 3: Peshawar Museum")

    elif destination == "Quetta":
    st.write("Day 1: Hanna Lake")
    st.write("Day 2: Quetta Museum")
    st.write("Day 3: Hazarganji National Park")

    elif destination == "Gilgit":
    st.write("Day 1: Kargah Buddha")
    st.write("Day 2: Naltar Valley")
    st.write("Day 3: Gilgit Bazaar")

    elif destination == "Fairy Meadows":
    st.write("Day 1: Fairy Meadows Trek")
    st.write("Day 2: Nanga Parbat Viewpoint")
    st.write("Day 3: Camping")

    elif destination == "Neelum Valley":
    st.write("Day 1: Keran")
    st.write("Day 2: Sharda")
    st.write("Day 3: Arang Kel")

    elif destination == "Chitral":
    st.write("Day 1: Chitral Fort")
    st.write("Day 2: Kalash Valley")
    st.write("Day 3: Shahi Mosque")

    elif destination == "Gwadar":
    st.write("Day 1: Gwadar Beach")
    st.write("Day 2: Hammerhead")
    st.write("Day 3: Marine Drive")
Added more destinations and itineraries
