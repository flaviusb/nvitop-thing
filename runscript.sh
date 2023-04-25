#!/bin/bash
running() {
  ps -C python3 -o args= | grep --quiet "logging-script-thing.py"
}
if running
then
  echo Already running
else
  scl enable python3.7 ./runscript2.sh
fi

