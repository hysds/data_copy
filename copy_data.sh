#!/bin/bash

source $HOME/verdi/bin/activate

BASE_PATH=$(dirname "${BASH_SOURCE}")

# check args
if [ "$#" -eq 3 ]; then
  query=$1
  destination=$2
  rule_name=$3
  
else
  echo "Invalid number or arguments ($#) $*" 1>&2
  exit 1
fi

# find data location, localize them and transfer them to user selected destination
echo "##########################################" 1>&2
echo -n "Transferring Data: " 1>&2
date 1>&2
python $BASE_PATH/copy_data.py "$query" "$destination" "$rule_name" > copy_data.log 2>&1
STATUS=$?
echo -n "Finished with copying data: " 1>&2
date 1>&2
if [ $STATUS -ne 0 ]; then
  echo "Failed to copy data." 1>&2
  cat copy_data.log 1>&2
  exit $STATUS
fi
