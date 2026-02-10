import React from 'react';

const StatusBadge = ({ loading, error }) => {
  if (loading) {
    return (
      <div style={{ textAlign: 'center', margin: '20px 0', color: 'var(--primary-color)' }}>
        
        <div className="spinner"></div> 
        <p>Pipeline is running on server... This may take a while.</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ 
        backgroundColor: '#fef2f2', 
        color: '#991b1b', 
        padding: '1rem', 
        borderRadius: '8px',
        border: '1px solid #fecaca',
        margin: '20px 0'
      }}>
        <strong> Error:</strong> {error}
      </div>
    );
  }

  return null;
};

export default StatusBadge;