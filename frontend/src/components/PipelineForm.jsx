import React from 'react';

const PipelineForm = ({ formData, handleChange }) => {
  return (
    <div className="card h-full">
      <h3 className="card-title"> Main Configuration</h3>
      <form> {/* ?*/}
        
        <div className="form-group">
          <label>PSL Input File</label>
          <input 
            type="text" 
            name="pslFile" 
            value={formData.pslFile} 
            onChange={handleChange} 
            className="form-input"
            placeholder="e.g., test_input.psl"
          />
          <p className="helper-text">Located in server/data directory</p>
        </div>

        <div className="form-group">
          <label>Target Chromosomes</label>
          <input 
            type="text" 
            name="filtered_chrs" 
            value={formData.filtered_chrs} 
            onChange={handleChange} 
            className="form-input"
            placeholder="e.g., chr1, chr2"
          />
        </div>

        <div className="form-group">
          <label>Filter Mode (PSL)</label>
          <select 
            name="filter_mode" 
            value={formData.filter_mode} 
            onChange={handleChange}
            className="form-select"
          >
            <option value="strict">Strict (Exact Match)</option>
            <option value="contain">Contain (Subset)</option>
          </select>
        </div>

        {/*: Mode settings */}
        <div className="form-group">
          <label>Filter Mode (BED)</label>
          <select 
            name="mode" 
            value={formData.mode} 
            onChange={handleChange}
            className="form-select"
          >
            <option value="exact">Exact ()</option>
            <option value="intersect">Intersect ()</option>
            <option value="subset">Subset ()</option>
          </select>
        </div>

      </form>
    </div>
  );
};

export default PipelineForm;