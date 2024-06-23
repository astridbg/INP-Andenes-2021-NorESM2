# INP-Andenes-2021-NorESM2
This repository contains code for processing observational Ice-Nucleating Particle (INP) data from Andenes 2021, and NorESM2 model data with constrained INPs

Authors: Astrid Bragstad Gjelsvik, Robert Oscar David, Tim Carlsen, Franziska Hellmuth, Zachary McGraw, Stefan Hofer and Trude Storelvmo

### Conda environment:
Run the command

conda env create --name envname --file=environment_INP-NorESM2.yml

to create the conda environment used in the writing of these scripts. 

### Datasets used:
The data sets produced for this study, both INP measurements and modelling results, can be found at https:
//doi.org/10.5281/zenodo.11617774. The CALIOP L2 data used to derive SLF metrics and the CERES EBAF data can be downloaded freely
at https://search.earthdata.nasa.gov/. The surface radiation flux can be downloaded freely at https://www.pangaea.de/. The ERA5 data used to
produce the back trajectories can be found at https://doi.org/10.24381/cds.bd0915c6. The surface air pressure observations in Andenes can be
downloaded from https://thredds.met.no/thredds/catalog/met.no/observations/surface/87110/178/catalog.html. The colormap from Crameri430
et al. (2020) was used when preparing the figures.

## Folders
- INP-observations: Contains files for processing INP observational data, and visualations
- calipso_comparison: Contains file for comparing cloud phase observed by CALIOP lidar and modelled by NorESM2 (author: Stefan Hofer)
- noresm_analysis: Contains files for analysing and visualizing NorESM2 model data
- noresm_setup: Contains the version details, source modifications and the namelist specifications for reproducing the NorESM2 runs
- radiation_comaprison: Contains files for comparing observed radiation fluxes and model data

