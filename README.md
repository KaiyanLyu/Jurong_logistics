# Jurong Logistics Optimization — Python + AMPL MILP

**Author:** KaiyanLyu
**Purpose:** Optimization of real logistics operations between Jiashan–Jurong–Zhenjiang to reduce cost and CO₂ emissions.

##  Overview
This repository implements a hybrid optimization workflow using **Python** for data generation and clustering, and **AMPL** for solving a **Mixed Integer Linear Programming (MILP)** model of route selection.

##  Methodology
1. **Data Simulation:** Generate 30 customers in Jurong clustered into 10 routes using KMeans.
2. **Optimization Model:** Binary variable z_i — whether route *i* is used. Integer variable trips_i — number of truck trips for route *i*.
3. **Sensitivity Analysis:** Evaluate total cost under different fuel prices, fixed truck costs, and road factors.

##  Results
- **Optimized monthly cost:** ¥46,377  
- **Baseline cost:** ¥60,000–80,000  
- **CO₂ reduced to:** 954 kg  
- **Savings:** ≈ 22.7 %

##  Requirements
Python ≥ 3.10  
Libraries: pandas, numpy, scikit-learn, matplotlib  
AMPL or solver 

##  Run Instructions
```bash
python scripts/generate_routes.py
python scripts/solve_milp.py
python scripts/sensitivity_analysis.py
```

##  ESG Impact
The project aligns with **ESG principles** by cutting fuel use and emissions while maintaining operational reliability.
