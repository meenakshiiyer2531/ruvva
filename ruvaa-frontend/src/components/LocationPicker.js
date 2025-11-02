import React, { useState } from 'react';
import { useLocation } from '../services/locationService';

export default function LocationPicker({ onLocationSelect, currentLocation, showLabel = true }) {
  const { 
    location, 
    loading, 
    error, 
    detectLocation, 
    setManualLocation, 
    clearLocation, 
    cities, 
    states 
  } = useLocation();
  
  const [showManualInput, setShowManualInput] = useState(false);
  const [selectedCity, setSelectedCity] = useState(currentLocation?.city || '');
  const [selectedState, setSelectedState] = useState(currentLocation?.state || '');
  const [searchTerm, setSearchTerm] = useState('');

  const filteredCities = cities.filter(city => 
    city.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleAutoDetect = async () => {
    const locationData = await detectLocation();
    if (locationData && onLocationSelect) {
      onLocationSelect(locationData);
    }
  };

  const handleManualSubmit = (e) => {
    e.preventDefault();
    if (selectedCity && selectedState) {
      const locationData = setManualLocation(selectedCity, selectedState);
      if (onLocationSelect) {
        onLocationSelect(locationData);
      }
      setShowManualInput(false);
    }
  };

  const handleClear = () => {
    clearLocation();
    setSelectedCity('');
    setSelectedState('');
    setSearchTerm('');
    if (onLocationSelect) {
      onLocationSelect(null);
    }
  };

  const displayLocation = currentLocation || location;

  return (
    <div style={containerStyle}>
      {showLabel && (
        <label style={labelStyle}>
          📍 Location {displayLocation && <span style={optionalStyle}>(Auto-detected)</span>}
        </label>
      )}
      
      {/* Current Location Display */}
      {displayLocation && (
        <div style={currentLocationStyle}>
          <div style={locationInfoStyle}>
            <span style={cityStyle}>{displayLocation.city}</span>
            {displayLocation.state && (
              <span style={stateStyle}>, {displayLocation.state}</span>
            )}
            <span style={countryStyle}> • {displayLocation.country || 'India'}</span>
            {displayLocation.manual && (
              <span style={manualTagStyle}>Manual</span>
            )}
          </div>
          <div style={actionButtonsStyle}>
            <button 
              type="button" 
              onClick={() => setShowManualInput(true)} 
              style={changeButtonStyle}
              title="Change location"
            >
              ✏️
            </button>
            <button 
              type="button" 
              onClick={handleClear} 
              style={clearButtonStyle}
              title="Clear location"
            >
              ✖️
            </button>
          </div>
        </div>
      )}

      {/* No Location - Show Options */}
      {!displayLocation && (
        <div style={noLocationStyle}>
          <div style={buttonGroupStyle}>
            <button 
              type="button" 
              onClick={handleAutoDetect} 
              disabled={loading}
              style={autoDetectButtonStyle}
            >
              {loading ? (
                <>🔄 Detecting...</>
              ) : (
                <>📍 Auto-Detect Location</>
              )}
            </button>
            <button 
              type="button" 
              onClick={() => setShowManualInput(true)}
              style={manualButtonStyle}
            >
              📝 Enter Manually
            </button>
          </div>
          
          {error && (
            <div style={errorStyle}>
              ⚠️ {error}
            </div>
          )}
        </div>
      )}

      {/* Manual Input Modal */}
      {showManualInput && (
        <div style={modalOverlayStyle}>
          <div style={modalStyle}>
            <div style={modalHeaderStyle}>
              <h3 style={modalTitleStyle}>Select Your Location</h3>
              <button 
                type="button"
                onClick={() => setShowManualInput(false)}
                style={closeButtonStyle}
              >
                ✖️
              </button>
            </div>

            <form onSubmit={handleManualSubmit} style={formStyle}>
              {/* State Selection */}
              <div style={fieldGroupStyle}>
                <label style={fieldLabelStyle}>State *</label>
                <select
                  value={selectedState}
                  onChange={(e) => setSelectedState(e.target.value)}
                  style={selectStyle}
                  required
                >
                  <option value="">Select State</option>
                  {states.map(state => (
                    <option key={state} value={state}>{state}</option>
                  ))}
                </select>
              </div>

              {/* City Search and Selection */}
              <div style={fieldGroupStyle}>
                <label style={fieldLabelStyle}>City *</label>
                <input
                  type="text"
                  placeholder="Search for your city..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  style={inputStyle}
                />
                
                {searchTerm && (
                  <div style={cityListStyle}>
                    {filteredCities.slice(0, 10).map(city => (
                      <button
                        key={city}
                        type="button"
                        onClick={() => {
                          setSelectedCity(city);
                          setSearchTerm(city);
                        }}
                        style={{
                          ...cityOptionStyle,
                          background: selectedCity === city ? '#e3f2fd' : 'transparent'
                        }}
                      >
                        {city}
                      </button>
                    ))}
                    {filteredCities.length === 0 && (
                      <div style={noCitiesStyle}>
                        No cities found. You can type any city name.
                      </div>
                    )}
                  </div>
                )}
                
                {/* Custom City Input */}
                <input
                  type="text"
                  placeholder="Or enter city name"
                  value={selectedCity}
                  onChange={(e) => setSelectedCity(e.target.value)}
                  style={{ ...inputStyle, marginTop: 8 }}
                  required
                />
              </div>

              <div style={modalActionsStyle}>
                <button 
                  type="button" 
                  onClick={() => setShowManualInput(false)}
                  style={cancelButtonStyle}
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  disabled={!selectedCity || !selectedState}
                  style={{
                    ...saveButtonStyle,
                    opacity: (!selectedCity || !selectedState) ? 0.5 : 1
                  }}
                >
                  Save Location
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

// Styles
const containerStyle = {
  width: '100%'
};

const labelStyle = {
  display: 'block',
  fontSize: 14,
  fontWeight: '600',
  color: 'var(--text)',
  marginBottom: 8
};

const optionalStyle = {
  fontSize: 12,
  fontWeight: '400',
  color: 'var(--muted)',
  marginLeft: 8
};

const currentLocationStyle = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  padding: 12,
  background: 'var(--card)',
  border: '2px solid #00b4d8',
  borderRadius: 12,
  boxShadow: '0 2px 8px rgba(0, 180, 216, 0.1)'
};

const locationInfoStyle = {
  display: 'flex',
  alignItems: 'center',
  flexWrap: 'wrap',
  gap: 4
};

const cityStyle = {
  fontWeight: '600',
  color: '#00b4d8',
  fontSize: 16
};

const stateStyle = {
  color: 'var(--text)',
  fontSize: 14
};

const countryStyle = {
  color: 'var(--muted)',
  fontSize: 12
};

const manualTagStyle = {
  background: '#ff9800',
  color: 'white',
  padding: '2px 8px',
  borderRadius: 12,
  fontSize: 10,
  fontWeight: '600',
  marginLeft: 8
};

const actionButtonsStyle = {
  display: 'flex',
  gap: 8
};

const changeButtonStyle = {
  background: '#2196f3',
  border: 'none',
  padding: '6px 8px',
  borderRadius: 8,
  cursor: 'pointer',
  fontSize: 12
};

const clearButtonStyle = {
  background: '#f44336',
  border: 'none',
  padding: '6px 8px',
  borderRadius: 8,
  cursor: 'pointer',
  fontSize: 12
};

const noLocationStyle = {
  padding: 16,
  border: '2px dashed #ddd',
  borderRadius: 12,
  textAlign: 'center'
};

const buttonGroupStyle = {
  display: 'flex',
  gap: 12,
  justifyContent: 'center',
  marginBottom: 12
};

const autoDetectButtonStyle = {
  background: '#4caf50',
  color: 'white',
  border: 'none',
  padding: '12px 20px',
  borderRadius: 8,
  cursor: 'pointer',
  fontWeight: '600',
  fontSize: 14
};

const manualButtonStyle = {
  background: '#2196f3',
  color: 'white',
  border: 'none',
  padding: '12px 20px',
  borderRadius: 8,
  cursor: 'pointer',
  fontWeight: '600',
  fontSize: 14
};

const errorStyle = {
  color: '#f44336',
  fontSize: 12,
  marginTop: 8
};

const modalOverlayStyle = {
  position: 'fixed',
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  background: 'rgba(0, 0, 0, 0.5)',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  zIndex: 1000
};

const modalStyle = {
  background: 'var(--card)',
  borderRadius: 16,
  width: '90%',
  maxWidth: 500,
  maxHeight: '80vh',
  overflow: 'auto',
  boxShadow: '0 20px 60px rgba(0, 0, 0, 0.2)'
};

const modalHeaderStyle = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  padding: '20px 24px',
  borderBottom: '1px solid #eee'
};

const modalTitleStyle = {
  margin: 0,
  color: '#00b4d8',
  fontSize: 18,
  fontWeight: '600'
};

const closeButtonStyle = {
  background: 'none',
  border: 'none',
  fontSize: 16,
  cursor: 'pointer',
  padding: 4
};

const formStyle = {
  padding: 24
};

const fieldGroupStyle = {
  marginBottom: 20
};

const fieldLabelStyle = {
  display: 'block',
  fontSize: 14,
  fontWeight: '600',
  color: 'var(--text)',
  marginBottom: 8
};

const selectStyle = {
  width: '100%',
  padding: 12,
  border: '1px solid #ddd',
  borderRadius: 8,
  fontSize: 14,
  background: 'var(--card)',
  color: 'var(--text)'
};

const inputStyle = {
  width: '100%',
  padding: 12,
  border: '1px solid #ddd',
  borderRadius: 8,
  fontSize: 14,
  background: 'var(--card)',
  color: 'var(--text)'
};

const cityListStyle = {
  marginTop: 8,
  border: '1px solid #ddd',
  borderRadius: 8,
  maxHeight: 200,
  overflow: 'auto',
  background: 'var(--card)'
};

const cityOptionStyle = {
  width: '100%',
  padding: 12,
  border: 'none',
  textAlign: 'left',
  cursor: 'pointer',
  fontSize: 14,
  color: 'var(--text)',
  background: 'transparent'
};

const noCitiesStyle = {
  padding: 12,
  color: 'var(--muted)',
  fontSize: 14,
  textAlign: 'center'
};

const modalActionsStyle = {
  display: 'flex',
  gap: 12,
  justifyContent: 'flex-end',
  marginTop: 24
};

const cancelButtonStyle = {
  background: 'transparent',
  border: '1px solid #ddd',
  padding: '10px 20px',
  borderRadius: 8,
  cursor: 'pointer',
  color: 'var(--text)'
};

const saveButtonStyle = {
  background: '#00b4d8',
  color: 'white',
  border: 'none',
  padding: '10px 20px',
  borderRadius: 8,
  cursor: 'pointer',
  fontWeight: '600'
};