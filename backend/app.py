import os
import json
import uuid
import logging
import subprocess
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent 

PIPELINE_DIR = PROJECT_ROOT / "pipeline"
TOOLS_DIR    = PROJECT_ROOT / "src" / "tools"
DATA_DIR     = PROJECT_ROOT / "data" 
WORK_DIR     = PROJECT_ROOT / "jobs" 


DOCKER_HUB_IMAGE = "musakrgzn/primera_test:v15" 


WORK_DIR.mkdir(exist_ok=True, parents=True)
DATA_DIR.mkdir(exist_ok=True, parents=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class PipelineManager:
    
    @staticmethod
    def validate_inputs(filepath):                                                                                                  #securely validate and resolve file paths
        if not filepath: raise ValueError("filepath error.")
        path = Path(filepath)
        if not path.is_absolute(): path = DATA_DIR / filepath
        if not path.exists(): raise FileNotFoundError(f"file not found: {path}")
        return str(path)

    @staticmethod

    def run_pipeline(params, run_id):
        job_dir = WORK_DIR / run_id
        job_dir.mkdir(exist_ok=True)

        
        raw_filter_mode = params.get("filter_mode", "strict")
        safe_filter_mode = "contain" if raw_filter_mode == "contains" else raw_filter_mode

        raw_mode = params.get("mode", "exact")
        safe_mode = "intersect" if raw_mode == "intersection" else raw_mode

        
        custom_primer_settings = params.get("primer_settings", None)                                                                #from front primer settings
        
        primer_config_path = str(PIPELINE_DIR / "primerSettings.json")                                                              #default primer settings

        if custom_primer_settings:
            custom_config_path = job_dir / "custom_primer_settings.json"
            with open(custom_config_path, "w") as f:
                json.dump(custom_primer_settings, f, indent=4)
            primer_config_path = str(custom_config_path)

        try:
            nf_params = {
                "pslFile": PipelineManager.validate_inputs(params.get("pslFile")),
                "blatdb": PipelineManager.validate_inputs(params.get("blatdb")),
                "filtered_chrs": params.get("filtered_chrs", "chr3"), 
                "filter_mode": safe_filter_mode,
                "mode": safe_mode,
                "outdir": str(job_dir),
                "scripts_dir": str(TOOLS_DIR.resolve()),
                "primer_config": primer_config_path 
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

        
        params_file = job_dir / "params.json"
        with open(params_file, "w") as f:
            json.dump(nf_params, f, indent=4)

        
        command = [
            "nextflow", "run", str(PIPELINE_DIR / "designPrimers.nf"),
            "-params-file", str(params_file),
            "-w", str(job_dir / "work"),
            "-with-report", str(job_dir / "report.html"),
            "-with-docker", DOCKER_HUB_IMAGE
        ]
        
        logger.info(f"Pipeline running (ID: {run_id})...")
        
        
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True, cwd=str(job_dir))
            return {"status": "success", "run_id": run_id, "stdout": result.stdout}
        except subprocess.CalledProcessError as e:
            logger.error(f"Job Failed: {e.stderr}")
            return {"status": "error", "message": "Pipeline error", "stderr": e.stderr}
        except Exception as e:
            logger.error(f"Unexpected: {str(e)}")
            return {"status": "error", "message": str(e)}





@app.route('/api/run', methods=['POST'])
def run_workflow():
    data = request.json
    if not data: return jsonify({"error": "No JSON"}), 400
    run_id = str(uuid.uuid4())
    result = PipelineManager.run_pipeline(data, run_id)
    return jsonify(result), 200 if result["status"] == "success" else 500




@app.route('/api/results/<run_id>/<filename>', methods=['GET'])
def get_result_file(run_id, filename):
    allowed_files = ["results.tsv", "results.bed", "report.html"]
    if filename not in allowed_files: return jsonify({"error": "Forbidden"}), 403
    
    job_dir = WORK_DIR / run_id
    results_dir = None
    if job_dir.exists():
        for item in job_dir.iterdir():
            if item.is_dir() and item.name.startswith("primera_results_"):
                results_dir = item
                break
    if not results_dir: results_dir = job_dir
    
    try:
        return send_from_directory(results_dir, filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)