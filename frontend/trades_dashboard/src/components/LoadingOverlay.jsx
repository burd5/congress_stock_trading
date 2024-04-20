import React from 'react';
import '../styles/loadingOverlay.css'; // Import the CSS file

const LoadingOverlay = () => {
    return (
        <div className="loading-overlay">
            <div className="loading-spinner"></div>
        </div>
    );
};

export default LoadingOverlay;
