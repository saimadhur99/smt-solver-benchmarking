import random, functools
from z3 import *
from operator import mul
import time
import psutil

def get_memory_usage():
    process = psutil.Process()
    memory_usage = process.memory_info().rss
    return memory_usage

def factor(n):
    #print ("factoring",n)

    in1,in2,out=Ints('in1 in2 out')

    s=Solver()
    s.add(out==n)
    s.add(in1*in2==out)
    # inputs cannot be negative and must be non-1:
    s.add(in1>1)
    s.add(in2>1)

    if s.check()==unsat:
        #print (n,"is prime (unsat)")
        return [n]
    if s.check()==unknown:
        #print (n,"is probably prime (unknown)")
        return [n]

    m=s.model()
    # get inputs of multiplier:
    in1_n=m[in1].as_long()
    in2_n=m[in2].as_long()

    #print ("factors of", n, "are", in1_n, "and", in2_n)
    # factor factors recursively:
    rt=sorted(factor (in1_n) + factor (in2_n))
    # self-test:
    assert functools.reduce(mul, rt, 1)==n
    return rt

# infinite test:
def test():
    while True:
        print (factor (random.randrange(1000000000)))

#test()
total_start_time = time.time()
for i in range(1,1000):
 start_time = time.time()
 factors=factor(i)
 end_time = time.time()
 print(factors)
 print(f"Running time for range 1 to {i}: {end_time - start_time:.2f} seconds")
    # Print memory usage
 print(f"Memory usage for range 1 to {i}: {get_memory_usage()} bytes")

total_end_time = time.time()
print("Total running time:", total_end_time - total_start_time, "seconds")
