
*-------------------Parameter declaration----------------------------

Parameter fct_PQ_BP(power_plant, zone)     "PQ factor of backpressures = power performance / heat performance"
Parameter fct_PQ_Extr(power_plant, zone)  "PQ factor of extractions = -power performance / heat performance"
Parameter min_load_fct(power_plant, zone)     "minimum performance factor"
Parameter eff_plant(power_plant, zone)     "marginal efficiency of power plants started up"
Parameter eff_plant_min(power_plant, zone)     "efficiency of power plants kept online at their minimal performance"
Parameter pump_eff(power_plant, zone)     "efficiency factor of hydro storages"
Parameter fuelusage_slope(power_plant,zone) "parameter for the calculation of fuel consumption"
Parameter fuelusage_section(power_plant,zone) "parameter for the calculation of fuel consumption"
;

*-----------------Data inclusion in Wilmar dB data structure-------------

Parameter GDATA(power_plant,zone,gdataset)     "data for generators"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par GDATA.inc"
/
;


*--------------additional data----------------------------------------------

Parameter fl_ratio_max(month)          "maximum fill level ratio depending on months"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par fl_ratio_max.inc"
/
;
Parameter fl_ratio_min(month)            "minimum fill level ratio depending on months"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par fl_ratio_min.inc"
/
;
Parameter pump_cap_fct(power_plant, zone)     "capacity factor of pumping storages"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par pump_cap_fct.inc"
/
;

*--------------------adaption of dB Data tPar declaration--------------

fct_PQ_BP(power_plant, zone)= GData(power_plant,zone,'GDCB');
eff_plant(power_plant,zone) = GDATA(power_plant, zone,'GDFULLLOAD');
eff_plant_min(power_plant,zone) = GDATA(power_plant, zone,'GDPARTLOAD');
min_load_fct(power_plant, zone) = GDATA(power_plant, zone,'GDMINLOADFACTOR');
fct_PQ_Extr(power_plant, zone)= GDATA(power_plant, zone,'GDCV');
pump_eff(power_plant, zone) = GDATA(power_plant, zone,'GDLOADLOSS');
fuelusage_slope(power_plant,zone) = GDATA(power_plant, zone,'GDFE_SLOPE');
fuelusage_section(power_plant,zone)= GDATA(power_plant, zone,'GDFE_SECTION');