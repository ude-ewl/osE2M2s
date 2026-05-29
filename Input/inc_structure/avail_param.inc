
* This file contains all parameters which consider the availability of generation units

Parameter availability(power_plant, month) "monthly availability of power plants"
/
$INCLUDE %PATH_IN_DATA%\inc_database\Par availability exist.inc
$INCLUDE %PATH_IN_DATA%\inc_database\Par availability new.inc
/;


Parameter b_wind_onshore(byear,bregio,node,time) "natural wind intensity onshore, given as a proportion in the installed wind power capacities"
/
$INCLUDE %PATH_IN_DATA%\inc_database\Par wind_onshore.inc
/
;
Parameter wind_onshore(bregio,node,time);


Parameter b_wind_offshore(byear,bregio,node,time) "natural wind intensity offshore, given as a proportion in the installed wind power capacities"
/
$INCLUDE %PATH_IN_DATA%\inc_database\Par wind_offshore.inc
/
;
Parameter wind_offshore(bregio,node,time);

Parameter b_PV(byear,bregio,node,time) "natural sun irradiance intensity, given as a proportion in the installed pv capacities"
/
$INCLUDE %PATH_IN_DATA%\inc_database\Par PV.inc
/
;
Parameter PV(bregio,node,time);


Parameter b_wind_onshore_crc(byear,bregio,power_plant,node,time) "natural wind intensity onshore, given as a proportion in the installed wind power capacities"
/
$INCLUDE %PATH_IN_DATA%\inc_database\Par wind_onshore_crc.inc
/
;
Parameter wind_onshore_crc(bregio,power_plant,node,time);


Parameter b_wind_offshore_crc(byear,bregio,power_plant,node,time) "natural wind intensity offshore, given as a proportion in the installed wind power capacities"
/
$INCLUDE %PATH_IN_DATA%\inc_database\Par wind_offshore_crc.inc
/
;
Parameter wind_offshore_crc(bregio,power_plant,node,time);


Parameter b_PV_crc(byear,bregio,power_plant,node,time) "natural wind intensity offshore, given as a proportion in the installed wind power capacities"
/
$INCLUDE %PATH_IN_DATA%\inc_database\Par PV_crc.inc
/
;
Parameter PV_crc(bregio,power_plant,node,time);


Parameter b_inflow_run_river(byear,node, time, power_plant, bregio) "maximum water inflow of the river plants"
/
*---- ChangeLog 17.01.2018 --- früher Par inflow must run av.inc -----
$INCLUDE %PATH_IN_DATA%\inc_database\Par b_inflow_run_river.inc
*----------------- end of changeLog 17.01.18-------------------------
/
;
Parameter inflow_run_river(node, time, power_plant, bregio)
;


*Parameter inflow_storage(node, time, power_plant, bregio) "inflow of hydro storage"
*/
*$INCLUDE %PATH_IN_DATA%\inc_database\Par inflow_storage.inc
*/
*;

*---------umbenannt, da es so genauer ist: ChangeLog 17.01.2018 --- früher b_inflow_ConvWater und inflow_ConvWater
Parameter b_inflow_annual_storage(byear,node, time, power_plant, bregio) "total inflow"
/
$INCLUDE %PATH_IN_DATA%\inc_database\Par inflow_annual_storage.inc
/
;

Parameter inflow_annual_storage(node, time, power_plant, bregio)
;
*----------------- end of changeLog 17.01.18-------------------------

Parameter b_fill_level_max(byear,power_plant, bregio)     "the maximal possible fill level of hydro storages"
/
$INCLUDE %PATH_IN_DATA%\inc_database\Par fill_level_max exist.inc
/
;
Parameter fill_level_max(power_plant, bregio)
;

*Parameter b_fill_level_heat_max(byear, bregio)     "the maximal possible fill level of hydro storages"
*/
*$INCLUDE %PATH_IN_DATA%\inc_database\Par fill_level_heat_max exist.inc
*/
*;
*Parameter fill_level_heat_max(bregio)
*;

Parameter avail_trans_cap(bregio, bregio1,byear)       "availability of transmission capacities"
/
$INCLUDE %PATH_IN_DATA%\inc_database\Par avail_trans_cap.inc
/
;

Parameter avail_trans_cap_h2(bregio, bregio1,byear)       "availability of transmission capacities for hydrogen"
/
$INCLUDE %PATH_IN_DATA%\inc_database\Par avail_trans_cap H2.inc
/
;

Parameter reliab(power_plant,zone)
/
$INCLUDE %PATH_IN_DATA%\inc_database\Par reliab exist.inc
$INCLUDE %PATH_IN_DATA%\inc_database\Par reliab new.inc
/
;

Parameter b_max_cap_nuclear(byear, country)
/
$INCLUDE %PATH_IN_DATA%\inc_database\Par max_cap_nuclear.inc
/
;
Parameter max_cap_nuclear(country)

Parameter b_max_cap_wind_off(byear, country)
/
$INCLUDE %PATH_IN_DATA%\inc_database\Par max_cap_wind_off.inc
/
;
Parameter max_cap_wind_off(country)

*========================================= availabilities for smart charging e-mobility (cluster)====================
*leaving means not able to load anymore in this context!

Parameter b_iLeave(time,power_plant,byear)"proportional amount of leaving cars of a e-mobility cluster (power_plant) in a timestep"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par iLeaveEmob.inc"
/;
Parameter iLeave(time,power_plant);

*arriving means able to load again in this context!
Parameter b_iArrive(time,power_plant,byear)"proportional amount of arriving cars of a e-mobility cluster (power_plant) in a timestep"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par iArriveEmob.inc"
/;
Parameter iArrive(time,power_plant);

Parameter b_iLoadPoss(time,power_plant,byear)"proportional amount cars of a e-mobility cluster (power_plant) which are able to load in a timestep"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par iLoadPossEmob.inc"
/;
Parameter iLoadPoss(time,power_plant);

*MSB 20210819: Add simultaneity parameter for smartchargers which can load simultaneously in a specific timestep
Parameter b_iLoadSimultaneity(time,power_plant,byear)"proportional amount cars of a e-mobility cluster (power_plant) which are able to load in a timestep simultaneously"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par iLoadSimultaneity.inc"
/;
Parameter iLoadSimultaneity(time,power_plant);
