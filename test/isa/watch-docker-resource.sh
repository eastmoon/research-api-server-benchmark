# Declare variable
[ -n ${1} ] && EXECUTE_MODE=${1} || true
WATCHER_PID=/tmp/watcher.pid
WATCHER_LOG=/tmp/watcher.log

# Declare function
function run() {
    [ -e ${WATCHER_LOG} ] && rm ${WATCHER_LOG} || true
    while true; do
        docker stats --no-stream --format json | tee --append ${WATCHER_LOG} > /dev/null
        sleep 0.03
    done
}
# Execute script
case ${EXECUTE_MODE} in
  enable)
      run &
      echo $! | tee /tmp/watcher.pid > /dev/null
  ;;
  disable)
      if [ -e ${WATCHER_PID} ] && [ $(ps aux | grep $(cat ${WATCHER_PID}) | wc -l) -gt 0 ]; then
          kill -9 $(cat ${WATCHER_PID})
          rm ${WATCHER_PID}
      fi
  ;;
  *)
      echo "Unknown mode '${EXECUTE_MODE}'"
  ;;
esac
