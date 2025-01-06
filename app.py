import streamlit as st
import requests
import pandas as pd
from datetime import datetime

API_KEY = "1508ab52824d4f1fa290aeb3d55765cd"
BASE_URL = "https://api.weatherbit.io/v2.0/forecast/daily"

REGIONS = [
    "Tashkent", "Samarqand", "Bukhara", "Khiva", "Namangan",
    "Andijan", "Fergana", "Nukus", "Karshi", "Termez",
    "Jizzakh", "Gulistan"
]

def fetch_weather_data(city):
    params = {
        "city": city,
        "key": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data for {city}. Status code: {response.status_code}")
        return None

def process_weather_data(data):
    forecast = data.get("data", [])
    processed_data = []
    for day in forecast:
        processed_data.append({
            "Date": day["valid_date"],
            "Temp (°C)": day["temp"],
            "Max Temp (°C)": day["max_temp"],
            "Min Temp (°C)": day["min_temp"],
            "Description": day["weather"]["description"],
            "Wind Speed (m/s)": day["wind_spd"],
            "Precipitation (mm)": day["precip"],
            "Humidity (%)": day["rh"]
        })
    return processed_data

st.title("O'zbekiston viloyatlari uchun ob-havo prognozi")

region = st.selectbox("Viloyatni tanlang:", REGIONS)

if st.button("Prognozni ko'rish"):
    weather_data = fetch_weather_data(region)
    if weather_data:
        city_name = weather_data.get("city_name", "Unknown")
        country_code = weather_data.get("country_code", "Unknown")
        st.subheader(f"{city_name}, {country_code} uchun 15 kunlik prognoz")

        forecast_data = process_weather_data(weather_data)
        forecast_df = pd.DataFrame(forecast_data)
        
        st.dataframe(forecast_df)

        st.line_chart(forecast_df.set_index("Date")["Temp (°C)"])

        st.write("*Ma'lumotlar Weatherbit API orqali taqdim etildi.")


