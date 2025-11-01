import math
import argparse
import pandas as pd
from math import ceil
try:
    from ortools.sat.python import cp_model
    ORTOOLS = True
except Exception:
    ORTOOLS = False

DEFAULT_PARAMS = {
    'cap_small': 10.0,
    'fuel_rate_small': 0.12,
    'p_fuel': 8.0,
    'C_fix': 400.0,
    'c_piece': 6.0,
    'w_piece': 0.02,
    'c_ton_long': 220.0,
    'total_weight': 80.0,
    'EF': 2.68
}

def load_routes(path='../data/jurong_10_routes_80t.csv'):
    return pd.read_csv(path)

def per_route_metrics(df, params):
    rows = []
    for _, r in df.iterrows():
        dist = float(r['route_distance_km'])
        load = float(r['load_tons'])
        trips = int(math.ceil(load / params['cap_small']))
        fuel_L = dist * params['fuel_rate_small'] * trips
        fuel_cost = fuel_L * params['p_fuel']
        fixed_cost = trips * params['C_fix']
        piece_count = int(round(load / params['w_piece']))
        piece_cost = piece_count * params['c_piece']
        rows.append({
            'route_id': int(r['route_id']),
            'dist': dist,
            'load': load,
            'trips': trips,
            'fuel_L': round(fuel_L, 3),
            'fuel_cost': round(fuel_cost, 2),
            'fixed_cost': round(fixed_cost, 2),
            'piece_count': piece_count,
            'piece_cost': piece_cost,
            'local_cost': round(fuel_cost + fixed_cost + piece_cost, 2),
            'CO2_kg': round(fuel_L * params['EF'], 2)
        })
    return pd.DataFrame(rows)

def solve_enumeration(df_costs, params):
    R = len(df_costs)
    best = None
    best_idx = None
    for bits in range(1, 1 << R):
        idxs = [i for i in range(R) if (bits >> i) & 1]
        sum_load = sum(df_costs.iloc[i]['load'] for i in idxs)
        if sum_load + 1e-9 >= params['total_weight']:
            total_cost = params['c_ton_long'] * params['total_weight'] + sum(df_costs.iloc[i]['local_cost'] for i in idxs)
            if best is None or total_cost < best['total_cost']:
                best = {'total_cost': total_cost}
                best_idx = idxs.copy()
    return best, df_costs.iloc[best_idx].reset_index(drop=True)

def export_ampl_dat(df_costs, out='../data/routes_opt.dat'):
    with open(out, 'w') as f:
        f.write('data;\n\nparam route_dist :=\n')
        for _, r in df_costs.iterrows():
            f.write(f"{int(r['route_id'])} {r['dist']}\n")
        f.write(';\n\nparam route_load :=\n')
        for _, r in df_costs.iterrows():
            f.write(f"{int(r['route_id'])} {r['load']}\n")
        f.write(';\n\nparam route_piece :=\n')
        for _, r in df_costs.iterrows():
            f.write(f"{int(r['route_id'])} {int(r['piece_count'])}\n")
        f.write(';\n\nend;\n')
    print(f'Wrote AMPL data to {out}')

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--routes', default='../data/jurong_10_routes_80t.csv')
    args = p.parse_args()
    params = DEFAULT_PARAMS.copy()
    df = load_routes(args.routes)
    df_costs = per_route_metrics(df, params)
    if ORTOOLS:
        best, selected = solve_enumeration(df_costs, params)
    else:
        best, selected = solve_enumeration(df_costs, params)
    selected.to_csv('../data/selected_routes_solution.csv', index=False)
    export_ampl_dat(df_costs)
    print('Best total cost: {:.2f}'.format(best['total_cost']))
