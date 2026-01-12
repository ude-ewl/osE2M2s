*Parameter demand(time, bregio,product) "demand for electricity and heat"
*;

Parameter heat_demand_ratio(heat_regio)  "proportion ratio of individual heat regions in the total heat demand in a modelling region"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par heat_demand_ratio.inc"
/
;
*Parameter demand_fct_y(byear, bregio, product) "annual demand growth rate for electricity and heat in each region"
*/
*$INCLUDE "%PATH_IN_DATA%\inc_database\Par demand_factor_year.inc"
*/
*;

Parameter demand_Y(byear,time, bregio, product) "annual demand for electricity and heat in each region"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par demand.inc"
/;
Parameter demand(time,bregio,product) "demand for electricity and heat in each region filled from demand_Y";


Parameter b_demand_emob_fix(byear,time, bregio, product) "annual time resolution for electricity demand of fixed e-mob demand (dumb charging)"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par demand_emob_fix.inc"
/;
Parameter demand_emob_fix(time,bregio,product) "electricity demand of fixed e-mob demand (dumb charging) filled from b_demand_emob_fix";


*Parameter b_el_dem_max(byear,bregio) "max hourly demand for electricity in each region"
*/
*$INCLUDE "%PATH_IN_DATA%\inc_database\Par el_dem_max.inc"
*/;
*Parameter el_dem_max(zone);


Parameter b_heat_dem_max(byear,bregio) "max hourly demand for heat in each region"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par heat_dem_max.inc"
/;
Parameter heat_dem_max(heat_regio);


Parameter ex_foreign_trade(byear,time, bregio, product) "annual foreign trade for electricity in each region"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par ex_foreign_trade.inc"
/;

*========================================= demand for smart charging e-mobility======================================
Parameter b_demand_clusterEmob(byear, power_plant,heat_regio) "overall demand of e-mobility cluster (power_plant) in heatregion and simyear"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par DemandClusterEmob.inc"
/;
Parameter demand_clusterEmob(power_plant,heat_regio);

Parameter b_idemand(time,power_plant,byear)"proportional demand of a e-mobility cluster (demand_clusterEmob) in a timestep"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par iDemandEmob.inc"
/;
Parameter idemand(time, power_plant);
*===================================================================================================================


*Parameter RES_bio(byear,time, bregio, product) "annual biomass production"
*/
*$INCLUDE "%PATH_IN_DATA%\inc_database\Par Biomass Power.inc"
*/;


*Parameter RES_geo(byear,time, bregio, product) "annual geothermie production"
*/
*$INCLUDE "%PATH_IN_DATA%\inc_database\Par Geothermal Power.inc"
*/;


*Parameter RES_sun(byear,time, bregio, product) "annual solar production"
*/
*$INCLUDE "%PATH_IN_DATA%\inc_database\Par Solar Africa Power.inc"
*/;


*Parameter DisGen(byear, time, bregio, product) "annual distributed generation"
*/
*$INCLUDE "%PATH_IN_DATA%\inc_database\Par DisGen Power.inc"
*/;
