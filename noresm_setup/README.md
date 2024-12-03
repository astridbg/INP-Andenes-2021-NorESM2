# Setup of the NorESM model runs

The model runs in this study have been produced using the second generation of the Norwegian Earth System Model (NorESM2), release 2.0.3 (https://github.com/NorESMhub/NorESM/tree/release-noresm2.0.3), see Seland et al. (2020).

### To reproduce these model runs, one must clone the git repository https://github.com/astridbg/NorESM into one's home directory. 

After doing so, the baseline case using the Meyers' (1992) parameterization can be set up and run using the script **setup_case_M92.sh** in this folder.
The case with the updated parameterization based on INP observations from Andenes can be set up and run using the script **setup_case_A21.sh** in this folder.

The modifications to the model sourcecode can be found in the folder **setup**, under **M92** for the baseline case and **A21** for the updated parameterization.
Both model runs include sourcecode modifications described in Shaw et al. (2022) and Hofer et al. (2024), including the parameterization update.


## Referances

Seland, Ø., Bentsen, M., Olivié, D., Toniazzo, T., Gjermundsen, A., Graff, L. S., Debernard, J. B., Gupta, A. K., He, Y.-C., Kirkevåg,
A., Schwinger, J., Tjiputra, J., Aas, K. S., Bethke, I., Fan, Y., Griesfeller, J., Grini, A., Guo, C., Ilicak, M., Karset, I. H. H., Landgren, 
O., Liakka, J., Moseid, K. O., Nummelin, A., Spensberger, C., Tang, H., Zhang, Z., Heinze, C., Iversen, T., and Schulz, M.: Overview
of the Norwegian Earth System Model (NorESM2) and key climate response of CMIP6 DECK, historical, and scenario simulations,
Geoscientific Model Development, 13, 6165–6200, https://doi.org/10.5194/gmd-13-6165-2020, 2020.

Shaw, J., McGraw, Z., Bruno, O., Storelvmo, T., & Hofer, S. (2022). Using satellite observations to evaluate model microphysical representation of Arctic mixed-phase clouds. Geophysical Research Letters, 49, e2021GL096191. https://doi.org/10.1029/2021GL096191 

Hofer, S., Hahn, L.C., Shaw, J.K. et al. Realistic representation of mixed-phase clouds increases projected climate warming. Commun Earth Environ 5, 390 (2024). https://doi.org/10.1038/s43247-024-01524-2
