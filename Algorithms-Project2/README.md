
# Algorithms Project 2
## Runtime Environment

Python Version: Python 3.8.10

### Installation/Uninstallation
No installation required. Just unzip the folder and navigate to each program as shown below.

To "uninstall" just remove the Algorithms-Project2 folder and zip file.

Both programs only use modules from the Python Standard Library and can easily be run
from a UNIX command line.

### Running Quicksort

Navigation and execution
```
$> cd Algorithms-Project2
$> # Basic Example
$> ./quicksort.py TestFiles/TestInput100.txt
```

Usage:
```
Usage: quicksort.py [test file]
Args:
        test file - input file of integers to sort
        -p, --profile - [optional] count calls instead of results
```

Examples:

Test with 100 random integers
```
$> ./quicksort.py TestFiles/TestInput100.txt
Median of Three Swaps: 258
Normal Swaps: 263
```

Profile the test with 100 random integers. Of note is the number of times `quicksort_mot`
and `quicksort_vanilla` are called as well as the number of swaps.
```
$> ./quicksort.py TestFiles/TestInput100.txt
         290 function calls (176 primitive calls) in 0.000 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.000    0.000 <string>:1(<module>)
       57    0.000    0.000    0.000    0.000 quicksort.py:31(median_of_three_pivot)
       57    0.000    0.000    0.000    0.000 quicksort.py:63(median_of_three_partition)
    115/1    0.000    0.000    0.000    0.000 quicksort.py:98(quicksort_mot)
        1    0.000    0.000    0.000    0.000 {built-in method builtins.exec}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.len}
       57    0.000    0.000    0.000    0.000 {built-in method math.floor}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


Median of Three Swaps: 258
         212 function calls (74 primitive calls) in 0.000 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.000    0.000 <string>:1(<module>)
       69    0.000    0.000    0.000    0.000 quicksort.py:112(vanilla_partition)
    139/1    0.000    0.000    0.000    0.000 quicksort.py:144(quicksort_vanilla)
        1    0.000    0.000    0.000    0.000 {built-in method builtins.exec}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.len}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


Normal Swaps: 263
```

## Tracerun Generation

Quicksort Trace Files at `Algorithms-Project2/TraceResults` generated with:
```
python3 -m trace --count -C TraceResults/ --ignore-module _bootlocale --ignore-module abc --ignore-module codecs --ignore-module functools --ignore-module cProfile --ignore-module posixpath --ignore-module profile quicksort.py TestFiles/SortedInput10000.txt

 python3 -m trace --count -C TraceResults/ --ignore-module _bootlocale --ignore-module abc --ignore-module codecs --ignore-module functools --ignore-module cProfile --ignore-module posixpath --ignore-module profile quicksort.py TestFiles/TestInput10000.txt
```

A caveat about running the traceresults is that the result file is named after the module so multiple runs erase past results so it's important to rename the results or move them. In this case they were renamed to include the input type and quantity.

## List of Files

### Structure

```
Algorithms-Project2/:
        SampleTestResults:
        TestFiles/:
        TraceResults/:

```

* SampleTestResults folders container inputs and outputs
* TestFiles folders contain test inputs
* TraceResults folders contain trace files of the code on the largest n tests


### List of files

```
Algorithms-Project2:
README.md  SampleTestResults  TODO  TestFiles  TraceResults  quicksort.py

Algorithms-Project2/SampleTestResults:
TestResult-SortedInput100-mot.txt       TestResult-TestInput1000-mot.txt
TestResult-SortedInput100-normal.txt    TestResult-TestInput1000-normal.txt
TestResult-SortedInput1000-mot.txt      TestResult-TestInput10000-mot.txt
TestResult-SortedInput1000-normal.txt   TestResult-TestInput10000-normal.txt
TestResult-SortedInput10000-mot.txt     TestResult-TestInput100000-mot.txt
TestResult-SortedInput10000-normal.txt  TestResult-TestInput100000-normal.txt
TestResult-TestInput100-mot.txt         TestResult-TestInput1000000-mot.txt
TestResult-TestInput100-normal.txt      TestResult-TestInput1000000-normal.txt

Algorithms-Project2/TestFiles:
SortedInput100.txt    SortedInput100000.txt   TestInput1000.txt    TestInput1000000.txt
SortedInput1000.txt   SortedInput1000000.txt  TestInput10000.txt   generate_sorted_data.py
SortedInput10000.txt  TestInput100.txt        TestInput100000.txt  generate_test_data.py

Algorithms-Project2/TraceResults:
quicksort-random-10000.cover  quicksort-sorted-10000.cover
morgana@Power-Of-Voodoo:~/src$ cd Algorithms-Project2/
```