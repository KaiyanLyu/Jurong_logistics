import math
import random
import argparse
from math import radians, sin, cos, atan2, sqrt
from typing import List, Dict
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

DEPOT_LAT = 31.95787
DEPOT_LON = 119.15953

def haversine_km(a_lat, a_lon, b_lat, b_lon):
    R = 6371.0
    dlat = radians(b_lat - a_lat)
    dlon = radians(b_lon - a_lon)
    u = sin(dlat/2)**2 + cos(radians(a_lat))*cos(radians(b_lat))*sin(dlon/2)**2
    return 2 * R * atan2(sqrt(u), sqrt(1-u))

def random_point(lat, lon, radius_km, rng):
    r = rng.uniform(0, radius_km)
    theta = rng.uniform(0, 2*math.pi)
    dx = r * math.cos(theta)
    dy = r * math.sin(theta)
    lat_new = lat + (dy / 111.0)
    lon_new = lon + (dx / (111.0 * math.cos(radians(lat))))
    return lat_new, lon_new

def build_routes(num_customers: int = 30,
                 clusters: int = 10,
                 km_radius: float = 20.0,
                 total_weight: float = 80.0,
                 seed: int = 42,
                 road_factor: float = 1.3):
    rng = random.Random(seed)
    pts = []
    rel = []
    for i in range(num_customers):
        lat, lon = random_point(DEPOT_LAT, DEPOT_LON, km_radius, rng)
        pts.append({'id': i+1, 'lat': lat, 'lon': lon})
        rel.append(rng.uniform(0.5, 1.5))
    rel = np.array(rel)
    demands = (rel / rel.sum()) * total_weight
    for i in range(num_customers):
        pts[i]['demand_t'] = float(round(demands[i], 3))
    coords = np.array([[p['lat'], p['lon']] for p in pts])
    kmeans = KMeans(n_clusters=clusters, random_state=seed).fit(coords)
    labels = kmeans.labels_
    clusters_dict = {}
    for i, lbl in enumerate(labels):
        clusters_dict.setdefault(int(lbl+1), []).append(pts[i])
    rows = []
    for rid, members in sorted(clusters_dict.items()):
        # nearest-neighbor order (simple heuristic)
        unvisited = members.copy()
        curr = {'lat': DEPOT_LAT, 'lon': DEPOT_LON}
        order = []
        total_dist = 0.0
        total_load = 0.0
        while unvisited:
            dists = [haversine_km(curr['lat'], curr['lon'], c['lat'], c['lon']) for c in unvisited]
            idx = int(np.argmin(dists))
            nxt = unvisited.pop(idx)
            total_dist += dists[idx]
            order.append(nxt['id'])
            total_load += nxt['demand_t']
            curr = {'lat': nxt['lat'], 'lon': nxt['lon']}
        total_dist += haversine_km(curr['lat'], curr['lon'], DEPOT_LAT, DEPOT_LON)
        rows.append({
            'route_id': rid,
            'route_distance_km': round(total_dist * road_factor, 2),
            'load_tons': round(total_load, 3),
            'num_customers': len(members),
            'visit_order': order
        })
    return pd.DataFrame(rows).sort_values('route_id')

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Generate clustered Jurong routes.')
    p.add_argument('--num_customers', type=int, default=30)
    p.add_argument('--clusters', type=int, default=10)
    p.add_argument('--total_weight', type=float, default=80.0)
    p.add_argument('--out', type=str, default='../data/jurong_10_routes_80t.csv')
    args = p.parse_args()
    df = build_routes(args.num_customers, args.clusters, total_weight=args.total_weight)
    df.to_csv(args.out, index=False)
    print(f'Wrote {len(df)} routes to {args.out}')
