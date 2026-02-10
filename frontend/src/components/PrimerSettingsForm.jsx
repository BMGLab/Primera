import React from 'react';

const PrimerSettingsForm = ({ settings, handleChange }) => {
  return (
    <div className="card h-full">
      <h3 className="card-title"> Primer  Settings</h3>
      
      
      <div className="settings-columns">
        
        
        <div className="settings-column">
          <div className="column-header">General Config</div>
          
          <div className="form-group">
            <label>Task</label>
            <input type="text" name="PRIMER_TASK" value={settings.PRIMER_TASK} onChange={handleChange} className="form-input" />
          </div>

          <div className="form-group">
            <label>Num Return</label>
            <input type="number" name="PRIMER_NUM_RETURN" value={settings.PRIMER_NUM_RETURN} onChange={handleChange} className="form-input" />
          </div>

          <div className="form-group checkbox-group">
            <label>
              <input 
                type="checkbox" 
                name="PRIMER_PICK_INTERNAL_OLIGO" 
                checked={settings.PRIMER_PICK_INTERNAL_OLIGO === 1} 
                onChange={handleChange} 
              />
              Pick Probe
            </label>
            
            <label>
              <input 
                type="checkbox" 
                name="PRIMER_EXPLAIN_FLAG" 
                checked={settings.PRIMER_EXPLAIN_FLAG === 1} 
                onChange={handleChange} 
              />
              Explain Flag
            </label>
          </div>
        </div>

        
        <div className="settings-column">
          <div className="column-header" style={{color: '#2563eb'}}>Primer Parameters</div>

          {/* Primer Size */}
          <div className="form-group">
            <label>Size (bp)</label>
            <div className="input-row compact">
               <input type="number" name="PRIMER_MIN_SIZE" value={settings.PRIMER_MIN_SIZE} onChange={handleChange} className="form-input" placeholder="Min" />
               <input type="number" name="PRIMER_OPT_SIZE" value={settings.PRIMER_OPT_SIZE} onChange={handleChange} className="form-input" placeholder="Opt" />
               <input type="number" name="PRIMER_MAX_SIZE" value={settings.PRIMER_MAX_SIZE} onChange={handleChange} className="form-input" placeholder="Max" />
            </div>
          </div>

          {/* Primer Tm */}
          <div className="form-group">
            <label>Tm (°C)</label>
            <div className="input-row compact">
               <input type="number" name="PRIMER_MIN_TM" value={settings.PRIMER_MIN_TM} onChange={handleChange} className="form-input" placeholder="Min" step="0.1"/>
               <input type="number" name="PRIMER_OPT_TM" value={settings.PRIMER_OPT_TM} onChange={handleChange} className="form-input" placeholder="Opt" step="0.1"/>
               <input type="number" name="PRIMER_MAX_TM" value={settings.PRIMER_MAX_TM} onChange={handleChange} className="form-input" placeholder="Max" step="0.1"/>
            </div>
          </div>

          {/* Primer GC */}
          <div className="form-group">
            <label>GC (%)</label>
            <div className="input-row compact">
               <input type="number" name="PRIMER_MIN_GC" value={settings.PRIMER_MIN_GC} onChange={handleChange} className="form-input" placeholder="Min" step="0.1"/>
               <input type="number" name="PRIMER_MAX_GC" value={settings.PRIMER_MAX_GC} onChange={handleChange} className="form-input" placeholder="Max" step="0.1"/>
            </div>
          </div>
        </div>

        {/* --- KOLON 3: PROBE (INTERNAL OLIGO) --- */}
        <div className="settings-column">
          <div className="column-header" style={{color: '#059669'}}>Probe Parameters</div>

          {/* Probe Size */}
          <div className="form-group">
            <label>Size (bp)</label>
            <div className="input-row compact">
               <input type="number" name="PRIMER_INTERNAL_OLIGO_MIN_SIZE" value={settings.PRIMER_INTERNAL_OLIGO_MIN_SIZE} onChange={handleChange} className="form-input" placeholder="Min" />
               <input type="number" name="PRIMER_INTERNAL_OLIGO_OPT_SIZE" value={settings.PRIMER_INTERNAL_OLIGO_OPT_SIZE} onChange={handleChange} className="form-input" placeholder="Opt" />
               <input type="number" name="PRIMER_INTERNAL_OLIGO_MAX_SIZE" value={settings.PRIMER_INTERNAL_OLIGO_MAX_SIZE} onChange={handleChange} className="form-input" placeholder="Max" />
            </div>
          </div>

          {/* Probe Tm */}
          <div className="form-group">
            <label>Tm (°C)</label>
            <div className="input-row compact">
               <input type="number" name="PRIMER_INTERNAL_OLIGO_MIN_TM" value={settings.PRIMER_INTERNAL_OLIGO_MIN_TM} onChange={handleChange} className="form-input" placeholder="Min" step="0.1"/>
               <input type="number" name="PRIMER_INTERNAL_OLIGO_OPT_TM" value={settings.PRIMER_INTERNAL_OLIGO_OPT_TM} onChange={handleChange} className="form-input" placeholder="Opt" step="0.1"/>
               <input type="number" name="PRIMER_INTERNAL_OLIGO_MAX_TM" value={settings.PRIMER_INTERNAL_OLIGO_MAX_TM} onChange={handleChange} className="form-input" placeholder="Max" step="0.1"/>
            </div>
          </div>

          {/* Probe GC */}
          <div className="form-group">
            <label>GC (%)</label>
            <div className="input-row compact">
               <input type="number" name="PRIMER_INTERNAL_OLIGO_MIN_GC" value={settings.PRIMER_INTERNAL_OLIGO_MIN_GC} onChange={handleChange} className="form-input" placeholder="Min" step="0.1"/>
               <input type="number" name="PRIMER_INTERNAL_OLIGO_MAX_GC" value={settings.PRIMER_INTERNAL_OLIGO_MAX_GC} onChange={handleChange} className="form-input" placeholder="Max" step="0.1"/>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default PrimerSettingsForm;