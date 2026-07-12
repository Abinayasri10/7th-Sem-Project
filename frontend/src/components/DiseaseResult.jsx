import React from 'react'
import '../styles/DiseaseResult.css'

function DiseaseResult({ result }) {
  if (!result) return null;

  const { predictedClass, confidence } = result;

  return (
    <div className="disease-result-card" id="disease-prediction-output">
      <div className="disease-result-header">
        <span className="disease-result-title">Deep Learning Classification</span>
        <span className="disease-model-badge">Model: MobileNetV2 Transfer Learning</span>
      </div>

      <div className="prediction-block">
        <span className="prediction-label">Detected Class / Health Status</span>
        <span className="prediction-class">{predictedClass}</span>
      </div>

      <div className="confidence-block">
        <div className="confidence-header">
          <span className="prediction-label">Model Confidence</span>
          <span className="confidence-percentage">{confidence.toFixed(2)}%</span>
        </div>
        <div className="confidence-bar-track">
          <div 
            className="confidence-bar-fill" 
            style={{ width: `${confidence}%` }}
          ></div>
        </div>
      </div>
    </div>
  )
}

export default DiseaseResult
