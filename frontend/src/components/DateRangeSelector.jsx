import React from 'react'
import '../styles/DateRangeSelector.css'

function DateRangeSelector({
  startDate,
  endDate,
  setStartDate,
  setEndDate
}) {
  return (
    <div className="date-range-selector" id="date-fields-wrapper">
      <div className="dates-row">
        <div className="date-input-group">
          <label className="date-label" htmlFor="input-start-date">Start Date</label>
          <input 
            type="date" 
            id="input-start-date"
            className="date-input"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </div>
        <div className="date-input-group">
          <label className="date-label" htmlFor="input-end-date">End Date</label>
          <input 
            type="date" 
            id="input-end-date"
            className="date-input"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </div>
      </div>
    </div>
  )
}

export default DateRangeSelector
