import random
import functools
import yices
import time
import psutil

def get_memory_usage():
    process = psutil.Process()
    memory_usage = process.memory_info().rss
    return memory_usage

def factor(n):
    cfg = yices.Config()
    ctx = yices.Context(cfg)

    in1 = yices.new_variable(ctx)
    in2 = yices.new_variable(ctx)
    out = yices.new_variable(ctx)

    yices.assert_formula(ctx, yices.arith_eq_atom(out, yices.integer(n)))
    yices.assert_formula(ctx, yices.arith_eq_atom(yices.mul(in1, in2), out))
    yices.assert_formula(ctx, yices.arith_gt_atom(in1, yices.integer(1)))
    yices.assert_formula(ctx, yices.arith_gt_atom(in2, yices.integer(1)))

    if yices.check_context(ctx, None) == yices.lbool_false:
        return [n]

    m = yices.get_model(ctx, False)
    in1_n = yices.get_int_value(m, in1)
    in2_n = yices.get_int_value(m, in2)

    rt = sorted(factor(in1_n) + factor(in2_n))
    assert functools.reduce(lambda x, y: x * y, rt, 1) == n
    return rt

total_start_time = time.time()
for i in range(1, 1000):
    start_time = time.time()
    factors = factor(i)
    end_time = time.time()
    print(factors)
    print(f"Running time for range 1 to {i}: {end_time - start_time:.2f} seconds")
    # Print memory usage
    print(f"Memory usage for range 1 to {i}: {get_memory_usage()} bytes")

total_end_time = time.time()
print("Total running time:", total_end_time - total_start_time, "seconds")
