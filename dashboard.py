
import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page settings
st.set_page_config(
    page_title="Weather Analytics Dashboard",
    page_icon="🌦️",
    layout="wide"
)

# Available cities and coordinates
cities = {
    "Pune": (18.5204, 73.8567),
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.6139, 77.2090),
    "Bengaluru": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Hyderabad": (17.3850, 78.4867)
}

# Sidebar settings
st.sidebar.header("Dashboard Settings")

selected_city = st.sidebar.selectbox(
    "Choose a city",
    list(cities.keys())
)

variables = {
    "Temperature": "Temperature",
    "Humidity": "Humidity",
    "Rainfall": "Rainfall",
    "Wind Speed": "Wind_Speed"
}

selected = st.sidebar.selectbox(
    "Choose a weather variable",
    list(variables.keys())
)

column = variables[selected]

# Load saved weather data
try:
    df = pd.read_csv("weather_data.csv")
    df["time"] = pd.to_datetime(df["time"])
except FileNotFoundError:
    st.error("weather_data.csv not found. Run main.py first.")
    st.stop()

# Refresh weather data for selected city
if st.sidebar.button("🔄 Refresh Weather Data"):
    try:
        url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": cities[selected_city][0],
            "longitude": cities[selected_city][1],
            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "wind_speed_10m"
            ],
            "forecast_days": 7,
            "timezone": "Asia/Kolkata"
        }

        with st.spinner("Fetching weather data..."):
            response = requests.get(
                url,
                params=params,
                timeout=30
            )
            response.raise_for_status()

            hourly = response.json()["hourly"]
            new_df = pd.DataFrame(hourly)

            new_df.rename(columns={
                "temperature_2m": "Temperature",
                "relative_humidity_2m": "Humidity",
                "precipitation": "Rainfall",
                "wind_speed_10m": "Wind_Speed"
            }, inplace=True)

            new_df["time"] = pd.to_datetime(new_df["time"])
            new_df.to_csv("weather_data.csv", index=False)

        st.success(f"Weather data updated for {selected_city}!")
        st.rerun()

    except Exception as e:
        st.error(f"Could not refresh weather data: {e}")

# Dashboard title
st.title(f"🌦️ Weather Analytics — {selected_city}")
st.write("Weather analysis using Python libraries")

# Summary cards
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Avg Temp",
    f"{df['Temperature'].mean():.1f} °C"
)

col2.metric(
    "Avg Humidity",
    f"{df['Humidity'].mean():.1f}%"
)

col3.metric(
    "Total Rain",
    f"{df['Rainfall'].sum():.1f} mm"
)

col4.metric(
    "Avg Wind",
    f"{df['Wind_Speed'].mean():.1f} km/h"
)

st.divider()

# Interactive time-series chart
st.subheader(f"{selected} Over Time")

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df["time"], df[column])
ax.set_xlabel("Time")
ax.set_ylabel(selected)
ax.tick_params(axis="x", rotation=45)
fig.tight_layout()

st.pyplot(fig)
plt.close(fig)

# Distribution chart
st.subheader(f"{selected} Distribution")

fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.histplot(
    data=df,
    x=column,
    bins=20,
    kde=True,
    ax=ax2
)
ax2.set_title(f"Distribution of {selected}")

st.pyplot(fig2)
plt.close(fig2)

# Weather data table
st.subheader("Weather Data")
st.dataframe(df, width="stretch")

# Download CSV
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Weather Data as CSV",
    data=csv,
    file_name="weather_data.csv",
    mime="text/csv"
)

