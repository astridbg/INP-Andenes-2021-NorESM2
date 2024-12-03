
# INP-Andenes-2021-NorESM2
This repository contains code for processing observational Ice-Nucleating Particle (INP) data from Andenes 2021, and NorESM2 model data with constrained INPs

Authors: Astrid Bragstad Gjelsvik, Robert Oscar David, Tim Carlsen, Franziska Hellmuth, Zachary McGraw, Stefan Hofer and Trude Storelvmo
Contact: Astrid Bragstad Gjelsvik, astridbg@uio.no

### Conda environment:
Run the command

conda env create --name envname --file=environment_INP-NorESM2.yml

to create the conda environment used for processing these scripts. 

### Datasets used:
The data sets produced for this study, both INP measurements and modelling results, can be found at https:
//doi.org/10.5281/zenodo.11617774. The CALIOP L2 data used to derive SLF metrics and the CERES EBAF data can be downloaded freely
at https://search.earthdata.nasa.gov/. The derived SLF metrics can be found at 10.5281/zenodo.8289057. 
The surface radiation flux can be downloaded freely at https://www.pangaea.de/. The surface air pressure observations in Andenes can be
downloaded from https://thredds.met.no/thredds/catalog/met.no/observations/surface/87110/178/catalog.html. The colormap from Crameri
et al. (2020) was used when preparing the figures. All data not produced in this study, but used for producing the scripts, can also be provided by the authors upon request.

## Folders
- INP-observations: Contains scripts for producing **Fig. 2** (INP data and paramterization) and **Fig. A1** (INP freezing temperatures with aerosol data)
- calipso_comparison: Contains scripts for producing **Fig. 7**, comparing cloud phase observed by CALIOP lidar and modelled by NorESM2, similar to Shaw et al. (2022) and Hofer et al. (2024), and for producing **Fig. 8**, comparing CALIPSO-GOCCP cloud cover with model output
- noresm_analysis: Contains scripts for analysing and visualizing NorESM2 model data, i.e. **Fig. 3**, **Fig. 4**, **Fig. 5**, **Fig. 6**, **Fig. 9**, **Fig. 10**, **Fig. 11**, **Fig. 14**, **Fig. B1**, **Fig. B2**, **Fig. B3** and **Fig. B4**. The file **PostProcessing.py** has been used to postprocess the model data, for which the postprocessed data can be found at https:
//doi.org/10.5281/zenodo.11617774. 
- noresm_setup: Contains the sourcecode modifications and scripts for reproducing the NorESM2 runs
- radiation_comaprison: Contains files for comparing observed radiation fluxes and model data, i.e. **Fig. 12** and **Fig. 13**. 

## Referances

Shaw, J., McGraw, Z., Bruno, O., Storelvmo, T., & Hofer, S. (2022). Using satellite observations to evaluate model microphysical representation of Arctic mixed-phase clouds. Geophysical Research Letters, 49, e2021GL096191. https://doi.org/10.1029/2021GL096191

Hofer, S., Hahn, L.C., Shaw, J.K. et al. Realistic representation of mixed-phase clouds increases projected climate warming. Commun Earth Environ 5, 390 (2024). https://doi.org/10.1038/s43247-024-01524-2
