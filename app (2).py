
import streamlit as st

st.title("🌍 GuidrGo AI Travel Assistant")

city = st.text_input("Destination")

days = st.slider("Number of Days",1,14,3)

travel_type = st.selectbox(
    "Travel Type",
    ["Family","Luxury","Adventure","Honeymoon","Solo"]
)

if st.button("Generate Travel Report"):
    st.success(f"Generating report for {city}")
