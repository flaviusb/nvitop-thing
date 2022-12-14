# nvitop-thing
A small script for writing out gpu usage data using nvitop

## To install this

```bash
git clone https://github.com/flaviusb/nvitop-thing.git
cd nvitop-thing
virtualenv foo
. foo/bin/activate
pip3 install --upgrade nvitop
```

Then, later, to run you can run:

```bash
cd nvitop-thing
. foo/bin/activate
python3 logging-script-thing.py
```

## Output format

The script outputs two sets of csv data interleaved into log files. The log files are rotated weekly. The default base filename is `usage.csv`.

The two formats are

```csv
"PhysicalGPU",unix time,device.physical_index,device.memory_used,device.memory_free,device.memory_total,\"device.performance_state\",device.power_usage,device.gpu_utilization
```

and

```csv
"Process",unix time,process.username,process.name,process.elapsed_time_in_seconds,process.gpu_time,process.gpu_sm_utilization,process.gpu_memory_utilization()
```

And so you can filter based on whether the first cell is `PhysicalGPU` or `Process`.
