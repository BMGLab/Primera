import React, { useState } from 'react';
import PipelineForm from './components/PipelineForm';
import PrimerSettingsForm from './components/PrimerSettingsForm';
import ResultsPanel from './components/ResultsPanel';
import { pipelineService } from './services/api';
import Header from './components/header';

function App() {
  // main pipeline parameters.                                                                                  //formData state : general settings
  const [formData, setFormData] = useState({        
    pslFile: "test_input.psl",
    blatdb: "hg38.2bit",
    filtered_chrs: "chr1",
    filter_mode: "strict",
    mode: "exact"
  });

  
  const [primerSettings, setPrimerSettings] = useState({
    
    PRIMER_TASK: "generic",
    PRIMER_PICK_INTERNAL_OLIGO: 1,
    PRIMER_EXPLAIN_FLAG: 1,
    PRIMER_NUM_RETURN: 10,
    
    
    PRIMER_MIN_SIZE: 18,
    PRIMER_OPT_SIZE: 20,
    PRIMER_MAX_SIZE: 25,
    PRIMER_MIN_TM: 55.0,
    PRIMER_OPT_TM: 59.0,
    PRIMER_MAX_TM: 63.0,
    PRIMER_MIN_GC: 30.0,
    PRIMER_MAX_GC: 70.0,
    
    
    PRIMER_INTERNAL_OLIGO_MIN_SIZE: 18,
    PRIMER_INTERNAL_OLIGO_OPT_SIZE: 20,
    PRIMER_INTERNAL_OLIGO_MAX_SIZE: 27,
    PRIMER_INTERNAL_OLIGO_MIN_TM: 57.0,
    PRIMER_INTERNAL_OLIGO_OPT_TM: 60.0,
    PRIMER_INTERNAL_OLIGO_MAX_TM: 70.0,
    PRIMER_INTERNAL_OLIGO_MIN_GC: 30.0,
    PRIMER_INTERNAL_OLIGO_MAX_GC: 70.0
  });

  const [loading, setLoading] = useState(false);
  const [runId, setRunId] = useState(null);
  const [error, setError] = useState(null);

  // main form change handler
  const handleMainChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Primer settings form change handler
  const handleSettingsChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    // Checkbox 1 and 0, num  float/int,text  string
    let finalValue = value;
    
    if (type === 'checkbox') {
        finalValue = checked ? 1 : 0;
    } else if (type === 'number') {
        finalValue = value === "" ? "" : parseFloat(value);
    }

    setPrimerSettings({ 
      ...primerSettings, 
      [name]: finalValue
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setRunId(null);

    // Backend package(formData + primerSettings) into a single payload
    const payload = {
      ...formData,
      
      primer_settings: {
        ...primerSettings,
        

        "PRIMER_PRODUCT_SIZE_RANGE": [[100, 300]] 
      }
    };

    try {
      const result = await pipelineService.runPipeline(payload);
      if (result.status === 'success') {
        setRunId(result.run_id);
      }
    } catch (err) {
      console.error(err);
      setError("Pipeline failed to start. Please check the backend connection.");
    } finally {
      setLoading(false);
    }
  };

  
  return (
    <div className="app-container">

    <Header /> 

      <main className="main-content">
        
        <div className="grid-layout">
          <PipelineForm 
            formData={formData} 
            handleChange={handleMainChange} 
          />
          
          <PrimerSettingsForm 
            settings={primerSettings} 
            handleChange={handleSettingsChange} 
          />
        </div>

        <div className="action-bar">
          <button 
            onClick={handleSubmit} 
            className="btn-primary btn-large" 
            disabled={loading}
          >
            {loading ? (
              <><span className="loading-spinner"></span> Processing...</>
            ) : (
              "Run Pipeline"
            )}
          </button>
        </div>

        {error && (
          <div style={{ marginTop: '1rem', padding: '1rem', borderRadius: '8px', backgroundColor: '#fef2f2', color: '#991b1b', border: '1px solid #fecaca' }}>
            ⚠️ {error}
          </div>
        )}

        <ResultsPanel 
          runId={runId} 
          downloadLinkFn={pipelineService.getDownloadLink} 
        />
      </main>
    </div>
  );
}

export default App;