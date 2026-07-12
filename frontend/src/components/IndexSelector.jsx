import React from 'react'
import '../styles/IndexSelector.css'

function IndexSelector({ indexType, setIndexType }) {
  return (
    <div className="index-selector" id="index-cards-wrapper">
      <div className="index-cards-row">
        <div 
          className={`index-card ${indexType === 'NDVI' ? 'active' : ''}`}
          onClick={() => setIndexType('NDVI')}
          id="select-ndvi-card"
        >
          <span className="index-card-title">NDVI</span>
          <span className="index-card-subtitle">Crop Health</span>
        </div>
        
        <div 
          className={`index-card ${indexType === 'NDWI' ? 'active' : ''}`}
          onClick={() => setIndexType('NDWI')}
          id="select-ndwi-card"
        >
          <span className="index-card-title">NDWI</span>
          <span className="index-card-subtitle">Water Stress</span>
        </div>
      </div>
    </div>
  )
}

export default IndexSelector
