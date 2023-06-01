#!/bin/bash
running() {
  ps -C python3 -o args= | grep --quiet "logging-script-thing.py"
}
if running
then
  echo Already running
else
  alias python3=python3.9
  alias pip3=pip3.9
  cd ~/nvitop-thing
  . foo/bin/activate
  python3 logging-script-thing.py /var/log/gpuusage/gpu-usage.log
fi

