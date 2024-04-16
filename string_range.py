from z3 import *
import time
import psutil


def rabin_karp_search(patterns, texts):
    results = []

    for pattern, text in zip(patterns, texts):
        n = len(text)
        m = len(pattern)
        result = []

        # Convert pattern and text to lists of ASCII values
        pattern_ascii = [ord(c) for c in pattern]
        text_ascii = [ord(c) for c in text]

        # Define Z3 solver
        solver = Solver()

        # Define Z3 integer variables
        pattern_hash = Int('pattern_hash')
        window_hash = Int('window_hash')

        # Compute hash value for the pattern
        solver.add(pattern_hash == hash_string(pattern_ascii))

        # Iterate over the text and check for matches
        start_time = time.time()  # Start measuring runtime
        for i in range(n - m + 1):
            # Compute hash value for the current window
            solver.add(window_hash == hash_string(text_ascii[i:i+m]))
            # Check if hash values match
            solver.add(window_hash == pattern_hash)
            # Check if the window content matches the pattern
            solver.add(If(window_hash == pattern_hash, text_ascii[i:i+m] == pattern_ascii, True))
            # Check if the constraints are satisfiable
            if solver.check() == sat:
                result.append(i)
        end_time = time.time()  # Stop measuring runtime

        # Measure memory usage
        process = psutil.Process()
        memory_usage = process.memory_info().rss

        results.append((result, end_time - start_time, memory_usage))

    return results

def hash_string(s):
    # Compute hash value using a simple polynomial hash function
    # (sum of ASCII values modulo a large prime)
    prime = 997  # Choose a large prime number
    h = 0
    for c in s:
        h = (h * 256 + c) % prime
    return h

# Example usage
patterns = ["abc", "def","defghi","klmnop"]
texts = ["abcdeabc", "defghdef","aexcnkdefhimvjhjbk","xgfdchvjklmnopgchvjh"]
results = rabin_karp_search(patterns, texts)
for i, (matches, runtime, memory) in enumerate(results):
    print(f"Matches for pattern {i+1}: {matches}")
    print(f"Runtime for pattern {i+1}: {runtime} seconds")
    print(f"Memory usage for pattern {i+1}: {memory} bytes")
