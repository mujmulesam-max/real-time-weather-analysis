
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# ---------------------------------
# STEP 1: Set Pune location
# ---------------------------------

latitude = 18.5204
longitude = 73.8567

# ---------------------------------
# STEP 2: Weather API URL
# ---------------------------------

url = "https://api.open-meteo.com/v1/forecast"

# ---------------------------------
# STEP 3: Request weather data
# ---------------------------------

params = {
    "latitude": latitude,
    "longitude": longitude,
    "hourly": [
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "wind_speed_10m"
    ],
    "forecast_days": 7,
    "timezone": "Asia/Kolkata"
}

# ---------------------------------
# STEP 4: Fetch data from API
# ---------------------------------

response = requests.get(
    url,
    params=params,
    timeout=30
)

# Check whether the request was successful
response.raise_for_status()

# Convert JSON response into Python dictionary
data = response.json()

print("Weather data fetched successfully!")

# ---------------------------------
# STEP 5: Extract hourly data
# ---------------------------------

hourly_data = data["hourly"]

# ---------------------------------
# STEP 6: Create Pandas DataFrame
# ---------------------------------

df = pd.DataFrame(hourly_data)

# Convert time column into datetime format
df["time"] = pd.to_datetime(df["time"])

# Rename columns
df.rename(columns={
    "temperature_2m": "Temperature",
    "relative_humidity_2m": "Humidity",
    "precipitation": "Rainfall",
    "wind_speed_10m": "Wind_Speed"
}, inplace=True)

# ---------------------------------
# STEP 7: Display weather data
# ---------------------------------

print("\nWeather Data for Pune")

print(df.head(10))

# ---------------------------------
# STEP 8: Display information
# ---------------------------------

print("\nData Information")

print(df.info())

# ---------------------------------
# STEP 9: Save data into CSV
# ---------------------------------

df.to_csv("weather_data.csv", index=False)

print("\nWeather data saved successfully!")

# ---------------------------------
# STEP 10: NumPy Analysis
# ---------------------------------

# Convert temperature column into NumPy array
temperature = df["Temperature"].to_numpy()

# Calculate statistics
average_temp = np.mean(temperature)

maximum_temp = np.max(temperature)

minimum_temp = np.min(temperature)

std_temp = np.std(temperature)

median_temp = np.median(temperature)

# Display results
print("\n========== NUMPY ANALYSIS ==========")

print("Average Temperature:", round(average_temp, 2), "°C")

print("Maximum Temperature:", maximum_temp, "°C")

print("Minimum Temperature:", minimum_temp, "°C")

print("Median Temperature:", median_temp, "°C")

print("Standard Deviation:", round(std_temp, 2), "°C")

# ---------------------------------
# STEP 11: Pandas Analysis
# ---------------------------------

print("\n========== PANDAS ANALYSIS ==========")

# Basic statistical summary
print("\nStatistical Summary:")

print(df.describe())

# Average humidity
average_humidity = df["Humidity"].mean()

print("\nAverage Humidity:",
      round(average_humidity, 2), "%")

# Total rainfall
total_rainfall = df["Rainfall"].sum()

print("Total Rainfall:",
      round(total_rainfall, 2), "mm")

# Average wind speed
average_wind = df["Wind_Speed"].mean()

print("Average Wind Speed:",
      round(average_wind, 2), "km/h")

# Highest humidity
maximum_humidity = df["Humidity"].max()

print("Maximum Humidity:",
      maximum_humidity, "%")

# ---------------------------------
# STEP 12: Matplotlib Temperature Graph
# ---------------------------------

plt.figure(figsize=(12, 5))

plt.plot(
    df["time"],
    df["Temperature"],
    marker="o",
    linewidth=2,
    label="Temperature"
)

plt.title("Pune Weather Temperature Analysis")

plt.xlabel("Date and Time")

plt.ylabel("Temperature (°C)")

plt.xticks(rotation=45)

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.show()

# ---------------------------------
# STEP 13: Rainfall Analysis
# ---------------------------------

plt.figure(figsize=(12, 5))

plt.bar(
    df["time"],
    df["Rainfall"],
    width=0.03,
    label="Rainfall"
)

plt.title("Pune Rainfall Analysis")

plt.xlabel("Date and Time")

plt.ylabel("Rainfall (mm)")

plt.xticks(rotation=45)

plt.legend()

plt.grid(axis="y")

plt.tight_layout()

plt.show()

# ---------------------------------
# STEP 14: Wind Speed Analysis
# ---------------------------------

plt.figure(figsize=(12, 5))

plt.plot(
    df["time"],
    df["Wind_Speed"],
    color="green",
    marker="o",
    label="Wind Speed"
)

plt.title("Pune Wind Speed Analysis")

plt.xlabel("Date and Time")

plt.ylabel("Wind Speed (km/h)")

plt.xticks(rotation=45)

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.show()

# ---------------------------------
# STEP 15: Seaborn Scatter Plot
# ---------------------------------

plt.figure(figsize=(8, 5))

sns.scatterplot(
    data=df,
    x="Humidity",
    y="Temperature"
)

plt.title("Temperature vs Humidity in Pune")

plt.xlabel("Humidity (%)")

plt.ylabel("Temperature (°C)")

plt.grid(True)

plt.tight_layout()

plt.show()

# ---------------------------------
# STEP 16: Correlation Heatmap
# ---------------------------------

# Select numerical columns
weather_columns = [
    "Temperature",
    "Humidity",
    "Rainfall",
    "Wind_Speed"
]

# Calculate correlation
correlation = df[weather_columns].corr()

# Create heatmap
plt.figure(figsize=(8, 6))

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5
)

plt.title("Weather Variables Correlation Heatmap")

plt.tight_layout()

plt.show()

# ---------------------------------
# STEP 17: Temperature Distribution
# ---------------------------------

plt.figure(figsize=(8, 5))

sns.histplot(
    data=df,
    x="Temperature",
    bins=20,
    kde=True
)

plt.title("Temperature Distribution in Pune")

plt.xlabel("Temperature (°C)")

plt.ylabel("Frequency")

plt.tight_layout()

plt.show()
# Step 5: SciPy statistical analysis

# Convert time into numbers: 0, 1, 2, 3...
hours = np.arange(len(df))

# Calculate the linear trend in temperature
result = stats.linregress(hours, df["Temperature"])

print("\n--- SciPy Temperature Trend ---")
print("Temperature change per hour:", round(result.slope, 4))
print("Correlation with time:", round(result.rvalue, 4))
print("P-value:", round(result.pvalue, 4))

# Detect unusually high or low temperatures

z_scores = stats.zscore(df["Temperature"])

unusual = df[np.abs(z_scores) > 2]

print("\n--- Unusual Temperature Readings ---")

if unusual.empty:
    print("No unusual temperature readings found.")
else:
    print(unusual[["time", "Temperature"]])


