import os
from PIL import Image

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def validate_uploaded_image(file_storage, allowed_extensions, max_size_bytes):
    """
    Validates an uploaded file from a Flask request.
    Returns: (is_valid, error_code, error_message)
    """
    if not file_storage or file_storage.filename == '':
        return False, "INVALID_INPUT", "No file selected or uploaded."

    # Validate file extension
    if not allowed_file(file_storage.filename, allowed_extensions):
        exts_str = ", ".join(sorted(allowed_extensions)).upper()
        return False, "INVALID_IMAGE", f"Unsupported file extension. Allowed formats are: {exts_str}."

    # Validate file size (check file descriptor size if possible)
    try:
        file_storage.seek(0, os.SEEK_END)
        size = file_storage.tell()
        file_storage.seek(0)  # Reset pointer
        
        if size > max_size_bytes:
            max_mb = max_size_bytes / (1024 * 1024)
            return False, "INVALID_IMAGE", f"File size exceeds the limit of {max_mb:.1f}MB."
    except Exception as e:
        return False, "SERVER_ERROR", f"Could not check file size: {str(e)}"

    # Validate image readability using Pillow
    try:
        img = Image.open(file_storage)
        img.verify()  # Verify it is a valid image file
        file_storage.seek(0)  # Reset pointer for subsequent reads
    except Exception:
        return False, "INVALID_IMAGE", "The uploaded file is not a valid or readable image."

    return True, None, None
