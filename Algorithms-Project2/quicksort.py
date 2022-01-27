#!/usr/bin/env python3

"""
Quicksort implementations using normal partitioning
and also using median of three partitioning. Uses
cprofile to compare function calls. Also prints out
the number of swaps that occur with each method.

Normal quicksort and the partitioning portions of this
code were derived from the psuedo-code in our textbook
in Chapter 7 section 1 (page 171).
"""

import math
import sys
import os
import cProfile

# adjusted to allow for more recursive calls
sys.setrecursionlimit(20000)

# count the number of swaps in each partitioning strategy
swaps = 0


def usage():
    """Simple CLI usage printout.
    """
    print(f'Usage: {sys.argv[0]} [test file]')
    print()
    print('Args:')
    print('\ttest file - input file of integers to sort')
    print('\t-p, --profile - [optional] count calls instead of results')
    exit(0)


def process_args():
    """A simple CLI args handler.

    Returns:
        Tuple: filename with integers and a boolean to use the profiler
    """
    filename = None
    profile = False
    if '-h' in sys.argv or '--help' in sys.argv:
        usage()
    if len(sys.argv) >= 3:
        if sys.argv[2] in ('--profile', '-p', '-p'):
            profile = True
        filename = sys.argv[1]
    elif len(sys.argv) >= 2:
        filename = sys.argv[1]
    else:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filename = f'{dir_path}/TestFiles/TestInput25.txt'
    return filename, profile


def get_input_array(filename):
    """Reads the data set into an array from a file

    Returns:
        List(int): a list of integers
    """
    array = list()
    with open(filename, 'r') as fin:
        for line in fin.readlines():
            array.append(int(line))
    return array


def median_of_three_pivot(array: list, start: int, end: int):
    """Selects the median of the 3 values at start, end, and
    a calculated mid index of array.

    Args:
        array (list): list of integers to partition
        start (int): starting index to partition
        end (int): last index to consider in the partition

    Returns:
        int: pivot index
    """
    mid = math.floor((start + end) / 2)

    # find median of array from these indices
    order_length = 3
    order = [start, mid, end]

    # insert sort over order
    for index in range(order_length):
        insertVal = order[index]
        insertPos = index
        while insertPos >= 0 and \
                array[order[insertPos - 1]] > array[insertVal]:
            order[insertPos] = order[insertPos - 1]
            insertPos -= 1
        order[insertPos] = insertVal
    # order[1] is the index of the median in my array between
    # indices start, mid, and end
    return order[1]


def median_of_three_partition(array: list, start: int, end: int):
    """[summary]

    Args:
        array (list): list of integers to partition
        start (int): starting index to partition
        end (int): last index to consider in the partition

    Returns:
        int: the index of the pivot for the subarry in [start, end]
    """

    global swaps

    pivot = median_of_three_pivot(array, start, end)
    # swap end and pivot
    array[end], array[pivot] = array[pivot], array[end]
    pivot = end

    lower = start - 1
    higher = start

    # partition
    while higher < end:
        if array[higher] <= array[pivot]:
            lower += 1
            array[lower], array[higher] = array[higher], array[lower]
            swaps += 1
        higher += 1

    # swap pivot to the mid point
    array[lower + 1], array[end] = array[end], array[lower + 1]
    return lower + 1


def quicksort_mot(array: list, start: int, end: int):
    """[summary]

    Args:
        array (list): list of integers to partition
        start (int): starting index to partition
        end (int): last index to consider in the partition
    """
    if start < end:
        partition = median_of_three_partition(array, start, end)
        quicksort_mot(array, start, partition - 1)
        quicksort_mot(array, partition + 1, end)


def vanilla_partition(array: list, start: int, end: int):
    """Normal partition for quicksort which selects end
    as the pivot.

    Args:
        array (list): list of integers to partition
        start (int): starting index to partition
        end (int): last index to consider in the partition

    Returns:
        int: the index of the pivot for the subarry in [start, end]
    """

    global swaps

    pivot = end
    lower = start - 1
    higher = start

    # partition
    while higher < end:
        if array[higher] <= array[pivot]:
            lower += 1
            array[lower], array[higher] = array[higher], array[lower]
            swaps += 1
        higher += 1

    # swap pivot to the mid point
    array[lower + 1], array[end] = array[end], array[lower + 1]
    return lower + 1


def quicksort_vanilla(array: list, start: int, end: int):
    """Normal quicksort method

    Args:
        array (list): list of integers to partition
        start (int): starting index to partition
        end (int): last index to consider in the partition
    """
    if start < end:
        partition = vanilla_partition(array, start, end)
        quicksort_vanilla(array, start, partition - 1)
        quicksort_vanilla(array, partition + 1, end)


def write_results(filename, unsorted_array, array, strategy):

    output = 'Input\n\n'
    nums_str = [str(num) for num in unsorted_array]
    unsorted_as_str = ', '.join(nums_str)
    output = f'{output}{unsorted_as_str}\n\n'

    output = f'{output}Output:\n\n'
    nums_str = [str(num) for num in array]
    sorted_as_str = ', '.join(nums_str)
    output = f'{output}{sorted_as_str}\n\nSwaps: {swaps}'

    inputDescription = os.path.basename(filename).split('.')[0]
    outfile = f'SampleTestResults/TestResult-{inputDescription}-{strategy}.txt'
    with open(outfile, 'w') as fout:
        fout.writelines(output)


if __name__ == '__main__':

    filename, profile = process_args()
    array = get_input_array(filename)
    unsorted_array = array.copy()
    if profile:
        cProfile.run('quicksort_mot(array, 0, len(array) - 1)')
    else:
        quicksort_mot(array, 0, len(array) - 1)
        write_results(filename, unsorted_array, array, 'mot')
    print(f'Median of Three Swaps: {swaps}')

    swaps = 0
    array = get_input_array(filename)
    unsorted_array = array.copy()
    if profile:
        cProfile.run('quicksort_vanilla(array, 0, len(array) - 1)')
    else:
        quicksort_vanilla(array, 0, len(array) - 1)
        write_results(filename, unsorted_array, array, 'normal')
    print(f'Normal Swaps: {swaps}')
