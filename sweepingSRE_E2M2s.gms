*insert correct path before starting 
$SETGLOBAL PATH_IN_DATA C:\...\Input
$SETGLOBAL PATH_OUT C:\...\Output

Option LP = cplex;
Option iterlim = 10000000;
Option reslim = 150000000;
* Parallel computation as desired
Option threads = 6;
Option LIMROW=0, LIMCOL=0, SOLPRINT=off, sysout = off;
$ONEMPTY

$onecho > cplex.o26
lpmethod 4
aggind 0
solutiontype 2
barepcomp 1.0e-07
$offecho

*---------------- Switch for h2 demand --------------------------------------------------
* Yearly h2 demand vs demand per time segment
$SetGlobal h2_yearly YES

*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ SETS @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

*---------------------- Definition of Sets for nodes and time resolution ----------------------------------
$include "%PATH_IN_DATA%\inc_structure\node_time_sets.inc";
display simyear;

*---- calculated Sets relating to Node and Time
Set node_hour(node, hour);
loop(day_segment,
node_hour(node, hour)$(segment_node(day_segment, node) and hour_segment(hour, day_segment)) = yes
);

Set month_succ(month, month1) "succeeding order of months";
month_succ(month, month1)=yes$(ord(month1)-ord(month) eq 1);
month_succ(month, month1)$((ord(month) eq card(month))$(ord(month1) eq 1))=yes;

Set node_time(node, time);
loop((day_type, hour, month),
node_time(node, time)$(daytype_time(day_type, time) and month_time(month, time)and hour_time(hour, time) and daytype_node(day_type, node) and month_node(month, node) and node_hour(node, hour))=yes
);

Set time_succ(time, time1);

loop((day_type, month, hour, hour1)$(ord(hour1)-ord(hour) eq 1),
     time_succ(time, time1)$(daytype_time(day_type, time) and daytype_time(day_type,time1) and month_time(month, time)and month_time(month, time1) and hour_time(hour, time) and hour_time(hour1, time1))= yes
);
loop((month, month1, hour, hour1)$(((ord(hour1) eq 1) and (ord(hour) eq card(hour))) and (sameas(month, month1) or month_succ(month, month1))),
     time_succ(time, time1)$(month_time(month, time)and month_time(month1, time1) and hour_time(hour, time) and hour_time(hour1, time1))=yes
);

Set node_trans(node, node1);
loop((node, node1, day_segment, day_segment1, time, time1)$((not sameas(day_segment, day_segment1)) and segment_node(day_segment, node) and segment_node(day_segment1, node1) and time_succ(time, time1) and node_time(node, time) and node_time(node1, time1)),
         node_trans(node, node1)=yes;
);
node_trans(node, node)=yes;

Set node_succ(node, node1, time, time1);
node_succ(node, node1, time, time1)$(node_trans(node, node1) and time_succ(time, time1) and node_time(node, time) and node_time(node1, time1) )=yes;

Set time_hour_segment(time, hour, day_segment);
time_hour_segment(time, hour, day_segment)$(hour_segment(hour,day_segment) and hour_time(hour,time))=yes;

Set time_segment(time, day_segment);
loop((time, day_segment, hour)$time_hour_segment(time, hour, day_segment),
time_segment(time, day_segment)=yes;
);

*use a different combination for daily storages in order to have only one scenario within the days
Set node_succ_4_storage(node1, node, time1, time);

node_succ_4_storage(node1, node, time1, time) =   node_succ(node1, node, time1, time);

loop((wind_scen,month, day_type),
node_succ_4_storage(node1, node, time1, time)$((month_node(month, node) and month_node(month, node1)
                                         and daytype_node(day_type, node) and  daytype_node(day_type, node1) )
                                         and ( win_node(wind_scen,node) xor win_node(wind_scen,node1)  )) = no;
);

*-----------------------------------------------------------------------------------------------
Set product /electricity, heat, h2, methane/;
Set category /fuel, fuel_cost, fuel_price, cost_misc, eff, cost_CO2, cap_exist, CO2_capt_fct, CO2_fct/;
Set spill /spill1, spill2/;

*----------------------------- Definition of Sets for regions ----------------------------------
$include "%PATH_IN_DATA%\inc_structure\Region_plant_sets.inc";

*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ PARAMETERS @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

*------------------------ Parameters for probabilities and frequencies--------------------------
$include "%PATH_IN_DATA%\inc_structure\Prob_freq_param.inc";

*-------------- Imported parameters for costs --------------------------------------------------
$include "%PATH_IN_DATA%\inc_structure\costs_param.inc";

*--------------------- Declaration of parameters for capacities --------------------------------
$include "%PATH_IN_DATA%\inc_structure\cap_param.inc";

*---------------- Parameters for availabilities of plants and nature resourses -----------------
$include "%PATH_IN_DATA%\inc_structure\avail_param.inc";

*------------------------ Parameters for efficiencies of power plants --------------------------
$include "%PATH_IN_DATA%\inc_structure\eff_param.inc";

*------------------------ Declaration of parameters for demands  -------------------------------
$include "%PATH_IN_DATA%\inc_structure\demand param.inc";

*-------------------------Declaration of parameters for co2-------------------------------------
$include "%PATH_IN_DATA%\inc_structure\co2_param.inc";

* ------------------------- Scalars for reserve-------------------------------------------------
Scalar angle_limit "limits the voltage angle between grid buses [/Radiant(30�)"  /0.5236/;
scalar resfkt_heat "Proportion of the installed capacity which is considered for heat_reserve" /0.02/;
scalar spin_fctPos "Proportion of the production of each zone which is considered for spinning (primary and secondary) pos reserve --> FCR+ and aFRR+" /0.0337/;
scalar spin_fctNeg "Proportion of the production of each zone which is considered for spinning (primary and secondary) neg reserve --> FCR- and aFRR-" /0.0311/;
scalar res_fct_MRLpos "Proportion of peak load which is considered for pos tertiary reserve --> mFRR+" /0.0214/;
scalar res_fct_MRLNeg "Proportion of peak load which is considered for neg tertiary reserve --> mFRR-" /0.0208/;
*-----------------------------------------------------------------------------------------------

* ------------------------- Scalar for storage--------------------------------------------------
scalar fullload_discharge "fullload_discharge represents the ratio of storage capacity and power (duration of discharge at full load)" /3/;

*----------------------------- Calculated parameters -------------------------------------------
Parameters
        fuel_price(primary_energy,zone)   "container fo fuel prices during the simulation process"
        fuel_price_m(month,primary_energy,zone)
        cost_opr(time, power_plant,bregio) "specific operating costs of existing plants when started up, will be calculated later"
        cost_opr_min(time, power_plant,bregio) "specific operating costs of existing plants at minimum load, will be calculated later"
        cost_CO2(time, power_plant,bregio)
        cost_CO2_min(time, power_plant,bregio)
        cost_startup(time, power_plant, bregio) "specific startup cost"
        co2emis(power_plant, heat_regio)    "co2 emission factor at normal performance"
        co2emis_min(power_plant, heat_regio)   "co2 emission factor at minimal performance"
        max_cap(primary_energy,zone) "maximum capacity"
        max_cap_wind(plant_type, zone) "maximale Kapazitaet depending on wind tech"
        max_cap_imports "upper or lower bound for h2 imports"
        trans_cap_CF(zone, zzone)
        trans_cap_CF_h2(zone, zzone)
        cap_ref(power_plant, heat_regio)     "container for adapted power plant capacities"
        cap_ref_heat(power_plant, heat_regio)     "container for adapted power plant capacities"
        cap_inv_max(power_plant, zone) "container for adapted maximum investment capacities"
        cap_chp(power_plant, heat_regio) "capacity of each CHP in each heat reigon"
        cap_chp_tot(power_plant, zone) "total capacity of a chp in one region"
        cap_chp_tot_calibr(power_plant, zone) "calibrated tot chp capacity in one region"
        cap_chp_calibr(power_plant, heat_regio) "CHP capacity calibration based on the IEA data"
        cap_n(power_plant, heat_regio)        "container for new power plant capacity during the simulation process"
        cap_n_sunk(power_plant, heat_regio)   "container for new power plant capacity during the simulation process, for the purpose of caculating sunk costs"
        cap_n_sunk_heat(power_plant, heat_regio)   "container for new power plant capacity during the simulation process, for the purpose of caculating sunk costs"
        demand_reserve(zone, product)    "to be endogenous calculated reserve requirement"
        annuity(power_plant)        "annuity of the invested plants"
        h2_costs_import    "container for h2 import costs"
;

*Calculation of annuity factors for each technology using exponential discounting
annuity(power_plant) = ir(power_plant)/(1-(1+ir(power_plant))**(-lifetime(power_plant)));

*---------------------------- Parameters for output --------------------------------------------
Parameters
        out_cap(simyear, power_plant, bregio)
        out_cap_infeasible(simyear, node, time, product, bregio)
        out_cap_new(simyear, power_plant, zone)
        out_cap_onl(simyear, time, node, power_plant, bregio)
        out_cap_startup(simyear, time, node, time1, node1, power_plant, bregio)
        out_co2emissions(zone,simyear)  "total CO2 emission from all power plants"
        out_co2_price(simyear)  "co2 prices"
        out_co2_price2(simyear)  "co2 prices specific Country from co2_bound2"
        out_demand(simyear, time, zone, product)
        out_demand_y(simyear, zone, product)
        out_el_price(simyear, node, time, zone)  "electricity prices"
        out_fill_level_h_exp(simyear, time, power_plant, bregio)
        out_heat_price(simyear, node, time, heat_regio)  "heat prices"
$ifi '%h2_yearly%' == Yes       out_h2_price(simyear, zone)  "hydrogen prices"
$ifi NOT '%h2_yearly%' == Yes   out_h2_price(simyear, node, time, zone)  "hydrogen prices"
        out_production(simyear, time, node, power_plant, bregio, product)
        out_production_y(simyear, power_plant, bregio, product) "yearly production per power plant and product"
        out_tcost(simyear)   "total costs"
        out_transpo(simyear, node, time, zone, zzone) "transport of energy between zones"
        out_transpo_y(simyear, zone, zzone) "calculated yearly transport of energy between zones"
        out_transpo_h2(simyear, node, time, zone, zzone) "transport of h2 between zones"
        out_transpo_h2_y(simyear, zone, zzone) "calculated yearly transport of h2 between zones"
        out_v_pump(simyear, node, time, power_plant, zone) "pumping/charging power of each power_plant in zone"
        out_v_pump_y(simyear, power_plant, zone) "yearly pumping/charging power of each power_plant in zone"
        out_v_pump_reserve(simyear, node, time, power_plant, zone)
        out_v_cur(simyear, node, time, power_plant, bregio)     "output of variable v_curtailment"
        out_v_cur_y(simyear, power_plant, bregio)               "yearly output of variable v_curtailment"
        out_cur_cost(simyear)                                   "total curtailment costs"
        out_var_cost_opr(simyear,time,power_plant,heat_regio)
        out_var_cost_startup(simyear,time,power_plant,heat_regio)
        out_var_cost_trans(simyear,time,zone,zzone)
        out_var_cost_trans_h2(simyear,time,zone,zzone)
        out_var_cost_co2(simyear,time,power_plant,heat_regio)
        out_fix_cost_irr(simyear,power_plant,heat_regio)
        out_fix_cost_sunk(simyear,power_plant,heat_regio)
        out_fix_cost_rev(simyear,power_plant,heat_regio)
        out_total_cost_reg(simyear, power_plant,heat_regio)
        out_demand_max(simyear, bregio, product) "output parameter to safe max demands per demand group"
        cap_exist(simyear, power_plant, bregio)
        val_spill(simyear, node, time,spill, power_plant, bregio)
        out_h2_import_costs(simyear)                    "output parameter for total h2 import costs"
        out_v_import_h2_y(simyear, zone)                "output parameter for yearly h2 imports"
$ifi NOT '%h2_yearly%' == Yes   out_v_import_h2(simyear, node, time, zone)      "output parameter for h2 imports"
;

*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ VARIABLES @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Free Variables
         total_cost      "to be minimized total cost over the current simulated period (simyear)"
         var_cost         "variable cost over the current simulated period for one node"
         var_cost_opr
         var_cost_startup
         var_cost_trans
         var_cost_trans_h2
         var_cost_co2     "Costs for emissions which exceed the co2 bound"
         var_fix_cost_irr
         var_fix_cost_rev
         var_trans_cost
         v_cur_cost      "total costs of curtailment"
         v_h2_cost       "total costs of h2 import"
;
Positive Variables
         v_fix_cost_sunk
         v_cap_new(power_plant,heat_regio)       "to be invested new capacities for electricity regarding plant type and region"
         v_cap(power_plant, heat_regio)         "installed capacities of existing plants"
         v_cap_heat(power_plant, heat_regio)
         v_production(node, time, power_plant, heat_regio, product)    "production of all power plants in one region and to one node"
         v_production_energy(node, time, power_plant, heat_regio) "energy supply of a power plant in one region and to one node including electricity and heat"
         v_cap_onl(node, time, power_plant, heat_regio)  "capacities kept online for electricity production"
         v_cap_startup(node, node1, time, time1, power_plant, heat_regio) "capacities started up at the transition from a node the next one"
         v_transpo(node, time, zone, zzone) "power transport from zone to zzone"
         v_transpo_h2(node, time, zone, zzone) "h2 transport from zone to zzone"
         v_pump(node, time, power_plant, heat_regio) "used pumping capacity for the electricity storage"
         v_pump_standing_neg(node, time, power_plant, bregio) "charging/pumping capacity reserved for (negative) standing reserve"
         v_pump_standing_pos(node, time, power_plant, bregio) "charging/pumping capacity reserved for (positive) standing reserve"
         v_fill_level_mon(water_scen, month, power_plant, heat_regio) "monthly fill level of the annual storages"
         v_fill_level_h(node, time, power_plant, heat_regio) "hourly fill level of IGELECSTORAGE storages (daily storages like pumpstorage or e-mobility)"
         v_fill_level_heat(node, time, heat_regio)
         v_fuelusage(node,time,power_plant,heat_regio) "fuelusage when producing energy"
         v_spill_ror(node, time, power_plant,heat_regio) "penalty for spill for RES"
         v_spill_ror2(node, time, power_plant,heat_regio) "penalty for spill for RES"
         v_demand_max(bregio,product) "highest electricity demand in each region (fixed and flexible demand)"
         v_curtailment(node, time, power_plant, heat_regio)      "curtailment of fluctuating renewable energy sources"
$ifi '%h2_yearly%' == Yes        v_import_h2(zone)   "import of hydrogen"
$ifi NOT '%h2_yearly%' == Yes        v_import_h2(node, time, zone)   "import of hydrogen"
;


*---------------------------- For SRE (MD) --------------------------------------------
scalar
*Configure a specific effect strength (e.g. 7.7% SRE, 17.2% SRE or 33% SRE)
*The value 0 can be used for the reference scenario without any rebound effect

*SRE_effect_strength /0/
*SRE_effect_strength /0.077/
*SRE_effect_strength /0.172/
*SRE_effect_strength /0.33/

*Sets the temporal distribution of the SRE:
*share_simSRE = 0 assigns the entire effect to hours with PV generation (simultaneous profile)
*share_sweSRE = 1 means no additional demand is allocated to PV-free (off-peak) hours
share_simSRE /0/
share_sweSRE /1/
;

Parameters
share_privatePV(zone) "percentage of PV installed on private households"
out_demand_y_inclSRE(simyear, zone, product) "stores the total annual electricity demand, including additional consumption due to the SRE"
out_demand_y_SRE(simyear,zone,product) "captures only the additional annual electricity demand directly attributable to the SRE"
;

