from flask import Blueprint, request, jsonify, current_app
from utils.image_validator import validate_uploaded_image
import logging

logger = logging.getLogger(__name__)

disease_blueprint = Blueprint('disease', __name__)

@disease_blueprint.route('/predict', methods=['POST'])
def predict():
    """
    POST /api/disease/predict
    Expects multipart/form-data with file upload field 'image'.
    Runs leaf disease detection using preloaded TensorFlow Keras model.
    """
    # 1. Check if prediction service is registered in Flask app
    prediction_service = getattr(current_app, 'prediction_service', None)
    if not prediction_service:
        return jsonify({
            "success": False,
            "error": {
                "code": "MODEL_NOT_AVAILABLE",
                "message": "Disease prediction service is not initialized on the server."
            }
        }), 500

    # 2. Extract image from request files
    if 'image' not in request.files:
        return jsonify({
            "success": False,
            "error": {
                "code": "INVALID_INPUT",
                "message": "Missing file payload with key 'image'."
            }
        }), 400

    image_file = request.files['image']

    # 3. Validate image upload
    allowed_exts = current_app.config.get('ALLOWED_EXTENSIONS')
    max_size = current_app.config.get('MAX_CONTENT_LENGTH')
    
    is_valid, err_code, err_msg = validate_uploaded_image(image_file, allowed_exts, max_size)
    if not is_valid:
        return jsonify({
            "success": False,
            "error": {
                "code": err_code,
                "message": err_msg
            }
        }), 400

    # 4. Trigger TensorFlow model prediction
    result = prediction_service.predict(image_file)
    if not result.get("success", False):
        error_details = result.get("error", {})
        return jsonify({
            "success": False,
            "error": {
                "code": error_details.get("code", "PREDICTION_FAILED"),
                "message": error_details.get("message", "Unable to analyze the uploaded crop leaf image.")
            }
        }), 500

    return jsonify({
        "success": True,
        "data": result["data"]
    })
