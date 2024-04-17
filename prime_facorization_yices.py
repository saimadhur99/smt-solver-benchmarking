import random
from operator import mul
from ctypes import CDLL
from ctypes import c_int32, POINTER

# Path to the libyices.dll file using a raw string to handle backslashes correctly
dll_path = r"C:\\Users\\pavan\\Downloads\\yices-2.6.4-x86_64-pc-mingw32-static-gmp\\yices-2.6.4\\bin\\libyices.dll"

# Load the DLL using its full path
libyices = CDLL(dll_path)
from yices import *
import psutil
import functools
import time
def get_memory_usage():
    process = psutil.Process()
    memory_usage = process.memory_info().rss
    return memory_usage


def factor(n):
    out = Terms.new_uninterpreted_term(Types.int_type(), "out")
    cfg = Config()
    cfg.default_config_for_logic("QF_UFLIA")
    ctx = Context(cfg)

    ctx.assert_formula(Terms.arith_eq_atom(out, Terms.integer(n)))

    factors = []
    for i in range(2, n + 1):
        while n % i == 0:
            factors.append(i)
            n //= i
        if n == 1:
            break

    ctx.dispose()
    cfg.dispose()

    return factors
# infinite test:
def test():
    while True:
        print(factor(random.randrange(1000000000)))

total_start_time = time.time()
for i in range(1, 1000):
    start_time = time.time()
    factors = factor(i)
    end_time = time.time()
    print(factors)
    print(f"Running time for range 1 to {i}: {end_time - start_time:.2f} seconds")
    # Print memory usage
    print(f"Memory usage for range 1 to {i}: {get_memory_usage()} bytes")

total_end_time = time.time()
print("Total running time:", total_end_time - total_start_time, "seconds")
