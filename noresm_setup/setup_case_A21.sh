#!/bin/bash

cur_fld=$(pwd)

nor_repo=$HOME/NorESM
nor_ver=INP-Andenes21-study_v1

cam_repo=$nor_repo/components/cam
cam_ver=slf-output-namelist

cime_repo=$nor_repo/cime
cime_ver=betzy-2024-updates

casename=NF2000climo_f19_tn14_A21_20241125
sourcemod_repo=$cur_fld/setup/A21/SourceMods

#Remove dirs to rerun if previous run failed
rm -r ./$casename
rm -r $USERWORK/archive/$casename
rm -r $USERWORK/noresm/$casename

cd $nor_repo
git checkout $nor_ver
./manage_externals/checkout_externals

cd $cam_repo
git checkout $cam_ver

cd $cime_repo
git checkout $cime_ver

cd $cur_fld

$nor_repo/cime/scripts/create_newcase --case /cluster/projects/nn9600k/astridbg/cases/$casename --compset NF2000climo --res f19_tn14 --machine betzy --project nn9600k --run-unsupported

cd $casename
echo "CASE CREATED"

./case.setup

./xmlchange --append CAM_CONFIG_OPTS=--offline_dyn,CAM_CONFIG_OPTS=-cosp

./xmlchange CALENDAR=GREGORIAN

./xmlchange STOP_N=39,STOP_OPTION=nmonths

./xmlchange RUN_STARTDATE=2007-01-01

./xmlchange --subgroup case.run JOB_WALLCLOCK_TIME=12:00:00

iecho "XML CHANGES DONE"

# Update namelists

printf "  
&slfsimulator_nl
 slf_isotherms = .true.
&metdata_nl
 met_nudge_only_uvps = .true.
 met_data_file= '/cluster/shared/noresm/inputdata/noresm-only/inputForNudging/z_ABG/ERA_f19_tn14/2007-01-01.nc'
 met_filenames_list = '/cluster/shared/noresm/inputdata/noresm-only/inputForNudging/z_ABG/ERA_f19_tn14/fileList3.txt'
 met_rlx_time = 6
&cam_initfiles_nl
 bnd_topo = '/cluster/shared/noresm/inputdata/noresm-only/inputForNudging/ERA_f19_tn14/ERA_bnd_topo.nc'

&phys_ctl_nl
 use_hetfrz_classnuc = .false.

&cam_history_nl
 fincl1 ='NIMEY'

&cospsimulator_nl
 docosp         = .true.
 cosp_amwg      = .true.
/" >> user_nl_cam

# Update sourcecode modifications for CAM

cp -r $sourcemod_repo/src.cam/* SourceMods/src.cam/.

echo "SOURCEMODS UPDATED"

./case.build

./case.submit
