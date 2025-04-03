from math import ceil
from z3 import Bools, Optimize, sat, Sum, PbLe
from random import randint, sample

k = 10000

usages = Bools(" ".join(f"use_code{i}" for i in range(k)))
values = [randint(0, k) for i in range(k)]

S = Sum([u * v for u, v in zip(usages, values, strict=True)])


optimizer = Optimize()

# exclusivity constraint
for _ in range(ceil(k / 100)):
    group = sample(usages, 5)
    optimizer.add(PbLe([(g, 1) for g in group], 1))

maximized = optimizer.maximize(S)

assert optimizer.check() == sat

m = optimizer.model()
print(m)
print("Value", maximized.value())
print("Using", m.eval(Sum(usages)), "codes")
