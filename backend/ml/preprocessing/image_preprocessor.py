import numpy as np
from PIL import Image
import tensorflow as tf

def preprocess_image_for_mobilenet(file_storage, target_size=(224, 224)):
    """
    Preprocesses an uploaded image file for MobileNetV2.
    - Loads the image file using PIL
    - Converts it to RGB
    - Resizes to target_size (default: 224x224)
    - Converts it to numpy array
    - Adds batch dimension
    - Applies MobileNetV2 preprocess_input
    Returns: preprocessed numpy array
    """
    # Load and convert image to RGB
    image = Image.open(file_storage)
    if image.mode != 'RGB':
        image = image.convert('RGB')
        
    # Resize image
    image = image.resize(target_size)
    
    # Convert to numpy array
    img_array = np.array(image, dtype=np.float32)
    
    # Expand dims to add batch dimension (1, height, width, channels)
    img_array = np.expand_dims(img_array, axis=0)
    
    # Preprocess inputs using TensorFlow's built-in MobileNetV2 preprocess function
    preprocessed_img = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    
    return preprocessed_img
