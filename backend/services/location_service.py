from geopy.geocoders import Nominatim
import logging

logger = logging.getLogger(__name__)

def get_location_name(latitude, longitude):
    """
    Reverse geocodes coordinate using Geopy Nominatim.
    Returns: string address or fallback coordinate format on error.
    """
    fallback_name = f"Lat {latitude:.4f}, Lon {longitude:.4f}"
    try:
        # Nominatim requires a distinct, descriptive user_agent header
        geolocator = Nominatim(user_agent="smart_agri_decision_support_platform")
        location = geolocator.reverse((latitude, longitude), timeout=5)
        
        if location and location.address:
            return location.address
            
        return fallback_name
    except Exception as e:
        logger.error(f"Geocoding failed for {latitude}, {longitude}: {str(e)}")
        # Reverse geocoding failure must not block analysis
        return fallback_name
