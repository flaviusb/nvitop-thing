# nvitop-thing
A small script for writing out gpu usage data using nvitop

## Requirements

This requires nvitop, which itself requires
- Python 3.7+
- NVIDIA Management Library (NVML)
- nvidia-ml-py
- psutil
- cachetools
- termcolor
- curses (with `libncursesw`)

## To install this

```bash
git clone https://github.com/flaviusb/nvitop-thing.git
cd nvitop-thing
python -m venv foo  # or you can use: virtualenv foo
. foo/bin/activate
pip3 install --upgrade nvitop
```

Then, later, to run you can run:

```bash
cd nvitop-thing
. foo/bin/activate
python3 logging-script-thing.py
```

The logging script can take a location to output the logfile to. For example:

```bash
cd nvitop-thing
. foo/bin/activate
python3 logging-script-thing.py /var/log/gpuusage/gpu-usage.log
```

## Output format

The script outputs three sets of csv data interleaved into log files. The log files are rotated weekly. The default base filename is `usage.csv`.

The three formats are

```csv
"PhysicalGPU",unix time,device.physical_index,device.memory_used,device.memory_free,device.memory_total,\"device.performance_state\",device.power_usage,device.gpu_utilization
```

and

```csv
"Process",unix time,process username,process name,process elapsed_time_in_seconds,process gpu_sm_utilization,process gpu_memory_utilization, process commandline
```

and

```csv
"User",unix time,process username,total gpu_memory_utilization,total gpu_sm_utilization
```

And so you can filter based on whether the first cell is `PhysicalGPU` or `Process` or `User`.

## Using the kicker maker

The kicker maker makes a script that you can run from a crontab, which will restart the logger if it has died.

The kicker maker can be run like so:

```shell
./mk-kicker.sh --base /program/location/nvitop-thing/ --venv nameOfVirtualenv --log /var/log/gpuusage/gpu-usage.log --python 3.9
```

which will try to run the logger from within `/program/location/nvitop-thing/`, using the venv inside that folder called `nameOfVirtualenv`, logging to `/var/log/gpuusage/gpu-usage.log`, and using pyton 3.9 and pip 3.9.

If your log location is somewhere only root can write to, then you will need to run the kicker script from the superuser's crontab.

The kicker is intended to be run a few times every hour from cron or equivalent; how often is up to you though. It causes minimal load when it runs, testing whether the logger is already running and exiting quickly if it is.
