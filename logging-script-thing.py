from nvitop import ResourceMetricCollector
import time

from logging.handlers import MemoryHandler, TimedRotatingFileHandler, WatchedFileHandler
import logging

import sys

lh = logging.getLogger()

out_location = "usage.csv"
if len(sys.argv) > 1:
  out_location = sys.argv[1]

import contextlib
import itertools
import math
import os
import threading
import time
from collections import OrderedDict, defaultdict
from typing import Callable, Generator, Iterable, NamedTuple, TypeVar
from weakref import WeakSet

from nvitop.api import host
from nvitop.api.device import CudaDevice, Device
from nvitop.api.process import GpuProcess, HostProcess

def getGraphicsCardUsage(snapshot, t):
    out = []
    users = {}
    for device in snapshot.devices:
      out.append(f"PhysicalGPU,{t},{device.physical_index},{device.memory_used},{device.memory_free},{device.memory_total},\"{device.performance_state}\",{device.power_usage},{device.gpu_utilization}")
      for process in device.real.processes().values():
          out.append(f"Process,{t},{process.username()},{process.name()},{process.elapsed_time_in_seconds()},{process.gpu_sm_utilization()},{process.gpu_memory_utilization()},{process.command()}")
          if users.get(process.username()) == None:
            users[process.username()] = (process.gpu_memory_utilization(), process.gpu_sm_utilization())
          else:
            mem, sm = users[process.username()]
            users[process.username()] = (mem + process.gpu_memory_utilization(), sm + process.gpu_sm_utilization())
    for user_name in users:
      user_mem, user_sm = users[user_name]
      out.append(f"User,{t},{user_name},{user_mem},{user_sm}")
    return lh.makeRecord("", 10, "", 10, '\n'.join(out), [], "")

file_handler = TimedRotatingFileHandler(out_location, backupCount=10000, when='W0')
x = ResourceMetricCollector()

while True:
    g = x.take_snapshots()
    t = time.time()
    data = getGraphicsCardUsage(g, t)
    file_handler.emit(data)
    # ... output
    time.sleep(300)