Free Variables
*Also declared as a formula below to ensure the model can reference its values dynamically based on input data and use them consistently when distributing sweeping SRE demand across time steps
pvAVG(heat_regio,node,time) "provides the normalized/avareged PV generation profile used to distribute sweeping SRE demand over the day"
;
*---------------------------- For SRE (MD) --------------------------------------------

*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ EQUATIONS @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
equations
*-------------------------------- Objective function and cost terms -------------------------------------------
         eq_total_cost           "objective function - describes the total cost over the modelling period - to be minimized"
         eq_var_cost_opr         "variable operation costs"
         eq_var_cost_startup     "variable startup costs"
         eq_var_cost_trans       "variable power transmission costs"
         eq_var_cost_trans_h2    "variable h2 transmission costs"
         eq_var_cost_co2         "variable costs of CO2-emissions"
         eq_fix_cost_irr         "irreversible fixed costs incurred in the first year"
         eq_fix_cost_sunk        "irreversible fixed costs attributed to the remained lifetime except the first year"
         eq_fix_cost_rev         "reversible fixed costs dependent on the installed capacity"       
*-----------------------------------------------------------------------------------------------
*------------------------------------ Restrictions ---------------------------------------------
         eq_supply(node, time, month, power_plant, heat_regio) "power supply based on monthly availability"
         eq_supply_heat(node, time, month, power_plant, heat_regio)
         eq_supply_backpressure(node, time, power_plant, heat_regio) "Power supply constraints for IGBACKPR CHPs"
         eq_demand_heatpump(node, time, power_plant, heat_regio) "Power demand constraint for heatpumps (IGHEATPUMP)"
         eq_demand_pth2(node, time, power_plant, heat_regio) "Power-demand constraint for hydrogen"
         eq_demand_ptm(node, time, power_plant, heat_regio) "Power-demand constraint for methane"
         eq_supply_extraction_2(node, time, power_plant, heat_regio)   "Powr supplyconstraints for IGEXTRACTION CHPs"
         eq_supply_energy_total(node, time, power_plant, heat_regio) "total energy supplied by a CHP, converted to the equivalent electricity supply"
         eq_supply_wind_onshore(node, time, month, power_plant, heat_regio) "onshore wind power supply based on the natural wind availability and capacity availability"
         eq_supply_wind_offshore(node, time, month, power_plant, heat_regio) "offshore wind power supply based on the natural wind availability and capacity availability"
         eq_supply_PV(node, time, month, power_plant, heat_regio) "SUN power supply based on the natural radiation availability and capacity availability"
         eq_cap(power_plant, heat_regio) "capacity restriction"
         eq_cap_max(primary_energy, zone) "maximum exogenous capacity per fuel and zone"
         eq_cap_max_wind(plant_type, zone)
         eq_demand_el(node, time, zone) "demand balance for power"
         eq_demand_heat(node, time, heat_regio) "demand balance for heat"
$ifi '%h2_yearly%' == Yes         eq_demand_h2(zone) "demand balance for hydrogen"
$ifi NOT '%h2_yearly%' == Yes     eq_demand_h2(node, time, zone) "demand balance for hydrogen"
         eq_transpo_CF(node, time, zone, zzone) "restriction for transmission capacities"
         eq_transpo_CF_h2(node, time, zone, zzone) "restriction for h2 transmission capacities"
         eq_MaxChargePower(node, time, month, power_plant, heat_regio) "capacity restriction for pumping energy"
         eq_MaxChargePower_Sim(node, time,month) "max simultaneous capacity restriction for charging of EV"
         eq_MaxChargePower_ptg(node, time,month,power_plant, heat_regio) "capacity restriction for pumping of electrolysers"
         eq_pump_standing_pos(node,time,power_plant, heat_regio) "pumped power could either be used for standing or spinning pos reserve --> this equations ensures separation"
         eq_supply_river(node, time, power_plant, heat_regio) "capacity restriction for HYDR_ROR plants"
         eq_resvr_annual(water_scen, month, month1, power_plant, heat_regio) "formation of reservoir level for annual storages"
         eq_resvr_daily(node, node1, time, time1, power_plant, heat_regio) "formation of reservoir level for IGELECSTORAGE (daily storages like pumpstorage or emob)"
         eq_resvrmax_annual(water_scen, month, power_plant, heat_regio) "maximum reservoir level of annual storages"
         eq_resvrmin_annual(water_scen, month, power_plant, heat_regio) "minimum reservoir level of annual storages"
         eq_MaxVolume(node, time, power_plant, heat_regio) "upper bound for loading (pumping) energy into storage through (available) storage volume (IGELECSTORAGE)"
         eq_prod_plant_ub(node, time, power_plant, heat_regio) "upper bound for the production of power plants except chp IGEXTRACTION plants"
         eq_prod_plant_ub2(node, time, power_plant, heat_regio) "upper bound for the production of chp IGEXTRACTION plants"
         eq_prod_plant_ub3(node, time, power_plant, heat_regio) "upper bound for the production of heatboilers"
         eq_prod_plant_ub4(node, time, power_plant, heat_regio) "bound for electricity production of heatboilers"
         eq_prod_plant_ub5(node, time, power_plant, heat_regio) "bound for electricity production of PTG"
         eq_BanVehicle2Grid(node, time, power_plant, heat_regio) "if used than v_production (discharging to grid) from E-mob is denied"
         eq_MaxDischargePower(node, time, month, power_plant, heat_regio) "*bound for electricity production from daily storages (IGELECSTORAGE, especially E-mobility)"
         eq_prod_plant_lb(node, time, power_plant, heat_regio) "lower bound for the production of power plants except chp IGEXTRACTION plants"
         eq_prod_plant_ub_VRE(node, time, power_plant, heat_regio) "constraint for wind and pv power production"
         eq_cap_startup(node, node1, time, time1, power_plant, heat_regio) "calculation of startup capacity"
         eq_reserve_cap_spinningPos(node, time, month, zone)  "incremental spinning reserve capacity (primary and secondary)"
         eq_reserve_cap_spinningNeg(node, time, month, zone)  "decremental spinning reserve capacity (primary and secondary)"
         eq_pump_onlyPump(node,time,power_plant, heat_regio) "ensure only techs which could charge/pump do so"
         eq_pump_standing_pos_onlyPump(node,time,power_plant, heat_regio) "this reserve type is only for techs which could charge/pump"
         eq_pump_standing_neg_onlyPump(node,time,power_plant, heat_regio) "this reserve type is only for techs which could charge/pump"
         eq_reserve_cap(country)
         eq_reserve_cap_heat(heat_regio)
         eq_reserve_cap_standingPos(node, time, month, country) "incremental standing reserve capacity (tertiary)"
         eq_reserve_cap_standingNeg(node, time, month, country) "incremental standing reserve capacity (tertiary)"
         eq_prod_nucl(node, time, country)
         eq_prod_wind_off(node, time, country)
         eq_co2_bound "for overall model region (e.g. Europe)"
         eq_co2_bound2 "for country specific co2 bound (e.g. Germany)"
         eq_cap_nucl(node, node1, time, time1, month, power_plant, heat_regio) "Zwingt Nuclear und Lignite innerhalb eines Monats zu konster Production"
         eq_cap_coal(node, time, time1, power_plant, heat_regio)
         eq_max_demand_el(zone,time,node) "equation determining the max electricity demand of each zone"            
         eq_MaxVolumeBATT(node, time, power_plant, heat_regio) "upper bound for loading (pumping) energy into storage through (available) storage volume (BATT_STO)"
         eq_cur_cost     "total cost of curtailment"
         eq_cost_import_h2       "total cost of h2 import"
         eq_min_gen(power_plant, heat_regio)
* H2 storage equations (not yet finished)
         eq_resvr_daily_h2(node, node1, time, time1, power_plant, heat_regio)
         eq_MaxVolumeH2(node, time, power_plant, heat_regio)
         eq_MaxChargeH2(node, time, month, power_plant, heat_regio)
         eq_MaxDischargeH2(node, time, month, power_plant, heat_regio)
         eq_pump_onlyPumpH2(node,time,power_plant, heat_regio)
         eq_import_constraint(zone) "restriction for third country imports"
         eq_max_import

*---------------------------- For SRE (MD) --------------------------------------------
eq_pv_avg(heat_regio,node,time) "Defines the normalized PV profile used to allocate sweeping SRE demand over time steps"
;
*---------------------------- For SRE (MD) --------------------------------------------

*------------------------------------- Objective function --------------------------------------
eq_total_cost ..
         total_cost =e= var_cost_opr + var_cost_startup + var_fix_cost_irr + v_fix_cost_sunk + var_fix_cost_rev  + var_cost_trans + var_cost_trans_h2 + v_cur_cost + v_h2_cost
;

