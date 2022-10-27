from nvitop import ResourceMetricCollector
import time

from logging.handlers import MemoryHandler, TimedRotatingFileHandler, WatchedFileHandler
import logging

lh = logging.getLogger()

def getGraphicsCardUsage(snapshot):
    out = []
    for device in snapshot.devices:
      out.append(f"{device.physical_index},{device.memory_used},{device.memory_free},{device.memory_total},\"{device.performance_state}\",{device.power_usage},{device.gpu_utilization}")
    return lh.makeRecord("", 10, "", 10, '\n'.join(out), [], "")

file_handler = TimedRotatingFileHandler("usage.csv", backupCount=10000, when='W0')
x = ResourceMetricCollector()

while True:
    g = x.take_snapshots()
    data = getGraphicsCardUsage(g)
    file_handler.emit(data)
    # ... output
    time.sleep(300)

