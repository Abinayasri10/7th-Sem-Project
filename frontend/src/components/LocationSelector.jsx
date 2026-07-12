import React from 'react'
import '../styles/LocationSelector.css'

function LocationSelector({
  latitude,
  longitude,
  setLatitude,
  setLongitude,
  gpsStatus,
  setGpsStatus
}) {
  const handleGPSDetect = () => {
    if (!navigator.geolocation) {
      setGpsStatus({ success: false, message: 'Geolocation is not supported by your browser.' });
      return;
    }

    setGpsStatus({ success: null, message: 'Detecting coordinates...' });

    navigator.geolocation.getCurrentPosition(
      (position) => {
        // Round coordinate decimal points to 6 digits for precision
        const lat = parseFloat(position.coords.latitude.toFixed(6));
        const lon = parseFloat(position.coords.longitude.toFixed(6));
        setLatitude(lat);
        setLongitude(lon);
        setGpsStatus({ success: true, message: 'GPS location detected successfully.' });
      },
      (error) => {
        let msg = 'Failed to retrieve location.';
        if (error.code === 1) {
          msg = 'Location permission denied by user.';
        } else if (error.code === 2) {
          msg = 'Location information is unavailable.';
        } else if (error.code === 3) {
          msg = 'Location request timed out.';
        }
        setGpsStatus({ success: false, message: msg });
      },
      { enableHighAccuracy: true, timeout: 8000, maximumAge: 0 }
    );
  };

  return (
    <div className="location-selector" id="location-fields-wrapper">
      <div className="coords-row">
        <div className="coord-input-group">
          <label className="coord-label" htmlFor="input-latitude">Latitude</label>
          <input 
            type="number" 
            id="input-latitude"
            className="coord-input"
            step="0.000001"
            min="-90"
            max="90"
            placeholder="e.g. 11.2742"
            value={latitude}
            onChange={(e) => {
              setLatitude(e.target.value === '' ? '' : parseFloat(e.target.value));
              setGpsStatus({ success: null, message: '' }); // Clear GPS status message on edit
            }}
          />
        </div>
        <div className="coord-input-group">
          <label className="coord-label" htmlFor="input-longitude">Longitude</label>
          <input 
            type="number" 
            id="input-longitude"
            className="coord-input"
            step="0.000001"
            min="-180"
            max="180"
            placeholder="e.g. 77.5806"
            value={longitude}
            onChange={(e) => {
              setLongitude(e.target.value === '' ? '' : parseFloat(e.target.value));
              setGpsStatus({ success: null, message: '' }); // Clear GPS status message on edit
            }}
          />
        </div>
      </div>

      <button 
        type="button" 
        className={`gps-btn ${gpsStatus.success ? 'active' : ''}`}
        onClick={handleGPSDetect}
        id="detect-gps-btn"
      >
        🛰️ Use My Current Location
      </button>

      {gpsStatus.message && (
        <span className={`gps-status ${gpsStatus.success === true ? 'success' : gpsStatus.success === false ? 'error' : ''}`}>
          {gpsStatus.success === true ? '✓ ' : gpsStatus.success === false ? '✗ ' : '⏳ '}
          {gpsStatus.message}
        </span>
      )}
    </div>
  )
}

export default LocationSelector
