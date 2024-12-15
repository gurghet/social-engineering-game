#!/bin/bash

# wait-for.sh - Wait for a service to be ready
# Usage: ./wait-for.sh [options] <host:port>[:http[s]:/path] [-- command args]
#   -t TIMEOUT  Timeout in seconds, zero for no timeout, default: 60
#   -s         Only execute subcommand if the test succeeds
#   -- COMMAND ARGS   Execute command with args after the test finishes

TIMEOUT=60
QUIET=0
PROTOCOL="http"
HEALTH_CHECK=1
HEALTH_PATH=""

usage() {
  echo "Usage: $0 [options] <host:port>[:http[s]:/path] [-- command args]"
  echo "  -q      Quiet mode"
  echo "  -t TO   Timeout in seconds, zero for no timeout, default: $TIMEOUT"
  echo "  -s      Only execute subcommand if the test succeeds"
  echo "  -- CMD  Execute command with args after the test finishes"
  exit 1
}

wait_for() {
  local wait_host=$1
  local wait_port=$2
  local protocol=$3
  local health_path=$4
  
  if [ "$TIMEOUT" -gt 0 ]; then
    echo "Waiting up to $TIMEOUT seconds for $wait_host:$wait_port to be ready..."
  else
    echo "Waiting for $wait_host:$wait_port to be ready without timeout"
  fi

  WAIT_START=$(date +%s)

  while :; do
    if [ -z "$health_path" ]; then
      echo "Error: Health check path is required"
      return 1
    fi
    
    # Always do HTTP health check
    HEALTH_URL="$protocol://$wait_host:$wait_port$health_path"
    echo "Checking health endpoint: $HEALTH_URL"
    curl --silent --fail "$HEALTH_URL" >/dev/null 2>&1
    result=$?
      
    if [ $result -eq 0 ]; then
      if [ $QUIET -eq 0 ]; then
        echo "Service at $wait_host:$wait_port is ready!"
      fi
      WAIT_END=$(date +%s)
      WAIT_TIME=$((WAIT_END-WAIT_START))
      echo "Waited for $WAIT_TIME seconds"
      return 0
    fi
    
    NOW=$(date +%s)
    ELAPSED=$((NOW-WAIT_START))
    
    if [ "$TIMEOUT" -gt 0 -a $ELAPSED -ge "$TIMEOUT" ]; then
      echo "Timeout occurred after $TIMEOUT seconds waiting for $wait_host:$wait_port"
      return 1
    fi
    sleep 1
  done
}

while getopts ":qst:" opt; do
  case $opt in
    q) QUIET=1 ;;
    s) STRICT=1 ;;
    t) TIMEOUT=$OPTARG ;;
    *) usage ;;
  esac
done

shift $((OPTIND-1))

if [ "$#" -eq 0 ]; then
  usage
fi

ADDR=$1
shift

# Parse host:port[:protocol://path]
if [[ $ADDR =~ ^([^:]+):([0-9]+)(:https?://.+)?$ ]]; then
  HOST=${BASH_REMATCH[1]}
  PORT=${BASH_REMATCH[2]}
  if [ -n "${BASH_REMATCH[3]}" ]; then
    HEALTH_PATH=${BASH_REMATCH[3]:1}  # Remove leading colon
    PROTOCOL=${HEALTH_PATH%%://*}
    HEALTH_PATH=${HEALTH_PATH#*://}
  fi
else
  echo "Error: Invalid address format. Use host:port or host:port:http[s]://path"
  usage
fi

if [ "$#" -gt 0 -a "$1" = "--" ]; then
  shift
  CLI="$@"
fi

wait_for "$HOST" "$PORT" "$PROTOCOL" "$HEALTH_PATH"
RESULT=$?

if [ "$CLI" != "" ]; then
  if [ $RESULT -ne 0 -a $STRICT -eq 1 ]; then
    echo "Failed to connect to $HOST:$PORT, exiting..."
    exit $RESULT
  fi
  exec $CLI
fi

exit $RESULT
