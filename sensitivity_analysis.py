"""Sensitivity analysis for selected routes.
Varies fuel price, fixed cost, and road factor.
Outputs sensitivity_results.csv.
"""

import pandas as pd

def load_selected(path='../data/selected_routes_solution.csv'):
    return pd.read_csv(path)

def run(selected, fuel_prices=(6.4,8.0,9.6), fixed_costs=(320,400,480), road_factors=(1.1,1.3,1.5)):
    rows = []
    for pf in fuel_prices:
        for cf in fixed_costs:
            for rf in road_factors:
                long_cost = 220.0 * 80.0
                local_cost = 0.0
                E_local = 0.0
                for _, r in selected.iterrows():
                    dist = float(r.get('dist', r.get('route_distance_km', 30.0))) * rf
                    trips = int(r.get('trips', 1))
                    fuel_L = dist * 0.12 * trips
                    local_cost += fuel_L * pf + trips * cf + r.get('piece_cost', 0)
                    E_local += fuel_L * 2.68
                rows.append({'p_fuel': pf, 'C_fix': cf, 'road_factor': rf,
                             'total_cost': round(long_cost + local_cost, 2),
                             'E_total_kg': round(E_local + (4 * 220.0 * 0.35 * 2.68), 2)})
    return pd.DataFrame(rows)

if __name__ == '__main__':
    sel = load_selected()
    df = run(sel)
    df.to_csv('../data/sensitivity_results.csv', index=False)
    print('Wrote sensitivity_results.csv')
