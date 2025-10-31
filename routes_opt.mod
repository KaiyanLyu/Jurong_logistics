# routes_opt.mod - AMPL MILP model
set ROUTES;
param route_dist{ROUTES};
param route_load{ROUTES};
param route_piece{ROUTES};
param cap_small; param total_weight; param c_ton_long; param p_fuel;
param fuel_rate_small; param C_fix; param c_piece; param w_piece;

var z{r in ROUTES} binary;
var trips{r in ROUTES} integer >= 0;

s.t. CoverLoad{r in ROUTES}: trips[r]*cap_small >= route_load[r]*z[r];
s.t. ServeAll: sum{r in ROUTES} route_load[r]*z[r] >= total_weight;

minimize TotalCost:
    c_ton_long*total_weight + sum{r in ROUTES}(p_fuel*fuel_rate_small*route_dist[r]*trips[r] + C_fix*trips[r] + c_piece*route_piece[r]*z[r]);
