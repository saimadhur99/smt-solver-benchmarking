from z3 import *
import time
from memory_profiler import memory_usage

def is_palindrome(s):
    solver = Solver()

    # Define variables for each character in the string
    chars = [Int(f"char_{i}") for i in range(len(s))]

    # Add constraints for each character
    for i in range(len(s)):
        # Ensure characters are ASCII values
        solver.add(32 <= chars[i], chars[i] <= 126)
        # Add constraint that each character is equal to its corresponding character from the end of the string
        solver.add(chars[i] == ord(s[i]))
    
    # Check if the constraints are satisfiable
    if solver.check() == sat:
        model = solver.model()
        # Check if all characters at corresponding positions are equal
        for i in range(len(s) // 2):
            char_at_i = model[chars[i]].as_long()
            char_at_len_minus_i = model[chars[len(s) - 1 - i]].as_long()
            if char_at_i != char_at_len_minus_i:
                return False
        return True  # String is a palindrome
    else:
        return False  # String is not a palindrome


if __name__ == '__main__':
    # List of strings to test
    strings = ["abcdba", "abcdcba", "abccbaabccbaaaandmd", "abcdefghijkkjihgfedcba", "srghwrhrhwrbwrhbjwnfikbvwikbrkvbkwnskdnkv",
               "aaaaaaaaaaaaaaaaaaaaabbbbaaaaaaaaaaaaaaaaaaaaaaaaaa",
               "aaaaaaaaaaaaaaaaaaaabcdefghijkkjihgfedcbaaabbbbaaaaaaaaabccbaabccbaaaandmdaaaaaaaaaaaaaaaaaa",
               "aaaaaaaaaaaaaaaaaaaabcdefghijkkjihgfedcbaaabbbbaaaaaaaaabccbaabccbaaaandmdaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabcdefghijkkjihgfedcbaaabbbbaaaaaaaaabccbaabccbaaaandmdaaaaaaaaaaaaaaaaaa"
               ,"abcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcbaabcdcba"]

    for s in strings:
        print(f"\nTesting string: {s}")
        
        # Measure time
        start_time = time.time()
        result = is_palindrome(s)
        end_time = time.time()
        print("Is the string a palindrome?", result)
        print("Execution time:", end_time - start_time, "seconds")

        # Measure memory usage
        mem_usage = memory_usage((is_palindrome, (s,), {}))
        print("Memory usage:", max(mem_usage), "MB")
