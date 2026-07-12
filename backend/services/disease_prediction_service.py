import os
import json
import numpy as np
import tensorflow as tf
import logging
from ml.preprocessing.image_preprocessor import preprocess_image_for_mobilenet

logger = logging.getLogger(__name__)

class DiseasePredictionService:
    def __init__(self, model_path, class_names_path):
        self.model_path = model_path
        self.class_names_path = class_names_path
        self.model = None
        self.class_names = []
        self.initialization_error = None
        
        self.load_model_and_classes()
        
    def load_model_and_classes(self):
        """
        Loads the Keras model and class names from configuration paths.
        Validates model output classes match class names list length.
        """
        # 1. Validate class_names.json existence
        if not os.path.exists(self.class_names_path):
            self.initialization_error = "CLASS_NAMES_NOT_FOUND"
            logger.error(f"Class names file not found at: {self.class_names_path}")
            return
            
        try:
            with open(self.class_names_path, 'r') as f:
                self.class_names = json.load(f)
            if not isinstance(self.class_names, list) or len(self.class_names) == 0:
                self.initialization_error = "INVALID_CLASS_NAMES"
                logger.error("Class names JSON must be a non-empty list.")
                return
        except Exception as e:
            self.initialization_error = "INVALID_CLASS_NAMES"
            logger.error(f"Failed to parse class names JSON: {str(e)}")
            return
            
        # 2. Validate model file existence
        if not os.path.exists(self.model_path):
            self.initialization_error = "MODEL_FILE_NOT_FOUND"
            logger.error(f"Model file not found at: {self.model_path}")
            return
            
        # 3. Load Keras model using TensorFlow
        try:
            self.model = tf.keras.models.load_model(self.model_path)
            logger.info("TensorFlow Keras model loaded successfully.")
        except Exception as e:
            self.initialization_error = "MODEL_LOAD_FAILED"
            logger.error(f"Failed to load Keras model: {str(e)}")
            return
            
        # 4. Validate output layer matches class names count
        try:
            output_shape = self.model.output_shape
            # output_shape is typically (None, num_classes)
            num_classes = output_shape[-1]
            if len(self.class_names) != num_classes:
                self.initialization_error = "CLASS_MISMATCH"
                logger.error(
                    f"Model output classes count ({num_classes}) does not match class_names.json count ({len(self.class_names)})"
                )
                self.model = None
        except Exception as e:
            self.initialization_error = "MODEL_VALIDATION_FAILED"
            logger.error(f"Failed to validate model shape: {str(e)}")
            self.model = None

    def is_available(self):
        return self.model is not None

    def get_error_code(self):
        return self.initialization_error or "MODEL_NOT_AVAILABLE"

    def predict(self, file_storage):
        """
        Executes prediction on an uploaded image.
        Returns: Dict containing success flag, prediction data, or error details.
        """
        if not self.is_available():
            return {
                "success": False,
                "error": {
                    "code": "MODEL_NOT_AVAILABLE",
                    "message": f"Deep learning model is not available on this server (Code: {self.get_error_code()})."
                }
            }
            
        try:
            # Apply preprocessing
            preprocessed_input = preprocess_image_for_mobilenet(file_storage)
            
            # Perform prediction
            predictions = self.model.predict(preprocessed_input)
            
            # Extract predicted index and confidence percentage
            pred_idx = int(np.argmax(predictions[0]))
            confidence = float(predictions[0][pred_idx]) * 100.0
            
            if pred_idx >= len(self.class_names):
                return {
                    "success": False,
                    "error": {
                        "code": "PREDICTION_FAILED",
                        "message": f"Predicted index {pred_idx} is out of bounds for the loaded class names."
                    }
                }
                
            predicted_class = self.class_names[pred_idx]
            
            return {
                "success": True,
                "data": {
                    "predictedClass": predicted_class,
                    "confidence": float(round(confidence, 2))
                }
            }
        except Exception as e:
            logger.error(f"Deep learning inference failed: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": "PREDICTION_FAILED",
                    "message": "Unable to analyze the uploaded crop leaf image."
                }
            }
