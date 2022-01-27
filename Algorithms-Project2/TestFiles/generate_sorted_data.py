#!/usr/bin/env python3

import sys

n = int(sys.argv[1])

with open(f'SortedInput{n}.txt', 'w') as fout:
    for i in range(n):
        fout.write(f'{i}\n')
