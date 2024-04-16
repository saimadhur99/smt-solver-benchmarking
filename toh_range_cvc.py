from cvc5.pythonic import *
import time
import psutil

# Define a function to get current memory usage
def get_memory_usage():
    process = psutil.Process()
    memory_usage = process.memory_info().rss
    return memory_usage

def setup_hanoi_problem(num_disks):
    num_steps = 2 ** num_disks - 1
    rods = [[[Int(f'rod_{step}_{disk}_{rod}') for rod in range(3)] for disk in range(num_disks)] for step in range(num_steps)]

    solver = Solver()

    # Initial and goal states
    for disk in range(num_disks):
        solver.add(rods[0][disk][0] == 1)
        solver.add(rods[0][disk][1] == 0)
        solver.add(rods[0][disk][2] == 0)
        solver.add(rods[-1][disk][2] == 1)
        solver.add(rods[-1][disk][0] == 0)
        solver.add(rods[-1][disk][1] == 0)

    # Rules and constraints
    for step in range(num_steps):
        for rod in range(3):
            for disk in range(num_disks):
                solver.add(Sum([rods[step][disk][r] for r in range(3)]) == 1)

            for disk1 in range(num_disks):
                for disk2 in range(disk1 + 1, num_disks):
                    solver.add(Implies(rods[step][disk2][rod] == 1, rods[step][disk1][rod] == 1))

        if step > 0:
            changes = [If(rods[step-1][disk][rod] != rods[step][disk][rod], 1, 0) for disk in range(num_disks) for rod in range(3)]
            solver.add(Sum(changes) == 2)

    return solver

def benchmark_hanoi(num_disks):
    solver = setup_hanoi_problem(num_disks)
    start_time = time.time()
    result = solver.check()
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Accessing statistics directly as a string
    stats_str = str(solver.statistics())

    # Get memory usage
    memory_usage = get_memory_usage()

    return result, elapsed_time, stats_str, memory_usage

# Running the benchmark
max_disks = 6
results = []
for num_disks in range(1, max_disks + 1):
    result, time_taken, stats_str, memory_usage = benchmark_hanoi(num_disks)
    results.append((num_disks, result, time_taken, stats_str, memory_usage))

for num_disks, result, time_taken, stats_str, memory_usage in results:
    print(f"Number of disks: {num_disks}, Result: {result}, Time taken: {time_taken:.4f}s")
    print("Statistics:")
    print(stats_str)
    print(f"Memory usage: {memory_usage} bytes")
