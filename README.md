### System requirements
This repository contains the model code, data, and analysis scripts used in the Solar Rebound study by **Delic & Bucksteeg (2026) (https://doi.org/10.1038/s41560-026-02031-8)**, based on a European power system model. To run the model, you need <kbd>GAMS</kbd> version 40.1 or higher. It was tested with a CPLEX license, but any solver capable of handling linear problems should work. For quick, ad hoc inspection of results, a spreadsheet program (e.g., <kbd>Excel</kbd>) is also convenient, since many outputs are tabular and can be exported from GDX. Python (version 3.9 or higher) is only required for post-processing of the visualizations; scripts and data are available in the <kbd>Supplementary material/</kbd> folder. The Python packages used include <code>pandas</code>, <code>matplotlib</code>, and <code>gdxpds</code>. The NTC map presented in the paper was created using <kbd>QGIS</kbd> (version 3.40); a corresponding project file is included with the results to enable reproduction or further editing. For smooth execution, at least 8 GB of RAM and 4 CPU cores are recommended. All necessary preparations and installations should be completed within an hour.

### Folder layout
This repository contains three run files (one <kbd>.gms</kbd> for each temporal profile) together with shared inputs, a preconfigured output folder, and supplementary materials. All three temporal profiles (dynamic, simultaneous, and sweeping) can be computed with the same input dataset located in the <kbd>Input/</kbd> folder.

### Quick start (demo)
For a quick test, clone this repository and use the layout below as a guide:

```text
├─ Input/                                  # shared parameter and structure files for all profiles
├─ Output/                                 # preconfigured output folder (filled automatically after execution)
├─ Supplementary material/                 # underlying paper figure and data
│  ├─ Additional demand/                         # SRE-induced extra demand (Fig. 2)
│  ├─ CO2 abatement costs & CO2 prices/          # CO2 prices and abatement costs (ED Fig. 5)
│  ├─ Electricity prices/                        # wholesale prices and deltas for maps (Fig. 7; ED Figs. 6, 7) and boxplots (ED Fig. 8)
│  ├─ Generation/                                # generation mixes (Fig. 4; ED Figs. 3, 4)
│  ├─ Grid expansion benefit/                    # congestion metrics with shadow values (Fig. 5)
│  ├─ Installed capacity/                        # capacity mixes (Fig. 3; ED Figs. 1, 2)
│  ├─ Meta-Study/                                # empirically observed rebound strengths (Fig. 1)
│  ├─ Policy Brief/                              # figures used in the accompanying Policy Brief
│  ├─ Rebound consumption patterns/              # SRE phases (ED Fig. 9), schematic profiles (ED Fig. 10) and dynamic-profile derivation
│  ├─ Total system costs/                        # system cost breakdowns (Fig. 6)
│  └─ Final_results_SRE.xlsx                     # underlying results (consolidated tables for quick spreadsheet checks)
├─ dynamicSRE_E2M2s.gms                    # dynamic profile (data-driven mix of PV-aligned and off-peak)
├─ simultaneousSRE_E2M2s.gms               # simultaneous profile (fully PV-aligned)
└─ sweepingSRE_E2M2s.gms                   # sweeping profile (evenly distributed)
```

The model has not been pre-run and must be executed manually before analysis. Open one of the three run files (<kbd>dynamicSRE_E2M2s.gms</kbd>, <kbd>simultaneousSRE_E2M2s.gms</kbd>, or <kbd>sweepingSRE_E2M2s.gms</kbd>) depending on the rebound profile you want to simulate. Before execution, adjust the input and output paths defined at the beginning of the selected file. Replace the placeholder values of <code>PATH_IN_DATA</code> and <code>PATH_OUT</code> with the full paths to your local <kbd>Input/</kbd> and <kbd>Output/</kbd> directories:

```text
gams
$SETGLOBAL PATH_IN_DATA C:\...\Input
$SETGLOBAL PATH_OUT C:\...\Output
```

### Full reproducibility (all SRE scenarios)
To locate the specific model adjustments, search the code (Ctrl+F) for keywords such as <code>SRE</code> or the author’s initials <code>MD</code>. The model uses predefined settings for the effect strength to be simulated. To activate a specific value, remove the asterisk <code>*</code> in front of the corresponding lines (253–256). For example, to simulate a scenario with 7.7% SRE, remove the asterisks before line 254:

```text
gams
*SRE_effect_strength /0/
SRE_effect_strength /0.077/
*SRE_effect_strength /0.172/
*SRE_effect_strength /0.33/
```

The value <code>/0/</code> can be used for the reference scenario/baseline run without rebound in <kbd>simultaneousSRE_E2M2s.gms</kbd> or <kbd>sweepingSRE_E2M2s.gms</kbd>. The baseline run should not be performed with <kbd>dynamicSRE_E2M2s.gms</kbd>. On a machine that meets the recommended system requirements, the full model run should be completed in about an hour.

### Inspecting results
Once the model run completes, all results are written to the <kbd>Output/</kbd> directory in GDX format. The visualizations used in the paper can be reproduced with the Python materials in the <kbd>Supplementary material/</kbd> folders; geospatial figures include the necessary shapefiles and a <kbd>QGIS</kbd> project. For quick spreadsheet analysis, a curated summary of all results is available in <kbd>Supplementary material/Final_results_SRE.xlsx</kbd>.

### License and citation
The contents of this repository are made available under the MIT license. For details, see the LICENSE file in the main branch. If you use this code or data in academic work, please cite the associated SRE paper once it is published.
