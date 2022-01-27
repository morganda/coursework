#!/usr/bin/env python3

import sys
import cProfile


class SignalReader:
    """Class to handle processing the input stream.
    """

    def __init__(self, stream: str, sigx, sigy) -> None:
        self.stream = stream

        # only chars in sigx and sigy are valid
        self.allowed_symbols = set(sigx).union(set(sigy))

        # index in the read stream
        self.cursor = 0

        # track most recently detected symbol
        self.most_recent_signal = ''
        self.most_recent_signal_index = 0

    def network_read(self, character: str):
        """Allows adding one additional character to help simulate
        a stream we're reading.

        Args:
            character (str): the character to append to stream
        """
        self.stream += character

    def next_signal(self):
        """Reads over stream until it finds a set of valid
        characters making up a potentially interwoven
        signal.

        Returns:
            string: a subset of stream of allowed characters
        """
        signal = ''

        # skip invalid chars
        while self.cursor < len(self.stream) and \
                self.stream[self.cursor] not in self.allowed_symbols:
            self.cursor += 1

        # append to existing signal if there were no invalid
        #   symbols read since the last call to next_signal
        if self.most_recent_signal_index + 1 == self.cursor:
            signal += self.most_recent_signal

        # capture next set of valid chars
        while self.cursor < len(self.stream) and \
                self.stream[self.cursor] in self.allowed_symbols:

            signal += self.stream[self.cursor]
            self.cursor += 1

        self.most_recent_signal = signal
        self.most_recent_signal_index = self.cursor - 1
        return signal

    def has_next(self):
        """Checks if there is another possible sequence of
        interwoven strings.

        Returns:
            boolean: True if there is anothe signal to validate
        """
        # pass over bad symbols
        while self.cursor < len(self.stream) and \
                self.stream[self.cursor] not in self.allowed_symbols:
            self.cursor += 1
        return self.cursor < len(self.stream)


def signal_processor_dp(sigx, sigy, stream, verbose=False):
    """Dynamic programming construction of a table that
    finds possible interweaving of six and sigy in stream.

    Args:
        sigx (string): x signal to match in stream
        sigy (string): y signal to match in stream
        stream (string): stream to detect interwoven signals in
        verbose (bool, optional): Print calculated table. Defaults to False.

    Returns:
        [type]: [description]
    """
    # 2d array that we dynamically size
    iw_table = list()

    # i and j correspond to the row and column in the DP table
    #   simplified names are used to make the code more readable
    j = 0
    for i in range(len(stream)+1):
        iw_table.append(list())
        while j <= len(stream) and i+j-1 < len(stream):
            iw_table[i].append(False)

            # pad mamtch signals dynamically for repeat matches
            if i == len(sigx):
                sigx = sigx * 2
            if j == len(sigy):
                sigy = sigy * 2

            # table[0][0] is a default True since it doesn't correspond to
            #   a signal match
            if i == 0 and j == 0:
                iw_table[i][j] = True
            elif i == 0:
                iw_table[i][j] = iw_table[i][j-1] and \
                    sigy[j-1] == stream[i+j-1]
            elif j == 0:
                iw_table[i][j] = iw_table[i-1][j] and \
                    sigx[i-1] == stream[i+j-1]
            else:
                iw_table[i][j] = (iw_table[i-1][j] and
                                  sigx[i-1] == stream[i+j-1]) \
                    or (iw_table[i][j-1] and sigy[j-1] == stream[i+j-1])
            j += 1
        j = 0

    if verbose:
        print('Answer table:')
        for m in range(len(iw_table)):
            print(','.join([str(val) for val in iw_table[m]]))
        print()

    return iw_table


def reconstruct_matches(iw_table, sigx, sigy):
    """Reconstruct the matched interwoven signals from
    the table calculated

    Args:
        table (list(list(boolean))): a 2D list of booleans - True indicates a
                                        match
        sigx (string): sigx string to match
        sigy (string): sigy string to match

    Returns:
        Tuple(string, string): the detected interweaving of sigx, sigy
    """

    # find end match marker
    endi = 0
    while endi < len(iw_table):
        endj = len(iw_table[endi]) - 1
        if iw_table[endi][endj] is True:
            break
        endi += 1

    if endi >= len(iw_table):
        return '', ''

    # count matched dimensions
    sigx_c = 0
    sigy_c = 0

    # pad signals to greater than the table size
    sigx = sigx * int((len(iw_table)/len(sigx) + 1))
    sigy = sigy * int((len(iw_table)/len(sigy) + 1))
    while endi > 0 or endj > 0:
        if endj > 0 and iw_table[endi][endj - 1] is True:
            sigy_c += 1
            endj -= 1
        elif iw_table[endi - 1][endj] is True:
            sigx_c += 1
            endi -= 1

    return sigx[:sigx_c], sigy[:sigy_c]


