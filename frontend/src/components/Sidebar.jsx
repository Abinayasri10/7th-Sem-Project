import React from 'react'
import LocationSelector from './LocationSelector'
import DateRangeSelector from './DateRangeSelector'
import IndexSelector from './IndexSelector'
import '../styles/Sidebar.css'

function Sidebar({
  latitude,
  longitude,
  setLatitude,
  setLongitude,
  gpsStatus,
  setGpsStatus,
  startDate,
  endDate,
  setStartDate,
  setEndDate,
  indexType,
  setIndexType,
  onAnalyze,
  loading
}) {
  const isSubmitDisabled = !latitude || !longitude || !startDate || !endDate || loading;

  return (
    <aside className="sidebar-panel" id="analysis-sidebar">
      <h2 className="sidebar-heading">Field Analysis Config</h2>
      
      <div className="sidebar-section">
        <label className="sidebar-label">1. Farm Coordinates</label>
        <LocationSelector 
          latitude={latitude}
          longitude={longitude}
          setLatitude={setLatitude}
          setLongitude={setLongitude}
          gpsStatus={gpsStatus}
          setGpsStatus={setGpsStatus}
        />
      </div>

      <div className="sidebar-section">
        <label className="sidebar-label">2. Analysis Period</label>
        <DateRangeSelector 
          startDate={startDate}
          endDate={endDate}
          setStartDate={setStartDate}
          setEndDate={setEndDate}
        />
      </div>

      <div className="sidebar-section">
        <label className="sidebar-label">3. Satellite Indicator</label>
        <IndexSelector 
          indexType={indexType}
          setIndexType={setIndexType}
        />
      </div>

      <button 
        className="analyze-btn" 
        onClick={onAnalyze} 
        disabled={isSubmitDisabled}
        id="trigger-analysis-btn"
      >
        {loading ? 'Analyzing Data...' : 'Analyze Crop Health'}
      </button>

      {loading && (
        <p className="analyze-loader-text">
          Analyzing Sentinel-2 satellite data...
        </p>
      )}
    </aside>
  )
}

export default Sidebar
