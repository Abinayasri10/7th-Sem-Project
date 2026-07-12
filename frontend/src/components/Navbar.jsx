import React from 'react'
import '../styles/Navbar.css'

function Navbar() {
  return (
    <nav className="navbar" id="app-navbar">
      <a href="/" className="navbar-brand">
        <span className="navbar-logo">🌱</span>
        <span className="navbar-title">Smart<span>Agri</span></span>
      </a>
      
      <ul className="navbar-menu">
        <li className="navbar-item">
          <a href="#" className="navbar-link active">Crop Health</a>
        </li>
        <li className="navbar-item">
          <a href="#" className="navbar-link disabled" onClick={(e) => e.preventDefault()}>
            Soil Intelligence <span className="badge">Soon</span>
          </a>
        </li>
        <li className="navbar-item">
          <a href="#" className="navbar-link disabled" onClick={(e) => e.preventDefault()}>
            Smart Irrigation <span className="badge">Soon</span>
          </a>
        </li>
        <li className="navbar-item">
          <a href="#" className="navbar-link disabled" onClick={(e) => e.preventDefault()}>
            Crop Suitability <span className="badge">Soon</span>
          </a>
        </li>
        <li className="navbar-item">
          <a href="#" className="navbar-link disabled" onClick={(e) => e.preventDefault()}>
            Crop Pattern Intelligence <span className="badge">Soon</span>
          </a>
        </li>
      </ul>
    </nav>
  )
}

export default Navbar
