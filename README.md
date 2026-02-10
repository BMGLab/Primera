# Primera 

![React](https://img.shields.io/badge/Frontend-React-61DAFB?logo=react)
![Flask](https://img.shields.io/badge/Backend-Flask-000000?logo=flask)
![Nextflow](https://img.shields.io/badge/Pipeline-Nextflow-24B898)
![Docker](https://img.shields.io/badge/Container-Docker-2496ED?logo=docker)

**Primera** is a comprehensive web-based application designed to orchestrate bioinformatics pipelines for primer design. The system integrates a **React** frontend for parameter configuration, a **Flask** backend for job management, and a **Nextflow** pipeline running inside **Docker** containers for reproducible bioinformatics analysis.

---

##  Table of Contents
- [System Overview](#system-overview)
- [Architecture](#architecture)
  - [Frontend (React)](#1-frontend-architecture-react)
  - [Backend (Flask)](#2-backend-architecture-flask)
  - [Nextflow Pipeline](#3-nextflow-pipeline-workflow)
- [Data Flow](#data-flow)
- [Key Features](#key-features)
- [API Documentation](#api-documentation)
---

## System Overview

Primera GUI allows researchers to upload PSL alignment files, configure Primer3 parameters, and filter results based on genomic coordinates. The system ensures reproducibility and scalability by utilizing containerized bioinformatics tools.

**Core Stack:**
* **Frontend:** React.js (Vite)
* **Backend:** Python Flask
* **Pipeline Orchestration:** Nextflow
* **Environment:** Docker (`musakrgzn/primera_test:v15`)

---

## Architecture

### 1. Frontend Architecture (React)

The frontend manages user input, state validation, and result retrieval.

* **Main Component (`App.jsx`):**
    * **State Management:** Handles `formData` (PSL file, chromosomes, filter modes) and `primerSettings` (Tm, GC content, size).
    * **Event Handling:** Converts types (checkboxes to integers, strings to floats) before submission.
    * **Submission:** Merges configs and adds hardcoded constraints (e.g., `PRIMER_PRODUCT_SIZE_RANGE: [[100, 300]]`).

**Component Hierarchy:**
```text
App
├── Header
├── PipelineForm        # Main pipeline config (Files, Chromosomes, Filter Modes)
├── PrimerSettingsForm  # Primer3 specific parameters (Size, Tm, GC)
└── ResultsPanel        # Conditional rendering of download links

```
### 2. Backend Architecture (Flask)

```text
PROJECT_ROOT/
├── backend/        # Flask application
├── pipeline/       # Nextflow scripts (*.nf)
├── src/tools/      # Python helper scripts
├── data/           # Input files (PSL, 2bit)
└── jobs/           # Dynamic output directories per run
```
### 3. Nextflow Pipeline Workflow
```text
graph TD
    A[Input: PSL & Config] --> B[FILTER_BLAT]
    B -->|Filtered FASTA| C[RUN_PRIMER3]
    C -->|Output .prim| D[MATCH_PRIMERS]
    D -->|Matched Pairs| E[PREPARE_FOR_ISPCR]
    E -->|Split into 16 chunks| F[RUN_ISPCR (Parallel)]
    F -->|BED Files| G[FILTER_SUCCESSFUL_PRIMERS]
    G -->|TSV Data| H[WRITE_RESULTS]
    H --> I[Final Output: TSV & BED]
```

#### Process Details:
```text
*  FILTER_BLAT: Extracts sequences from 2bit genome based on PSL alignment.

*  RUN_PRIMER3: Designs primers in batches of 500 sequences.

*  MATCH_PRIMERS: Pairs forward/reverse primers with probes.

*  RUN_ISPCR: Validates primers against the genome (16 parallel instances).

*  FILTER_SUCCESSFUL_PRIMERS: Filters amplicons based on exact/intersect/subset modes.
```

##  Data Flow
### User Interaction Flow
*  Configuration: User fills PipelineForm and PrimerSettingsForm.

*  Submission: handleSubmit() sends POST request to /api/run.

*  Processing: Backend creates a job ID, generates params.json, and starts Nextflow.

*  Monitoring: Frontend waits for response.

*  Completion: On success, ResultsPanel appears with download links.

*  Retrieval: Files are downloaded via GET /api/results/{runId}/{filename}.

### File Transformations
*  PSL → FASTA (via filter.py)

*  FASTA → PRIMER3_OUT (via runPrimer3.py)

*  PRIMER3_OUT → MATCHED_PRIMERS (via matchPrimers.py)

*  MATCHED_PRIMERS → AMPLICON_BED (via isPcr)

*  AMPLICON_BED → RESULTS.TSV (via filterBED.py)


## Key Features
*  Controlled Input: React forms utilize controlled components with strict type checking.

*  Security: Path traversal prevention and file whitelisting in the API.

*  Parallelization: The pipeline splits Primer3 and isPcr tasks into chunks/channels for speed.

*  Containerization: All bioinformatics tools run in the musakrgzn/primera_test:v15 Docker image.

*  Reproducibility: Every run preserves its own params.json and logs.

##  API Documentation
###  1. Run Pipeline


*  Endpoint: ```POST /api/run```

*  Body: JSON object containing ```formData``` and ```primer_settings```.

*  Response:
```test
JSON

{
  "status": "success",
  "run_id": "uuid-string",
  "stdout": "Pipeline output log..."
}
```
### 2. Download Results
*  Endpoint      : ```GET /api/results/<run_id>/<filename>```

*  Allowed Files : ```results.tsv, results.bed, report.html.```

*  Logic         : ```Searches in jobs/{run_id}/primera_results_*/ or the job root.```
