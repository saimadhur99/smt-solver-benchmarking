import os
from ctypes import CDLL

# Path to the libyices.dll file using a raw string to handle backslashes correctly
dll_path = r"C:\\Users\\Sai Madhur\\Downloads\\yices-2.6.4-x86_64-pc-mingw32-static-gmp\\yices-2.6.4\bin\\libyices.dll"

# Load the DLL using its full path
libyices = CDLL(dll_path)
import yices
import time
import psutil

# Define a function to get current memory usage
def get_memory_usage():
    process = psutil.Process()
    memory_usage = process.memory_info().rss
    return memory_usage

def setup_hanoi_problem(num_disks):
    num_steps = 2 ** num_disks - 1
    rods = [[[yices.Terms.new_uninterpreted_term(yices.Types.bool_type()) for _ in range(3)] for _ in range(num_disks)] for _ in range(num_steps)]
    config = yices.Config()
    config.default_config_for_logic('QF_BV')
    context = yices.Context(config)

    # Initial and goal states
    for disk in range(num_disks):
        context.assert_formula(rods[0][disk][0])
        context.assert_formula(yices.Terms.not_(rods[0][disk][1]))  # use not_ if it's the correct method
        context.assert_formula(yices.Terms.not_(rods[0][disk][2]))
        context.assert_formula(rods[-1][disk][2])
        context.assert_formula(yices.Terms.not_(rods[-1][disk][0]))
        context.assert_formula(yices.Terms.not_(rods[-1][disk][1]))

    # Rules and constraints
    for step in range(num_steps):
        for rod in range(3):
            for disk in range(num_disks):
                context.assert_formula(yices.Terms.or3(rods[step][disk][0], rods[step][disk][1], rods[step][disk][2]))
            for disk1 in range(num_disks):
                for disk2 in range(disk1 + 1, num_disks):
                    context.assert_formula(yices.Terms.implies(rods[step][disk2][rod], rods[step][disk1][rod]))
        if step > 0:
            changes = [yices.Terms.ite(yices.Terms.neq(rods[step-1][disk][rod], rods[step][disk][rod]), 1, 0) for disk in range(num_disks) for rod in range(3)]
            context.assert_formula(yices.Terms.eq(yices.Terms.sum(changes), 2))

    return context

def benchmark_hanoi(num_disks):
    context = setup_hanoi_problem(num_disks)
    start_time = time.time()
    result = context.check_context()
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Get memory usage
    memory_usage = get_memory_usage()

    return result, elapsed_time, memory_usage

# Running the benchmark
max_disks = 6
results = []
for num_disks in range(1, max_disks + 1):
    result, time_taken, memory_usage = benchmark_hanoi(num_disks)
    results.append((num_disks, result, time_taken, memory_usage))

for num_disks, result, time_taken, memory_usage in results:
    print(f"Number of disks: {num_disks}, Result: {'SAT' if result.is_sat() else 'UNSAT'}, Time taken: {time_taken:.4f}s")
    print(f"Memory usage: {memory_usage} bytes")
