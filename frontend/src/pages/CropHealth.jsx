import React, { useState } from 'react'
import Sidebar from '../components/Sidebar'
import ScoreCard from '../components/ScoreCard'
import InsightCard from '../components/InsightCard'
import SatelliteMap from '../components/SatelliteMap'
import DiseaseUpload from '../components/DiseaseUpload'
import DiseaseResult from '../components/DiseaseResult'
import { analyzeCropHealth } from '../services/cropHealthApi'
import { predictDisease } from '../services/diseaseApi'
import '../styles/CropHealth.css'

function CropHealth() {
  // Satellite analysis state
  const [latitude, setLatitude] = useState(11.2742)
  const [longitude, setLongitude] = useState(77.5806)
  const [startDate, setStartDate] = useState('2026-01-01')
  const [endDate, setEndDate] = useState('2026-06-30')
  const [indexType, setIndexType] = useState('NDVI')
  const [analysisResult, setAnalysisResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [gpsStatus, setGpsStatus] = useState({ success: null, message: '' })

  // Disease classification state
  const [selectedImage, setSelectedImage] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  const [diseaseResult, setDiseaseResult] = useState(null)
  const [diseaseLoading, setDiseaseLoading] = useState(false)
  const [diseaseError, setDiseaseError] = useState(null)

  const handleSatelliteAnalyze = async () => {
    if (!latitude || !longitude || !startDate || !endDate) return

    setLoading(true)
    setError(null)
    setAnalysisResult(null)

    try {
      const payload = {
        latitude: parseFloat(latitude),
        longitude: parseFloat(longitude),
        startDate,
        endDate,
        indexType
      }
      const res = await analyzeCropHealth(payload)
      if (res.success) {
        setAnalysisResult(res.data)
      } else {
        setError(res.error || { code: 'SERVER_ERROR', message: 'Failed to process request.' })
      }
    } catch (err) {
      setError(err)
    } finally {
      setLoading(false)
    }
  }

  const handleDiseasePredict = async () => {
    if (!selectedImage) return

    setDiseaseLoading(true)
    setDiseaseError(null)
    setDiseaseResult(null)

    try {
      const res = await predictDisease(selectedImage)
      if (res.success) {
        setDiseaseResult(res.data)
      } else {
        setDiseaseError(res.error || { code: 'PREDICTION_FAILED', message: 'Analysis failed.' })
      }
    } catch (err) {
      setDiseaseError(err)
    } finally {
      setDiseaseLoading(false)
    }
  }

  return (
    <div className="crop-health-page">
      <Sidebar
        latitude={latitude}
        longitude={longitude}
        setLatitude={setLatitude}
        setLongitude={setLongitude}
        gpsStatus={gpsStatus}
        setGpsStatus={setGpsStatus}
        startDate={startDate}
        endDate={endDate}
        setStartDate={setStartDate}
        setEndDate={setEndDate}
        indexType={indexType}
        setIndexType={setIndexType}
        onAnalyze={handleSatelliteAnalyze}
        loading={loading}
      />

      <main className="analysis-main-content">
        {/* SECTION 1: SATELLITE CROP INTELLIGENCE */}
        <section className="section-card" id="satellite-intelligence-section">
          <h1 className="section-title">🛰️ Real-Time Satellite Crop Health Monitor</h1>
          <p className="section-subtitle">
            Geospatial agricultural intelligence powered by Google Earth Engine. Select coordinates 
            and date ranges on the left to map NDVI (vegetation growth) or NDWI (water moisture/stress) indexes.
          </p>

          {error && (
            <div className="api-error-alert" id="satellite-error">
              <div className="error-title">Satellite Analysis Failed ({error.code || 'UNKNOWN'})</div>
              <div className="error-message">{error.message || 'An unexpected error occurred.'}</div>
            </div>
          )}

          {analysisResult && (
            <>
              <ScoreCard 
                score={analysisResult.score}
                status={analysisResult.status}
                captureDate={analysisResult.captureDate}
                indexType={analysisResult.indexType}
              />
              
              <InsightCard 
                insight={analysisResult.insight}
                indexType={analysisResult.indexType}
              />
            </>
          )}

          <SatelliteMap 
            latitude={analysisResult ? analysisResult.latitude : latitude}
            longitude={analysisResult ? analysisResult.longitude : longitude}
            location={analysisResult ? analysisResult.location : null}
            tileUrl={analysisResult ? analysisResult.tileUrl : null}
            indexType={analysisResult ? analysisResult.indexType : indexType}
          />
        </section>

        <hr className="section-divider" />

        {/* SECTION 2: DEEP LEARNING DISEASE ANALYSIS */}
        <section className="section-card" id="ai-disease-detection-section">
          <h1 className="section-title">🔬 AI Crop Leaf Disease Detection</h1>
          <p className="section-subtitle">
            Deep learning leaf analyzer powered by MobileNetV2. Upload a crop leaf photo to identify crop health issues, 
            diseases, or infections with diagnostic confidence rates.
          </p>

          {diseaseError && (
            <div className="api-error-alert" id="disease-error">
              <div className="error-title">Disease Detection Failed ({diseaseError.code || 'UNKNOWN'})</div>
              <div className="error-message">{diseaseError.message || 'An unexpected error occurred.'}</div>
            </div>
          )}

          <div className="level-grid">
            <div className="grid-upload-area">
              <DiseaseUpload 
                selectedImage={selectedImage}
                setSelectedImage={setSelectedImage}
                imagePreview={imagePreview}
                setImagePreview={setImagePreview}
                onAnalyze={handleDiseasePredict}
                loading={diseaseLoading}
              />
            </div>
            
            <div className="grid-result-area">
              <DiseaseResult result={diseaseResult} />
            </div>
          </div>
        </section>
      </main>
    </div>
  )
}

export default CropHealth
