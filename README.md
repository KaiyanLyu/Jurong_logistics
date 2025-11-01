# Jurong Logistics Optimization — Python + AMPL MILP

**Author:** KaiyanLyu

**Purpose:** Optimization of real logistics operations between Jiashan–Jurong–Zhenjiang to reduce cost and CO₂ emissions.

##  Overview
This repository documents the design and implementation of a data-driven logistics optimization framework for regional transportation between Jiashan, Zhenjiang, and Jurong. The original distribution network exhibited high operational costs and excessive fuel use due to redundant routes and inconsistent dispatch scheduling.

The project applies mathematical optimization to enhance both **economic efficiency** and **environmental sustainability**, aligning with the **United Nations Sustainable Development Goal (SDG) 9 — Industry, Innovation, and Infrastructure**. By combining spatial data modeling with optimization techniques, the study demonstrates how **digital decision tools can modernize logistics operations** and reduce environmental impact in medium-scale industrial systems.

The optimized model reduced total monthly transportation cost from approximately ¥60,000–80,000 to ¥46,377, while lowering CO₂ emissions to **954 kg**, achieving a **22.7% improvement** in overall efficiency.

##  Methodology
1. **Data Simulation:** Generate 30 customers in Jurong clustered into 10 routes using KMeans.
2. **Optimization Model:** Binary variable z_i — whether route *i* is used. Integer variable trips_i — number of truck trips for route *i*.
3. **Sensitivity Analysis:** Evaluate total cost under different fuel prices, fixed truck costs, and road factors.
The system consists of two integrated components: **route generation** and **optimization modeling**.

### Route Generation
Customer delivery points were grouped using the **K-Means clustering** algorithm to create spatially coherent delivery routes. Within each cluster, a **Nearest Neighbor heuristic** was applied to approximate realistic delivery paths based on geographical proximity and truck capacity limits. Each route was summarized by its total distance, load, and customer count.

### Optimization Model

A Mixed Integer Linear Programming (MILP) model is implemented in AMPL to determine the optimal set of routes and vehicle trips.



$$
\min C_{total} \;=\; \sum_{i} \Big( p_f \, f_r \, d_i \, t_i \;+\; C_f \, t_i \;+\; c_p \, \frac{L_i}{w_p} \, z_i \Big)
$$



$$
t_i \;\ge\; \left\lceil \dfrac{L_i}{\text{cap}} \right\rceil \, z_i
\qquad\text{for all routes } i,
$$

subject to capacity and demand constraints ensuring each route can serve its assigned load:

$$
\sum_{i} L_i \, z_i \;\ge\; L_{\text{total}}
$$



Legend:
- p_f : fuel price (RMB per liter)  
- f_r : fuel consumption rate (L per km)  
- d_i : route distance (km)  
- t_i : integer number of small-truck trips assigned to route i  
- C_f : fixed truck cost per trip (RMB)  
- c_p : per-piece handling cost (RMB per piece)  
- L_i : route load (tons)  
- w_p : weight per piece (tons per piece)  
- cap : truck capacity (tons)  
- L_total : total demand to serve (tons)

Emission levels were derived from total fuel usage using an emission factor of **2.68 kg CO₂ per liter of diesel**.

## Results
| Metric | Baseline | Optimized | Reduction |
|--------|-----------|------------|------------|
| Monthly logistics cost | ¥60,000–80,000 | **¥46,377** | **22.7%** |
| CO₂ emissions | ~1,200 kg | **954 kg** | **20.5%** |

The findings show that mathematical optimization can effectively balance cost and sustainability, providing a reproducible quantitative framework for multi-stage logistics systems.
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

## SDG 9 Alignment
This project supports **SDG Goal 9: Industry, Innovation, and Infrastructure** by demonstrating how mathematical optimization and data analytics can drive industrial modernization.  
It reflects sustainable transformation through:
- Application of algorithmic planning to real logistics systems,  
- Quantifiable improvement in energy efficiency,  
- Integration of digital modeling with ESG-oriented decision making.

##  ESG Impact
The project aligns with **ESG principles** by cutting fuel use and emissions while maintaining operational reliability.