eq_var_cost_opr..
         var_cost_opr =e= sum((node,time)$node_time(node, time), (prob_node(node)*hour_resolution(time)*freq_time(time)*
                                 (
* Differentiation between operating costs of power plants without CHP extraction-condensing

                                        sum(exist_plant(power_plant, heat_regio)$((not power_plant_type(power_plant,'IGEXTRACTION'))
                                         and (not power_plant_type(power_plant,'IGHEATBOILER')) and (min_load_fct(power_plant,heat_regio)<1)
                                         and (not power_plant_type(power_plant,'IGHEATPUMP'))),
                                                 cost_opr(time, exist_plant)* (
                                                                   (v_production(node, time, exist_plant,'electricity')-v_cap_onl(node, time, exist_plant)) * min_load_fct(power_plant,heat_regio)/(1-min_load_fct(power_plant,heat_regio))
                                                                   +
                                                                   v_production(node, time, exist_plant,'electricity')
                                                                   )
                                                 +
                                                 cost_opr_min(time, exist_plant)*(v_cap_onl(node, time, exist_plant)-v_production(node, time, exist_plant,'electricity'))*min_load_fct(power_plant,heat_regio)/(1-min_load_fct(power_plant,heat_regio))

                                         )
                                         +
                                         sum(exist_plant(power_plant, heat_regio)$((not power_plant_type(power_plant,'IGEXTRACTION'))
                                          and (not power_plant_type(power_plant,'IGHEATBOILER')) and (min_load_fct(power_plant,heat_regio)=1)
                                         and (not power_plant_type(power_plant,'IGHEATPUMP'))),
                                                 cost_opr(time, exist_plant) * v_production(node, time, exist_plant,'electricity')
                                         )
                                         +

* and with CHP extraction-condensing plants
                                        sum(exist_plant(power_plant, heat_regio)$(power_plant_type(power_plant,'IGEXTRACTION') and (min_load_fct(power_plant,heat_regio)<1)),
                                                 cost_opr(time, exist_plant)* (

                                                                   (v_production_energy(node, time, exist_plant)-v_cap_onl(node, time, exist_plant))*min_load_fct(power_plant,heat_regio)/(1-min_load_fct(power_plant,heat_regio))
                                                                   +

                                                                   v_production_energy(node, time, exist_plant)
                                                                   )
                                                 +

                                                 cost_opr_min(time, exist_plant)*(v_cap_onl(node, time, exist_plant)-v_production_energy(node, time, exist_plant))*min_load_fct(power_plant,heat_regio)/(1-min_load_fct(power_plant,heat_regio))

                                         )
                                         +
                                         sum(exist_plant(power_plant, heat_regio)$(power_plant_type(power_plant,'IGEXTRACTION') and (min_load_fct(power_plant,heat_regio)=1)),
                                                 cost_opr(time, exist_plant) * v_production_energy(node, time, exist_plant)
                                         )
* and heat boilers
                                         +
                                         sum(exist_plant(power_plant, heat_regio)$(power_plant_type(power_plant,'IGHEATBOILER') and not power_plant_type(power_plant,'IGHEATPUMP')),
                                                 cost_opr(time, exist_plant) * v_production(node, time, exist_plant,'heat')
                                         )
                                         )
                                 )
* end of sum part one which is multiplied with (prob_node(node)*hour_resolution(time)*freq_time(time)
                                 +
*penalty terms for spill for RES ----
                                 sum(exist_plant,v_spill_ror(node, time, exist_plant)) * 100000
                                 +
                                 sum(exist_plant(power_plant, heat_regio),v_spill_ror2(node, time, exist_plant)) * 100000
                         )
;
*end of var_cost_opr

eq_var_cost_startup..
         var_cost_startup =e= sum((node,node1,time,time1,exist_plant(power_plant, heat_regio))$(node_succ(node, node1, time, time1)$ (not power_plant_type(power_plant, 'WIND'))$(cost_startup(time, exist_plant)>0)),
                                  prob_node(node)*prob_node_trans(node,node1)*v_cap_startup(node, node1, time, time1, exist_plant)*cost_startup(time, exist_plant)*hour_resolution(time)*freq_time(time)
                              )
;

eq_var_cost_trans..
         var_cost_trans =e=
                            sum((node,time,exist_line_CF(zone, zzone))$node_time(node, time),
                                 prob_node(node)*v_transpo(node, time, zone, zzone)*cost_trans(zone,zzone)*hour_resolution(time)*freq_time(time)
                            )
;

eq_var_cost_trans_h2..
         var_cost_trans_h2 =e=
                            sum((node,time,exist_line_CF_h2(zone, zzone))$node_time(node, time),
                                 prob_node(node)*v_transpo_h2(node, time, zone, zzone)*cost_trans_h2(zone,zzone)*hour_resolution(time)*freq_time(time)
                            )
;

*Prod el / efficiency (utilisation) * fuel specific emission factor
eq_var_cost_co2..
         var_cost_co2 =e= sum((node,time)$node_time(node, time), prob_node(node)*hour_resolution(time)*freq_time(time)*
                                 (
* Differentiation between operating costs of power plants without CHP extraction-condensing
                                        sum(exist_plant(power_plant, heat_regio)$((not power_plant_type(power_plant,'IGEXTRACTION'))
                                         and (not power_plant_type(power_plant,'IGHEATBOILER')) and (min_load_fct(power_plant,heat_regio)<1)
                                         and (not power_plant_type(power_plant,'IGHEATPUMP'))),
                                                 cost_CO2(time, exist_plant)* (

                                                                   (v_production(node, time, exist_plant,'electricity')-v_cap_onl(node, time, exist_plant))*min_load_fct(power_plant,heat_regio)/(1-min_load_fct(power_plant,heat_regio))
                                                                   +

                                                                   v_production(node, time, exist_plant,'electricity')
                                                                   )
                                                 +

                                                 cost_CO2_min(time, exist_plant)*(v_cap_onl(node, time, exist_plant)-v_production(node, time, exist_plant,'electricity'))*min_load_fct(power_plant,heat_regio)/(1-min_load_fct(power_plant,heat_regio))

                                         )
                                         +
                                         sum(exist_plant(power_plant, heat_regio)$((not power_plant_type(power_plant,'IGEXTRACTION'))
                                          and (not power_plant_type(power_plant,'IGHEATBOILER')) and (min_load_fct(power_plant,heat_regio)=1)
                                         and (not power_plant_type(power_plant,'IGHEATPUMP'))),
                                                 cost_CO2(time, exist_plant) * v_production(node, time, exist_plant,'electricity')
                                         )
                                         +
* and with CHP extraction-condensing plants
                                        sum(exist_plant(power_plant, heat_regio)$(power_plant_type(power_plant,'IGEXTRACTION') and (min_load_fct(power_plant,heat_regio)<1)),
                                                 cost_CO2(time, exist_plant)* (

                                                                   (v_production_energy(node, time, exist_plant)-v_cap_onl(node, time, exist_plant))*min_load_fct(power_plant,heat_regio)/(1-min_load_fct(power_plant,heat_regio))
                                                                   +

                                                                   v_production_energy(node, time, exist_plant)
                                                                   )
                                                 +

                                                 cost_CO2_min(time, exist_plant)*(v_cap_onl(node, time, exist_plant)-v_production_energy(node, time, exist_plant))*min_load_fct(power_plant,heat_regio)/(1-min_load_fct(power_plant,heat_regio))

                                         )
                                         +
                                         sum(exist_plant(power_plant, heat_regio)$(power_plant_type(power_plant,'IGEXTRACTION') and (min_load_fct(power_plant,heat_regio)=1)),
                                                 cost_CO2(time, exist_plant) * v_production_energy(node, time, exist_plant)
                                         )
                                         +
* and heat boilers
                                         sum(exist_plant(power_plant, heat_regio)$(power_plant_type(power_plant,'IGHEATBOILER') and (not power_plant_type(power_plant,'IGHEATPUMP'))),
                                                 cost_CO2(time, exist_plant) * v_production(node, time, exist_plant,'heat')
                                         )
                                 )
                          )
;
*Note: inv_plant_regio has been described in the loop via b_inv_plant_regio and is (or can be) different depending on simyear.
*In contrast, inv_plant_regio2 is constant (for each power plant and heat region) independently of simyear.
eq_fix_cost_irr..
         var_fix_cost_irr =e= sum((inv_plant_regio(inv_plant,heat_regio)), annuity(inv_plant)*cost_inv(inv_plant)*1000*v_cap_new(inv_plant_regio))
;

eq_fix_cost_sunk..
         v_fix_cost_sunk =e= sum((inv_plant_regio2(inv_plant,heat_regio)), annuity(inv_plant)*cost_inv(inv_plant)*1000*cap_n_sunk(inv_plant_regio2))
                         + sum((exist_plant(power_plant,heat_regio)), annuity(power_plant)*cost_inv(power_plant)*1000*cap_ref(exist_plant))
;

eq_fix_cost_rev..
         var_fix_cost_rev =e= sum(exist_plant(power_plant,heat_regio), cost_fix(power_plant)*1000*v_cap(exist_plant))
;

eq_cur_cost..   v_cur_cost =e= sum((node,time)$node_time(node, time),
                                    (prob_node(node)*hour_resolution(time)*freq_time(time)
                                    * sum(exist_plant(power_plant,heat_regio),
                                        v_curtailment(node, time, exist_plant) * 50)));

$ifi '%h2_yearly%' == Yes       eq_cost_import_h2..  v_h2_cost =e= sum(zone,
$ifi '%h2_yearly%' == Yes                               v_import_h2(zone) * h2_costs_import);

$ifi NOT '%h2_yearly%' == Yes   eq_cost_import_h2..     v_h2_cost =e= sum((node,time)$node_time(node, time),
$ifi NOT '%h2_yearly%' == Yes                                    (prob_node(node) * hour_resolution(time) * freq_time(time) * 
$ifi NOT '%h2_yearly%' == Yes                                       sum(zone, v_import_h2(node, time, zone) * h2_costs_import)));

*-----------------------------------------------------------------------------------------------

*--------------------------------   Restrictions -----------------------------------------------
*Power supply must be subject to the plant capacities as well as its availability, wind power production will be described seperately
eq_supply(node, time, month, exist_plant(power_plant, heat_regio))$
*excluded Combi-Tech
                 (node_time(node,time) and month_time(month,time) and not power_plant_type(power_plant, 'WIND') and not power_plant_type(power_plant, 'SUN'))..
         v_cap_onl(node, time, exist_plant) =l= v_cap(exist_plant) * availability(power_plant, month)
;

*Wind power supply is furthermore restricted by the natural wind availability and the wind power is always preferred according to the feed-in principle
eq_supply_wind_onshore(node, time, month, exist_plant(power_plant, heat_regio))$
                 (node_time(node,time) and month_time(month, time) and (power_plant_type(power_plant, 'WIND_ON')) and not power_plant_type(power_plant, 'crc_wind_ons'))..
         v_cap_onl(node, time, exist_plant) =e= wind_onshore(heat_regio,node,time) * v_cap(exist_plant) * availability(power_plant, month) - v_curtailment(node, time, exist_plant)
;
eq_supply_wind_offshore(node, time, month, exist_plant(power_plant, heat_regio))$
                 (node_time(node, time) and month_time(month, time) and (power_plant_type(power_plant, 'WIND_OFF')) and not power_plant_type(power_plant, 'crc_wind_offs'))..
         v_cap_onl(node, time, exist_plant) =e= wind_offshore(heat_regio,node,time) * v_cap(exist_plant) * availability(power_plant, month) - v_curtailment(node, time, exist_plant)
;
eq_supply_PV(node, time, month, exist_plant(power_plant, heat_regio))$
                 (node_time(node, time) and month_time(month, time) and (power_plant_type(power_plant, 'SUN')) and not power_plant_type(power_plant, 'crc_solar'))..
         v_cap_onl(node, time, exist_plant) =e= PV(heat_regio,node,time) * v_cap(exist_plant) * availability(power_plant, month) - v_curtailment(node, time, exist_plant)
;

eq_supply_heat(node, time, month, exist_plant(power_plant, heat_regio))$(node_time(node,time) and month_time(month,time) and power_plant_type(power_plant, 'heat'))..
         v_production(node, time, exist_plant, 'heat') =l= v_cap_heat(exist_plant) * availability(power_plant, month)
;
eq_supply_backpressure(node, time, exist_plant(power_plant, heat_regio))$(node_time(node, time) and power_plant_type(power_plant, 'IGBACKPR'))..
         v_production(node, time, exist_plant, 'electricity') =e= v_production(node, time, exist_plant, 'heat') * fct_PQ_BP(power_plant)
;

*since demand is modelled in MWh_el it is sufficient to use -1. However, v_production is positve variable --> make it equal and use - 1 on other points
eq_demand_heatpump(node, time, exist_plant(power_plant, heat_regio))$(node_time(node, time) and power_plant_type(power_plant, 'IGHEATPUMP'))..
         v_production(node, time, exist_plant, 'electricity') =e= v_production(node, time, exist_plant, 'heat') / eff_plant(power_plant,heat_regio)
;

*pth2-production restriction
eq_demand_pth2(node, time, exist_plant(power_plant, heat_regio))$(node_time(node, time) and (power_plant_type(power_plant, 'PTH2')))..
         v_production(node, time, exist_plant, 'h2') =e= v_pump(node, time, exist_plant) * pump_eff(exist_plant)
;

*ptm-production restriction 
eq_demand_ptm(node, time, exist_plant(power_plant, heat_regio))$(node_time(node, time) and power_plant_type(power_plant, 'PTM'))..
         v_production(node, time, exist_plant, 'methane') =e= v_pump(node, time, exist_plant) * pump_eff(exist_plant)
;
*End new implementation

eq_supply_extraction_2(node, time, exist_plant(power_plant, heat_regio))$(node_time(node, time) and power_plant_type(power_plant, 'IGEXTRACTION'))..
         v_production(node, time, exist_plant, 'electricity') =g= v_production(node, time, exist_plant, 'heat') * fct_PQ_BP(power_plant)
;

*Total energy supply of a power plant includin electricity and heat
eq_supply_energy_total(node, time, exist_plant(power_plant, heat_regio))$(node_time(node,time) and power_plant_type(power_plant, 'IGEXTRACTION'))..
         v_production_energy(node, time, exist_plant) =e= v_production(node, time, exist_plant, 'electricity') +  v_production(node, time, exist_plant, 'heat') * fct_PQ_Extr(power_plant)
;

*Power plant capacity less or equal the installed capacity in the reference year plus invested capacity during the simulated periods
eq_cap(exist_plant(power_plant, heat_regio))..
         v_cap(exist_plant) =e= cap_ref(exist_plant) + v_cap_new(exist_plant)$inv_plant_regio(power_plant,heat_regio) + cap_n_sunk(exist_plant)$inv_plant_regio2(power_plant,heat_regio);
;

*equation for exogenous maximum capacity restriction per primary energy and zone
eq_cap_max(primary_energy, zone)..
         sum(exist_plant(power_plant, heat_regio)$(heatregio_in_zone(heat_regio,zone) AND fuel(power_plant, primary_energy)), v_cap(exist_plant)) =l= max_cap(primary_energy, zone);
;

*equation for exogenous maximum capacity restriction per wind technology
eq_cap_max_wind(plant_type_wind(plant_type), zone)..
         sum(exist_plant(power_plant, heat_regio)$(heatregio_in_zone(heat_regio,zone) AND (power_plant_type(power_plant, plant_type_wind))),
            v_cap(exist_plant)) =l= max_cap_wind(plant_type_wind, zone)
;

*Power and heat production must meet the demand at any time under consideration of the pumping energy and power exchange among the considered regions
eq_demand_el(node,time, zone)$(node_time(node, time))..
         demand(time, zone,'electricity')
                 + demand_emob_fix(time, zone, 'electricity')
        +sum(exist_line_CF(zone, zzone), v_transpo(node, time, exist_line_CF))
        +sum(exist_plant(power_plant, heat_regio)$(heatregio_in_zone(heat_regio,zone) and power_plant_type(power_plant, 'IGELECSTORAGE')) ,
                 v_pump(node, time, exist_plant))
        +sum((heat_regio,exist_plant(power_plant, heat_regio)) $(heatregio_in_zone(heat_regio,zone) and power_plant_type(power_plant,'IGHEATPUMP')),
                 v_production(node, time, exist_plant, 'electricity'))
        +sum((heat_regio,exist_plant(power_plant, heat_regio)) $(heatregio_in_zone(heat_regio,zone) and power_plant_type(power_plant,'IGPTG')),
                 v_pump(node, time, exist_plant))

*---------------------------- For SRE (MD) --------------------------------------------    
*Simultaneous SRE
*Adds additional demand in alignment with PV generation, concentrating load around midday.            
        + sum((heat_regio, exist_plant(power_plant, heat_regio))$(heatregio_in_zone(heat_regio, zone) AND power_plant_type(power_plant, 'SUN')),
        (cap_n_sunk(exist_plant) + cap_ref(exist_plant))
        * PV(heat_regio, node, time)
        * SRE_effect_strength *  share_privatePV(zone) * share_simSRE) 
        
*Sweeping SRE
*Spreads additional demand evenly across the day based on an averaged PV profile.   
        + sum((heat_regio, exist_plant(power_plant, heat_regio))$(heatregio_in_zone(heat_regio, zone) AND power_plant_type(power_plant, 'SUN')),
        (cap_n_sunk(exist_plant) + cap_ref(exist_plant))
        * pvAVG(heat_regio,node,time) 
*       * sum((node1,time1)$node_time(node1, time1), prob_node(node1) * hour_resolution(time1) * freq_time(time1) * PV(heat_regio, node1, time1)) / sum((node1,time1)$node_time(node1, time1), prob_node(node1) * hour_resolution(time1) * freq_time(time1)) 
        * SRE_effect_strength *  share_privatePV(zone) * share_sweSRE)
*---------------------------- For SRE (MD) --------------------------------------------
        
       =e=
    
         sum((heat_regio,exist_plant(power_plant, heat_regio))$(heatregio_in_zone(heat_regio,zone)
                                                         and (not power_plant_type(power_plant,'IGHEATBOILER')) and (not power_plant_type(power_plant,'IGHEATPUMP'))
                                                         and (not power_plant_type(power_plant,'IGPTG'))),
                 v_production(node, time, exist_plant, 'electricity'))

        + sum(exist_line_CF(zzone, zone), v_transpo(node, time, exist_line_CF))

;

*---------------------------- For SRE (MD) -------------------------------------------- 
*Defines the normalized PV profile (pvAVG) used for sweeping SRE by averaging PV output.
eq_pv_avg(heat_regio,node,time)$(node_time(node, time)).. pvAVG(heat_regio,node,time) =e= sum((node1,time1)$node_time(node1, time1), prob_node(node1) * hour_resolution(time1) * freq_time(time1) * PV(heat_regio, node1, time1)) / sum((node1,time1)$node_time(node1, time1), prob_node(node1) * hour_resolution(time1) * freq_time(time1))
;
*---------------------------- For SRE (MD) --------------------------------------------

*Note: heat pumps have their own heat_regio (in the data), so that the demand is separate and can only be covered by hp.
eq_demand_heat(node,time, heat_regio)$node_time(node, time)..
     demand(time, heat_regio, 'heat')
     =e= sum(exist_plant(power_plant, heat_regio)$
                 (power_plant_type(power_plant, 'chp') or power_plant_type(power_plant, 'IGHEATBOILER')or power_plant_type(power_plant, 'IGHEATPUMP')),
                 v_production(node, time, exist_plant, 'heat'))
;

*H2 demand on a yearly basis
$ifi '%h2_yearly%' == Yes       eq_demand_h2(zone)..
$ifi '%h2_yearly%' == Yes            sum(time, demand(time, zone, 'h2') * hour_resolution(time) * freq_time(time))
$ifi '%h2_yearly%' == Yes            +
$ifi '%h2_yearly%' == Yes            sum((node,time)$node_time(node, time), prob_node(node) * hour_resolution(time) * freq_time(time) *
$ifi '%h2_yearly%' == Yes               sum(exist_plant(power_plant, heat_regio)$(heatregio_in_zone(heat_regio, zone) AND fuel(power_plant, 'HYDROGEN')),
$ifi '%h2_yearly%' == Yes                   v_production(node, time, exist_plant, 'electricity') / eff_plant(power_plant, heat_regio)))
$ifi '%h2_yearly%' == Yes               +
$ifi '%h2_yearly%' == Yes            sum((node,time)$node_time(node, time), prob_node(node) * hour_resolution(time) * freq_time(time) *
$ifi '%h2_yearly%' == Yes               sum(exist_plant(power_plant, heat_regio)$(heatregio_in_zone(heat_regio, zone) AND power_plant_type(power_plant, 'IGHEATBOILER') AND fuel(power_plant, 'HYDROGEN')),
$ifi '%h2_yearly%' == Yes                   v_production(node, time, exist_plant, 'heat') / eff_plant(power_plant, heat_regio)))
*H2 demand of H2 storages
*$ifi '%h2_yearly%' == Yes          + sum((node,time)$node_time(node, time), prob_node(node) * hour_resolution(time) * freq_time(time) *
*$ifi '%h2_yearly%' == Yes            sum(exist_plant(power_plant, heat_regio)$(heatregio_in_zone(heat_regio, zone) AND power_plant_type(power_plant,'H2_STO')), v_pump_h2(node, time, exist_plant)))
$ifi '%h2_yearly%' == Yes            + sum((node,time)$node_time(node, time), prob_node(node) * hour_resolution(time) * freq_time(time) * sum(exist_line_CF_h2(zone, zzone), v_transpo_h2(node, time, exist_line_CF_h2)))   
$ifi '%h2_yearly%' == Yes            =e=
*added combi-tech     
$ifi '%h2_yearly%' == Yes            sum((node,time)$node_time(node, time), prob_node(node) * hour_resolution(time) * freq_time(time) *
$ifi '%h2_yearly%' == Yes               sum(exist_plant(power_plant, heat_regio)$(heatregio_in_zone(heat_regio, zone) AND (power_plant_type(power_plant, 'PTH2'))),  
$ifi '%h2_yearly%' == Yes                   v_production(node, time, exist_plant, 'h2')))
*H2 demand of H2 storages
*$ifi '%h2_yearly%' == Yes         + sum((node,time)$node_time(node, time), prob_node(node) * hour_resolution(time) * freq_time(time) *
*$ifi '%h2_yearly%' == Yes            sum(exist_plant(power_plant, heat_regio)$(heatregio_in_zone(heat_regio, zone) AND power_plant_type(power_plant,'H2_STO')), v_production(node, time, exist_plant, 'h2')))
$ifi '%h2_yearly%' == Yes              + sum((node,time)$node_time(node, time), prob_node(node) * hour_resolution(time) * freq_time(time) * sum(exist_line_CF_h2(zzone, zone), v_transpo_h2(node, time, exist_line_CF_h2)))
$ifi '%h2_yearly%' == Yes                        + v_import_h2(zone)$h2_import_zones(zone)
$ifi '%h2_yearly%' == Yes       ;

*third country restriction
$ifi '%h2_yearly%' == Yes eq_import_constraint(zone)..
$ifi '%h2_yearly%' == Yes        v_import_h2(zone) =L= 0.5 * (sum(time, demand(time, zone, 'h2') * hour_resolution(time) * freq_time(time))
$ifi '%h2_yearly%' == Yes                             + sum((node,time)$node_time(node, time), prob_node(node) * hour_resolution(time) * freq_time(time) *
$ifi '%h2_yearly%' == Yes               sum(exist_plant(power_plant, heat_regio)$(heatregio_in_zone(heat_regio, zone) AND fuel(power_plant, 'HYDROGEN')),
$ifi '%h2_yearly%' == Yes                   v_production(node, time, exist_plant, 'electricity') / eff_plant(power_plant, heat_regio))))
$ifi '%h2_yearly%' == Yes                    ;

$ifi '%h2_yearly%' == Yes eq_max_import..
$ifi '%h2_yearly%' == Yes   sum(zone$h2_import_zones(zone), v_import_h2(zone)) =G= max_cap_imports;

*H2 demand on a time segment basis
$ifi NOT '%h2_yearly%' == Yes       eq_demand_h2(node,time, zone)$(node_time(node, time))..
$ifi NOT '%h2_yearly%' == Yes        demand(time, zone, 'h2') + sum(exist_plant(power_plant, heat_regio)$(heatregio_in_zone(heat_regio, zone) AND fuel(power_plant, 'HYDROGEN')),
$ifi NOT '%h2_yearly%' == Yes               v_production(node, time, exist_plant, 'electricity') / eff_plant(power_plant, heat_regio))
$ifi NOT '%h2_yearly%' == Yes        + sum(exist_plant(power_plant, heat_regio)$(heatregio_in_zone(heat_regio, zone) AND power_plant_type(power_plant, 'IGHEATBOILER') AND fuel(power_plant, 'HYDROGEN')),
$ifi NOT '%h2_yearly%' == Yes               v_production(node, time, exist_plant, 'heat') / eff_plant(power_plant, heat_regio))
*H2 demand of H2 storages
*$ifi NOT '%h2_yearly%' == Yes       + sum(exist_plant(power_plant, heat_regio)$(heatregio_in_zone(heat_regio, zone) AND power_plant_type(power_plant,'H2_STO')), v_pump_h2(node, time, exist_plant))
$ifi NOT '%h2_yearly%' == Yes         + sum(exist_line_CF_h2(zone, zzone), v_transpo_h2(node, time, exist_line_CF_h2))
$ifi NOT '%h2_yearly%' == Yes        =e=
*added combi-tech     
$ifi NOT '%h2_yearly%' == Yes           sum(exist_plant(power_plant, heat_regio)$(heatregio_in_zone(heat_regio, zone) AND (power_plant_type(power_plant, 'PTH2'))),
$ifi NOT '%h2_yearly%' == Yes                   v_production(node, time, exist_plant, 'h2'))
*H2 demand of H2 storages
*$ifi NOT '%h2_yearly%' == Yes     + sum(exist_plant(power_plant, heat_regio)$(heatregio_in_zone(heat_regio, zone) AND power_plant_type(power_plant,'H2_STO')), v_production(node, time, exist_plant, 'h2'))
$ifi NOT '%h2_yearly%' == Yes          + sum(exist_line_CF_h2(zzone, zone), v_transpo_h2(node, time, exist_line_CF_h2)) + v_import_h2(node, time, zone)$h2_import_zones(zone)
$ifi NOT '%h2_yearly%' == Yes   ;

*third country restriction
$ifi NOT '%h2_yearly%' == Yes eq_import_constraint(zone)..
$ifi NOT '%h2_yearly%' == Yes   sum((node,time)$node_time(node, time), prob_node(node) * hour_resolution(time) * freq_time(time) * v_import_h2(node, time, zone)) =L= 0.5 * (sum(time, demand(time, zone, 'h2') * hour_resolution(time) * freq_time(time)) +
$ifi NOT '%h2_yearly%' == Yes          sum((node,time)$node_time(node, time), prob_node(node) * hour_resolution(time) * freq_time(time) *
$ifi NOT '%h2_yearly%' == Yes               sum(exist_plant(power_plant, heat_regio)$(heatregio_in_zone(heat_regio, zone) AND fuel(power_plant, 'HYDROGEN')),
$ifi NOT '%h2_yearly%' == Yes                   v_production(node, time, exist_plant, 'electricity') / eff_plant(power_plant, heat_regio))))
$ifi NOT '%h2_yearly%' == Yes   ;

$ifi NOT '%h2_yearly%' == Yes eq_max_import..
$ifi NOT '%h2_yearly%' == Yes   sum((node,time,zone)$(node_time(node, time) AND h2_import_zones(zone)), prob_node(node) * hour_resolution(time) * freq_time(time) * v_import_h2(node, time, zone)) =L= max_cap_imports;

*power transmission may not exceed the capacity of existing transmission lines
eq_transpo_CF(node, time, zone,zzone) $(exist_line_CF(zone, zzone) $node_time(node, time))..
         v_transpo(node, time, zone, zzone) =l= sum(month$month_time(month,time),trans_cap_m(zone, zzone, month))
;

*h2 transmission may not exceed the capacity of existing transmission lines
eq_transpo_CF_h2(node, time, zone,zzone) $(exist_line_CF_h2(zone, zzone) $node_time(node, time))..
         v_transpo_h2(node, time, zone, zzone) =l= sum(month$month_time(month,time), trans_cap_m_h2(zone, zzone, month))
;

*production of HYDR_ROR plants may not exceed the maximmal possible water inflow
eq_supply_river(node, time, exist_plant(power_plant, heat_regio))$(node_time(node, time) and power_plant_type(power_plant, 'HYDR_ROR'))..
         v_production(node, time, exist_plant, 'electricity') =l= inflow_run_river(node, time, exist_plant)
;

*fill level of annual storages at the end of a month results from the fill level at the end of the
*month before plus water inflow in the hydro storages in the calculated month and minus the production by the hydro storages (+ and - some slackvars)
* --> be aware that this is the only HYDR_RES limitation regarding v_production
eq_resvr_annual(water_scen, month, month1, exist_plant(power_plant, heat_regio))$(month_succ(month1, month) and power_plant_type(power_plant, 'HYDR_RES'))..
        v_fill_level_mon(water_scen, month, exist_plant)
                 =e= v_fill_level_mon(water_scen, month1, exist_plant)
                   +     sum((node, time)$(node_time(node, time)$month_time(month,time)), prob_node(node) *  hour_resolution(time) * freq_time(time)*
                                 (- v_production(node, time, exist_plant, 'electricity') + inflow_annual_storage(node, time, exist_plant)
                                 - v_spill_ror(node, time, exist_plant) + v_spill_ror2(node, time, exist_plant))
                            )
;

*fill level of annaul storages may not exceed their maximum of possible reservoir level dependent on months
eq_resvrmax_annual(water_scen, month, exist_plant(power_plant, heat_regio))$power_plant_type(power_plant, 'HYDR_RES')..
         v_fill_level_mon(water_scen, month, exist_plant) =l= fl_ratio_max(heat_regio,month) * fill_level_max(exist_plant)
;

*minimum reservoir level of annual storages depending on months
eq_resvrmin_annual(water_scen, month, exist_plant(power_plant, heat_regio))$power_plant_type(power_plant, 'HYDR_RES')..
         v_fill_level_mon(water_scen, month, exist_plant) =g= fl_ratio_min(heat_regio,month)*fill_level_max(exist_plant)
;

*relation between the storage fill level (for HYDR_RS water reservoir level) in every two succeeding hours
*for e-mobility leaving and arriving cars of pool are assumed to leave and arrive with average storage level
*of last timestep and the demand of drives occure when arriving --> proxy --> demand could be more or less through
* leave and arrive term
eq_resvr_daily(node, node1, time,time1, exist_plant(power_plant, heat_regio))$(node_succ_4_storage(node1, node, time1, time)
                 and power_plant_type(power_plant, 'IGELECSTORAGE'))..
         v_fill_level_h(node, time, exist_plant)
                 =e= v_fill_level_h(node1, time1, exist_plant)
                     + (v_pump(node, time, exist_plant)*pump_eff(power_plant,heat_regio)
                     - v_production(node, time, exist_plant,'electricity')
                     + (iArrive(time, power_plant) - iLeave(time, power_plant)) * fill_level_max(exist_plant)
                     - idemand(time,power_plant) * demand_clusterEmob(exist_plant)
                 )*hour_resolution(time)
;

$ONTEXT
*H2 storage equation
 eq_resvr_daily_h2(node, node1, time,time1, exist_plant(power_plant, heat_regio))$(node_succ_4_storage(node1, node, time1, time)
                 and power_plant_type(power_plant, 'H2_STO'))..
         v_fill_level_h(node, time, exist_plant)
                 =e= v_fill_level_h(node1, time1, exist_plant)
                     + (v_pump_h2(node, time, exist_plant) * pump_eff(power_plant,heat_regio)
                     - v_production(node, time, exist_plant,'h2')
                 )*hour_resolution(time)
; 
$OFFTEXT

*maximum reservoir level of IGELECSTORAGE (daily) storages for each hour and node may not exceed the maximum of possible fill level
eq_MaxVolume(node, time, exist_plant(power_plant, heat_regio))$(node_time(node, time) and power_plant_type(power_plant, 'IGELECSTORAGE') and not power_plant_type(power_plant, 'BATT_STO'))..
          v_fill_level_h(node, time, exist_plant) =l= fill_level_max(exist_plant) * iLoadPoss(time, power_plant);
          
*fullload_discharge represents the ratio of storage capacity and power (duration of discharge at full load)
eq_MaxVolumeBATT(node, time, exist_plant(power_plant, heat_regio))$(node_time(node, time) and power_plant_type(power_plant, 'BATT_STO'))..
         v_fill_level_h(node, time, exist_plant) =l= v_cap(exist_plant) * fullload_discharge * iLoadPoss(time, power_plant);

$ONTEXT
*H2 storage max volume
*fullload_discharge represents the ratio of storage capacity and power (duration of discharge at full load)
eq_MaxVolumeH2(node, time, exist_plant(power_plant, heat_regio))$(node_time(node, time) and power_plant_type(power_plant, 'H2_STO'))..
         v_fill_level_h(node, time, exist_plant) =l= v_cap(exist_plant) * fullload_discharge_h2 * iLoadPoss(time, power_plant);
$OFFTEXT

*used pumping capacity and reserved pumping capacity (for standing reserve) may not exceed the maximal possible pumping capacity of storages in timestep (for HYDR_PS iLoadPoss == 1)
*use v_cap instead of v_cap_online here since v_cap_online is used in order to have a value between installed, avail capacity and v_production separating standing in spinning on the production side but not on the pumping side
eq_MaxChargePower(node, time,month, exist_plant(power_plant, heat_regio))$(node_time(node, time) and month_time(month, time) and power_plant_type(power_plant, 'IGELECSTORAGE'))..
         v_pump(node, time, exist_plant) + v_pump_standing_neg(node,time,exist_plant) =l= 
*                                                                                               pump_cap_fct(exist_plant,time)
                                                                                                v_cap(exist_plant) * availability(power_plant, month) * iLoadPoss(time, power_plant);

*restriction for simultaneous EV-charging (smart charging); currently hardcoded with 0.1
eq_MaxChargePower_Sim(node, time,month)$(node_time(node, time) and month_time(month, time))..

        sum(exist_plant(power_plant, heat_regio)$(power_plant_type(power_plant, 'IGELECSTORAGE')
	and not power_plant_type(power_plant, 'BATT_STO') and not power_plant_type(power_plant, 'HYDR_PS')),
	v_pump(node, time, exist_plant) + v_pump_standing_neg(node,time,exist_plant))

	=l= sum(exist_plant(power_plant, heat_regio)$(power_plant_type(power_plant, 'IGELECSTORAGE')
	and not power_plant_type(power_plant, 'BATT_STO') and not power_plant_type(power_plant, 'HYDR_PS')),
	v_cap(exist_plant)) * 0.1;

*MaxChargePower for IGPTG
eq_MaxChargePower_ptg(node, time, month, exist_plant(power_plant, heat_regio))$(node_time(node, time) and month_time(month, time) and power_plant_type(power_plant, 'IGPTG'))..
         v_pump(node, time, exist_plant) + v_pump_standing_neg(node,time,exist_plant) =l= v_cap(exist_plant) * availability(power_plant, month);

$ONTEXT
*H2 storage max charging
eq_MaxChargeH2(node, time,month, exist_plant(power_plant, heat_regio))$(node_time(node, time) and month_time(month, time) and power_plant_type(power_plant, 'H2_STO'))..
         v_pump_h2(node, time, exist_plant) =l= v_cap(exist_plant) * availability(power_plant, month);

*H2 storage max discharging
eq_MaxDischargeH2(node, time,month, exist_plant(power_plant, heat_regio))$(node_time(node,time) and month_time(month,time) and power_plant_type(power_plant, 'H2_STO'))..
         v_cap_onl(node, time, exist_plant) =l= v_cap(exist_plant) * availability(power_plant, month) * iLoadPoss(time,power_plant);
$OFFTEXT

* v_pump could either be used for standing pos reserve or for spinning pos reserve. v_pump_standing_pos seperates both proportions
eq_pump_standing_pos(node,time,exist_plant(power_plant, heat_regio))$(node_time(node, time) and power_plant_type(power_plant, 'IGELECSTORAGE'))..
         v_pump_standing_pos(node,time,exist_plant) =l= v_pump(node, time, exist_plant);

eq_pump_onlyPump(node,time,exist_plant(power_plant, heat_regio))$(node_time(node, time) and not power_plant_type(power_plant, 'IGELECSTORAGE') and not power_plant_type(power_plant, 'IGPTG'))..
         v_pump(node,time,exist_plant) =e= 0;

$ONTEXT
*Only H2_STO can pump h2
eq_pump_onlyPumpH2(node,time,exist_plant(power_plant, heat_regio))$(node_time(node, time) and not power_plant_type(power_plant, 'H2_STO'))..
         v_pump_h2(node,time,exist_plant) =e= 0;
$OFFTEXT

eq_pump_standing_pos_onlyPump(node,time,exist_plant(power_plant, heat_regio))$(node_time(node, time) and not power_plant_type(power_plant, 'IGELECSTORAGE'))..
         v_pump_standing_pos(node,time,exist_plant) =e= 0;

eq_pump_standing_neg_onlyPump(node,time,exist_plant(power_plant, heat_regio))$(node_time(node, time) and not power_plant_type(power_plant, 'IGELECSTORAGE'))..
         v_pump_standing_neg(node,time,exist_plant) =e= 0;

eq_MaxDischargePower(node, time,month, exist_plant(power_plant, heat_regio))$
                 (node_time(node,time) and month_time(month,time) and power_plant_type(power_plant, 'IGELECSTORAGE'))..
         v_cap_onl(node, time, exist_plant) =l= v_cap(exist_plant) * availability(power_plant, month) * iLoadPoss(time,power_plant);

*upper bound for power production
eq_prod_plant_ub(node, time, exist_plant(power_plant, heat_regio))$(node_time(node, time)
         and (not power_plant_type(power_plant, 'IGEXTRACTION')) and (not power_plant_type(power_plant, 'IGHEATBOILER')) and (not power_plant_type(power_plant, 'IGHEATPUMP'))
         and (not power_plant_type(power_plant, 'WIND')) and (not power_plant_type(power_plant, 'SUN')))..
         v_production(node, time, exist_plant,'electricity') =l= v_cap_onl(node, time, exist_plant);

*upper bound for power and heat production for chp IGEXTRACTION plants
eq_prod_plant_ub2(node, time, exist_plant(power_plant, heat_regio))$(node_time(node, time) and (power_plant_type(power_plant, 'IGEXTRACTION')))..
         v_production_energy(node, time, exist_plant) =l= v_cap_onl(node, time, exist_plant);

*upper bound for heat production from heat boilers
eq_prod_plant_ub3(node, time, exist_plant(power_plant, heat_regio))$(node_time(node, time) and
                                                                 (power_plant_type(power_plant, 'IGHEATBOILER') or power_plant_type(power_plant, 'IGHEATPUMP')))..
         v_production(node, time, exist_plant,'heat') =l= v_cap_onl(node, time, exist_plant);

*bound for electricity production from heat boilers
eq_prod_plant_ub4(node, time, exist_plant(power_plant, heat_regio))$(node_time(node, time) and power_plant_type(power_plant, 'IGHEATBOILER')
                                                                         and (not power_plant_type(power_plant, 'IGHEATPUMP')))..
         v_production(node, time, exist_plant,'electricity') =e= 0;

*bound for electricity production from PTG
eq_prod_plant_ub5(node, time, exist_plant(power_plant, heat_regio))$(node_time(node, time) and ((power_plant_type(power_plant, 'PTH2') OR power_plant_type(power_plant, 'PTM'))
* New Implementation for H2-Paper: No electricity production from H2_STO
*       OR power_plant_type(power_plant, 'H2_STO')
        ))..
         v_production(node, time, exist_plant,'electricity') =e= 0;

*if this equation is active ( is removed) e-mobility could not discharge into grid (to satisfy demand)
 eq_BanVehicle2Grid(node, time, exist_plant(power_plant, heat_regio))$(node_time(node, time)
                         and (power_plant_type(power_plant, 'IGELECSTORAGE') and (not power_plant_type(power_plant, 'HYDR_PS')) and (not power_plant_type(power_plant, 'BATT_STO'))))..
         v_production(node, time, exist_plant,'electricity') =e= 0;

*lower bound for the power and heat production of all power plants
eq_prod_plant_lb(node, time, exist_plant(power_plant, heat_regio))$(node_time(node, time)
         and (not power_plant_type(power_plant, 'IGHEATBOILER'))and (not power_plant_type(power_plant, 'IGHEATPUMP'))
         and (not power_plant_type(power_plant, 'WIND')) and (not power_plant_type(power_plant, 'SUN')) and (not power_plant_type(power_plant, 'IGPTG')))..
         v_production(node, time, exist_plant,'electricity') =g= min_load_fct(power_plant,heat_regio)*v_cap_onl(node, time, exist_plant)
;

*special constraint for wind power production which should always equal the capacity kept online (feed in condition)
eq_prod_plant_ub_VRE(node, time, exist_plant(power_plant, heat_regio))$(node_time(node, time) and (power_plant_type(power_plant, 'WIND') or power_plant_type(power_plant, 'SUN')))..
         v_production(node, time, exist_plant, 'electricity') =e= v_cap_onl(node, time, exist_plant);
*cap_ref(exist_plant) *availability(power_plant, month)
;

*capacity started up between two nodes equals the differece of the capacities kept online in these two nodes
*v_cap_startup: capacities started up at the transition from a node the next one --> =g= is okay, since model tries to reduce this capacity automatically!
eq_cap_startup(node, node1, time, time1, exist_plant(power_plant, heat_regio))$(node_succ(node, node1, time, time1)and (not power_plant_type(Power_plant,'WIND'))and (not power_plant_type(Power_plant,'SUN')))..
         v_cap_startup(node, node1, time, time1, exist_plant) =g= v_cap_onl(node1, time1, exist_plant)-v_cap_onl(node, time, exist_plant)
;

*incremental spinning reserve: capacity kept online should at least equal the production plus the spinning reserve in addtion
*(v_cap_online - v_production) +  --> wieviel kann hochgefahren werden + wieviel kann laden reduziert werden
eq_reserve_cap_spinningPos(node, time, month, zone)$(node_time(node, time) and month_time(month, time))..
         sum(exist_plant(power_plant, heat_regio)$(power_plant_type(power_plant, 'spinning') and heatregio_in_zone(heat_regio, zone)
                                                 and (not power_plant_type(power_plant,'NoReserveCapGroup'))),
                 v_cap_onl(node, time, exist_plant)-v_production(node, time, exist_plant,'electricity')
                                 + v_pump(node, time, exist_plant) - v_pump_standing_pos(node, time, exist_plant))
                 =g= spin_fctPos * sum(exist_plant(power_plant, heat_regio) $heatregio_in_zone(heat_regio,zone),v_production(node, time, exist_plant,'electricity'));

*decremental spinning reserve: capacity kept online should at least equal the production plus the spinning reserve in addtion
*(v_production - minProduction) + (v_cap_onl_charge_connected - v_pump - v_pump_standing_neg) --> wieviel kann runtergefahren werden + wieviel kann laden erh�ht werden
eq_reserve_cap_spinningNeg(node, time,month,  zone)$(node_time(node, time) and month_time(month, time))..
         sum(exist_plant(power_plant, heat_regio)$(power_plant_type(power_plant, 'spinning') and heatregio_in_zone(heat_regio, zone)
                                                 and (not power_plant_type(power_plant,'NoReserveCapGroup'))),
                 (v_production(node, time, exist_plant,'electricity')- min_load_fct(power_plant,heat_regio)* v_cap_onl(node, time, exist_plant))
         +              (v_cap(exist_plant)
*                                               * pump_cap_fct(exist_plant,time)
                                                * iLoadPoss(time, power_plant)* availability(power_plant, month) - v_pump(node, time, exist_plant) - v_pump_standing_neg(node,time,exist_plant)))
                 =g= spin_fctNeg * sum(exist_plant(power_plant, heat_regio) $heatregio_in_zone(heat_regio,zone),v_production(node, time, exist_plant,'electricity'));

*incremental standing reserve --> roughly: only fast startable plants; e.g. no nuclear, coal or lignite   --> positive tertiary reserve
*(v_cap - v_cap_online) + v_pump_standing_pos --> wieviel kann hochgefahren werden + wieviel kann laden reduziert werden
eq_reserve_cap_standingPos(node, time,month, country)$(node_time(node, time)and month_time(month, time))..
*               Differenzierung nicht IGELECSTORAGE (wegen iLoadPoss) und v_pump_standing_pos
         sum(exist_plant(power_plant, heat_regio)$(heatregio_in_country(heat_regio, country) and power_plant_type(power_plant, 'standing')
                                                 and (not power_plant_type(power_plant,'NoReserveCapGroup')) and (not power_plant_type(power_plant,'IGELECSTORAGE'))),
                 v_cap(exist_plant)*availability(power_plant, month)-v_cap_onl(node, time, exist_plant))
*               Differenzierung IGELECSTORAGE (wegen iLoadPoss) und v_pump_standing_pos
                +sum(exist_plant(power_plant, heat_regio)$(heatregio_in_country(heat_regio, country) and power_plant_type(power_plant, 'standing')
                                                 and (not power_plant_type(power_plant,'NoReserveCapGroup')) and power_plant_type(power_plant,'IGELECSTORAGE')),
                 v_cap(exist_plant)*availability(power_plant, month)* iLoadPoss(time, power_plant) - v_cap_onl(node, time, exist_plant)
                                 +v_pump_standing_pos(node, time, exist_plant))
                                  =g= sum(zone_in_country(zone, country), res_fct_MRLpos * v_demand_max(zone, 'electricity'));

*decremental standing reserve --> charging storage (v_pump_standing_neg) could relax restriction if increaseds
*since v_pump_standing_neg is coupled to the pump capacity via the pump_cap_fct by v_pump, it can only make a contribution for techs with pump_cap_fct > 0 --> no restriction to IGELECSTORAGE necessary.
eq_reserve_cap_standingNeg(node, time,month, country)$(node_time(node, time) and month_time(month, time))..
         sum(exist_plant(power_plant, heat_regio)$(heatregio_in_country(heat_regio, country) and power_plant_type(power_plant, 'standing')
                                                                                             and (not power_plant_type(power_plant,'NoReserveCapGroup'))),
                 min_load_fct(power_plant,heat_regio)* v_cap_onl(node, time, exist_plant)
                                 +  v_pump_standing_neg(node, time, exist_plant))
                =g= sum(zone_in_country(zone, country), res_fct_MRLneg * v_demand_max(zone, 'electricity'));

*equation to ensure a adequate level of installed capacity to maintain security of supply
eq_reserve_cap(country)..
         sum(exist_plant(power_plant, heat_regio)$(heatregio_in_country(heat_regio, country)
                         and (not power_plant_type(power_plant,'NoReserveCapGroup'))
                         and (not power_plant_type(power_plant,'IGELECSTORAGE')$(not power_plant_type(power_plant,'HYDR_PS')))),
                 v_cap(exist_plant) * sum(month, availability(power_plant, month)) / card(month))
         + sum(exist_plant(power_plant, heat_regio)$(heatregio_in_country(heat_regio, country)
                         and power_plant_type(power_plant,'BATT_STO')),
                 v_cap(exist_plant) * 0.5 * sum(month, availability(power_plant, month)) / card(month))
         + sum(exist_plant(power_plant, heat_regio)$(heatregio_in_country(heat_regio, country)
                         and power_plant_type(power_plant,'HYDR_ROR')),
                 smin((node,time)$node_time(node, time),inflow_run_river(node, time, exist_plant)))
                + sum(exist_plant(power_plant, heat_regio)$(heatregio_in_country(heat_regio, country)
                         and power_plant_type(power_plant,'HYDR_RES')),
                 smin((node,time)$node_time(node, time),inflow_annual_storage(node, time, exist_plant)))
         + sum(exist_plant(power_plant, heat_regio)$(heatregio_in_country(heat_regio, country)
                         and (power_plant_type(power_plant,'WIND_ON'))),
                 v_cap(exist_plant) * (sum(month, availability(power_plant, month)) / card(month)) * smin((node,time)$node_time(node, time),wind_onshore(heat_regio,node,time)))
         + sum(exist_plant(power_plant, heat_regio)$(heatregio_in_country(heat_regio, country)
                         and (power_plant_type(power_plant,'WIND_OFF'))),
                 v_cap(exist_plant) * (sum(month, availability(power_plant, month)) / card(month)) * smin((node,time)$node_time(node, time),wind_offshore(heat_regio,node,time)))
         + sum(exist_plant(power_plant, heat_regio)$(heatregio_in_country(heat_regio, country)
                         and (power_plant_type(power_plant,'SUN'))),
                 v_cap(exist_plant) * (sum(month, availability(power_plant, month)) / card(month)) * smin((node,time)$node_time(node, time),PV(heat_regio,node,time)))
                =g= sum(zone_in_country(zone, country),v_demand_max(zone, 'electricity'));

eq_reserve_cap_heat(heat_regio)..
                 sum(exist_plant(power_plant, heat_regio)$power_plant_type(power_plant, 'heat'), v_cap_heat(exist_plant) * smax(month, availability(power_plant, month) ) )
                 =g= heat_dem_max(heat_regio) * (1 + resfkt_heat)
;

eq_cap_nucl(node, node1, time, time1, month, exist_plant(power_plant, heat_regio))
                 $(node_succ(node, node1, time, time1)
                         and (power_plant_type(power_plant,'nuclear')or power_plant_type(power_plant,'lignite') )
                         and month_time(month,time1) and month_time(month,time))..
         v_cap_onl(node1, time1, exist_plant)$month_time(month,time1) =e= v_cap_onl(node, time, exist_plant)$month_time(month,time);

eq_cap_coal(node, time, time1, exist_plant(power_plant, heat_regio))
                 $(power_plant_type(power_plant,'coal') and node_time(node,time) and node_time(node,time1))..
         v_cap_onl(node, time1, exist_plant) =e= v_cap_onl(node, time, exist_plant);

*upper bound nuclear production
eq_prod_nucl(node, time, country)$(node_time(node, time) )..
         sum(exist_plant(power_plant, heat_regio)$(heat_regio_countries(heat_regio,country) and (power_plant_type(power_plant,'nuclear'))),
         v_production(node, time, exist_plant,'electricity')) =l= max_cap_nuclear(country);
         
*upper bound wind offshore production
eq_prod_wind_off(node, time, country)$(node_time(node, time) )..
         sum(exist_plant(power_plant, heat_regio)$(heat_regio_countries(heat_regio,country) and (power_plant_type(power_plant,'WIND_OFF'))),
         v_production(node, time, exist_plant,'electricity')) =l= max_cap_wind_off(country);

*MinGen BFG and WASTE
eq_min_gen(power_plant, heat_regio)$(fuel(power_plant, 'BFG') OR fuel(power_plant, 'MUNI_WASTE'))..
        sum((node,time)$node_time(node, time), prob_node(node) * hour_resolution(time) * freq_time(time) *
                v_production(node, time, power_plant, heat_regio, 'electricity'))
                                                                =G= v_cap(power_plant, heat_regio) * 5000;
*eq_min_gen(node, time, power_plant, heat_regio, product)$(fuel(power_plant, 'BFG') OR fuel(power_plant, 'MUNI_WASTE'))..
*        v_production(node, time, power_plant, heat_regio, 'electricity') =G= v_cap(power_plant, heat_regio) * 0.7;

*country specific co2 bound
eq_co2_bound..
co2_bound + co2_bound2
                                        =g= sum((node,time)$node_time(node, time), prob_node(node)*hour_resolution(time)*freq_time(time)*
                                         (
                                         sum(exist_plant(power_plant, heat_regio)$((not power_plant_type(power_plant,'IGEXTRACTION'))
                                         and (not power_plant_type(power_plant,'IGHEATBOILER')) and (min_load_fct(power_plant,heat_regio)<1)
                                         and (not power_plant_type(power_plant,'IGHEATPUMP')) and (not power_plant_type(power_plant,'IGPTG'))),
                                                 co2emis(power_plant, heat_regio)* (
                                                                   (v_production(node, time, exist_plant,'electricity')-v_cap_onl(node, time, exist_plant))*min_load_fct(power_plant,heat_regio)/(1-min_load_fct(power_plant,heat_regio))
                                                                   +
                                                                   v_production(node, time, exist_plant,'electricity')
                                                                   )
                                                 +
                                                co2emis_min(power_plant, heat_regio)*(v_cap_onl(node, time, exist_plant)-v_production(node, time, exist_plant,'electricity'))*min_load_fct(power_plant,heat_regio)/(1-min_load_fct(power_plant,heat_regio))
                                            )
                                         +
                                         sum(exist_plant(power_plant, heat_regio)$((not power_plant_type(power_plant,'IGEXTRACTION'))
                                          and (not power_plant_type(power_plant,'IGHEATBOILER')) and (min_load_fct(power_plant,heat_regio)=1)
                                         and (not power_plant_type(power_plant,'IGHEATPUMP')) and (not power_plant_type(power_plant,'IGPTG'))),
                                                 co2emis(power_plant, heat_regio) * v_production(node, time, exist_plant,'electricity')
                                            )
                                         +
                                         sum(exist_plant(power_plant, heat_regio)$(power_plant_type(power_plant,'IGEXTRACTION') and (min_load_fct(power_plant,heat_regio)<1)),
                                                  co2emis(power_plant, heat_regio) * (
                                                                   (v_production_energy(node, time, exist_plant)-v_cap_onl(node, time, exist_plant))*min_load_fct(power_plant,heat_regio)/(1-min_load_fct(power_plant,heat_regio))
                                                                   +
                                                                   v_production_energy(node, time, exist_plant)
                                                                               )
                                                 +
                                                 co2emis_min(power_plant, heat_regio) * (v_cap_onl(node, time, exist_plant)-v_production_energy(node, time, exist_plant))*min_load_fct(power_plant,heat_regio)/(1-min_load_fct(power_plant,heat_regio))
                                            )
                                         +
                                         sum(exist_plant(power_plant, heat_regio)$(power_plant_type(power_plant,'IGEXTRACTION') and (min_load_fct(power_plant,heat_regio)=1)),
                                                 co2emis(power_plant, heat_regio) * v_production_energy(node, time, exist_plant)
                                            )
                                         +
                                         sum(exist_plant(power_plant, heat_regio)$(power_plant_type(power_plant,'IGHEATBOILER')and (not power_plant_type(power_plant,'IGHEATPUMP')) and (not power_plant_type(power_plant,'IGPTG'))),
                                                 co2emis(power_plant, heat_regio) * v_production(node, time, exist_plant,'heat')
                                            )
                                         )
                                );

eq_co2_bound2..
co2_bound2
                                        =g= sum((node,time)$node_time(node, time), prob_node(node)*hour_resolution(time)*freq_time(time)*
                                         (
                                         sum(exist_plant(power_plant, heat_regio_co2_subset2)$((not power_plant_type(power_plant,'IGEXTRACTION'))
                                         and (not power_plant_type(power_plant,'IGHEATBOILER')) and (min_load_fct(power_plant,heat_regio_co2_subset2)<1)
                                         and (not power_plant_type(power_plant,'IGHEATPUMP')) and (not power_plant_type(power_plant,'IGPTG'))),
                                                 co2emis(power_plant, heat_regio_co2_subset2)* (
                                                                   (v_production(node, time, exist_plant,'electricity')-v_cap_onl(node, time, exist_plant))*min_load_fct(power_plant,heat_regio_co2_subset2)/(1-min_load_fct(power_plant,heat_regio_co2_subset2))
                                                                   +
                                                                   v_production(node, time, exist_plant,'electricity')
                                                                   )
                                                 +
                                                co2emis_min(power_plant, heat_regio_co2_subset2)*(v_cap_onl(node, time, exist_plant)-v_production(node, time, exist_plant,'electricity'))*min_load_fct(power_plant,heat_regio_co2_subset2)/(1-min_load_fct(power_plant,heat_regio_co2_subset2))
                                            )
                                         +
                                         sum(exist_plant(power_plant, heat_regio_co2_subset2)$((not power_plant_type(power_plant,'IGEXTRACTION'))
                                          and (not power_plant_type(power_plant,'IGHEATBOILER')) and (min_load_fct(power_plant,heat_regio_co2_subset2)=1)
                                         and (not power_plant_type(power_plant,'IGHEATPUMP')) and (not power_plant_type(power_plant,'IGPTG'))),
                                                 co2emis(power_plant, heat_regio_co2_subset2) * v_production(node, time, exist_plant,'electricity')
                                            )
                                         +
                                         sum(exist_plant(power_plant, heat_regio_co2_subset2)$(power_plant_type(power_plant,'IGEXTRACTION') and (min_load_fct(power_plant,heat_regio_co2_subset2)<1)),
                                                  co2emis(power_plant, heat_regio_co2_subset2) * (
                                                                   (v_production_energy(node, time, exist_plant)-v_cap_onl(node, time, exist_plant))*min_load_fct(power_plant,heat_regio_co2_subset2)/(1-min_load_fct(power_plant,heat_regio_co2_subset2))
                                                                   +
                                                                   v_production_energy(node, time, exist_plant)
                                                                               )
                                                 +
                                                 co2emis_min(power_plant, heat_regio_co2_subset2) * (v_cap_onl(node, time, exist_plant)-v_production_energy(node, time, exist_plant))*min_load_fct(power_plant,heat_regio_co2_subset2)/(1-min_load_fct(power_plant,heat_regio_co2_subset2))
                                            )
                                         +
                                         sum(exist_plant(power_plant, heat_regio_co2_subset2)$(power_plant_type(power_plant,'IGEXTRACTION') and (min_load_fct(power_plant,heat_regio_co2_subset2)=1)),
                                                 co2emis(power_plant, heat_regio_co2_subset2) * v_production_energy(node, time, exist_plant)
                                            )
                                         +
                                         sum(exist_plant(power_plant, heat_regio_co2_subset2)$(power_plant_type(power_plant,'IGHEATBOILER')and (not power_plant_type(power_plant,'IGHEATPUMP')) and (not power_plant_type(power_plant,'IGPTG'))),
                                                 co2emis(power_plant, heat_regio_co2_subset2) * v_production(node, time, exist_plant,'heat')
                                            )
                                         )
                                );
                                
eq_max_demand_el(zone,time,node)$(node_time(node, time))..
        v_demand_max(zone, 'electricity') =g= demand(time, zone, 'electricity') + demand_emob_fix(time, zone, 'electricity')
        +sum(exist_plant(power_plant, heat_regio)$(heatregio_in_zone(heat_regio,zone) and power_plant_type(power_plant, 'IGELECSTORAGE') and not power_plant_type(power_plant, 'BATT_STO') and not power_plant_type(power_plant, 'HYDR_PS')) ,
                 v_pump(node, time, exist_plant))
         +sum((heat_regio,exist_plant(power_plant, heat_regio)) $(heatregio_in_zone(heat_regio,zone) and power_plant_type(power_plant,'IGHEATPUMP')),
                 v_production(node, time, exist_plant, 'electricity'))

*---------------------------- For SRE (MD) --------------------------------------------
*ensures total electricity demand accounts for all components, including SRE-induced rebound demand
*Simultaneous SRE                 
        + sum((heat_regio, exist_plant(power_plant, heat_regio))$(heatregio_in_zone(heat_regio, zone) AND power_plant_type(power_plant, 'SUN')),
        (cap_n_sunk(exist_plant) + cap_ref(exist_plant)) * PV(heat_regio, node, time)
        * SRE_effect_strength *  share_privatePV(zone) * share_simSRE) 
        
*Sweeping SRE        
        + sum((heat_regio, exist_plant(power_plant, heat_regio))$(heatregio_in_zone(heat_regio, zone) AND power_plant_type(power_plant, 'SUN')),
        (cap_n_sunk(exist_plant) + cap_ref(exist_plant))
        *  pvAVG(heat_regio,node,time)    
        * SRE_effect_strength *  share_privatePV(zone) * share_sweSRE)
;
*---------------------------- For SRE (MD) --------------------------------------------

*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ MODEL @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
*static model
model plp_static
*/all/;
/
eq_total_cost
eq_var_cost_opr
eq_var_cost_startup
eq_var_cost_trans
eq_var_cost_trans_h2
*eq_var_cost_co2
eq_fix_cost_irr
eq_fix_cost_sunk
eq_fix_cost_rev

eq_cur_cost
eq_cost_import_h2

eq_supply
eq_supply_heat
eq_supply_backpressure

eq_demand_el
eq_demand_heat
eq_demand_h2
eq_demand_heatpump
eq_demand_pth2
eq_demand_ptm
eq_max_demand_el   

eq_supply_extraction_2
eq_supply_energy_total
eq_supply_wind_onshore
eq_supply_wind_offshore
eq_supply_PV

eq_cap
eq_cap_max
eq_cap_max_wind
eq_cap_startup

eq_transpo_CF
eq_transpo_CF_h2

eq_MaxChargePower
eq_MaxChargePower_Sim
eq_MaxChargePower_ptg
eq_MaxDischargePower
eq_MaxVolumeBATT

eq_pump_standing_pos
eq_supply_river
eq_resvr_annual
eq_resvr_daily
eq_resvrmax_annual
eq_resvrmin_annual
eq_MaxVolume

eq_prod_plant_ub
eq_prod_plant_ub2
eq_prod_plant_ub3
eq_prod_plant_ub4
eq_prod_plant_ub5
eq_prod_plant_ub_VRE
eq_prod_plant_lb

eq_BanVehicle2Grid

eq_reserve_cap_spinningPos
eq_reserve_cap_spinningNeg
eq_reserve_cap_standingPos
eq_reserve_cap_standingNeg

*eq_reserve_cap_heat
eq_reserve_cap

eq_pump_onlyPump
eq_pump_standing_pos_onlyPump
eq_pump_standing_neg_onlyPump

eq_prod_nucl
eq_cap_nucl
eq_cap_coal

eq_co2_bound
eq_co2_bound2
 
* H2 storage equations
*eq_resvr_daily_h2
*eq_MaxVolumeH2
*eq_MaxChargeH2
*eq_MaxDischargeH2
*eq_pump_onlyPumpH2

*eq_import_constraint
*eq_max_import
*eq_min_gen

*---------------------------- For SRE (MD) --------------------------------------------
*Declares that the formula (used for sweeping SRE) is properly integrated into the optimization model.
eq_pv_avg
*---------------------------- For SRE (MD) --------------------------------------------

/;
plp_static.optfile = 26;

*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ MODELLING @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
*======================================================================================================================
*======================================================================================================================
*-------------------- successive optimisation for each modelling period ------------------------
*======================================================================================================================
*======================================================================================================================
*---- initialisation of cap_n, container for new capacity
*at present the capacity degression is modelled with a negative 'capfn', instead of the degression factor
cap_n(power_plant, heat_regio) =0;
cap_n_sunk(exist_plant(power_plant, heat_regio))=0;
cap_n_sunk_heat(exist_plant(power_plant, heat_regio))=0;

loop (simyear,
*======================================================================================================================
*========part 1) filling parameters for specific year and calculation of endogenous parameters=========================
*======================================================================================================================
*assignment of input parameters for the simulated year
      fuel_price(primary_energy,zone)= b_fuel_price(simyear, primary_energy, zone)*(1+gr_cost_inv)**(numyear(simyear)-2010);
      wind_onshore(bregio,node,time) = b_wind_onshore(simyear,bregio,node,time);
      wind_offshore(bregio,node,time) = b_wind_offshore(simyear,bregio,node,time);
      PV(bregio,node,time) = b_PV(simyear,bregio,node,time);
      prob_node(node) = b_prob_node(simyear,node);
         display prob_node;
      prob_node_trans(node,node1) = b_prob_node_trans(simyear,node,node1);
      freq_trans(node,node1) = b_freq_trans(simyear,node,node1);
      
*---------------------------- For SRE (MD) --------------------------------------------
*This assignment retrieves the Rooftop PV share data from the Inc_database, where it is stored as Par share_privatePV ("C:\Users\...\Input\Inc_database\Par share_privatePV.inc").
*The parameter is listed under avail_param in the inc_structure ("C:\Users\...\Input\inc_structure\avail_param.inc").
*Since it is defined over the set simyear, it must be reassigned here to ensure it is correctly included in the recursive optimization loop.     
      share_privatePV(zone) = b_share_privatePV(simyear,zone);
*---------------------------- For SRE (MD) --------------------------------------------

      cost_inv(power_plant)= cost_inv0(power_plant)*(1+gr_cost_inv)**(numyear(simyear) - 2010);
      cost_inv(inv_plant)$power_plant_type(inv_plant,'crc_biomass') = cost_inv0(inv_plant) * plant_degr_fct(simyear,inv_plant) * (1 + gr_cost_inv)**(numyear(simyear) - 2010);
      cost_inv(inv_plant)$power_plant_type(inv_plant,'crc_solar') = cost_inv0(inv_plant) * plant_degr_fct(simyear,inv_plant) * (1 + gr_cost_inv)**(numyear(simyear) - 2010);
      cost_inv(inv_plant)$power_plant_type(inv_plant,'crc_wind_offs') = cost_inv0(inv_plant) * plant_degr_fct(simyear,inv_plant) * (1 + gr_cost_inv)**(numyear(simyear) - 2010);
      cost_inv(inv_plant)$power_plant_type(inv_plant,'crc_wind_ons') = cost_inv0(inv_plant) * plant_degr_fct(simyear,inv_plant) * (1 + gr_cost_inv)**(numyear(simyear) - 2010);
      
      cost_fix(power_plant) = cost_fix0(power_plant) *(1+gr_cost_inv)**(numyear(simyear)-2010);
      cost_fix(power_plant)$power_plant_type(power_plant,'crc_biomass') = cost_fix0(power_plant) * plant_degr_fct2(simyear,power_plant) * (1 + gr_cost_inv)**(numyear(simyear) - 2010);
      cost_fix(power_plant)$power_plant_type(power_plant,'crc_solar') = cost_fix0(power_plant) * plant_degr_fct2(simyear,power_plant) * (1 + gr_cost_inv)**(numyear(simyear) - 2010);
      cost_fix(power_plant)$power_plant_type(power_plant,'crc_wind_offs') = cost_fix0(power_plant) * plant_degr_fct2(simyear,power_plant) * (1 + gr_cost_inv)**(numyear(simyear) - 2010);
      cost_fix(power_plant)$power_plant_type(power_plant,'crc_wind_ons') = cost_fix0(power_plant) * plant_degr_fct2(simyear,power_plant) * (1 + gr_cost_inv)**(numyear(simyear) - 2010);

      cost_startup_abr(power_plant) = cost_startup_abr0(power_plant) *(1+gr_cost_inv)**(numyear(simyear)-2010);
      cost_misc(power_plant) = cost_misc0(power_plant) *(1+gr_cost_inv)**(numyear(simyear)-2010);
      cost_trans(zone,zzone) = cost_trans0(zone,zzone) * (1+gr_cost_inv)**(numyear(simyear)-2010);
      cost_trans_h2(zone,zzone) = cost_trans0_h2(zone,zzone) * (1+gr_cost_inv)**(numyear(simyear)-2010);

      inv_plant_regio(power_plant, heat_regio) = b_inv_plant_regio(simyear, power_plant, heat_regio);
      inflow_run_river(node, time, power_plant, bregio) = b_inflow_run_river(simyear,node, time, power_plant, bregio);
      inflow_annual_storage(node, time, power_plant, bregio) = b_inflow_annual_storage(simyear,node, time, power_plant, bregio);
      fill_level_max(exist_plant) = b_fill_level_max(simyear,exist_plant);

      max_cap(primary_energy, zone) = bmax_cap(simyear,primary_energy, zone);
      max_cap_wind(plant_type, zone) = bmax_cap_wind(simyear,plant_type, zone);
      h2_costs_import = b_h2_costs_import(simyear);
      max_cap_imports = b_max_cap_imports(simyear);

      heat_dem_max(heat_regio) = b_heat_dem_max(simyear, heat_regio);
      max_cap_nuclear(country) = b_max_cap_nuclear(simyear, country);
      max_cap_wind_off(country) = b_max_cap_wind_off(simyear, country);
      exist_line_CF(zone, zzone) = b_exist_line_CF(simyear,zone, zzone);
      exist_line_CF_h2(zone, zzone) = b_exist_line_CF_h2(simyear,zone, zzone);

      co2_bound =bco2_bound(simyear);  
      co2_bound2 =bco2_bound2(simyear);
      co2_cost = bco2_cost(simyear);
      co2_capture_fct(power_plant) = b_co2_capture_fct(simyear,power_plant);

*e-mobility information
      demand_clusterEmob(power_plant,heat_regio) = b_demand_clusterEmob(simyear,power_plant,heat_regio);
      iLeave(time, power_plant)       = b_iLeave(time, power_plant, simyear);
      iArrive(time, power_plant)      = b_iArrive(time, power_plant, simyear);
      idemand(time,power_plant)       = b_idemand(time, power_plant, simyear);
      iLoadPoss(time, power_plant)    = b_iLoadPoss(time, power_plant, simyear);
      iLoadSimultaneity(time, power_plant) =b_iLoadSimultaneity(time, power_plant, simyear);

*calculate demand of each zone as internal demand of each zone plus trade balance with zones not included; i.e. foreign zones
      demand(time,zone,'electricity')= demand_Y(simyear,time,zone,'electricity')+ ex_foreign_trade(simyear,time,zone,'electricity');
      demand(time,heat_regio,'heat')= demand_Y(simyear,time,heat_regio,'heat') + ex_foreign_trade(simyear,time,heat_regio,'heat');
      demand(time,zone,'h2')= demand_Y(simyear,time,zone,'h2')+ ex_foreign_trade(simyear,time,zone,'h2');
      demand_emob_fix(time,zone,product) = b_demand_emob_fix(simyear, time,zone,product);

*calculation of operating costs including fuel costs and miscellaneous costs
         loop (exist_plant(power_plant, heat_regio),
         if( (eff_plant(power_plant,heat_regio)$exist_plant(power_plant, heat_regio)) = 0,
           display "display eff_plant if zero", power_plant,heat_regio;
         ););

      cost_opr(time, exist_plant(power_plant, heat_regio))
         = cost_misc(power_plant)
         + sum(primary_energy$(fuel(power_plant, primary_energy)$exist_plant(power_plant, heat_regio)),
                 sum((zone)$(heatregio_in_zone(heat_regio,zone)), fuel_price(primary_energy,zone))/eff_plant(power_plant,heat_regio));

      cost_opr_min(time, exist_plant(power_plant, heat_regio))
         = cost_misc(power_plant)
         + sum(primary_energy$fuel(power_plant, primary_energy),
                 sum((zone) $(heatregio_in_zone(heat_regio,zone) and (fuel_price(primary_energy,zone)>0)),
                 fuel_price(primary_energy,zone))/eff_plant_min(power_plant,heat_regio));


      cost_opr(time, exist_plant(power_plant, heat_regio))$(exist_plant(power_plant, heat_regio)
                                                         and power_plant_type(power_plant,'crc_biomass'))
         = (cost_misc(power_plant)
           + sum(primary_energy$(fuel(power_plant, primary_energy)$exist_plant(power_plant, heat_regio)),
                 sum((zone)$(heatregio_in_zone(heat_regio,zone)), fuel_price(primary_energy,zone))/eff_plant(power_plant,heat_regio)));

      cost_opr_min(time, exist_plant(power_plant, heat_regio))$(exist_plant(power_plant, heat_regio)
                                                         and power_plant_type(power_plant,'crc_biomass'))
         = (cost_misc(power_plant)
           + sum(primary_energy$fuel(power_plant, primary_energy),
                 sum((zone) $(heatregio_in_zone(heat_regio,zone) and (fuel_price(primary_energy,zone)>0)),
                 fuel_price(primary_energy,zone))/eff_plant_min(power_plant,heat_regio)));

* calculation of variable startup costs including fuel costs for the startup process and costs for abrasion
      cost_startup(time, exist_plant(power_plant, heat_regio))
                 = cost_startup_abr(power_plant)
                   + cost_startup_fuel(power_plant)*sum((zone,primary_energy)$(fuel(power_plant, primary_energy) and heatregio_in_zone(heat_regio,zone)), fuel_price(primary_energy,zone));

      co2emis(exist_plant(power_plant, heat_regio))
                 = sum((primary_energy)$fuel(power_plant,primary_energy),co2factor(primary_energy)/eff_plant(power_plant, heat_regio));

      co2emis_min(exist_plant(power_plant, heat_regio))
                 = sum((primary_energy)$fuel(power_plant,primary_energy),co2factor(primary_energy)/eff_plant_min(power_plant, heat_regio));

*        adding exogeneously defined capacity change to the usable capacities before modelling for the present period
      cap_ref(exist_plant(power_plant, heat_regio)) = bcap_ref(power_plant, heat_regio, simyear);
      cap_ref_heat(exist_plant(power_plant, heat_regio)) = bcap_ref_heat(power_plant, heat_regio, simyear);

      cap_res_wat(exist_plant(power_plant, heat_regio)) = bcap_res_wat(power_plant, heat_regio, simyear);
      trans_cap_m(zone, zzone, month) = btrans_cap(zone, zzone, simyear, month);
      trans_cap_m_h2(zone, zzone, month) = btrans_cap_h2(zone, zzone, simyear, month);

      cap_regr_fct(power_plant,zone) = 1;

*======================================================================================================================
*=============Part 2)  ========OPTIMIZATION FOR ACTUAL SIMYEAR IS DONE HERE ===========================================
*======================================================================================================================
*------- execution of the simulation process ---Optimization of the model using linear optimization solve----------
      solve plp_static usingf lp minimizing total_cost;
      Option Bratio=1;

