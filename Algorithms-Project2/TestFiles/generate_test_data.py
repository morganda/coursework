#!/usr/bin/env python3

import random
import sys


MAX = 100000

n = int(sys.argv[1])
values = list()

# generate the points
for i in range(n):
    values.append(random.randint(0, MAX))

# shuffle the points for good measure
random.shuffle(values)

values_output = list()
for x in values:
    values_output.append(f'{x}')

# write test file
with open(f'TestInput{n}.txt', 'w') as fout:
    fout.write('\n'.join(values_output))
fout.close()
