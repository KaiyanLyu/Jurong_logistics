Jurong Logistics Optimization
=================================================

Purpose
-------
Reproducible pipeline for route-level logistics optimization using Python and AMPL.
The implementation focuses on clarity and reproducibility.

Repository layout
-----------------
- scripts/generate_routes.py        Generate clustered route summaries (CSV)
- scripts/solve_milp.py             Compute per-route metrics and solve route-selection MILP
- scripts/sensitivity_analysis.py   Sensitivity sweeps for key parameters
- models/routes_opt.mod             AMPL model (route selection with integer trips)

How to run
----------
1. Generate route data:
   python scripts/generate_routes.py --num_customers 30 --clusters 10 --total_weight 80

2. Solve route-selection (enumeration for small number of routes):
   python scripts/solve_milp.py

3. Run sensitivity analysis:
   python scripts/sensitivity_analysis.py

Remarks
-------
- For full VRP (sequencing decisions) a different MILP formulation is required.