*======================================================================================================================
*============Part 3) ==============execution after solve to update the values==========================================
*======================================================================================================================

*        adding endogeneously decided capacity investment to the installed capacities in the next period
      cap_n(exist_plant(power_plant, heat_regio)) = cap_n(exist_plant)+v_cap_new.l(exist_plant);
      cap_n(power_plant,heat_regio)$power_plant_type(power_plant, 'chp')=cap_n(power_plant, heat_regio) + v_cap_new.l(power_plant, heat_regio);
      cap_n_sunk(exist_plant(power_plant, heat_regio)) = cap_n_sunk(exist_plant)+v_cap_new.l(exist_plant);
      cap_n_sunk_heat(exist_plant(power_plant, heat_regio)) = cap_n_sunk_heat(exist_plant)
      + v_cap_new.l(exist_plant)$((power_plant_type(power_plant, 'IGHEATBOILER') or power_plant_type(power_plant,'IGHEATPUMP')) and inv_plant_regio(power_plant,heat_regio))
      + (v_cap_new.l(power_plant, heat_regio) / fct_PQ_BP(power_plant))$(power_plant_type(power_plant, 'IGBACKPR') and inv_plant_regio(power_plant,heat_regio))
      + (v_cap_new.l(power_plant, heat_regio) / (fct_PQ_BP(power_plant) + fct_PQ_Extr(power_plant)))$(power_plant_type(power_plant, 'IGEXTRACTION') and inv_plant_regio(power_plant,heat_regio));

