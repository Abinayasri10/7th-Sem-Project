import React from 'react'
import '../styles/ScoreCard.css'

function ScoreCard({ score, status, captureDate, indexType }) {
  // Helper to determine status color class based on GEE classification string
  const getStatusClass = (statusStr) => {
    if (!statusStr) return '';
    const s = statusStr.toLowerCase();
    if (s.includes('excellent') || s.includes('high')) return 'status-excellent';
    if (s.includes('healthy') || s.includes('sufficient')) return 'status-healthy';
    if (s.includes('moderate')) return 'status-moderate';
    if (s.includes('severe')) return 'status-severe';
    return 'status-info';
  };

  return (
    <div className="score-cards-grid" id="satellite-score-cards">
      <div className="score-card">
        <span className="score-card-label">Current {indexType} Score</span>
        <span className="score-card-value">{score !== undefined && score !== null ? score.toFixed(4) : 'N/A'}</span>
      </div>

      <div className="score-card">
        <span className="score-card-label">Analysis Status</span>
        <span className={`score-card-value ${getStatusClass(status)}`} style={{ fontSize: '1.35rem', fontWeight: 700 }}>
          {status || 'N/A'}
        </span>
      </div>

      <div className="score-card">
        <span className="score-card-label">Capture Date</span>
        <span className="score-card-value" style={{ fontSize: '1.45rem' }}>
          {captureDate || 'N/A'}
        </span>
      </div>
    </div>
  )
}

export default ScoreCard
