import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Weather Dashboard", layout="wide")

st.title("🌤️ Weather Data Dashboard")

API_KEY = "53e21889cc71d68dffa7019f696e13f4"

city = st.text_input("Enter City Name", "lonavala")

if st.button("Get Weather Data"):

    # Current Weather API
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]

        st.subheader(f"Current Weather in {city}")

        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature (°C)", temp)
        col2.metric("Humidity (%)", humidity)
        col3.metric("Pressure (hPa)", pressure)

        # 5 Day Forecast API
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()

        temps = []
        dates = []

        for item in forecast_data["list"]:
            temps.append(item["main"]["temp"])
            dates.append(item["dt_txt"])

        df = pd.DataFrame({
            "Date": pd.to_datetime(dates),
            "Temperature": temps
        })

        fig = px.line(df, x="Date", y="Temperature",
                      title=f"5-Day Temperature Forecast for {city}")

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("City not found or API error!")
