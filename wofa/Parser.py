import re
import os
import pathlib
from wofa import FiniteAutomata
from wofa.Constants import *


def get_submission(directory, name):
    """ Method specifies the automaton stored in the file which is specified by directory and name. The different tasks
    and the number of files per directory are specified in ./assets/README.

    Args:
        directory (string): Directory in which the file of the machine is located.
        name (string):      Name of the file.

    Returns:
        FiniteAutomata:     The generated FiniteAutomata Object
    """
    path = os.path.join(pathlib.Path(__file__).parent, 'assets', 'submissions', directory, name) + '.txt'

    try:
        return parse(__get_lines(path))
    except FileNotFoundError:
        raise FileNotFoundError(f'It exists for the task {directory} no submission {name}')
    except Exception as _:
        return None


def get_solution(exercise):
    """ Returns a solution of the various tasks as a FiniteAutomaton object.

    Args:
        exercise (string): Name of the Exercise.

    Returns:
        FiniteAutomata: The solution Object
    """
    path = os.path.join(pathlib.Path(__file__).parent, 'assets', 'solutions', exercise) + '.txt'
    try:
        return parse(__get_lines(path))
    except Exception:
        return None


def __get_lines(path):
    """Opens a file and read the lines.

    Args:
        path (string): path of the file.

    Raises:
        Exception: File Not Found, if the file doesn't exist.

    Returns:
        list: List of the lines.
    """
    try:
        file = open(path, 'r')
    except FileNotFoundError:
        raise FileNotFoundError("Error: File Not Found")

    lines = file.readlines()
    file.close()

    return lines


def parse(lines):
    """Parses the stored automata and then creates the corresponding automaton object.

    Args:
        lines (list of strings): List of lines of stored automata.

    Raises:
        Exception: Parsing error.

    Returns:
        FiniteAutomata: The parsed object.
    """

    state_dict = dict()
    state_counter = 0

    # Remove whitespace, ignore comments, remove empty lines
    purged = []
    for line in lines:
        new_line = line.split("#")[0].strip()
        if new_line != "":
            purged.append(new_line)

    first = purged[0]
    second = purged[1]
    third = purged[2]
    last = purged[len(purged) - 1]

    if not (first.startswith(INPUT_ALPHABET)
            and second.startswith(START_STATES)
            and third.startswith(TRANSITIONS)
            and last.startswith(ACC_STATES)):
        raise Exception(
            "Error: Key words input_alphabet, start_states, transitions and acc_states must occur in exactly in "
            "this order")

    # Alphabet
    input_alphabet = first.split("=")
    if len(input_alphabet) != 2:
        raise Exception("Error: input_alphabet must be followed by equal sign")

    candidates = input_alphabet[1].split(',')
    if len(candidates) < 1:
        raise Exception("Error: There must be at least one symbol in the alphabet")

    alphabet = {symbol.strip() for symbol in candidates}

    # Initial states.
    initials_line = second.split("=")
    if len(initials_line) != 2:
        raise Exception("Error: start_states must be followed by equal sign")

    candidates = initials_line[1].split(',')

    initials = set()
    for state in candidates:
        state = state.strip()
        if re.match(STATE_NAME, state):
            if state.strip() not in state_dict:
                state_dict[state.strip()] = state_counter
                state_counter += 1
            initials.add(state_dict[state])
        else:
            raise Exception(f'Error: Unexpected symbol in state identifier. ({state})')

    # Finial states
    final_line = last.split("=")
    if len(final_line) != 2:
        raise Exception("Error: acc_states must be followed by equal sign")

    candidates = final_line[1].split(",")

    finials = set()
    for state in candidates:
        state = state.strip()
        if re.match(STATE_NAME, state):
            if state.strip() not in state_dict:
                state_dict[state.strip()] = state_counter
                state_counter += 1
            finials.add(state_dict[state])
        else:
            raise Exception(f'Error: Unexpected symbol in state identifier. ({state})')

    # Transitions
    transition_first_line = third.split("=")
    if len(transition_first_line) != 2:
        raise Exception("Error: transitions must be followed by equal sign")

    transition_lines = [transition_first_line[1]] + [line for line in purged[3:len(purged) - 1]]

    transitions = []
    for line in transition_lines:
        line_split = line.split("->")
        if len(line_split) != 2:
            raise Exception("Error: only one production arrow allowed per line")
        left = tuple(line_split[0].strip().split(","))
        key = (left[0].strip(), left[1].strip())
        right_side = line_split[1].split(";")
        value = set()
        for state in right_side:
            state = state.strip()
            if re.match(STATE_NAME, state):
                value.add(state.strip())
            else:
                raise Exception(f'Error: Unexpected symbol in state identifier. ({state})')

        for end in value:
            start = key[0]
            if start.strip() not in state_dict:
                state_dict[start.strip()] = state_counter
                state_counter += 1
            start = state_dict[start.strip()]

            if end.strip() not in state_dict:
                state_dict[end.strip()] = state_counter
                state_counter += 1
            end = state_dict[end.strip()]

            if key[1] not in alphabet:
                raise Exception("Error: Symbol of transition is not in the alphabet.")

            transitions.append((start, key[1], end))

    # crate a FiniteAutomata Object
    return FiniteAutomata(initials, transitions, finials)