def read_signal_input_file(filename):
    """Reads input from a file

    Args:
        filename (string): name of the file with the test case

    Returns:
        list(string): a 3-tuple of the x, y strings to match and
                        and a string representing the stream of chars
    """
    inputs = list()
    with open(filename, 'r') as fin:
        for line in fin.readlines():
            inputs.append(line.strip())
    return inputs


def is_better_signal(best_signal, sigx_matches, sigy_matches):
    """Returns true if the new signal check is a longer match
    than the previous match.

    Args:
        best_signal (dict[str, str]): dict containing best match yet
        sigx_matches (str): detected interwoven sigx singals
        sigy_matches (str): detected interwoven sigy signals

    Returns:
        boolean: True if the new signal is a longer match
    """
    # check if new best match
    signal_match_length = len(sigx_matches) + len(sigy_matches)
    if best_signal['SIGX'] is None:
        best_match_length = 0
    else:
        best_match_length = len(best_signal['SIGX']) + \
            len(best_signal['SIGY'])
    if signal_match_length > best_match_length:
        return True
    return False


def usage():
    """Print the usage summary of the program
    """
    print(f'Usage: ./{sys.argv[0]} filename [--stream]')
    print()
    print('Args:')
    print('\tfilename - name of the input file')
    print()
    print('Options:')
    print('\t--stream - (optional) read stream one char at a time and attempt \
          to analyze the substring before continuing on')
    print('\t--profile - (optional) Run profiler output for key code')


def process_args(args: list):
    """List of arguments to the application

    Args:
        args (list): arguments to the application

    Returns:
        Tuple(string, boolean, boolean): (filename of input,
            to process as a stream or as a whole,
            whether to profile or not)
    """
    as_stream = False
    profile = False
    if '--stream' in args:
        as_stream = True
        args.remove('--stream')
    if '--profile' in args:
        profile = True
        args.remove('--profile')
    if len(args) == 1:
        filename = args[0]
    else:
        print(args)
        usage()
        exit(1)

    return filename, as_stream, profile


def main(stream, sigx, sigy, as_stream):
    # track the best signal detected
    best_signal = {
        'SIGX': None,
        'SIGY': None
    }

    # simulate live stream
    if as_stream:
        signal_reader = SignalReader('', sigx, sigy)
        stream_length = len(stream)
    else:
        signal_reader = SignalReader(stream, sigx, sigy)
        stream_length = 1
    for i in range(stream_length):
        # simulate stream by calculating
        if as_stream:
            signal_reader.network_read(stream[i])
        while signal_reader.has_next():
            possible_signal = signal_reader.next_signal()
            print(f'Found Possible Signal: {possible_signal}')

            # Optimization: track sub tables for partial signals
            table = signal_processor_dp(sigx, sigy, possible_signal)
            sigx_matches, sigy_matches = reconstruct_matches(table, sigx, sigy)

            # check for valid signal
            if sigx_matches.startswith(sigx) and sigy_matches.startswith(sigy):

                # track best detected signal
                if is_better_signal(best_signal, sigx_matches, sigy_matches):
                    best_signal['SIGX'] = sigx_matches
                    best_signal['SIGY'] = sigy_matches

                # print signal
                print('Interwoven Signals:')
                print(f'\tSIGX: {sigx_matches}')
                print(f'\tSIGY: {sigy_matches}')
            else:
                print('Invalid Signal')
            print()

    if best_signal['SIGX'] is not None:
        print('Best Match:')
        print(f'\tSIGX: {best_signal["SIGX"]}')
        print(f'\tSIGY: {best_signal["SIGY"]}')
    else:
        print('No valid signal detected')


if __name__ == '__main__':
    """Main Driver
    """
    filename, as_stream, profile = process_args(sys.argv[1:])
    SIGX, SIGY, STREAM = read_signal_input_file(filename)

    if profile:
        cProfile.run('main(STREAM, SIGX, SIGY, as_stream)')
    else:
        main(STREAM, SIGX, SIGY, as_stream)
