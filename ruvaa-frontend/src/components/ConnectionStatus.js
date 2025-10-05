import React, { useState, useEffect } from 'react';
import './ConnectionStatus.css';

const ConnectionStatus = () => {
  const [status, setStatus] = useState({
    backend: 'checking',
    ai: 'checking',
    backendMock: 'checking'
  });

  const [isVisible, setIsVisible] = useState(() => {
    const saved = localStorage.getItem('connectionStatusVisible');
    return saved !== 'false'; // Default to visible
  });

  useEffect(() => {
    checkConnections();
    const interval = setInterval(checkConnections, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const checkConnections = async () => {
    // Check Backend Connection
    try {
      const backendResponse = await fetch('https://ruvva-32l2.onrender.com/api/auth/health', {
        method: 'GET'
      });
      setStatus(prev => ({
        ...prev,
        backend: backendResponse.ok ? 'connected' : 'disconnected',
        backendMock: backendResponse.ok ? 'live' : 'disconnected'
      }));
    } catch (error) {
      setStatus(prev => ({ ...prev, backend: 'disconnected', backendMock: 'disconnected' }));
    }

    // Check AI Service Connection
    try {
      const aiResponse = await fetch('https://ruvva.onrender.com/health', {
        method: 'GET'
      });
      setStatus(prev => ({ ...prev, ai: aiResponse.ok ? 'connected' : 'disconnected' }));
    } catch (error) {
      setStatus(prev => ({ ...prev, ai: 'disconnected' }));
    }
  };

  const getStatusColor = (serviceStatus) => {
    switch (serviceStatus) {
      case 'connected': return '#4CAF50'; // Green
      case 'mock': return '#FF9800'; // Orange for mock
      case 'live': return '#4CAF50'; // Green for live
      case 'disconnected': return '#F44336'; // Red
      case 'checking': return '#2196F3'; // Blue
      default: return '#9E9E9E'; // Gray
    }
  };

  const getStatusText = (serviceStatus) => {
    switch (serviceStatus) {
      case 'connected': return 'Connected';
      case 'mock': return 'Mock Mode';
      case 'live': return 'Live';
      case 'disconnected': return 'Disconnected';
      case 'checking': return 'Checking...';
      default: return 'Unknown';
    }
  };

  const handleClose = () => {
    setIsVisible(false);
    localStorage.setItem('connectionStatusVisible', 'false');
  };

  const handleShow = () => {
    setIsVisible(true);
    localStorage.setItem('connectionStatusVisible', 'true');
  };

  if (!isVisible) {
    return (
      <button className="status-toggle-btn" onClick={handleShow} title="Show Connection Status">
        🔌
      </button>
    );
  }

  return (
    <div className="connection-status">
      <div className="status-header">
        <h4>🔌 Integration Status</h4>
        <div className="header-actions">
          <button onClick={checkConnections} className="refresh-btn" title="Refresh Status">
            🔄
          </button>
          <button onClick={handleClose} className="close-btn" title="Hide Status">
            ✕
          </button>
        </div>
      </div>

      <div className="status-grid">
        <div className="status-item">
          <div
            className="status-indicator"
            style={{ backgroundColor: getStatusColor(status.backend) }}
          ></div>
          <div className="status-info">
            <span className="service-name">Backend API</span>
            <span className="service-url">: careerconnect-4bi9.onrender.com/api</span>
            <span className="service-status">{getStatusText(status.backend)}</span>
          </div>
        </div>

        <div className="status-item">
          <div
            className="status-indicator"
            style={{ backgroundColor: getStatusColor(status.ai) }}
          ></div>
          <div className="status-info">
            <span className="service-name">AI Service</span>
            <span className="service-url">:5000</span>
            <span className="service-status">{getStatusText(status.ai)}</span>
          </div>
        </div>

        <div className="status-item">
          <div
            className="status-indicator"
            style={{ backgroundColor: getStatusColor(status.backendMock) }}
          ></div>
          <div className="status-info">
            <span className="service-name">Auth Mode</span>
            <span className="service-url">Mock/Live</span>
            <span className="service-status">
              {status.backendMock === 'mock' ? 'Mock Auth' :
               status.backendMock === 'live' ? 'Live Auth' :
               getStatusText(status.backendMock)}
            </span>
          </div>
        </div>
      </div>

      <div className="status-legend">
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: '#4CAF50' }}></div>
          <span>Connected / Live</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: '#FF9800' }}></div>
          <span>Mock Mode</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: '#F44336' }}></div>
          <span>Disconnected</span>
        </div>
      </div>
    </div>
  );
};

export default ConnectionStatus;
