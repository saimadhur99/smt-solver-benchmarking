from z3 import *
import time
import psutil

def towers_of_hanoi_z3(num_disks):
    # Create a solver instance
    solver = Solver()
    # We need to represent states and transitions, let's define the number of steps
    # Typically the minimum number of moves required is 2^n - 1
    num_steps = 2 ** num_disks - 1

    # Define the state variable: rod[i][j] means disk j is at rod i at step j
    rods = [[[Int(f'rod_{step}{disk}{rod}') for rod in range(3)] for disk in range(num_disks)] for step in range(num_steps)]

    # Initial state: all disks are on rod 0
    for disk in range(num_disks):
        solver.add(rods[0][disk][0] == 1)  # 1 means present
        solver.add(rods[0][disk][1] == 0)  # 0 means absent
        solver.add(rods[0][disk][2] == 0)

    # Goal state: all disks are on rod 2
    for disk in range(num_disks):
        solver.add(rods[-1][disk][2] == 1)
        solver.add(rods[-1][disk][0] == 0)
        solver.add(rods[-1][disk][1] == 0)

    # Validity constraints for each step
    for step in range(num_steps):
        for rod in range(3):
            # Each disk is on exactly one rod
            for disk in range(num_disks):
                solver.add(Sum([rods[step][disk][r] for r in range(3)]) == 1)

            # No disk can be placed on top of a smaller disk
            for disk1 in range(num_disks):
                for disk2 in range(disk1 + 1, num_disks):
                    # If disk2 is on this rod, then all disks smaller than disk2 must also be on this rod below it
                    solver.add(Implies(rods[step][disk2][rod] == 1, rods[step][disk1][rod] == 1))

        # Move constraints: only one disk can be moved at a time
        if step > 0:
            # Count changes from the previous state
            changes = []
            for disk in range(num_disks):
                for rod in range(3):
                    changes.append(If(rods[step-1][disk][rod] != rods[step][disk][rod], 1, 0))
            solver.add(Sum(changes) == 2)  # since a disk move will change two states (from and to)

    # Measure the time and memory consumption before solving
    start_time = time.time()
    start_memory = psutil.Process().memory_info().rss

    # Check if the solver can find a solution
    if solver.check() == sat:
        m = solver.model()
        # Measure the time and memory consumption after solving
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss

        # Print solution in a readable way
        for step in range(num_steps):
            print(f"Step {step+1}:")
            for rod in range(3):
                print(f"Rod {rod+1}: ", end="")
                for disk in range(num_disks):
                    if m.evaluate(rods[step][disk][rod]).as_long() == 1:
                        print(disk+1, end=" ")
                print()
        
        # Calculate the number of steps
        num_steps = (2 ** num_disks) - 1

        # Print performance metrics
        print(f"Number of steps: {num_steps}")
        print(f"Time taken: {end_time - start_time:.6f} seconds")
        print(f"Memory consumption: {end_memory - start_memory} bytes")
    else:
        print("No solution found")

# Example: 3 disks
towers_of_hanoi_z3(5)
