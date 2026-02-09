Parameter JAZ(power_plant,heat_regio) "contains the Jahreasarbeitszahl (JAZ) for Heatpumps"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par JAZ.inc"
/
;

Parameter pump_cap_fct(power_plant, bregio , time)     "capacity factor of pumping storages"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par pump_cap_fct exist.inc"
$INCLUDE "%PATH_IN_DATA%\inc_database\Par pump_cap_fct new.inc"
/
;
Parameter fct_PQ_BP(power_plant)     "PQ factor of backpressures = power performance / heat performance"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par fct_pq_bp exist.inc"
$INCLUDE "%PATH_IN_DATA%\inc_database\Par fct_pq_bp new.inc"
/
;
Parameter fct_PQ_Extr(power_plant)  "PQ factor of extractions = -power performance / heat performance"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par fct_pq_extr exist.inc"
$INCLUDE "%PATH_IN_DATA%\inc_database\Par fct_pq_extr new.inc"
/
;
Parameter min_load_fct(power_plant,heat_regio)     "minimum performance factor"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par min_load_fct exist.inc"
$INCLUDE "%PATH_IN_DATA%\inc_database\Par min_load_fct new.inc"
/
;
Parameter eff_plant(power_plant, heat_regio)     "marginal efficiency of power plants started up"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par eff_plant exist.inc"
$INCLUDE "%PATH_IN_DATA%\inc_database\Par eff_plant new.inc"
/
;
Parameter eff_plant_min(power_plant,heat_regio)     "efficiency of power plants kept online at their minimal performance"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par eff_plant_min exist.inc"
$INCLUDE "%PATH_IN_DATA%\inc_database\Par eff_plant_min new.inc"
/
;
Parameter pump_eff(power_plant,heat_regio)     "efficiency factor of hydro storages"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par pump_eff exist.inc"
$INCLUDE "%PATH_IN_DATA%\inc_database\Par pump_eff new.inc"
/
;
Parameter fl_ratio_max(bregio,month)          "maximum fill level ratio depending on months"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par fl_ratio_max.inc"
/
;
Parameter fl_ratio_min(bregio,month)          "minimum fill level ratio depending on months"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par fl_ratio_min.inc"
/
;
