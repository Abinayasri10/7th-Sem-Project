import React from 'react'
import Navbar from './components/Navbar'
import CropHealth from './pages/CropHealth'
import './styles/App.css'

function App() {
  return (
    <div className="app-container">
      <Navbar />
      <div className="app-main">
        <CropHealth />
      </div>
    </div>
  )
}

export default App
