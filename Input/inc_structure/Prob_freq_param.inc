*----------------------------------------stochastic values----------------------------------------
Parameter b_prob_node(byear,node)
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par prob_node.inc"
/
;
Parameter prob_node(node);

Parameter b_prob_node_trans(byear,node, node1) "transition probability from the state at one day segment to the state at the succeeding day segment"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par Prob_trans.inc"
/
;
Parameter prob_node_trans(node, node1);

Parameter freq_time(time) "frequency of a time unit"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par freq_time.inc"
/
;
parameter freq_trans(node,node1);

parameter b_freq_trans(byear,node,node1)
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par freq_trans.inc"
/
;
Parameter hour_resolution(time) "hour resolution of a time unit"
/
$INCLUDE "%PATH_IN_DATA%\inc_database\Par hour_resolution.inc"
/
;