*======================================================================================================================
*============Part 4) ==============calculation for output==============================================================
*======================================================================================================================

      out_tcost(simyear) = total_cost.l;

* calculation of prices as marginal cost of electricity or heat demand
      out_el_price(simyear,node,time,zone) = (eq_demand_el.m(node,time,zone))*(-1)/(hour_resolution(time)*freq_time(time)*prob_node(node));
      out_heat_price(simyear,node,time,heat_regio) = (eq_demand_heat.m(node,time,heat_regio))*(-1)/(hour_resolution(time)*freq_time(time)*prob_node(node));

* calculation of h2 price as marginal of h2 demand
$ifi '%h2_yearly%' == Yes      out_h2_price(simyear,zone) = eq_demand_h2.m(zone);
$ifi NOT '%h2_yearly%' == Yes  out_h2_price(simyear,node, time, zone) = eq_demand_h2.m(node, time, zone)/(hour_resolution(time)*freq_time(time)*prob_node(node));

      out_var_cost_opr(simyear,time,exist_plant(power_plant,heat_regio)) = sum((node)$node_time(node, time), prob_node(node)*
                              (
* Differentiation between operating costs of power plants without CHP extraction-condensing
                                                      (
                                                      cost_opr(time, exist_plant)* (

                                                      (v_production.l(node, time, exist_plant,'electricity')-v_cap_onl.l(node, time, exist_plant))*min_load_fct(exist_plant)/(1-min_load_fct(exist_plant))
                                                      +

                                                      v_production.l(node, time, exist_plant,'electricity')
                                                      )
                                                      +

                                                      cost_opr_min(time, exist_plant)*(v_cap_onl.l(node, time, exist_plant)-v_production.l(node, time, exist_plant,'electricity'))*min_load_fct(exist_plant)/(1-min_load_fct(exist_plant))

                                                      )$((not power_plant_type(power_plant,'IGEXTRACTION'))
                                                      and (not power_plant_type(power_plant,'IGHEATBOILER')) and (not power_plant_type(power_plant,'IGHEATPUMP')) and (min_load_fct(exist_plant)<1))
                                                      +
                                                      (
                                                      cost_opr(time, exist_plant) * v_production.l(node, time, exist_plant,'electricity')
                                                      )$((not power_plant_type(power_plant,'IGEXTRACTION'))
                                                      and (not power_plant_type(power_plant,'IGHEATBOILER'))and (not power_plant_type(power_plant,'IGHEATPUMP')) and (min_load_fct(power_plant,heat_regio)=1))
                                                      +
* and with CHP extraction-condensing plants
                                                      (
                                                                              cost_opr(time, exist_plant)* (

                                                                              (v_production_energy.l(node, time, exist_plant)-v_cap_onl.l(node, time, exist_plant))*min_load_fct(exist_plant)/(1-min_load_fct(exist_plant))
                                                                              +

                                                                              v_production_energy.l(node, time, exist_plant)
                                                                              )
                                                                              +

                                                                              cost_opr_min(time, exist_plant)*(v_cap_onl.l(node, time, exist_plant)-v_production_energy.l(node, time, exist_plant))*min_load_fct(exist_plant)/(1-min_load_fct(exist_plant))

                                                      )$(power_plant_type(power_plant,'IGEXTRACTION') and (min_load_fct(exist_plant)<1))
                                                      +
                                                      (
                                                                        cost_opr(time, exist_plant) * v_production_energy.l(node, time, exist_plant)
                                                      )$(power_plant_type(power_plant,'IGEXTRACTION') and (min_load_fct(exist_plant)=1))
                                                      +
* and heat boilers
                                                      (
                                                                        cost_opr(time, exist_plant) * v_production.l(node, time, exist_plant,'heat')
                                                      )$(power_plant_type(power_plant,'IGHEATBOILER') and (not power_plant_type(power_plant,'IGHEATPUMP')))
                              )
                                    +
                                    v_spill_ror.l(node, time, exist_plant) * 100000
                                    +
                                    v_spill_ror2.l(node, time, exist_plant) * 100000
      )
      ;


      out_var_cost_startup(simyear,time,exist_plant) = sum((node,node1,time1)$(node_succ(node, node1, time, time1)$(cost_startup(time, exist_plant)>0)),
      prob_node(node)*prob_node_trans(node,node1)*v_cap_startup.l(node, node1, time, time1, exist_plant)*cost_startup(time, exist_plant)
      )
      ;

      out_var_cost_trans(simyear,time,exist_line_CF(zone, zzone)) =
      sum((node)$node_time(node, time),
      prob_node(node)*v_transpo.l(node, time, zone, zzone)*cost_trans(zone,zzone)
      );

      out_var_cost_trans_h2(simyear,time,exist_line_CF_h2(zone, zzone)) =
      sum((node)$node_time(node, time),
      prob_node(node)*v_transpo_h2.l(node, time, zone, zzone)*cost_trans_h2(zone,zzone)
      );

