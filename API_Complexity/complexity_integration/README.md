# `complexity_integration`

This package groups the core components used for API complexity (uncertainty) experiments:

1. **Complexity matching** – measure relevance between complexity and API functions
2. **Scenario generation** – turn abstract complexity types into realistic scenarios
3. **Scenario assessment** – evaluate those scenarios

---
## 1. Complexity matching

### `generate_all_assessments.py`
- Takes API function descriptions from all 7 environments and generates uncertainty assessment instructions (prompt templates) for each API function against each uncertainty type.
- Output directory: `api_assessments/` (note: this directory may not exist yet in the current repo state).

### `generate_all_assessments.ipynb`
- Notebook version of the same idea as `generate_all_assessments.py`.
- Used for interactive exploration, debugging, and inspecting individual assessment templates while you develop or refine them.
- The `.py` script is for batch / CLI runs; the `.ipynb` is for step‑by‑step, manual runs.

### `run_assessments.ipynb`
- Loads the assessment templates created with `generate_all_assessments.py` / `.ipynb` and runs them through Claude to obtain uncertainty assessments.
- Expected to read from `api_assessments/` and write results into directories like `api_assessment_{0,1,2}/` for multiple runs.

---
## 2. Scenario generation

### `generate_inst_scenarios.ipynb`
- Generates realistic uncertainty **scenario templates (INST)** for the top function–uncertainty pairs.
- Writes instruction templates under the `inst_scenarios/` directory.

### `generate_complexity_scenarios.ipynb`
- Converts abstract uncertainty types into specific, practical manifestations for API functions by processing the instructional scenario templates in `inst_scenarios/` through Claude.
- Writes model‑generated scenario JSON files under `inst_scenarios_gen/inst_scenarios_gen_run_{run_id}/`.

### `organize_scenarios.py`
- Organizes the raw scenarios from `inst_scenarios_gen/inst_scenarios_gen_run_*` into a canonical structure grouped by domain, function, and uncertainty type.
- Output directory: `complexity_scenario_assessment/organized_scenarios/`.

---
## 3. Scenario assessment

### `scenario_assessment.py`
- Generates assessment templates (Markdown) for uncertainty scenarios stored in `organized_scenarios/`.
- For each domain–function–uncertainty–run combination, produces a `*_assessment.md` file under `scenario_assessments/`.

### `scenario_assessment_cluade_run.ipynb`
- Processes scenario assessment templates through Claude to evaluate uncertainty scenarios.
- Takes the templates generated in the `scenario_assessments/` directory and obtains detailed evaluations for each scenario, saving them for downstream analysis.
