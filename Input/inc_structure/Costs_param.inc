Parameter ir(power_plant)     "discount rate"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par ir.inc"
/
;

Parameter cost_inv0(power_plant)    "investment cost of new plants in base year"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par cost_inv new.inc"
$INCLUDE "%PATH_IN_DATA%\inc_database\Par cost_inv exist.inc"
/
Parameter cost_inv(power_plant)  "investment cost of new plants in simulation year"

Parameter gr_cost_inv "change in investment costs over the years"
/
0.00
/
;

Parameter cost_trans0(zone,zone)  "fix cost of existing plants dependent on the regions in base year"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par trans_cost.inc"

/
;

Parameter cost_trans(zone,zone)
;

Parameter cost_trans0_h2(zone,zone)  "fix cost of existing plants dependent on the regions in base year"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par trans_cost H2.inc"

/
;

Parameter cost_trans_h2(zone,zone)
;

Parameter cost_fix0(power_plant)  "fix cost of existing plants dependent on the regions in base year"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par cost_fix exist.inc"
$INCLUDE "%PATH_IN_DATA%\inc_database\Par cost_fix new.inc"
/
;
Parameter cost_fix(power_plant)  "fix cost of existing plants dependent on the regions in simulation year"

Parameter b_fuel_price(byear,primary_energy,zone)             "predicted fuel prices in the basis years"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par b_fuel_price.inc"
/
;

*Parameter b_fuel_price_m(byear,month,primary_energy,zone)             "predicted fuel prices in the basis years"
*/
*$INCLUDE "%PATH_IN_DATA%\inc_database\Par b_fuel_price_m.inc"
*/
*;
Parameter cost_misc0(power_plant)     "miscellaneous costs in base year"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par cost_misc exist.inc"
$INCLUDE "%PATH_IN_DATA%\inc_database\Par cost_misc new.inc"
/
;
Parameter cost_misc(power_plant)     "miscellaneous costs in simulation year"

Parameter cost_startup_abr0(power_plant)  "variable abrasion costs for startup process in base year"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par cost_startup_abr exist.inc"
$INCLUDE "%PATH_IN_DATA%\inc_database\Par cost_startup_abr new.inc"
/
;
Parameter cost_startup_abr(power_plant)  "variable abrasion costs for startup process in simulation year"

Parameter cost_startup_fuel(power_plant)      "variable fuel costs coefficient for startup process"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par cost_startup_fuel exist.inc"
$INCLUDE "%PATH_IN_DATA%\inc_database\Par cost_startup_fuel new.inc"
/
;


*Add H2-Import-Costs
Parameter b_h2_costs_import(byear) "h2 import costs per year"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par b_h2_costs_import.inc"
/
;

*-------Should be given in [t_CO2/MWh]-------------------
parameter co2factor(primary_energy)  "fuel specific CO2 emission factor"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par co2factor.inc"
/
;

Parameter b_co2_capture_fct(byear,power_plant)  "capture rate CO2"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par CO2_Capture_exist.inc"
$INCLUDE "%PATH_IN_DATA%\inc_database\Par CO2_Capture_new.inc"
/
;
Parameter co2_capture_fct(power_plant)  "capture rate CO2"

Parameter plant_degr_fct(byear,inv_plant)  "degression rate"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par plant_degr_fct.inc"
/
;

Parameter plant_degr_fct2(byear,power_plant)  "degression rate"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par plant_degr_fct.inc"
/
;

Parameter cost_transpoCapInv(zone,zzone)  "degression rate"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par cost_transpoCapInv.inc"
/
;