*    Prod el / Wirkungsgrad(Auslastung) * rohstoffabh�ngiger Emissionsfaktor
      cost_CO2(time, exist_plant(power_plant, heat_regio))
                 = sum(primary_energy$fuel(power_plant, primary_energy), co2factor(primary_energy) * eq_co2_bound.m / eff_plant(power_plant, heat_regio));

      cost_CO2_min(time, exist_plant(power_plant, heat_regio))
                 = sum(primary_energy$fuel(power_plant, primary_energy), co2factor(primary_energy) * eq_co2_bound.m / eff_plant_min(power_plant, heat_regio));


      out_var_cost_co2(simyear,time,exist_plant(power_plant,heat_regio)) = sum((node)$node_time(node, time), prob_node(node) *
                              (
* Differentiation between operating costs of power plants without CHP extraction-condensing
                                                      (
                                                      cost_CO2(time, exist_plant)* (

                                                      (v_production.l(node, time, exist_plant,'electricity')-v_cap_onl.l(node, time, exist_plant))*min_load_fct(exist_plant)/(1-min_load_fct(exist_plant))
                                                      +

                                                      v_production.l(node, time, exist_plant,'electricity')
                                                      )
                                                      +

                                                      cost_CO2_min(time, exist_plant)*(v_cap_onl.l(node, time, exist_plant)-v_production.l(node, time, exist_plant,'electricity'))*min_load_fct(exist_plant)/(1-min_load_fct(exist_plant))

                                                      )$((not power_plant_type(power_plant,'IGEXTRACTION'))
                              and (not power_plant_type(power_plant,'IGHEATBOILER')) and (not power_plant_type(power_plant,'IGHEATPUMP')) and (min_load_fct(exist_plant)<1))
                              +
                                                      (
                                                      cost_CO2(time, exist_plant) * v_production.l(node, time, exist_plant,'electricity')
                                                      )$((not power_plant_type(power_plant,'IGEXTRACTION'))
                              and (not power_plant_type(power_plant,'IGHEATBOILER')) and (not power_plant_type(power_plant,'IGHEATPUMP')) and (min_load_fct(exist_plant)=1))
                              +
* and with CHP extraction-condensing plants
                                                      (
                                                      cost_CO2(time, exist_plant)* (

                                                      (v_production_energy.l(node, time, exist_plant)-v_cap_onl.l(node, time, exist_plant))*min_load_fct(exist_plant)/(1-min_load_fct(exist_plant))
                                                      +

                                                      v_production_energy.l(node, time, exist_plant)
                                                      )
                                                      +

                                                      cost_CO2_min(time, exist_plant)*(v_cap_onl.l(node, time, exist_plant)-v_production_energy.l(node, time, exist_plant))*min_load_fct(exist_plant)/(1-min_load_fct(exist_plant))

                                                      )$(power_plant_type(power_plant,'IGEXTRACTION') and (min_load_fct(exist_plant)<1))
                              +
                                                      (
                                                      cost_CO2(time, exist_plant) * v_production_energy.l(node, time, exist_plant)
                                                      )$(power_plant_type(power_plant,'IGEXTRACTION') and (min_load_fct(exist_plant)=1))
                              +
*and heat boilers
                                                      (
                                                      cost_CO2(time, exist_plant) * v_production.l(node, time, exist_plant,'heat')
                                                      )$(power_plant_type(power_plant,'IGHEATBOILER') and (not power_plant_type(power_plant,'IGHEATPUMP')))
                              )
      )
      ;

      out_fix_cost_irr(simyear,power_plant,heat_regio)$inv_plant_regio2(power_plant,heat_regio) = annuity(power_plant)*cost_inv(power_plant)*1000* v_cap_new.l(power_plant,heat_regio)
      ;

