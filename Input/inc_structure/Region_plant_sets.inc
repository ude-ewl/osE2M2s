*all regional sets are determined here

Set bregio     "contains all the electiricty regions and heating regions"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set bregio.inc"
/
;
alias  (bregio,bregio1);

Set zone(bregio)        "contains the model regions for electricity supply"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set zone_ptdf.inc"
/
;
alias  (zone,zzone);
alias  (zone_org,zzone);

Set country        "contains the model countries for electricity supply"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set countries.inc"
/
;

Set heat_regio(bregio)   "contains heating regions, there allocation to the elctricity regions is defined in the parameter heatregio_in_regio"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set heatregio.inc"
/
;
Set heatregio_in_zone(heat_regio, zone)
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set heatregions_in_zone.inc"
/
;

Set heatregio_in_country(heat_regio, country) "heatregions in a country"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set HeatRegions - Country.inc"
/
;

Set zone_in_country(zone, country) "zones in a country"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set Zone - Country.inc"
/
;
***all power plant sets are determined here

Set primary_energy "set of primary energies (fuels)"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set primaryenergy.inc"
/
;

Set heat_regio_co2_subset1(heat_regio)   "contains heating regions, there allocation to the elctricity regions is defined in the parameter heatregio_in_regio"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set heatregio_co2_subset1.inc"
/
;

Set heat_regio_co2_subset2(heat_regio)   "contains only heating regions for one country" 
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set heatregio_co2_subset2.inc"
/
;

Set h2_import_zones(bregio)   "contains zones that can import h2 from third countries" 
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set h2 import zones.inc"
/
;

*----------------------------------------------------------------------------------------


*------------------------- Definition of sets for power plants --------------------------
Set power_plant     "contains all the power plant types to be modelled"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set plant exist.inc"
$INCLUDE "%PATH_IN_DATA%\inc_database\Set plant new.inc"
/
;

Set fuel(power_plant,primary_energy)  "assigns thermal power plant types to used fuels"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set plant_fuel new.inc"
$INCLUDE "%PATH_IN_DATA%\inc_database\Set plant_fuel exist.inc"
/
;
Set plant_type "type of power plant groups"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set plant_type.inc"
/
;
Sets power_plant_type(power_plant, plant_type)
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set power_plant_type.inc"
/
;
Set inv_plant(power_plant) "contains all the power plant types possible for investment"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set plant new.inc"
/
;
* Subset for wind plant types
Set plant_type_wind(plant_type)
/
WIND_ON
WIND_OFF
/;

*-------------------------------------------------------------------------------------
*inv_plant_regio wird �ber b_inv_plant_regio in der Loop beschrieben und 
*ist abh�ngig vom simyear anders (oder kann es sein)
*hingegen ist inv_plant_regio2 unabh�ngig vom simyear konstant (je power_plant und heat_regio)
*und legt die grunds�tzliche Kombinationsm�glichkeit fest 

Set inv_plant_regio(power_plant, heat_regio);
Set b_inv_plant_regio(byear, power_plant, heat_regio) "constains all the power plant types which could be invested in a certain region"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set b_plant_heatregio New.inc"
/
;


Set inv_plant_regio2(power_plant, heat_regio) "constains all the power plant types which could be invested in a certain region"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set plant_heatregio new.inc"
/
;
*-------------------------------------------------------------------------------------

*fr�her hie� es mal max_capb
*Set fuel_with_Cap_Limit(primary_energy,zone) "Legt fest, f�r welche Fuels in welchen regionen Kapazit�tsrestriktionen betrachtet werden"
Set fuel_with_Cap_Limit(primary_energy) "Legt fest, f�r welche Fuels Kapazit�tsrestriktionen betrachtet werden"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set fuel_with_Cap_Limit.inc"
/
;

Set exist_plant(power_plant,heat_regio) "combination of power plant types and the region which possesses such ones"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set plant_heatregio new.inc"
$INCLUDE "%PATH_IN_DATA%\inc_database\Set Plant_HeatRegio Exist.inc"
/
;


* --------------actually not used -------------------------
*Set b_exist_plant_zone(byear,power_plant,zone) "first active plant class in Zone"
*/
*$INCLUDE "%PATH_IN_DATA%\inc_database\Set b_Plant_zone Exist.inc"
*/
*;
*Set exist_plant_zone1(power_plant,zone)


*---------------- Definitions of sets associated with power transmission ----------------
Set trans_line   "contains transmission line types"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set trans_line.inc"
/
;

Set b_exist_line_CF(byear,zone, zzone)      "existing transmission line between the adjacent regions"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set line exist CF.inc"
/
;
Set exist_line_CF(zone, zzone);

Set exist_line(trans_line,zone, zzone)      "existing transmission line between the adjacent regions"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set line exist.inc"
/
;

Set b_exist_line_CF_h2(byear,zone, zzone)      "existing h2 transmission line between the adjacent regions"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set line exist CF H2.inc"
/
;
Set exist_line_CF_h2(zone, zzone);

Set exist_line_h2(trans_line,zone, zzone)      "existing h2 transmission line between the adjacent regions"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set line exist H2.inc"
/
;

Set exist_plant_zone(power_plant,zone) "combination of power plant types and the region which possesses such ones"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set plant_zone New.inc"
$INCLUDE "%PATH_IN_DATA%\inc_database\Set plant_zone Exist.inc"
/
;


*Set heat_stor_region(heat_regio)
*/
*$INCLUDE "%PATH_IN_DATA%\inc_database\Set heat_stor_region.inc"
*/;


Set heat_regio_countries(heat_regio,country)
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set HeatRegions - Country.inc"
/;

Set HeatRegions - Country

*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
*++++++++++++++++++++++++++++++++++ cost resource courve sets - crc +++++++++++++++++++++++++++++++++++++++++
*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Set techgroup
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set Techgroup_crc.inc"
/
;

Set plant_techgroup_crc(power_plant,techgroup)
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set plant_techgroup_crc.inc"
/;

Set type_crc
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set type_crc.inc"
/;


Set techgroup_type_crc(techgroup,type_crc)
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set techgroup_type_crc.inc"
/;

*display techgroup, plant_techgroup_crc, type_crc, techgroup_type_crc;
*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
