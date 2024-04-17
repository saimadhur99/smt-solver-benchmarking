import os
import psutil
import time
from ctypes import CDLL

# Path to the libyices.dll file
dll_path = r"C:\\Users\\nehak\\Downloads\\yices-2.6.4-x86_64-pc-mingw32-static-gmp (1)\\yices-2.6.4\\bin\\libyices.dll"

# Load the Yices DLL
libyices = CDLL(dll_path)

from yices import *

def get_memory_usage():
    process = psutil.Process()
    memory_usage = process.memory_info().rss
    return memory_usage

def is_palindrome(s):
    n = len(s)
    ctx = Context()
    
    # Define terms for the characters of the string
    term_dict = {}
    for i, char in enumerate(s):
        term_dict[char] = Terms.new_uninterpreted_term(Types.int_type(), f"char_{i}")
        ctx.assert_formula(Terms.arith_eq_atom(term_dict[char], Terms.integer(ord(char))))

    # Check if the string is a palindrome
    for i in range(n // 2):
        ctx.assert_formula(Terms.arith_eq_atom(term_dict[s[i]], term_dict[s[n - i - 1]]))
    
    # Check satisfiability
    result = ctx.check_context()
    
    # Dispose context
    ctx.dispose()
    
    # Return True if the string is a palindrome, False otherwise
    return result == Status.SAT

def measure_time_and_memory(test_strings):
    for test_string in test_strings:
        start_time = time.time()
        start_memory = get_memory_usage()
        result = is_palindrome(test_string)
        end_time = time.time()
        end_memory = get_memory_usage()
        
        time_taken = end_time - start_time
        memory_used = end_memory - start_memory
        
        print(f"'{test_string}' is a palindrome: {result}")
        print(f"Time taken: {time_taken:.6f} seconds")
        print(f"Memory used: {memory_used} bytes\n")

# Test the function with multiple strings
test_strings = ["radar", "hello", "level", "algorithm", "stats", "deified"]
measure_time_and_memory(test_strings)
