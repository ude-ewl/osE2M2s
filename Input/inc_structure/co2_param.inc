Parameter co2_bound                       "exogenous given bound of CO2 emissions"
;
parameter bco2_bound(byear)     'CO2-restriction for all single years'
/
$INCLUDE "%PATH_IN_DATA%\inc_database\par bco2_bound.inc"
/
;

Parameter co2_bound2                       "exogenous given bound of CO2 emissions"
;
parameter bco2_bound2(byear)     'CO2-restriction for all single years'
/
$INCLUDE "%PATH_IN_DATA%\inc_database\par bco2_bound2.inc"
/
;

parameter co2_cost             'CO2-costs for the year in the optimisation'
;
parameter bco2_cost(byear)     'CO2-costs for all single years'
/
$INCLUDE "%PATH_IN_DATA%\inc_database\par bco2_cost.inc"
/