*since cap_n_sunk was increased after solving already one needs to reduce it here again by v_cap_new.l
      out_fix_cost_sunk(simyear,exist_plant(power_plant, heat_regio)) = annuity(power_plant) * cost_inv(power_plant) * 1000 * (cap_n_sunk(exist_plant) - v_cap_new.l(exist_plant) + cap_ref(exist_plant))
      ;
      
      out_fix_cost_rev(simyear,exist_plant(power_plant, heat_regio)) = cost_fix(power_plant) * 1000 * v_cap.l(exist_plant)
      ;

*calculation of CO2 emissions
      out_co2emissions(zone, simyear) = sum((node,time)$node_time(node, time), prob_node(node)*hour_resolution(time)*freq_time(time)*
                  (
                          sum(exist_plant(power_plant, heat_regio)$((not power_plant_type(power_plant,'IGEXTRACTION')) and (heatregio_in_zone(heat_regio,zone))
                          and (not power_plant_type(power_plant,'IGHEATBOILER')) and (not power_plant_type(power_plant,'IGHEATPUMP')) and (min_load_fct(power_plant,heat_regio)<1)),
                           co2emis(power_plant, heat_regio)* (
                          (v_production.l(node, time, exist_plant,'electricity')-v_cap_onl.l(node, time, exist_plant))*min_load_fct(power_plant,heat_regio)/(1-min_load_fct(power_plant,heat_regio))
                          +
                          v_production.l(node, time, exist_plant,'electricity')
                          )
                          +
                          co2emis_min(power_plant, heat_regio)*(v_cap_onl.l(node, time, exist_plant)-v_production.l(node, time, exist_plant,'electricity'))*min_load_fct(power_plant,heat_regio)/(1-min_load_fct(power_plant,heat_regio))

                          )
                          +
                          sum(exist_plant(power_plant, heat_regio)$((not power_plant_type(power_plant,'IGEXTRACTION'))and (heatregio_in_zone(heat_regio,zone))
                          and (not power_plant_type(power_plant,'IGHEATBOILER')) and (not power_plant_type(power_plant,'IGHEATPUMP')) and (min_load_fct(power_plant,heat_regio)=1)),
                           co2emis(power_plant, heat_regio) * v_production.l(node, time, exist_plant,'electricity')
                          )
                          +
                          sum(exist_plant(power_plant, heat_regio)$(power_plant_type(power_plant,'IGEXTRACTION') and (min_load_fct(power_plant,heat_regio)<1) and (heatregio_in_zone(heat_regio,zone))),
                           co2emis(power_plant, heat_regio) * (
                          (v_production_energy.l(node, time, exist_plant)-v_cap_onl.l(node, time, exist_plant))*min_load_fct(power_plant,heat_regio)/(1-min_load_fct(power_plant,heat_regio))
                          +
                          v_production_energy.l(node, time, exist_plant)
                          )
                          +
                           co2emis_min(power_plant, heat_regio) * (v_cap_onl.l(node, time, exist_plant)-v_production_energy.l(node, time, exist_plant))*min_load_fct(power_plant,heat_regio)/(1-min_load_fct(power_plant,heat_regio))
                          )
                          +
                          sum(exist_plant(power_plant, heat_regio)$(power_plant_type(power_plant,'IGEXTRACTION') and (min_load_fct(power_plant,heat_regio)=1) and (heatregio_in_zone(heat_regio,zone))),
                           co2emis(power_plant, heat_regio) * v_production_energy.l(node, time, exist_plant)
                          )
                          +
                          sum(exist_plant(power_plant, heat_regio)$(power_plant_type(power_plant,'IGHEATBOILER') and (not power_plant_type(power_plant,'IGHEATPUMP')) and (heatregio_in_zone(heat_regio,zone))),
                          co2emis(power_plant, heat_regio) * v_production.l(node, time, exist_plant,'heat')
                          )
                  )
      );

