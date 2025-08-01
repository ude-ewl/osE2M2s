System requirements

To run the model, you need GAMS version 40.1 or higher. It was tested with a CPLEX license, but any solver capable of handling linear problems should work. Python (version 3.9 or higher) is only required for post-processing and visualization. The Python packages used include pandas, matplotlib, and gdxpds. For smooth execution, at least 8 GB of RAM and 4 CPU cores are recommended.

Folder layout

The main driver file is named E2M2s-SRE_run.gms and located in the E2M2s_RunModel&InputData_SRE.rar. All input data is organized under the folder “Input”, which includes parameter files and structural definitions. After execution, the model automatically creates an “Output” that contains raw output files in GDX format.

Quick start (demo)

To run a quick test, first clone the GitHub repository and navigate to the demo folder. Then extract the archive E2M2s_RunModel&InputData_SRE.rar and open the folder model_SREinE2M2s, which contains the main model file E2M2s-SRE_run.gms. 

Full reproducibility (all SRE scenarios)

Before running the model, you must manually adjust the input and output paths at the beginning of the file E2M2s-SRE_run.gms. Specifically, replace the placeholder paths assigned to the variables PATH_IN_DATA and PATH_OUT with the full paths to your local input and output directories.
Additionally, the model uses predefined settings for the strength and timing of the SRE. To activate a specific scenario, you must remove the asterisk (*) in front of the corresponding lines in the parameter block:

gams
*SRE_effect_strength /0.0660/
*share_simSRE /1/
*share_sweSRE /0/

For example, to simulate a scenario with 6.6% rebound concentrated during midday (Simultaneous), remove the asterisks before these lines. Only one SRE scenario should be active at a time.

Inspecting results

Once the model run completes successfully, all output data will be available in the “Output” directory. To generate the visualizations as used in the paper, Python scripts are provided in the repository. This script reads the model results and produces the figures in the required format and resolution.

Licence and citation

The contents of this forekd repository are made available under the MIT license. For details, refer to the LICENSE file in the main directory.
