# **Exploring Vehicle-to-Grid (V2G) Integration and Connecting Behavior in E2M2s**

This repository contains the model code, data, and analysis scripts used in the V2G study by **Bucksteeg et al. (2026) [DOI: ...]**, based on a European power system model. A toolbox first applies a time-inhomogeneous Markov chain to survey-based electric vehicle (EV) plug-in behavior to estimate connection probabilities. These probabilities are then used in a Monte Carlo simulation to generate time-resolved fleet-level V2G capacity, forming a Markov-chain Monte Carlo (<code>MCMC</code>) framework. The repository is designed as a fully documented companion to the paper, ensuring reproducibility of all key results.

## System requirements
To run the adjusted model, you need <kbd>GAMS</kbd> version 40.1 or higher. A linear solver licence is required; the model was tested with <kbd>CPLEX</kbd>, but any LP-capable solver should work. For the <kbd>MCMC toolbox</kbd> and post-processing, <kbd>Python</kbd> 3.9 or higher and <kbd>Jupyter Notebook</kbd> (or <kbd>JupyterLab</kbd>) are required. The necessary Python packages include `numpy`, `pandas`, `matplotlib`, and `scipy`, along with the standard-library modules `dataclasses`, `pathlib`, and `typing`. For the MCMC analysis, the `gaussian_kde` module from `scipy.stats` is used, as well as other components from `matplotlib` for visualization. The NTC map presented in the paper is created using <kbd>QGIS</kbd> (version 3.40); a corresponding project file is included with the results to enable reproduction or further editing. For quick, ad hoc inspection of results, a spreadsheet program (e.g., <kbd>Excel</kbd>) is also convenient, as many outputs are tabular and can be exported from <kbd>.gdx</kbd>-files. For smooth execution, at least 8 GB of RAM and 4 CPU cores are recommended. All necessary installations and preparations should be completed within 1-2 hours on a standard workstation.

## Folder layout
This repository contains one run file (<kbd>osE2M2s_V2G.gms</kbd>) together with shared inputs, a preconfigured <kbd>Output/</kbd> folder, a dedicated folder for the <kbd>MCMC toolbox</kbd> and supplementary materials. For a quick test, clone this repository and use the layout below as a guide:

```
├─ Input/                                   # Shared parameter and structure files for all V2G scenarios and sensitivities
├─ MCMC/                                    # Plug-in probabilities and available battery capacities derived by scaling survey data (Figs. 1, 8, 9, 10)                           
├─ Output/                                  # Preconfigured folder with automatically filled results after execution and prepared results of the paper
├─ Supplementary material/                          # Data, figures, and results used in the paper
│  ├─ Abstract MCMC/                                # Visualizing the interdependencies through survey, MCMC-based simulation, and energy system modeling         
│  ├─ Capacities/                                   # Capacity mix (Fig. 11)
│  ├─ CO2 abatement/                                # CO2 prices and abatement costs (Fig. 14)
│  ├─ Electricity prices/                           # Wholesale electricity prices in box- & violinplots (Figs. 6, 16)
│  ├─ Generation/                                   # Generation mixes (Figs. 2, 13, 15)
│  ├─ Peak-hour generation/                         # Analysis for winter and summer peaking systems and their dependence on EV plug-in availability (Fig. 3)
│  ├─ System costs/                                 # System cost breakdowns and per EV added value (Figs. 5, 7, 12)
│  ├─ Transmission congestion costs                 # Congestion metrics with shadow values (Fig. 4)
│  ├─ Bat_sens_V2G.xlsx                             # Sensitivity results for additional exogenous battery capacity (consolidated tables for quick spreadsheet checks)
│  ├─ GasPrice_sens_V2G                             # Sensitivity results for doubled gas prices (consolidated tables for quick spreadsheet checks)
│  └─ Final_results.xlsx                            # Main results for quick spreadsheet checks (consolidated tables for quick spreadsheet checks)
├─ osE2M2s_V2G.gms                          # GAMS model file for running the V2G scenarios and sensitivities
```

