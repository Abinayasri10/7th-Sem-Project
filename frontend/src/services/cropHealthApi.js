/**
 * API service for Google Earth Engine Crop Health Analysis.
 */

export async function analyzeCropHealth(payload) {
  const baseUrl = import.meta.env.VITE_API_BASE_URL || '';
  
  try {
    const response = await fetch(`${baseUrl}/api/crop-health/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
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
        code: "SERVER_ERROR",
        message: data.message || "An error occurred during satellite analysis."
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
