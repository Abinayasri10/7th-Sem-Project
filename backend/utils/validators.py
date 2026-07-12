from datetime import datetime

def validate_crop_health_input(data):
    """
    Validates crop health request payload.
    Expected payload format:
    {
        "latitude": float (between -90 and 90),
        "longitude": float (between -180 and 180),
        "startDate": "YYYY-MM-DD",
        "endDate": "YYYY-MM-DD",
        "indexType": "NDVI" or "NDWI"
    }
    Returns: (is_valid, error_message)
    """
    if not isinstance(data, dict):
        return False, "Request payload must be a JSON object."

    required_fields = ["latitude", "longitude", "startDate", "endDate", "indexType"]
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

    # Validate Coordinates
    try:
        lat = float(data["latitude"])
        lon = float(data["longitude"])
    except (ValueError, TypeError):
        return False, "latitude and longitude must be numbers."

    if not (-90 <= lat <= 90):
        return False, "latitude must be between -90 and 90."
    
    if not (-180 <= lon <= 180):
        return False, "longitude must be between -180 and 180."

    # Validate indexType
    if data["indexType"] not in ["NDVI", "NDWI"]:
        return False, "indexType must be either 'NDVI' or 'NDWI'."

    # Validate Dates
    try:
        start_date = datetime.strptime(data["startDate"], "%Y-%m-%d").date()
        end_date = datetime.strptime(data["endDate"], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return False, "startDate and endDate must be in 'YYYY-MM-DD' format."

    if start_date >= end_date:
        return False, "startDate must be strictly before endDate."

    # Get current date in server local time
    today = datetime.now().date()
    if end_date > today:
        return False, f"endDate cannot be in the future (today is {today})."

    return True, None
