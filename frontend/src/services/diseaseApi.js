/**
 * API service for Deep Learning Crop Leaf Disease Detection.
 */

export async function predictDisease(imageFile) {
  const baseUrl = import.meta.env.VITE_API_BASE_URL || '';
  
  try {
    const formData = new FormData();
    formData.append('image', imageFile);

    const response = await fetch(`${baseUrl}/api/disease/predict`, {
      method: 'POST',
      body: formData,
    });

    const contentType = response.headers.get("content-type");
    if (!contentType || !contentType.includes("application/json")) {
      throw {
        code: "SERVER_ERROR",
        message: "Server returned a non-JSON response. Please check server status."
      };
    }

    const data = await response.json();

    if (!response.ok) {
      throw data.error || {
        code: "PREDICTION_FAILED",
        message: data.message || "An error occurred during leaf image prediction."
      };
    }

    return data;
  } catch (err) {
    if (err.code) {
      throw err;
    }
    throw {
      code: "NETWORK_ERROR",
      message: err.message || "Failed to connect to the backend server. Please verify the backend is running."
    };
  }
}
