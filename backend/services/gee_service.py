import json
import ee
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Track if Earth Engine was successfully initialized
_gee_initialized = False

def initialize_gee(key_path):
    """
    Initializes Google Earth Engine using a service account private key.
    Reads client_email and project_id from the JSON.
    Returns: (success, error_message)
    """
    global _gee_initialized
    try:
        with open(key_path, 'r') as f:
            key_data = json.load(f)
            
        email = key_data.get("client_email")
        project = key_data.get("project_id")
        
        if not email:
            return False, "Service account JSON is missing 'client_email'."
            
        credentials = ee.ServiceAccountCredentials(email, key_path)
        ee.Initialize(credentials)
        _gee_initialized = True
        logger.info("Google Earth Engine initialized successfully.")
        return True, None
    except Exception as e:
        _gee_initialized = False
        err_msg = f"Failed to initialize Google Earth Engine: {str(e)}"
        logger.error(err_msg)
        return False, err_msg

def is_gee_ready():
    return _gee_initialized

def analyze_crop_health(latitude, longitude, start_date_str, end_date_str, index_type):
    """
    Runs Earth Engine analysis.
    Returns a dict with results or raises ValueError/RuntimeError on failure.
    """
    if not _gee_initialized:
        raise RuntimeError("Google Earth Engine is not initialized.")
        
    farm_point = ee.Geometry.Point([float(longitude), float(latitude)])
    
    # Load Sentinel-2 harmonized collection
    collection = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(farm_point)
        .filterDate(start_date_str, end_date_str)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
    )
    
    # Check if collection is empty
    count = int(collection.size().getInfo())
    if count == 0:
        return {
            "success": False,
            "error_code": "NO_IMAGERY",
            "message": "No cloud-free Sentinel-2 satellite images were found for the selected date range."
        }
        
    # Get the latest image sorted by capture time
    latest_image = collection.sort("system:time_start", False).first()
    
    # Get capture date
    time_start = latest_image.get("system:time_start").getInfo()
    capture_date = datetime.utcfromtimestamp(time_start / 1000.0).strftime('%Y-%m-%d')
    
    # Calculate indices and visualization parameters
    if index_type == "NDVI":
        # NDVI formula B8 (NIR) and B4 (Red)
        index_image = latest_image.normalizedDifference(["B8", "B4"]).rename("NDVI")
        vis_params = {
            "min": 0,
            "max": 0.8,
            "palette": ["red", "yellow", "green"]
        }
        reducer_band = "NDVI"
    else:
        # NDWI formula B3 (Green) and B8 (NIR)
        index_image = latest_image.normalizedDifference(["B3", "B8"]).rename("NDWI")
        vis_params = {
            "min": -0.1,
            "max": 0.5,
            "palette": ["brown", "lightcyan", "blue"]
        }
        reducer_band = "NDWI"
        
    # Compute mean index value
    stats = index_image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=farm_point,
        scale=10
    )
    
    mean_val = stats.get(reducer_band).getInfo()
    if mean_val is None:
        raise ValueError("The farm location coordinate did not intersect with any valid satellite data.")
        
    score = float(round(mean_val, 4))
    
    # Compute rule-based insights and status
    status, insight = get_satellite_insights(score, index_type)
    
    # Generate Map ID and Tile URL
    vis_image = index_image.visualize(**vis_params)
    map_id = vis_image.getMapId()
    tile_url = map_id['tile_fetcher'].url_format
    
    return {
        "success": True,
        "data": {
            "latitude": float(latitude),
            "longitude": float(longitude),
            "captureDate": capture_date,
            "indexType": index_type,
            "score": score,
            "status": status,
            "insight": insight,
            "tileUrl": tile_url
        }
    }

def get_satellite_insights(score, index_type):
    """
    Computes threshold-based remote sensing interpretation.
    """
    if index_type == "NDVI":
        if score >= 0.6:
            return (
                "Excellent Vegetation Health",
                "Dense and healthy vegetation is detected. Maintain current crop management practices."
            )
        elif score >= 0.4:
            return (
                "Healthy Crop",
                "Crop vegetation appears healthy. Continue regular monitoring."
            )
        elif score >= 0.2:
            return (
                "Moderate Crop Stress",
                "Possible vegetation stress is detected. Check soil moisture and crop conditions."
            )
        else:
            return (
                "Severe Crop Stress",
                "Low vegetation activity is detected. Field inspection is recommended."
            )
    else:  # NDWI
        if score > 0.3:
            return (
                "High Moisture",
                "High water or moisture presence is detected."
            )
        elif score > 0:
            return (
                "Sufficient Moisture",
                "Current moisture conditions appear suitable."
            )
        elif score >= -0.2:
            return (
                "Moderate Water Stress",
                "Reduced moisture is detected. Monitor irrigation requirements."
            )
        else:
            return (
                "Severe Water Stress",
                "Significant water stress is detected. Irrigation assessment is recommended."
            )