* calculation of total electrictiy and heat production in a region per time step and year
      out_production(simyear,time, node, power_plant, zone, product)= sum(heat_regio$heatregio_in_zone(heat_regio, zone), v_production.l(node, time, power_plant, heat_regio, product));

      out_production_y(simyear, power_plant, zone, product) = sum((node,time)$node_time(node, time), prob_node(node)*hour_resolution(time)*freq_time(time)*
                                                                sum(heat_regio$heatregio_in_zone(heat_regio, zone), v_production.l(node, time, power_plant, heat_regio, product)));

*        calculation of total online capacity in a region
                out_cap_onl(simyear, time, node, exist_plant) = v_cap_onl.l(node, time, exist_plant);

*        calculation of prices as marginal cost of co2 bound
      out_co2_price(simyear) = eq_co2_bound.m;
      out_co2_price2(simyear) = eq_co2_bound2.m;

*               startup capacity
      out_cap_startup(simyear, time, node, time1, node1, exist_plant) = v_cap_startup.l(node, node1, time, time1, exist_plant);

      val_spill(simyear, node, time,"spill1", exist_plant) = v_spill_ror.l(node, time, exist_plant);
      val_spill(simyear, node, time,"spill2", exist_plant) = v_spill_ror2.l(node, time, exist_plant);

      out_total_cost_reg(simyear, exist_plant) = sum(time, hour_resolution(time) * freq_time(time) * (out_var_cost_opr(simyear,time,exist_plant) - sum((node, spill), val_spill(simyear, node, time, spill, exist_plant)) * 100000 + out_var_cost_startup(simyear,time,exist_plant))) + sum(time, sum((node,spill), val_spill(simyear, node, time, spill, exist_plant)) * 100000) + out_fix_cost_irr(simyear,exist_plant) + out_fix_cost_sunk(simyear,exist_plant) + out_fix_cost_rev(simyear,exist_plant)
      ;

      out_cap_new(simyear, power_plant, zone)=
      sum(heat_regio$heatregio_in_zone(heat_regio, zone), v_cap_new.l(power_plant, heat_regio));

      out_cap(simyear, power_plant, zone)=
      sum(heat_regio$heatregio_in_zone(heat_regio, zone), v_cap.l(power_plant, heat_regio));

      cap_exist(simyear, power_plant, zone)=
      sum(heat_regio$heatregio_in_zone(heat_regio, zone), cap_ref(power_plant, heat_regio) + cap_n_sunk(power_plant, heat_regio)$inv_plant_regio2(power_plant,heat_regio));

*     write out transport information
        out_transpo(simyear, node, time, zone, zzone) =  v_transpo.l(node, time, zone, zzone)$exist_line_CF(zone, zzone);

*     yearly transport information
        out_transpo_y(simyear, zone, zzone) = sum((node,time)$node_time(node, time), prob_node(node) * hour_resolution(time) * freq_time(time) * v_transpo.l(node, time, zone, zzone)$exist_line_CF(zone, zzone));

*     write out h2 transport information
        out_transpo_h2(simyear, node, time, zone, zzone) =  v_transpo_h2.l(node, time, zone, zzone)$exist_line_CF_h2(zone, zzone);

*     yearly h2 transport information
        out_transpo_h2_y(simyear, zone, zzone) = sum((node,time)$node_time(node, time), prob_node(node) * hour_resolution(time) * freq_time(time) * v_transpo_h2.l(node, time, zone, zzone)$exist_line_CF_h2(zone, zzone));

*      remember all pumping information per zone for gdx output use
       out_v_pump(simyear, node, time, power_plant, zone)=
       sum(heat_regio$heatregio_in_zone(heat_regio, zone), v_pump.l(node, time, power_plant, heat_regio) );

       out_v_pump_y(simyear, power_plant, zone) = sum((node,time)$node_time(node, time), prob_node(node)*hour_resolution(time)*freq_time(time)*
       sum(heat_regio$heatregio_in_zone(heat_regio, zone), v_pump.l(node, time, power_plant, heat_regio)));

       out_v_pump_reserve(simyear, node, time, power_plant, zone)=
       sum(heat_regio$heatregio_in_zone(heat_regio, zone), v_pump_standing_neg.l(node, time, power_plant, heat_regio));

*       remember curtailment
        out_v_cur(simyear, node, time, power_plant, zone) =
        sum(heat_regio$heatregio_in_zone(heat_regio, zone), v_curtailment.l(node, time, power_plant, heat_regio));

        out_v_cur_y(simyear, power_plant, zone) = sum((node,time)$node_time(node, time), prob_node(node)*hour_resolution(time)*freq_time(time)*
        sum(heat_regio$heatregio_in_zone(heat_regio, zone), v_curtailment.l(node, time, power_plant, heat_regio)));

        out_cur_cost(simyear) = v_cur_cost.l;

*       remember demand
        out_demand(simyear, time, zone, product) = demand(time,zone, product) + demand_emob_fix(time, zone, product);
        out_demand(simyear, time, zone, 'heat') = sum(heat_regio$heatregio_in_zone(heat_regio, zone), demand(time, heat_regio, 'heat'));

*       remember yearly demand
        out_demand_y(simyear, zone, product) = sum(time, (demand(time, zone, product) + demand_emob_fix(time, zone, product)) * hour_resolution(time) * freq_time(time));
        out_demand_y(simyear, zone, 'electricity') = sum(time, (demand(time, zone, 'electricity') + demand_emob_fix(time, zone, 'electricity')) * hour_resolution(time) * freq_time(time))
                                        + sum((node,time)$node_time(node, time), prob_node(node) * hour_resolution(time) * freq_time(time) *
                                          sum(exist_plant(power_plant, heat_regio)$heatregio_in_zone(heat_regio, zone), v_pump.l(node, time, power_plant, heat_regio)))
                                        + sum((node,time)$node_time(node, time), prob_node(node) * hour_resolution(time) * freq_time(time) *
                                          sum(exist_plant(power_plant, heat_regio)$(heatregio_in_zone(heat_regio, zone) AND power_plant_type(power_plant,'IGHEATPUMP')), v_production.l(node, time, power_plant, heat_regio, 'electricity')));

        out_demand_y(simyear, zone, 'h2') = sum(time, demand(time, zone, 'h2') * hour_resolution(time) * freq_time(time))
                               + sum((node,time)$node_time(node, time), prob_node(node) * hour_resolution(time) * freq_time(time) *
                                sum(exist_plant(power_plant, heat_regio)$(heatregio_in_zone(heat_regio, zone) AND fuel(power_plant, 'HYDROGEN')),
                                v_production.l(node, time, exist_plant, 'electricity') / eff_plant(power_plant, heat_regio)))
                                + sum((node,time)$node_time(node, time), prob_node(node) * hour_resolution(time) * freq_time(time) *
                                sum(exist_plant(power_plant, heat_regio)$(heatregio_in_zone(heat_regio, zone) AND power_plant_type(power_plant,'IGHEATBOILER') AND fuel(power_plant, 'HYDROGEN')),
                                v_production.l(node, time, exist_plant, 'heat') / eff_plant(power_plant, heat_regio)));

        out_demand_y(simyear, zone, 'heat') = sum(time, hour_resolution(time) * freq_time(time) * sum(heat_regio$heatregio_in_zone(heat_regio, zone), demand(time, heat_regio, 'heat')));

*---------------------------- For SRE (MD) --------------------------------------------
*Export routine to report total annual electricity demand including additional SRE-related consumption.        
        out_demand_y_inclSRE(simyear, zone, 'electricity') = sum(time, (demand(time, zone, 'electricity') + demand_emob_fix(time, zone, 'electricity')) * hour_resolution(time) * freq_time(time))
                                        + sum((node,time)$node_time(node, time), prob_node(node) * hour_resolution(time) * freq_time(time) *
                                          sum(exist_plant(power_plant, heat_regio)$heatregio_in_zone(heat_regio, zone), v_pump.l(node, time, power_plant, heat_regio)))
                                        + sum((node,time)$node_time(node, time), prob_node(node) * hour_resolution(time) * freq_time(time) *
                                          sum(exist_plant(power_plant, heat_regio)$(heatregio_in_zone(heat_regio, zone) AND power_plant_type(power_plant,'IGHEATPUMP')), v_production.l(node, time, power_plant, heat_regio, 'electricity')))                                        
                                        + sum((node,time)$node_time(node, time), prob_node(node) * hour_resolution(time) * freq_time(time) *
*Simultaneous SRE
                                        ( sum((heat_regio, exist_plant(power_plant, heat_regio))$(heatregio_in_zone(heat_regio, zone) AND power_plant_type(power_plant, 'SUN')),
                                        (cap_n_sunk(exist_plant) - v_cap_new.l(exist_plant) + cap_ref(exist_plant)) * PV(heat_regio, node, time)
                                        * SRE_effect_strength * share_privatePV(zone) * share_simSRE) 
*Sweeping SRE        
                                        + sum((heat_regio, exist_plant(power_plant, heat_regio))$(heatregio_in_zone(heat_regio, zone) AND power_plant_type(power_plant, 'SUN')),
                                        (cap_n_sunk(exist_plant)- v_cap_new.l(exist_plant) + cap_ref(exist_plant))
                                        * pvAVG.l(heat_regio,node,time)   
                                        * SRE_effect_strength * share_privatePV(zone) * share_sweSRE)))
;

*Export routine to report isolated electricity demand caused by the SRE.
        out_demand_y_SRE(simyear, zone, 'electricity') = + sum((node,time)$node_time(node, time), prob_node(node) * hour_resolution(time) * freq_time(time) *
*Simultaneous SRE
                                        ( sum((heat_regio, exist_plant(power_plant, heat_regio))$(heatregio_in_zone(heat_regio, zone) AND power_plant_type(power_plant, 'SUN')),
                                        (cap_n_sunk(exist_plant) - v_cap_new.l(exist_plant) + cap_ref(exist_plant)) * PV(heat_regio, node, time)
                                        * SRE_effect_strength * share_privatePV(zone) * share_simSRE) 
*Sweeping SRE        
                                        + sum((heat_regio, exist_plant(power_plant, heat_regio))$(heatregio_in_zone(heat_regio, zone) AND power_plant_type(power_plant, 'SUN')),
                                        (cap_n_sunk(exist_plant)- v_cap_new.l(exist_plant) + cap_ref(exist_plant))
                                        * pvAVG.l(heat_regio,node,time)   
                                        * SRE_effect_strength * share_privatePV(zone) * share_sweSRE)))
;
*---------------------------- For SRE (MD) --------------------------------------------

*       remember h2 imports
        out_h2_import_costs(simyear) = v_h2_cost.l;

$ifi '%h2_yearly%' == Yes        out_v_import_h2_y(simyear, zone) = v_import_h2.l(zone);
$ifi NOT '%h2_yearly%' == Yes    out_v_import_h2(simyear, node, time, zone) = v_import_h2.l(node, time, zone);
$ifi NOT '%h2_yearly%' == Yes    out_v_import_h2_y(simyear, zone) = sum((node,time)$node_time(node, time),
$ifi NOT '%h2_yearly%' == Yes    prob_node(node) * hour_resolution(time) * freq_time(time) * v_import_h2.l(node, time, zone));

*       estimated fill level
        out_fill_level_h_exp(simyear, time, exist_plant) = sum(node$node_time(node,time), prob_node(node)* v_fill_level_h.l(node, time, exist_plant));

        out_demand_max(simyear, bregio, product) = v_demand_max.l(bregio,product);

*------------------------ Writing modelling results in GDX file ----------------
          
        execute_unload "%PATH_OUT%\GDX\E2M2s_simyear.gdx";
    
*---------------------------------------------------------------------------------------------------------------------------------------
*------------------------- Reset variable of new capacity ------------------------------------------------------------------------------
*---------------------------------------------------------------------------------------------------------------------------------------

        v_cap_new.l(power_plant, heat_regio)=0;

*---------------------------------------------------------------------------------------------------------------------------------------
);
*---------------------------------------------------------------------------------------------------------------------------------------
*------------End of simyear loop -> start new loop over next simyear--------------------------------------------------------------------
*---------------------------------------------------------------------------------------------------------------------------------------