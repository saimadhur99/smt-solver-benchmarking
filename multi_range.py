from z3 import *
import time
import psutil

# Define a function to get current memory usage
def get_memory_usage():
    process = psutil.Process()
    memory_usage = process.memory_info().rss
    return memory_usage

# Define a function to find the multiplicative inverse for a given range
def find_multiplicative_inverse(start, end):
    # Define a solver
    solver = Solver()

    # Declare integer variable
    x = Int('x')

    # Iterate over numbers in the specified range
    for i in range(start, end + 1):
        # Reset the solver before adding new constraints
        solver.reset()
        # Add constraint: x * i == 1
        solver.add(x * i == 1)
        # Check if there is a solution
        if solver.check() == sat:
            # Get the model
            model = solver.model()
            # Print multiplicative inverse
            # print(f"Multiplicative inverse of {i} is {model[x].as_long()}")
        else:
            # print(f"No solution for {i}")
            pass

# Start recording total running time
total_start_time = time.time()

# Iterate over ranges from 1 to 1000
for end in range(10, 1001, 50):
    start_time = time.time()
    # Find multiplicative inverses for the current range
    find_multiplicative_inverse(1, end)
    end_time = time.time()
    # Calculate and print the running time for the current range
    print(f"Running time for range 1 to {end}: {end_time - start_time:.2f} seconds")
    # Print memory usage
    print(f"Memory usage for range 1 to {end}: {get_memory_usage()} bytes")

# Calculate and print the total running time
total_end_time = time.time()
print("Total running time:", total_end_time - total_start_time, "seconds")
