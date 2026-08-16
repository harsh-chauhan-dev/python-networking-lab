import time
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parents[1]))

from generator.number import generate_numeric

def benchmark(length):
    total = 10 ** length

    start = time.perf_counter()

    count =0

    for _ in generate_numeric(length):
        count+=1

    elapsed = time.perf_counter()-start 
    speed = count/elapsed

    print("\n === Benchmark ===")
    print(f"Length:{length}") 
    print(f"Candidates:{count:,}") 
    print(f"Time:{elapsed:.4f} seconds") 
    print(f"Speed: {speed:,.2f} candidates/sec")


if __name__=="__main__":
    benchmark(6)
