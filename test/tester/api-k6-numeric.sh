## Declare variable
export TESTCASE_NAME=numeric
export TARGET_SCRIPT=${PWD}/k6/${TESTCASE_NAME}.js
export ENV_DURATION=10s
export ENV_TIMES=1
for op in "${@}"; do
  [[ "${op}" =~ "--vue=" ]] && export ENV_VUS=$(echo ${op} | awk -F'=' '{print $2}')
  [[ "${op}" =~ "--duration=" ]] && export ENV_DURATION=$(echo ${op} | awk -F'=' '{print $2}')
  [[ "${op}" =~ "--server=" ]] && export ENV_SERVER=$(echo ${op} | awk -F'=' '{print $2}')
  [[ "${op}" =~ "--times=" ]] && export ENV_TIMES=$(echo ${op} | awk -F'=' '{print $2}')
done

## Declare function
function run() {
    vus=${1}
    times=${2}
    k6 run --duration "${ENV_DURATION}" --vus=${vus} ${TARGET_SCRIPT}
    if [ -e /tmp/summary.json ]; then
        if [ -z ${ENV_TIMES} ]; then
            mv /tmp/summary.json /tmp/summary-${TESTCASE_NAME}-${ENV_DURATION}-${vus}.json
        else
            mv /tmp/summary.json /tmp/summary-${TESTCASE_NAME}-${ENV_DURATION}-${vus}-${times}.json
        fi
    fi
}
## Execute script
#
if [ -e ${TARGET_SCRIPT} ]; then
    if [ -z ${ENV_VUS} ]; then
        for i in {1..10..1}; do
            run ${i} 1
        done
    else
        for ((i=1; i<=${ENV_TIMES}; i++)); do
            run ${ENV_VUS} ${i}
        done
    fi
else
    echo "${TARGET_SCRIPT} not find."
fi
