#!/usr/bin/env python3

"""Most method names are named after states using general Turing
Machine notation: e.g. q0, q1,... qN, qY.
"""

import sys
import re

# Tape symbols
B = 'B'  # delimeter
b = '#'  # blank
W = 'W'  # Symbol to track subtraction
ONE = '1'


def usage():
    """Simple CLI usage printout.
    """
    print(f'Usage: ./{sys.argv[0]} [num1] [num2]')
    print()
    print('Args:')
    print('\tnum1 - a non-negative number consisting of num1 1\'s')
    print('\tnum2 - a non-negative number consisting of num1 1\'s')
    exit(1)


def tm_input(op1, op2):
    """Formats the operand input

    Args:
        op1 (string): a non-negative number consisting of op1 1\'s Ex: '111'
        op2 (string): a non-negative number consisting of op2 1\'s EX: '11'

    Returns:
        string: the Turing Machine tape formatted input
    """
    return f'{op1}{B}{op2}{B}'


def gen_tape(op1, op2):
    """Constructs the tape of the Turing Machine from some input.

    Args:
        op1 (string): a non-negative number consisting of op1 1\'s Ex: '111'
        op2 (string): a non-negative number consisting of op2 1\'s EX: '11'

    Returns:
        List[string]: a sequence of characters that make up the tape of the TM
    """
    # wrap input with blanks
    tape = [b]
    tape.extend(list(tm_input(op1, op2)))
    tape.append(b)
    return tape


def qY(state, head, tape):
    """The accepting halt state of the TM.

    Args:
        state (function): the method object referencing a state method
        head (int): points to the location on the tape
        tape (List[string]): Sequence of chars that make up the TM tape
    """
    print('Accepted')
    print(f'State: {state}')
    print(f'Head: {head}')
    print(f'Result Tape: {tape}')
    exit(0)


def qN(state, head, tape):
    """The rejecting halt state of the TM.

    Args:
        state (function): the method object referencing a state method
        head (int): points to the location on the tape
        tape (List[string]): Sequence of chars that make up the TM tape
    """
    tape[head] = b
    head -= 1
    print('Rejected')
    print(f'State: {state}')
    print(f'Head: {head}')
    print(f'Result Tape: {tape}')
    exit(1)


def q0(state, head, tape):
    """Starting state of the subtraction TM. Starts by writing W's on
    the first operand to encode our subtraction state.

    Args:
        state (function): the method object referencing a state method
        head (int): points to the location on the tape
        tape (List[string]): Sequence of chars that make up the TM tape

    Returns:
        Tuple[funciton, int, List[string]]: stateful components of the TM
    """
    while tape[head] == ONE:
        tape[head] = W
        head += 1

    if tape[head] == B:
        head += 1
        state = q1
    else:
        state = qN
    return state, head, tape


def q1(state, head, tape):
    """Writes W's on the second operand for us encode the subtraction
    state.

    Args:
        state (function): the method object referencing a state method
        head (int): points to the location on the tape
        tape (List[string]): Sequence of chars that make up the TM tape

    Returns:
        Tuple[funciton, int, List[string]]: stateful components of the TM
    """
    while tape[head] == ONE:
        tape[head] = W
        head += 1

    if tape[head] == B:
        head -= 1
        state = q2
    else:
        state = qN
    return state, head, tape


def q2(state, head, tape):
    """Passes any ones that it sees and writes a W on the 2 operand to
    track the start of doing incremental subtraction. The state then
    passes on to q3 unless a B is seen. If it sees a B, that indicates
    we've finished subtracting from the 1st operand and passes state
    to q7 to see if we've arrived in an acceptance state.

    Args:
        state (function): the method object referencing a state method
        head (int): points to the location on the tape
        tape (List[string]): Sequence of chars that make up the TM tape

    Returns:
        Tuple[funciton, int, List[string]]: stateful components of the TM
    """
    while tape[head] == ONE:
        head -= 1

    if tape[head] == W:
        tape[head] = ONE
        head -= 1
        state = q3
    elif tape[head] == B:
        head -= 1
        state = q7
    else:
        state = qN
    return state, head, tape


def q3(state, head, tape):
    """Passes over the remaining W's in the second operand heading back
    to the first operand. State then passes to q4.

    Args:
        state (function): the method object referencing a state method
        head (int): points to the location on the tape
        tape (List[string]): Sequence of chars that make up the TM tape

    Returns:
        Tuple[funciton, int, List[string]]: stateful components of the TM
    """
    while tape[head] == W:
        head -= 1

    if tape[head] == B:
        head -= 1
        state = q4
    else:
        state = qN
    return state, head, tape


def q4(state, head, tape):
    """Passes over any 1's in the first operand looking for a W to
    replace with a 1 to track our subtraction. State then passes to q5.

    Args:
        state (function): the method object referencing a state method
        head (int): points to the location on the tape
        tape (List[string]): Sequence of chars that make up the TM tape

    Returns:
        Tuple[funciton, int, List[string]]: stateful components of the TM
    """
    while tape[head] == ONE:
        head -= 1

    if tape[head] == W:
        tape[head] = ONE
        head += 1
        state = q5
    else:
        state = qN
    return state, head, tape


