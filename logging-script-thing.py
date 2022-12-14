from nvitop import ResourceMetricCollector
import time

from logging.handlers import MemoryHandler, TimedRotatingFileHandler, WatchedFileHandler
import logging

lh = logging.getLogger()

def getGraphicsCardUsage(snapshot, t):
    out = []
    for device in snapshot.devices:
      out.append(f"PhysicalGPU,{t},{device.physical_index},{device.memory_used},{device.memory_free},{device.memory_total},\"{device.performance_state}\",{device.power_usage},{device.gpu_utilization}")
    for process in snapshot.gpu_processes:
      out.append(f"Process,{t},{process.username},{process.name},{process.elapsed_time_in_seconds},{process.gpu_time},{process.gpu_sm_utilization},{process.gpu_memory_utilization}")
    return lh.makeRecord("", 10, "", 10, '\n'.join(out), [], "")

file_handler = TimedRotatingFileHandler("usage.csv", backupCount=10000, when='W0')
x = ResourceMetricCollector()

while True:
    g = x.take_snapshots()
    t = time.time()
    data = getGraphicsCardUsage(g, t)
    file_handler.emit(data)
    # ... output
    time.sleep(300)

