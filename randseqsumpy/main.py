import timeit
from seqsum_threader import Seqsum_threader

def run(THREADS):
    threader = Seqsum_threader(10, 100, 100, THREADS)
    threader.run(blocking=True)

print(timeit.timeit(lambda: run(1), number=1000))
print(timeit.timeit(lambda: run(10), number=1000))
print(timeit.timeit(lambda: run(100), number=1000))
