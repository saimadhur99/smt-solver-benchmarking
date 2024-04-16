import os
from ctypes import CDLL
from ctypes import c_int32, POINTER

# Path to the libyices.dll file using a raw string to handle backslashes correctly
dll_path = r"C:\\Users\\pavan\\Downloads\\yices-2.6.4-x86_64-pc-mingw32-static-gmp\\yices-2.6.4\\bin\\libyices.dll"

# Load the DLL using its full path
libyices = CDLL(dll_path)
from yices import *
import time
import psutil

def get_memory_usage():
    process = psutil.Process()
    memory_usage = process.memory_info().rss
    return memory_usage

def find_multiplicative_inverse(start, end):
    x = Terms.new_uninterpreted_term(Types.real_type(), 'x')
    for i in range(start, end + 1):
        ctx = Context()
        try:
            i_term = Terms.rational(i, 1)
            eq = Terms.arith_eq_atom(Terms.mul(x, i_term), Terms.rational(1,1))
            ctx.assert_formula(eq)
            if ctx.check_context() == Status.SAT:
                model = Model.from_context(ctx, keep_subst=True)
                value = model.get_float_value(x)  # Use get_double_value for real numbers
                print(f"Multiplicative inverse of {i} is {value}")
            else:
                print(f"No solution for {i}")
        finally:
            ctx.dispose()

total_start_time = time.time()
for end in range(10, 1001, 50):
    start_time = time.time()
    find_multiplicative_inverse(1, end)
    end_time = time.time()
    print(f"Running time for range 1 to {end}: {end_time - start_time:.2f} seconds")
    print(f"Memory usage for range 1 to {end}: {get_memory_usage()} bytes")
total_end_time = time.time()
print("Total running time:", total_end_time - total_start_time, "seconds")
