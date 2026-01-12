Parameter bcap_ref(power_plant, heat_regio, byear) "total installed capacity in modelling regions in reference year"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par cap_ref exist.inc"
/
;

Parameter bcap_ref_50GWBAT(power_plant, heat_regio, byear) "installed capacity with +50 GW additional battery capacity in Europe in 2030"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par cap_ref exist_50GWBAT.inc"
/;

Parameter bcap_ref_100GWBAT(power_plant, heat_regio, byear) "installed capacity with +100 GW additional battery capacity in Europe in 2030"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par cap_ref exist_100GWBAT.inc"
/;

Parameter bcap_ref_heat(power_plant, heat_regio, byear) "total installed capacity in modelling regions in reference year"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par cap_ref_heat exist.inc"
/
;

Parameter bcap_res_wat(power_plant, heat_regio, byear) "total installed capacity in modelling regions in reference year"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par Cap_res wat.inc"
/
;
Parameter cap_res_wat(power_plant, heat_regio)

*************************this parameter is currently not in use; a negative capfn is used*****
Parameter cap_regr_fct(power_plant, bregio)       "regression factor of the power plant capacity"
;
*Parameter cap_chp_y(byear, power_plant, heat_regio)        "CHP capacity in each heat region and in each year"
*/
*$INCLUDE "%PATH_IN_DATA%\inc_database\Par cap_chp_y exist.inc"
*$INCLUDE "%PATH_IN_DATA%\inc_database\Par cap_chp_y new.inc"
*/
*;

Parameter bmax_cap(byear,primary_energy, zone) "restriction for max capacity depending on fuel type, year and zone"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par bmax_cap.inc"
/
;

Parameter b_max_cap_imports(byear) "annual upper or lower bound for h2 imports"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par bmax_cap_imports_h2.inc"
/
;

Parameter bmax_cap_wind(byear,plant_type, zone) "restriction for max capacity depending on plant type, year and zone"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par bmax_cap_wind.inc"
/
;

Parameter pump_cap(power_plant, heat_regio)
;

*if not %With_Loadflow% == Yes

Parameter btrans_cap(zone, zzone, byear, month) "transmission capacity"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par trans_cap_m.inc"
/
;

*if %With_Loadflow% == Yes
*Parameter btrans_cap(trans_line, zone, zzone, byear) "transmission capacity"
*/
*$INCLUDE "%PATH_IN_DATA%\inc_database\Par trans_cap NTC.inc"
*/
*;

Parameter btrans_cap_h2(zone, zzone, byear, month) "transmission capacity for hydrogen"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par trans_cap_m H2.inc"
/
;

Parameter trans_cap_m(zone, zzone, month) "transmission capacity"
;

Parameter trans_cap_m_h2(zone, zzone, month) "transmission capacity for hydrogen"
;


*Parameter mtdauer(power_plant, heat_regio)     "Maximale Turbinierungsdauer der SKW"
*/
*$INCLUDE "%PATH_IN_DATA%\inc_database\Par pump_duration_fct exist.inc"
*$INCLUDE "%PATH_IN_DATA%\inc_database\Par pump_duration_fct new.inc"
*/
*;


Parameter lifetime(power_plant)      "lifetime of power plants"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par lifetime new.inc"
$INCLUDE "%PATH_IN_DATA%\inc_database\Par lifetime exist.inc"
/
;
*Parameter cap_inv_year(power_plant, heat_regio)      "definition of year from which capacities can be invested in"
*/
*$INCLUDE "%PATH_IN_DATA%\inc_database\Par cap_inv_year new.inc"
*/
*;

*Parameter b_capsp(byear,power_plant,zone)      "capacity steps for the reserve calculation"

Parameter capsp(power_plant,zone)      "capacity steps for the reserve calculation"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par capsp exist.inc"
$INCLUDE "%PATH_IN_DATA%\inc_database\Par capsp new.inc"
/
;
*Parameter capsp(power_plant,zone);

*Parameter susceptance(trans_line, zone, zzone) "susceptance of the electricity transmission grid"
*/
*$INCLUDE "%PATH_IN_DATA%\inc_database\Par susceptance.inc"
*/
*;

*Parameter trans_capfn(byear, trans_line, zone, zzone) "exogenous change in transmission capacity"
*/
*$INCLUDE "%PATH_IN_DATA%\inc_database\Par trans_capfn.inc"
*
*/
*;

*Parameter max_cap_crc(zone,techgroup) "total installed capacity in modelling regions in reference year"
*/
**$INCLUDE "%PATH_IN_DATA%\inc_database\Par max_cap_crc.inc"
*/
*;
