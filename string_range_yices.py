import os
from ctypes import CDLL

# Path to the libyices.dll file using a raw string to handle backslashes correctly
dll_path = r"C:\\Users\\Sai Madhur\\Downloads\\yices-2.6.4-x86_64-pc-mingw32-static-gmp\\yices-2.6.4\bin\\libyices.dll"

# Load the DLL using its full path
libyices = CDLL(dll_path)
from yices import *
import time
import psutil

def rabin_karp_search_yices(patterns, texts):
    results = []

    for pattern, text in zip(patterns, texts):
        n = len(text)
        m = len(pattern)
        result = []

        pattern_ascii = [ord(c) for c in pattern]
        text_ascii = [ord(c) for c in text]

        # Initialize Yices context
        ctx = Context()

        try:
            # Compute hash value for the pattern as a Yices term
            pattern_hash = Terms.integer(hash_string_yices(pattern_ascii))

            start_time = time.time()  # Start measuring runtime
            for i in range(n - m + 1):
                window_hash = Terms.integer(hash_string_yices(text_ascii[i:i+m]))
                ctx.push()
                ctx.assert_formula(Terms.arith_eq_atom(pattern_hash, window_hash))

                # Direct check without parameters
                if ctx.check() == Status.SAT:
                    if pattern_ascii == text_ascii[i:i+m]:
                        result.append(i)
                ctx.pop()

            end_time = time.time()  # Stop measuring runtime

        finally:
            ctx.dispose()  # Dispose of the context properly

        process = psutil.Process()
        memory_usage = process.memory_info().rss

        results.append((result, end_time - start_time, memory_usage))

    return results

def hash_string_yices(s):
    prime = 997
    h = 0
    for c in s:
        h = (h * 256 + c) % prime
    return h

# Example usage
patterns = ["abc", "def", "defghi", "klmnop"]
texts = ["abcdeabc", "defghdef", "aexcnkdefhimvjhjbk", "xgfdchvjklmnopgchvjh"]
results = rabin_karp_search_yices(patterns, texts)
for i, (matches, runtime, memory) in enumerate(results):
    print(f"Matches for pattern {i+1}: {matches}")
    print(f"Runtime for pattern {i+1}: {runtime} seconds")
    print(f"Memory usage for pattern {i+1}: {memory} bytes")
