source /sps/lsst/software/lsst_distrib/w_2018_08/loadLSST.bash
setup lsst_distrib
cd /sps/lsst/users/nchotard/drpexplorer
./runDRPE.py --drp /sps/lsst/data/clusters/workflow/weeklies/work/201749004/output &
export servers=`netstat -lnt | grep 127.0.0.1:1986`
while [[ $servers != *'127.0.0.1:1986'* ]]; do sleep 1; servers=`netstat -lnt | grep 127.0.0.1:1986`; echo $servers; done
firefox http://127.0.0.1:1986/ &
fg 1
