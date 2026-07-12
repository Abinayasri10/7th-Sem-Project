from flask import Flask, jsonify
from flask_cors import CORS
import logging
import os

from config import Config
from routes.crop_health_routes import crop_health_blueprint
from routes.disease_routes import disease_blueprint
from services.gee_service import initialize_gee
from services.disease_prediction_service import DiseasePredictionService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": Config.CORS_ORIGINS}})

    # 1. Initialize Google Earth Engine on startup
    gee_key = Config.GEE_PRIVATE_KEY_PATH
    if os.path.exists(gee_key):
        logger.info(f"Initializing Earth Engine with key: {gee_key}")
        # Note: Do not print actual credentials inside logs for security.
        success, err = initialize_gee(gee_key)
        if not success:
            logger.error(f"Google Earth Engine initialization failed: {err}")
    else:
        logger.warning(
            f"GEE service account key not found at '{gee_key}'. GEE functionalities will return GEE_INIT_FAILED."
        )

    # 2. Preload TensorFlow Disease Prediction Service
    logger.info("Initializing Disease Prediction Service (preloading TensorFlow model)...")
    prediction_service = DiseasePredictionService(Config.MODEL_PATH, Config.CLASS_NAMES_PATH)
    # Attach to app context for route access
    app.prediction_service = prediction_service

    # 3. Register Blueprints
    app.register_blueprint(crop_health_blueprint, url_prefix='/api/crop-health')
    app.register_blueprint(disease_blueprint, url_prefix='/api/disease')

    # 4. Error handlers
    @app.errorhandler(413)
    def request_entity_too_large(error):
        max_mb = Config.MAX_CONTENT_LENGTH / (1024 * 1024)
        return jsonify({
            "success": False,
            "error": {
                "code": "INVALID_IMAGE",
                "message": f"Upload payload exceeds maximum allowable size of {max_mb:.1f}MB."
            }
        }), 413

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": {
                "code": "NOT_FOUND",
                "message": "Resource not found."
            }
        }), 404

    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.exception("An unhandled exception occurred:")
        return jsonify({
            "success": False,
            "error": {
                "code": "SERVER_ERROR",
                "message": "An internal server error occurred."
            }
        }), 500

    return app

if __name__ == '__main__':
    flask_app = create_app()
    port = Config.PORT
    logger.info(f"Starting Smart Agri Flask Backend on port {port}...")
    flask_app.run(host='0.0.0.0', port=port, debug=Config.DEBUG)
