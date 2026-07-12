import React, { useState, useRef } from 'react'
import '../styles/DiseaseUpload.css'

function DiseaseUpload({ 
  selectedImage, 
  setSelectedImage, 
  imagePreview, 
  setImagePreview, 
  onAnalyze, 
  loading 
}) {
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      validateAndSetFile(file);
    }
  };

  const handleBrowse = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const validateAndSetFile = (file) => {
    // Validate format
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    const extension = file.name.split('.').pop().toLowerCase();
    const isValidExt = ['jpg', 'jpeg', 'png'].includes(extension);

    if (!validTypes.includes(file.type) && !isValidExt) {
      alert("Invalid file format. Only JPG, JPEG, and PNG images are supported.");
      return;
    }
    
    // Validate size (5MB)
    const maxSize = 5 * 1024 * 1024;
    if (file.size > maxSize) {
      alert("File size is too large. Maximum size allowed is 5MB.");
      return;
    }

    setSelectedImage(file);
    
    // Create preview URL
    const reader = new FileReader();
    reader.onloadend = () => {
      setImagePreview(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const handleClear = () => {
    setSelectedImage(null);
    setImagePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="upload-container" id="leaf-upload-wrapper">
      {!imagePreview ? (
        <div 
          className={`upload-dropzone ${dragActive ? 'drag-active' : ''}`}
          onDragEnter={handleDrag}
          onDragOver={handleDrag}
          onDragLeave={handleDrag}
          onDrop={handleDrop}
          onClick={handleBrowse}
        >
          <input 
            type="file" 
            ref={fileInputRef}
            style={{ display: 'none' }}
            accept=".jpg,.jpeg,.png"
            onChange={handleFileChange}
          />
          <span className="upload-icon">📸</span>
          <p className="upload-text">
            Drag and drop your leaf image here, or <span>browse</span>
          </p>
          <p className="upload-subtext">Supports JPG, JPEG, PNG (max 5MB)</p>
        </div>
      ) : (
        <div className="preview-container">
          <div className="image-preview-frame">
            <img src={imagePreview} alt="Leaf preview" className="image-preview-img" />
          </div>
          
          <div className="preview-actions">
            <button 
              type="button" 
              className="predict-btn" 
              onClick={onAnalyze}
              disabled={loading}
            >
              {loading ? 'Analyzing...' : 'Analyze Leaf Image'}
            </button>
            <button 
              type="button" 
              className="clear-btn" 
              onClick={handleClear}
              disabled={loading}
            >
              Clear
            </button>
          </div>

          {loading && (
            <p className="disease-loader-text">
              Analyzing crop leaf using Deep Learning model...
            </p>
          )}
        </div>
      )}
    </div>
  )
}

export default DiseaseUpload
