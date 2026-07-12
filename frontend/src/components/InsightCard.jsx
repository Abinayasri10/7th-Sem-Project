import React from 'react'
import '../styles/InsightCard.css'

function InsightCard({ insight, indexType }) {
  if (!insight) return null;

  return (
    <div className={`insight-card ${indexType === 'NDWI' ? 'theme-ndwi' : ''}`} id="decision-support-insight">
      <div className="insight-card-header">
        <span className="insight-card-badge">Satellite Decision Support</span>
        <span className="insight-card-title">{indexType} Rule-Based Interpretation</span>
      </div>
      <p className="insight-card-text">{insight}</p>
    </div>
  )
}

export default InsightCard
