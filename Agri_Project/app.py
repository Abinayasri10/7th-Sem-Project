import streamlit as st
import ee
import folium
from streamlit_folium import st_folium
import datetime
from streamlit_geolocation import streamlit_geolocation
from geopy.geocoders import Nominatim

# 1. PAGE SETUP - MUST BE FIRST
st.set_page_config(page_title="Smart Agri Decision Support", layout="wide")

st.title("🌱 Real-Time Satellite Crop Health Monitor (Tamil Nadu)")

# Helper function for location name
def get_location_name(lat, lon):
    try:
        geolocator = Nominatim(user_agent="smart_agri_app")
        location = geolocator.reverse((lat, lon), language='en')
        return location.address if location else "Unknown Location"
    except:
        return "Location lookup failed"

# 2. INITIALIZATION
def initialize_gee():
    try:
        # FIXED: Removed the double .json extension
        key_path = r"D:\\7th-Sem-Project\\Agri_Project\\gee_credentials.json.json"
        credentials = ee.ServiceAccountCredentials(key_file=key_path)
        ee.Initialize(credentials)
        return True
    except Exception as e:
        st.error(f"Error initializing Earth Engine: {e}")
        return False

if initialize_gee():
    # 3. SIDEBAR CONFIGURATION
    st.sidebar.header("📍 Select Farm Location")
    
    # Auto-detect location
    location = streamlit_geolocation()
    
    if location and location.get('latitude') is not None:
        lat = location['latitude']
        lon = location['longitude']
        st.sidebar.success(f"📍 GPS Detected: {lat:.4f}, {lon:.4f}")
    else:
        st.sidebar.warning("GPS not detected. Using manual input:")
        lat = st.sidebar.number_input("Manual Latitude", value=11.2742, format="%.4f")
        lon = st.sidebar.number_input("Manual Longitude", value=77.5806, format="%.4f")
    
    # Display the Location Name
    location_name = get_location_name(lat, lon)
    st.sidebar.info(f"🌍 Address: {location_name}")
    
    farm_point = ee.Geometry.Point([lon, lat])

    st.sidebar.header("📅 Select Date Range")
    start_date = st.sidebar.date_input("Start Date", value=datetime.date(2026, 1, 1))
    end_date = st.sidebar.date_input("End Date", value=datetime.date(2026, 6, 30))

    index_type = st.sidebar.selectbox("Select Vegetation Index", ["NDVI (Crop Health)", "NDWI (Water Stress)"])

    # 4. PROCESSING MODULE
    s2_collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
        .filterBounds(farm_point) \
        .filterDate(str(start_date), str(end_date)) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))

    if s2_collection.size().getInfo() == 0:
        st.warning("⚠️ No cloud-free satellite images found for this date range.")
    else:
        latest_image = s2_collection.sort('system:time_start', False).first()
        capture_time = ee.Date(latest_image.get('system:time_start')).format('yyyy-MM-dd').getInfo()
        
        st.success(f"📡 Displaying data from satellite image captured on: **{capture_time}**")

        if index_type == "NDVI (Crop Health)":
            calculated_layer = latest_image.normalizedDifference(['B8', 'B4']).rename('NDVI')
            vis_params = {'min': 0, 'max': 0.8, 'palette': ['red', 'yellow', 'green']}
        else:
            calculated_layer = latest_image.normalizedDifference(['B3', 'B8']).rename('NDWI')
            vis_params = {'min': -0.1, 'max': 0.5, 'palette': ['brown', 'lightcyan', 'blue']}

        pixel_value = calculated_layer.reduceRegion(reducer=ee.Reducer.mean(), geometry=farm_point, scale=10).getInfo()
        current_score = list(pixel_value.values())[0] if pixel_value else 0

        # 5. UI DISPLAY
        col1, col2 = st.columns([1, 2])

        with col1:
            st.metric(label=f"Current {index_type.split()[0]} Score", value=f"{current_score:.4f}")
            st.subheader("💡 Decision Support Insights")
            if index_type == "NDVI (Crop Health)":
                st.info("🟢 Healthy" if current_score > 0.5 else "🔴 Stressed")
            else:
                st.info("💧 Sufficient Moisture" if current_score > 0 else "⚠️ Water Stress Detected")

        with col2:
            m = folium.Map(location=[lat, lon], zoom_start=14)
            map_id_dict = ee.Image(calculated_layer).getMapId(vis_params)
            folium.TileLayer(tiles=map_id_dict['tile_fetcher'].url_format, attr='Google Earth Engine').add_to(m)
            folium.Marker([lat, lon], popup=location_name).add_to(m)
            st_folium(m, width=700, height=450)