The model has not been pre-run and must be executed manually before analysis. Before execution, adjust the input and output paths defined at the beginning of the run file (<kbd>osE2M2s_V2G.gms</kbd>). Replace the placeholder values of <code>PATH_IN_DATA</code> and <code>PATH_OUT</code> with the full paths to your local <kbd>Input/</kbd> and <kbd>Output/</kbd> directories:

```text
gams
$SETGLOBAL PATH_IN_DATA C:\...\Input
$SETGLOBAL PATH_OUT C:\...\Output
```

For the <code>MCMC toolbox</code>, navigate to the corresponding folder and open <kbd>Run_MCMC_modul.ipynb</kbd> in Jupyter. Execute the notebook from top to bottom. The notebook will clean and filter the EV survey data (<kbd>raw_data_surveyV2G.csv</kbd>), estimate plug-in profiles using Markov-chain transition matrices, run a Monte Carlo simulation to compute available V2G capacity, and export the resulting empirical plug-in probability (<kbd>Par iLoadPluginProb_61.inc</kbd> + <kbd>Par iLoadPluginProb_25.inc</kbd>) files for the respective scenarios. In the notebook, a key Monte Carlo fleet parameter is set as `n_vehicles = 100_000` for testing purposes. To fully reproduce the results with the full fleet size used in the paper, change this value to `n_vehicles = 122_000_000`.

## Full reproducibility (V2G scenarios and sensitivities)
To locate the specific model adjustments, search the code (Ctrl+F) for keywords such as <code>V2G</code> or the author’s initials <code>MB</code>. The code is preconfigured for the full availability sceanrio (100%) without any sensitivities. To switch between scenarios or activate sensitivities, add or remove a <code>*</code> in front of the corresponding **`lines 1247-1266`**. On the right-hand side of the equal sign, the parameter name is used to denote the corresponding scenario or sensitivity, such as `b_iLoadPluginProb_61` for the average scenario with 61% availability or `b_fuel_price_doubleGAS` for the gas price doubling sensitivity.

```gams
*---------------------------- For V2G (MB) --------------------------------------------
[...]
*    iLoadPluginProb(time, power_plant)    = b_iLoadPluginProb_25(time, power_plant, simyear);
*    iLoadPluginProb(time, power_plant)    = b_iLoadPluginProb_61(time, power_plant, simyear);
    iLoadPluginProb(time, power_plant)    = b_iLoadPluginProb_100(time, power_plant, simyear);

*---------------------------- For V2G (MB) --------------------------------------------
[...]
    fuel_price(primary_energy,zone)= b_fuel_price(simyear, primary_energy, zone)*(1+gr_cost_inv)**(numyear(simyear)-2010);
*    fuel_price(primary_energy,zone)= b_fuel_price_doubleGAS(simyear, primary_energy, zone)*(1+gr_cost_inv)**(numyear(simyear)-2010);
    
    cap_ref(exist_plant(power_plant, heat_regio)) = bcap_ref(power_plant, heat_regio, simyear);
*    cap_ref(exist_plant(power_plant, heat_regio)) = bcap_ref_50GWBAT(power_plant, heat_regio, simyear);
*    cap_ref(exist_plant(power_plant, heat_regio)) = bcap_ref_100GWBAT(power_plant, heat_regio, simyear);
*---------------------------- For V2G (MB) --------------------------------------------
```

## Inspecting results
After a successful model run, results are saved in the <kbd>Output/</kbd> directory as <kbd>E2M2s_simyear.gdx</kbd>, which can be opened with <kbd>GAMS</kbd> utilities. For reproducing figures, use the <kbd>Python</kbd> and/or <kbd>QGIS</kbd> materials in the <kbd>Supplementary material/</kbd> folder, where selected results are pre-processed into figure-ready tables and visualizations. Please note that depending on the computational settings or updates, the results may slightly differ from those presented in the paper.

## Licence and citation
The contents of this repository are made available under the MIT license. For details, see the LICENSE file in the main branch. If you use this code or data in academic work, please cite the associated V2G paper once it is published. A suggested reference format will be added to this `README` as soon as the final publication details are available.
