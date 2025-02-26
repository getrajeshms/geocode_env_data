import streamlit as st
import csv
import requests

# Google Maps Geocoding API
def get_geocoding_google(address, api_key):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
    return None, None

# OpenWeatherMap Air Pollution API
def get_environmental_data(lat, lon, api_key):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Function to save data to CSV
def save_to_csv(data, filename):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Address", "Latitude", "Longitude", "Air Quality Index", "CO", "NO2", "O3", "SO2", "PM2_5", "PM10"])
        writer.writerow(data)

# Streamlit App
def main():
    st.title("Institute of Public Health - Geocoding and Environmental Data App")
    st.write("Enter an address in India to fetch its geocoding and environmental data.")

    # Input fields for API keys
    google_maps_api_key = st.text_input("Enter your Google Maps API Key:", type="password")
    openweathermap_api_key = st.text_input("Enter your OpenWeatherMap API Key:", type="password")

    # Input address from the user
    address = st.text_input("Enter the address in India:")

    if st.button("Fetch Data"):
        if not google_maps_api_key or not openweathermap_api_key:
            st.error("Please enter both API keys.")
        elif not address:
            st.error("Please enter an address.")
        else:
            # Get geocoding using Google Maps API
            lat, lon = get_geocoding_google(address, google_maps_api_key)
            if lat is None or lon is None:
                st.error("Geocoding failed. Please check the address and try again.")
            else:
                st.success(f"Geocoding successful! Latitude: {lat}, Longitude: {lon}")

                # Get environmental data (air quality)
                environmental_data = get_environmental_data(lat, lon, openweathermap_api_key)
                if environmental_data:
                    st.success("Environmental data fetched successfully.")

                    # Extract air quality data
                    aqi = environmental_data['list'][0]['main']['aqi']
                    components = environmental_data['list'][0]['components']

                    # Display results
                    st.subheader("Results")
                    st.write(f"**Air Quality Index (AQI):** {aqi}")
                    st.write(f"**CO (Carbon Monoxide):** {components.get('co', 'N/A')} μg/m³")
                    st.write(f"**NO2 (Nitrogen Dioxide):** {components.get('no2', 'N/A')} μg/m³")
                    st.write(f"**O3 (Ozone):** {components.get('o3', 'N/A')} μg/m³")
                    st.write(f"**SO2 (Sulfur Dioxide):** {components.get('so2', 'N/A')} μg/m³")
                    st.write(f"**PM2.5 (Fine Particulate Matter):** {components.get('pm2_5', 'N/A')} μg/m³")
                    st.write(f"**PM10 (Coarse Particulate Matter):** {components.get('pm10', 'N/A')} μg/m³")

                    # Prepare data for CSV
                    csv_data = [
                        address, lat, lon, aqi,
                        components.get('co', 'N/A'), components.get('no2', 'N/A'),
                        components.get('o3', 'N/A'), components.get('so2', 'N/A'),
                        components.get('pm2_5', 'N/A'), components.get('pm10', 'N/A')
                    ]

                    # Save data to CSV
                    csv_filename = "geocoding_environmental_data_india.csv"
                    save_to_csv(csv_data, csv_filename)

                    # Provide download link for CSV
                    with open(csv_filename, "rb") as file:
                        btn = st.download_button(
                            label="Download CSV",
                            data=file,
                            file_name=csv_filename,
                            mime="text/csv"
                        )
                else:
                    st.error("Failed to fetch environmental data.")

# Run the Streamlit app
if __name__ == "__main__":
    main()