# Industrial Symbiosis Agent-Based Model

This repository contains the NetLogo source code and Python analysis scripts for an Agent-Based Model (ABM) simulating the "Hold-Up Problem" in Industrial Symbiosis networks.

## Description

This project explores the "Hold-Up Problem" in Industrial Symbiosis (IS) networks using an Agent-Based Model (ABM) built in NetLogo, accompanied by Python analysis scripts. The simulation investigates how Green Energy industrial networks survive under conditions of market turbulence, varying contract enforcement strength, and social learning.

**Key Components:**
*   **NetLogo Model (`IS_Model.nlogo`):** Simulates producer-consumer interactions where investments in green technology can be exploited ("held up") by opportunistic partners. It models dynamic market prices, risk perception, and memory-based decision making.
*   **Data Analysis:** Python scripts process BehaviorSpace experiment data to identify phase transitions ("tipping points") where network trust collapses.

The study reveals that while strong legal contracts promote stability, social mechanisms like reputation memory can effectively substitute for weak legal institutions, providing a buffer against market volatility.

## Repository Contents

- `IS_Model.nlogo`: The main Agent-Based Model source code (NetLogo 6.x).
- `analysis.py`: Python script for analyzing experiment results, generating phase transition statistics and heatmaps.
- `analysis_comparison.py`: Utility script for comparing different model versions (requires specific directory structure).
- `ABSTRACT.md`: Extended abstract describing the theoretical background and key findings.

## Requirements

### NetLogo
- NetLogo 6.3 or later is required to run `IS_Model.nlogo`.
- Standard extensions used (if any).

### Python Analysis
To run the analysis scripts, you need Python 3.8+ and the following libraries:
```bash
pip install pandas numpy matplotlib seaborn
```

## Data & Usage

**Note on Data Files:**
The BehaviorSpace experiment generates large dataset files (approx. 500MB+). This repository does **not** include the raw CSV data (`Industrial Symbiosis lock-in experiment-table.csv`) by default due to GitHub file size limits.

To replicate the analysis:
1.  Open `IS_Model.nlogo` in NetLogo.
2.  Open BehaviorSpace and run the experiment setup.
3.  Save the results as `Industrial Symbiosis lock-in experiment-table.csv`.
4.  Place the CSV file in the root directory of this repository.
5.  Run the analysis:
    ```bash
    python analysis.py
    ```

## License
MIT License
