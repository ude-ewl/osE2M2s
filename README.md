# **Present Bias and the Cost Efficiency of Solar Support Policies in E2M2s**

This repository contains the model code, data, and analysis scripts used in the study by **Bucksteeg et al. (2027) [DOI: ...]**, based on a European power system model. The study integrates heterogeneous and time-inconsistent (hyperbolic) discounting into the open-source energy system model E2M2s and compares equivalent residential (rooftop) PV support instruments (upfront grants vs. feed-in tariffs) until 2050. The repository is designed as a fully documented companion to the paper, ensuring reproducibility of all key results.

## System requirements
To run the adjusted model, you need <kbd>GAMS</kbd> version 40.1 or higher. A linear solver licence is required; the model was tested with <kbd>CPLEX</kbd>, but any LP-capable solver should work. <kbd>Python</kbd> (version 3.9 or higher) is mainly required for post-processing of the visualizations; scripts and data are available in the <kbd>Supplementary material/</kbd> folder. The Python packages used include <code>pandas</code>, <code>matplotlib</code>, <code>geopandas</code>, and <code>gdxpds</code>; the support-structure map additionally uses <code>shapely</code>. For quick, ad hoc inspection of results, a spreadsheet program (e.g., <kbd>Excel</kbd>) is also convenient, since many outputs are tabular and can be exported from <kbd>.gdx</kbd>-files. For smooth execution, at least 8 GB of RAM and 4 CPU cores are recommended. All necessary installations and preparations should be completed within an hour on a standard workstation.

## Folder layout
This repository contains a single run file (<kbd>osE2M2s_v01.gms</kbd>) together with shared inputs, a preconfigured <kbd>Output/</kbd> folder, and supplementary materials. All discounting scenarios and support instruments are selected via switches inside the run file (see *Full reproducibility* below), so no separate model file per scenario is required. For a quick test, clone this repository and use the layout below as a guide:

```text
├─ Input/                                          # Shared parameter and structure files for all scenarios
│  ├─ Inc_database/                                     # Parameter and set include files (.inc), incl. discounting & support inputs
│  └─ inc_structure/                                    # Structural set definitions
├─ Output/                                         # Preconfigured output folder (filled automatically after execution)
│  └─ GDX/                                              # GDX result files written per simulation year
├─ Supplementary material/                         # Data, figures, and results used in the paper
│  ├─ 1) Support strucutre/                             # Derivation of the 60% support level, support-scheme maps (Fig. 1)
│  │  ├─ PV_support_map.ipynb                               # Notebook: support maps + derivation of the ~56% feed-in coverage
│  │  ├─ pv_support_data.csv                                # Researched feed-in tariffs & investment grants incl. sources (URLs)
│  │  └─ world-administrative-boundaries.*                  # Shapefile (geometry) for the European maps
│  ├─ 2) Generation/                                    # Generation & storage charging mixes (Fig. 1 in paper)
│  ├─ 3) Capacity/                                      # Installed capacity mixes (Fig. 2)
│  ├─ 4) System cost/                                   # System cost trajectories & decompositions (Fig. 3)
│  ├─ 5) Electricity price/                             # Wholesale electricity price distributions (Fig. 4)
│  ├─ 6) Support cost/                                  # Public support expenditure & cost intensity (Fig. 5)
│  └─ Results_Discounting_final.xlsx                    # Consolidated result tables for quick spreadsheet checks
└─ osE2M2s_v01.gms                                 # GAMS model file for running all discounting & support scenarios
```

The model has not been pre-run and must be executed manually before analysis. Before execution, adjust the input and output paths defined at the beginning of the run file (<kbd>osE2M2s_v01.gms</kbd>). Replace the placeholder values of <code>PATH_IN_DATA</code> and <code>PATH_OUT</code> with the full paths to your local <kbd>Input/</kbd> and <kbd>Output/</kbd> directories:

```text
gams
$SETGLOBAL PATH_IN_DATA C:\...\Input
$SETGLOBAL PATH_OUT C:\...\Output
```

## Full reproducibility (discounting and support scenarios)
To locate the specific model adjustments, search the code (Ctrl+F) for the author's initials <code>MB</code>. All changes relative to the public base model are wrapped in clearly labelled blocks (`*--- For discounting (MB) ---`). The different scenarios are handled via a **scenario switch in the model file**. The available scenarios are documented in the scenario-selection block in **`lines 172–184`**:

```gams
*==============================================================================
* DISCOUNTING AND SUPPORT MECHANISM SCENARIO SELECTION
*==============================================================================
* Choose one scenario by setting SCENARIO to one of the following:
* 01. exp            : Exponential discounting, NO support (Baseline)
* 02. exp_upfront    : Exponential discounting, upfront payment support
* 03. exp_feedin     : Exponential discounting, feed-in tariff support
* 04. hyp            : Hyperbolic discounting, NO support (Baseline)
* 05. hyp_upfront    : Hyperbolic discounting, upfront payment support
* 06. hyp_feedin     : Hyperbolic discounting, feed-in tariff support
* 07. hyp_feedin_eq  : Hyperbolic discounting, feed-in with equivalent annuity
*==============================================================================
```

To activate a scenario, set <code>SCENARIO</code> to the corresponding **name (without the leading number)** in **`line 187`**. By default the repository is preconfigured for the hyperbolic upfront scenario:

```gams
$setglobal SCENARIO hyp_upfront
```

For example, to reproduce the hyperbolic feed-in tariff with an upfront-equivalent annuity, change this single line to `$setglobal SCENARIO hyp_feedin_eq` and re-run the model. No other edits are required; the model resolves the matching discount function (exponential or hyperbolic), the support mechanism (none, upfront, or feed-in), and the support payments accounting accordingly.

### Derivation of the 60% support level
The support level used in the analysis (60% of investment costs) is derived empirically from the prevailing European feed-in tariffs. If you want to follow this calculation step by step, check out the notebook in **`Supplementary material/1) Support strucutre/PV_support_map.ipynb`**. It reproduces how the discounted feed-in payments translate into an average coverage of about 56% of the cost of a 2024 investment (rounded to 60% for the analysis) and generates the support-scheme maps. The underlying researched data — the country-level feed-in tariffs and investment grants together with their sources (as URLs) — are provided in **`Supplementary material/1) Support strucutre/pv_support_data.csv`**.

## Inspecting results
After a successful model run, results are saved in the <kbd>Output/GDX/</kbd> directory in GDX format, which can be opened with <kbd>GAMS</kbd> utilities. For reproducing figures, use the <kbd>Python</kbd> materials in the numbered <kbd>Supplementary material/</kbd> folders, where selected results are pre-processed into figure-ready tables and visualizations. For quick spreadsheet analysis, a curated summary of all results is available in <kbd>Supplementary material/Results_Discounting_final.xlsx</kbd>. Please note that depending on the computational settings or updates, the results may slightly differ from those presented in the paper.

## Licence and citation
The contents of this repository are made available under the MIT license. For details, see the LICENSE file in the main branch. If you use this code or data in academic work, please cite the associated discounting paper once it is published. A suggested reference format will be added to this `README` as soon as the final publication details are available.