import threading
import random
from math import ceil
import numpy as np
import random as rnd

from typing import Callable

def seqsum(nums, total):
  a = np.random.random(nums, )
  a = a/np.sum(a)*total

  a = np.round(a)

  error = total - np.sum(a)
  step = 1 if error > 0 else -1
  while error != 0:
    i = np.random.randint(nums)
    if a[i]+step < 0: continue
    a[i] += step
    error -= step

  assert np.sum(a) == total
  assert len(a) == nums

  return a

class Seqsum_threader():
  """
  Class that helps to parallelize the calculation of seqsum.
  """
  def __init__(self, nums: int, total: int, SAMPLES: int, THREADS: int, seqsum: Callable[[int, int], list] = seqsum):
    self.nums = int(nums)
    self.total = int(total)
    self.SAMPLES = int(SAMPLES)
    self.THREADS = int(THREADS)
    if SAMPLES % THREADS != 0:
      print(f"Actual number of samples will be {SAMPLES%THREADS} more than expected.")
    self.samples_per_thread = ceil(SAMPLES/THREADS)
    self.seqsum = seqsum
    self.seqs = []
    self.threads = (threading.Thread(target=self._repeater, args=()) for _ in range(THREADS))

  def run(self, blocking: bool = False) -> None:
    """
    Run all the threads.

    Parameters
    ----------
    blocking : bool
      If true, block until all the threads are finished.
    """
    for thread in self.threads:
      thread.start()
    if blocking:
      for thread in self.threads:
        thread.join()

  def _repeater(self):
    for _ in range(self.samples_per_thread):
      self.seqs.append(list(self.seqsum(self.nums, self.total)))

  def join(self):
    """
    Block until all the threads are finished.
    """
    for thread in self.threads:
      thread.join()

if __name__ == '__main__':
  seqsum_threader = Seqsum_threader(10, 100, 1000, 20)
  seqsum_threader.run(blocking=True)
  print(seqsum_threader.seqs)
