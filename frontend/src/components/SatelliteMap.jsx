import React, { useEffect } from 'react'
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet'
import L from 'leaflet'
import '../styles/SatelliteMap.css'

// Bulletproof CDN icons to prevent Vite asset compiling issues
const markerIconSvg = L.icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
})

// Helper component to handle dynamic Map panning/zooming when coordinates change
function ChangeView({ center }) {
  const map = useMap();
  useEffect(() => {
    if (center && center[0] !== undefined && center[1] !== undefined) {
      map.setView(center, 13);
    }
  }, [center, map]);
  return null;
}

function SatelliteMap({ latitude, longitude, location, tileUrl, indexType }) {
  const center = [
    latitude && !isNaN(latitude) ? latitude : 11.2742,
    longitude && !isNaN(longitude) ? longitude : 77.5806
  ];

  return (
    <div className="map-wrapper" id="farm-map-wrapper">
      <MapContainer 
        center={center} 
        zoom={13} 
        scrollWheelZoom={true} 
        className="satellite-map-container"
      >
        <ChangeView center={center} />
        
        {/* OpenStreetMap Base Layer */}
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {/* Google Earth Engine NDVI/NDWI Tile Overlay */}
        {tileUrl && (
          <TileLayer
            url={tileUrl}
            attribution="&copy; Google Earth Engine / Sentinel-2 Harmonized"
          />
        )}
        
        {/* Farm Location Marker */}
        <Marker position={center} icon={markerIconSvg}>
          <Popup>
            <div style={{ fontWeight: 500 }}>
              <strong>Farm Location</strong><br/>
              {location || `${center[0]}, ${center[1]}`}
            </div>
          </Popup>
        </Marker>
      </MapContainer>

      {/* Floating Legend */}
      <div className="map-legend">
        <span className="legend-title">{indexType} Map Legend</span>
        <div className="legend-items">
          {indexType === 'NDVI' ? (
            <>
              <div className="legend-item">
                <span className="legend-color color-stressed"></span>
                <span>Stressed (&lt; 0.2)</span>
              </div>
              <div className="legend-item">
                <span className="legend-color color-moderate"></span>
                <span>Moderate (0.2 - 0.4)</span>
              </div>
              <div className="legend-item">
                <span className="legend-color color-healthy"></span>
                <span>Healthy (&gt; 0.4)</span>
              </div>
            </>
          ) : (
            <>
              <div className="legend-item">
                <span className="legend-color color-water-stress"></span>
                <span>Water Stress (&lt; -0.2)</span>
              </div>
              <div className="legend-item">
                <span className="legend-color color-mod-moisture"></span>
                <span>Moderate Moisture (-0.2 - 0)</span>
              </div>
              <div className="legend-item">
                <span className="legend-color color-high-moisture"></span>
                <span>High Moisture (&gt; 0)</span>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default SatelliteMap
