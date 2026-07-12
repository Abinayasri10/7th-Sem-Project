from flask import Blueprint, request, jsonify
from utils.validators import validate_crop_health_input
from services.location_service import get_location_name
from services.gee_service import analyze_crop_health
import logging

logger = logging.getLogger(__name__)

crop_health_blueprint = Blueprint('crop_health', __name__)

@crop_health_blueprint.route('/analyze', methods=['POST'])
def analyze():
    """
    POST /api/crop-health/analyze
    Analyzes crop health (NDVI or NDWI) for a given location and date range.
    """
    try:
        data = request.get_json()
    except Exception:
        return jsonify({
            "success": False,
            "error": {
                "code": "INVALID_INPUT",
                "message": "Malformed JSON payload in request."
            }
        }), 400

    # 1. Validate Input
    is_valid, err_msg = validate_crop_health_input(data)
    if not is_valid:
        return jsonify({
            "success": False,
            "error": {
                "code": "INVALID_INPUT",
                "message": err_msg
            }
        }), 400

    lat = float(data["latitude"])
    lon = float(data["longitude"])
    start_date = data["startDate"]
    end_date = data["endDate"]
    index_type = data["indexType"]

    # 2. Get Geocoded Location Name (failure is non-fatal)
    location_name = get_location_name(lat, lon)

    # 3. Call Earth Engine processing pipeline
    try:
        result = analyze_crop_health(lat, lon, start_date, end_date, index_type)
        
        if not result.get("success", False):
            # Known domain error, e.g. NO_IMAGERY
            error_code = result.get("error_code", "SERVER_ERROR")
            message = result.get("message", "Satellite analysis failed.")
            return jsonify({
                "success": False,
                "error": {
                    "code": error_code,
                    "message": message
                }
            }), 400

        # Inject reverse geocoded location address into the response
        response_data = result["data"]
        response_data["location"] = location_name

        return jsonify({
            "success": True,
            "data": response_data
        })

    except RuntimeError as re:
        # Handles case when GEE is not initialized
        logger.error(f"GEE execution runtime error: {str(re)}")
        return jsonify({
            "success": False,
            "error": {
                "code": "GEE_INIT_FAILED",
                "message": "Google Earth Engine service is not initialized on the backend. Please check setup."
            }
        }), 500
    except ValueError as ve:
        # Handles coordinate out of imagery bounds
        logger.error(f"GEE processing value error: {str(ve)}")
        return jsonify({
            "success": False,
            "error": {
                "code": "INVALID_INPUT",
                "message": str(ve)
            }
        }), 400
    except Exception as e:
        logger.error(f"GEE analysis unexpected failure: {str(e)}")
        return jsonify({
            "success": False,
            "error": {
                "code": "SERVER_ERROR",
                "message": f"An unexpected error occurred during GEE analysis: {str(e)}"
            }
        }), 500
