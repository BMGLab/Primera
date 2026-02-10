import React from 'react';

const ResultsPanel = ({ runId, downloadLinkFn }) => {
  if (!runId) return null;

  return (
    <div className="results-container">
      <div style={{ fontSize: '3rem', marginBottom: '10px' }}>✅</div>
      <h3 style={{ color: '#065f46', margin: '0 0 0.5rem 0' }}>Analysis Completed</h3>
      <p style={{ color: '#047857' }}>
        Run ID: <code style={{ background: 'rgba(255,255,255,0.5)', padding: '2px 6px', borderRadius: '4px' }}>{runId}</code>
      </p>
      
      <div className="btn-group">
        <a href={downloadLinkFn(runId, 'results.tsv')} className="btn-download">
           Download TSV
        </a>
        <a href={downloadLinkFn(runId, 'results.bed')} className="btn-download">
           Download BED
        </a>
        <a href={downloadLinkFn(runId, 'report.html')} className="btn-download" target="_blank" rel="noopener noreferrer">
           View Report
        </a>
      </div>
    </div>
  );
};

export default ResultsPanel;