
# Algorithms Project 3
## Runtime Environment

Python Version: Python 3.8.10

### Installation/Uninstallation
No installation required. Just unzip the folder and navigate to each program as shown below.

To "uninstall" just remove the Algorithms-Project3 folder and zip file.

Both programs only use modules from the Python Standard Library and can easily be run
from a UNIX command line.

### Running Quicksort

Navigation and execution
```
$> cd Algorithms-Project3
$> # Basic Example
$> ./signal-processor.py TestFiles/TestInput1.txt
```

Input files are relatively simple:
* Line 1 contains the x signal.
* Line 2 contains the y signal.
* Line 3 contains the interwoven signal, s.
```
101
00
1000101010
```

Usage:
```
Usage: ./signal-processor.py filename [--stream]

Args:
        filename - name of the input file

Options:
        --stream - (optional) read stream one char at a time and attempt to analyze the substring before continuing on
        --profile - (optional) Run profiler output for key code
```

Example:

Test with Problem Prompt Example
```
$> ./signal-processor.py TestFiles/TestInput1.txt
Found Possible Signal: 100010101
Interwoven Signals:
        SIGX: 101101
        SIGY: 000

Best Match:
        SIGX: 101101
        SIGY: 000
```

Same execution, but with --stream and --profile flags. It should be noted that the `--profile` flag isn't as useful for this application. The trace file results are much more useful in measuring performance.
```
$> ./signal-processor.py TestFiles/TestInput1.txt --stream --profile
Found Possible Signal: 1
Invalid Signal

Found Possible Signal: 10
Invalid Signal

Found Possible Signal: 100
Invalid Signal

Found Possible Signal: 1000
Invalid Signal

Found Possible Signal: 10001
Interwoven Signals:
        SIGX: 101
        SIGY: 00

Found Possible Signal: 100010
Interwoven Signals:
        SIGX: 101
        SIGY: 000

Found Possible Signal: 1000101
Interwoven Signals:
        SIGX: 1011
        SIGY: 000

Found Possible Signal: 10001010
Interwoven Signals:
        SIGX: 1011
        SIGY: 0000

Found Possible Signal: 100010101
Interwoven Signals:
        SIGX: 101101
        SIGY: 000

Best Match:
        SIGX: 101101
        SIGY: 000
         1569 function calls in 0.001 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.001    0.001 <string>:1(<module>)
        1    0.000    0.000    0.000    0.000 signal-processor.py:11(__init__)
        9    0.000    0.000    0.000    0.000 signal-processor.py:134(reconstruct_matches)
        5    0.000    0.000    0.000    0.000 signal-processor.py:194(is_better_signal)
        9    0.000    0.000    0.000    0.000 signal-processor.py:24(network_read)
        1    0.000    0.000    0.001    0.001 signal-processor.py:261(main)
        9    0.000    0.000    0.000    0.000 signal-processor.py:33(next_signal)
       18    0.000    0.000    0.000    0.000 signal-processor.py:64(has_next)
        9    0.000    0.000    0.000    0.000 signal-processor.py:78(signal_processor_dp)
        1    0.000    0.000    0.001    0.001 {built-in method builtins.exec}
     1177    0.000    0.000    0.000    0.000 {built-in method builtins.len}
       40    0.000    0.000    0.000    0.000 {built-in method builtins.print}
      273    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
       14    0.000    0.000    0.000    0.000 {method 'startswith' of 'str' objects}
        1    0.000    0.000    0.000    0.000 {method 'union' of 'set' objects}
```

## Tracerun Generation

Signal Processor Trace Files at `Algorithms-Project3/TraceResults` generated with:
```
python3 -m trace --count -C TraceResults/ --ignore-module _bootlocale --ignore-module abc --ignore-module codecs --ignore-module functools --ignore-module cProfile --ignore-module posixpath --ignore-module profile signal-processor.py TestFiles/TestInput4.txt
```

A caveat about running the traceresults is that the result file is named after the module so multiple runs erase past results so it's important to rename the results or move them. In this case they were renamed to include the input type and quantity.

## List of Files

### Structure

```
Algorithms-Project3/:
        SampleTestResults:
        TestFiles/:
        TraceResults/:

```

* SampleTestResults folders container inputs and outputs
* TestFiles folders contain test inputs
* TraceResults folders contain trace files of the code on the largest n tests. Trace files were generated with both the `--stream` and without the `--stream` option over the same dataset. The results are discussed in the Analysis PDF.


### List of files

Produced a list by running `ls -r`

Algorithms-Project3
```
README.md  SampleTestResults  TestFiles  TraceResults  signal-processor.py

./SampleTestResults:
TestResult-TestInput1.txt  TestResult-TestInput3.txt  TestResult-TestInput5.txt
TestResult-TestInput2.txt  TestResult-TestInput4.txt

./TestFiles:
PerfTest1.txt  PerfTest3.txt  PerfTest5.txt   TestInput2.txt  TestInput4.txt
PerfTest2.txt  PerfTest4.txt  TestInput1.txt  TestInput3.txt  TestInput5.txt

./TraceResults:
PerfTest1_signal-processor.cover         PerfTest4_signal-processor.cover
PerfTest1_stream_signal-processor.cover  PerfTest5_signal-processor.cover
PerfTest2_signal-processor.cover         Perftest3_stream_signal-processor.cover
PerfTest2_stream_signal-processor.cover  Perftest4_stream_signal-processor.cover
PerfTest3_signal-processor.cover         Perftest5_stream_signal-processor.cover
```