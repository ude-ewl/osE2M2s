*** This include files determines all time and node sets for E2M2s

*-----------Definition of sets for basis and simulated years-------------------------
Set byear
/
2000*2100
/;

Set simyear(byear) "set of simyears which are executed consecutively"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set simYears.inc"
/
;

*-----------Definition of sets for time steps-------------------------
Set hour         "represents the smallest time unit simulated in the model"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set hour.inc"
/
;
alias(hour, hour1);

Set day_type     "describes the characteristic days considered in the model"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set day_type.inc"
/
;
alias (day_type, day_type1);

Set month   "describes the aggregration of months in the model"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set month.inc"
/
;
alias(month, month1);


Set day_segment    "determines time segments one day is divided into in the model"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set day_segment.inc"
/
;
alias(day_segment, day_segment1);


Set water_scen  "determines how many water scenarios are considered in the model"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set water_scen.inc"
/
;
alias(water_scen, water_scen1);


Set wind_scen "determines how many wind scenarios are considered in the model"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set wind_scen.inc"
/

;
alias(wind_scen, wind_scen1);


set hour_segment(hour, day_segment) "relates set 'hour' tSet 'day_segment'"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set hour_segment.inc"
/
;

Set node
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set node.inc"
/
;
Alias(node, node1);


Set time
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set time.inc"
/
;
Alias(time, time1);


Set daytype_node(day_type, node)
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set type_node.inc"
/
;

Set month_node(month, node)
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set month_node.inc"
/
;

Set segment_node(day_segment, node)
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set segment_node.inc"
/
;
Set wat_node(water_scen, node)
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set wat_node.inc"
/
;

Set win_node(wind_scen, node)
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set wind_node.inc"
/
;


Set daytype_time(day_type, time)
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set type_time.inc"
/

;
Set month_time(month, time)
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set month_time.inc"
/
;

Set hour_time(hour, time)
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Set hour_time.inc"
/

Parameter numyear(byear) "numerical value of year"
;
* assumption that byear always starts with year 2000

numyear(byear)=ord(byear)+1999;
