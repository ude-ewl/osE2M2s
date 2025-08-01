### System requirements

To run the model, you need GAMS version 40.1 or higher. It was tested with a CPLEX license, but any solver capable of handling linear problems should work. Python (version 3.9 or higher) is only required for post-processing and visualization, available in the <kbd>SRE_Results&Figures.rar</kbd> file. The Python packages used include <kbd>pandas</kbd>, <kbd>matplotlib</kbd>, and <kbd>gdxpds</kbd>. For smooth execution, at least 8 GB of RAM and 4 CPU cores are recommended.

### Folder layout

The main driver file is named <kbd>E2M2s-SRE_run.gms</kbd> and located in the <kbd>E2M2s_RunModel&InputData_SRE.rar</kbd>. All input data is organized under the folder “Input”, which includes parameter files and structural definitions. After execution, the model automatically creates an “Output” that contains raw output files in GDX format.

### Quick start (demo)

To run a quick test, first clone the GitHub repository. Then extract the archive <kbd>E2M2s_RunModel&InputData_SRE.rar</kbd> and open the folder <kbd>model_SREinE2M2s</kbd>, which contains the main model file <kbd>E2M2s-SRE_run.gms</kbd>. 

```text
model_SREinE2M2s/
├─ E2M2s-SRE_run.gms        # main driver
├─ Input/
│  ├─ Inc_database/         # parameter *.inc files (costs, demand, …)
│  └─ inc_structure/        # set & parameter declarations
└─ Output/                  # gets created after running the model
   ├─ GDX/                  # raw output (*.gdx)
```

The model has not been pre-run and must be executed manually before analysis. Before running, you have to adjust the input and output paths at the beginning of the file <kbd>E2M2s-SRE_run.gms</kbd>. Specifically, replace the placeholder paths assigned to the variables PATH_IN_DATA and PATH_OUT with the full paths to your local input and output directories.

```text
gams
$SETGLOBAL PATH_IN_DATA C:\###...\Input
$SETGLOBAL PATH_OUT C:\###...\Output
```

### Full reproducibility (all SRE scenarios)

The model uses predefined settings for the strength and timing of the SRE. To activate a specific scenario, you must remove the asterisk (*) in front of the corresponding lines in the parameter block:

```text
gams
*SRE_effect_strength /0.0660/
*share_simSRE /1/
*share_sweSRE /0/
```
For example, to simulate a scenario with 6.6% rebound concentrated during midday (Simultaneous), remove the asterisks before these lines. Only one SRE scenario should be active at a time.

### Inspecting results

Once the model run completes successfully, all output data will be available in the “Output” directory. To generate the visualizations as used in the paper, Python scripts are provided in the repository. All results presented in the paper are also provided in a descriptively prepared form in the <kbd>SRE_Results&Figures.rar</kbd>, including shapefiles for the geospatial visualizations.

### Licence and citation

The contents of this forekd repository are made available under the MIT license. For details, refer to the LICENSE file in the main directory.