def q5(state, head, tape):
    """Moves back right passing over any 1's in the first operand. State
    then passes to q6.

    Args:
        state (function): the method object referencing a state method
        head (int): points to the location on the tape
        tape (List[string]): Sequence of chars that make up the TM tape

    Returns:
        Tuple[funciton, int, List[string]]: stateful components of the TM
    """
    while tape[head] == ONE:
        head += 1

    if tape[head] == B:
        head += 1
        state = q6
    else:
        state = qN
    return state, head, tape


def q6(state, head, tape):
    """Passes over all the W's in the second operand until it gets to
    a 1 and then reverses direction to operate on the last W. At this point
    state passed back to q2.

    Args:
        state (function): the method object referencing a state method
        head (int): points to the location on the tape
        tape (List[string]): Sequence of chars that make up the TM tape

    Returns:
        Tuple[funciton, int, List[string]]: stateful components of the TM
    """
    while tape[head] == W:
        head += 1

    if tape[head] == ONE:
        head -= 1
        state = q2
    else:
        state = qN
    return state, head, tape


def q7(state, head, tape):
    """Starts the process of writing the answer to the tape. Shifts left
    on the first operand until it encounters a W which is replaced with
    a 1. State then passes to q8.

    Args:
        state (function): the method object referencing a state method
        head (int): points to the location on the tape
        tape (List[string]): Sequence of chars that make up the TM tape

    Returns:
        Tuple[funciton, int, List[string]]: stateful components of the TM
    """
    while tape[head] == ONE:
        head -= 1

    if tape[head] == b:
        head += 1  # back to the initial position
        state = qY
        qY(state, head, tape)
    elif tape[head] == W:
        tape[head] = ONE
        head += 1
        state = q8
    else:
        state = qN
    return state, head, tape


def q8(state, head, tape):
    """Travels over the 1s in the 1st operand since we're done with those.
    Once the B on the end is encountered we pass the state to q9.

    Args:
        state (function): the method object referencing a state method
        head (int): points to the location on the tape
        tape (List[string]): Sequence of chars that make up the TM tape

    Returns:
        Tuple[funciton, int, List[string]]: stateful components of the TM
    """
    while tape[head] == ONE:
        head += 1

    if tape[head] == B:
        head += 1
        state = q9
    else:
        state = qN
    return state, head, tape


def q9(state, head, tape):
    """Passes over any 1's in the second operand and until it
    encounters the B preceding the answer space on the tape. It shifts
    right and passes the state to q10.

    Args:
        state (function): the method object referencing a state method
        head (int): points to the location on the tape
        tape (List[string]): Sequence of chars that make up the TM tape

    Returns:
        Tuple[funciton, int, List[string]]: stateful components of the TM
    """
    while tape[head] == ONE:
        head += 1

    if tape[head] == b:
        tape[head] = B
        head += 1
        state = q10
    elif tape[head] == B:
        head += 1
        state = q10
    else:
        state = qN
    return state, head, tape


def q10(state, head, tape):
    """Passes right over any 1's in the answer until it finds the blank
    at the end of our tape. It then replaces the blank with a 1 and
    starts shifting the head back left. State transitions to q11.

    This takes an additional step to add an extra blank on the end of the
    tape so that it can dynamically expand to write in the answer.

    Args:
        state (function): the method object referencing a state method
        head (int): points to the location on the tape
        tape (List[string]): Sequence of chars that make up the TM tape

    Returns:
        Tuple[funciton, int, List[string]]: stateful components of the TM
    """
    if head == len(tape):
        tape.append(b)
    else:
        while tape[head] == ONE:
            head += 1

    # this can be simplified, but I'm trying to
    # simulate the TM
    if tape[head] == b:
        tape[head] = ONE
        tape.append(b)
        head -= 1
        state = q11
    else:
        state = qN
    return state, head, tape


def q11(state, head, tape):
    """Travels left over any 1's written in the answer back toward the
    operands. Once the B preceding the answer is encountered, state is
    shifted back to q2 to pass back over the operands.

    Args:
        state (function): the method object referencing a state method
        head (int): points to the location on the tape
        tape (List[string]): Sequence of chars that make up the TM tape

    Returns:
        Tuple[funciton, int, List[string]]: stateful components of the TM
    """
    while tape[head] == ONE:
        head -= 1

    if tape[head] == B:
        head -= 1
        state = q2
    else:
        state = qN
    return state, head, tape


def tm_subtract(op1, op2):
    """Wrapper function that executes the TM.

    Args:
        op1 (string): a non-negative number consisting of op1 1\'s Ex: '111'
        op2 (string): a non-negative number consisting of op2 1\'s EX: '11'
    """
    tape = gen_tape(op1, op2)
    print(f'Iniital Tape: {tape}')
    head = 1
    state = q0

    while state not in [qN, qY]:
        state, head, tape = state(state, head, tape)

    state(state, head, tape)


if __name__ == '__main__':
    # argument checks
    if len(sys.argv) != 3:
        usage()
    else:
        p = re.compile('^[1]+$')
        if not p.match(sys.argv[1]) or not p.match(sys.argv[2]):
            usage()

    # start turing machine
    tm_subtract(sys.argv[1], sys.argv[2])
