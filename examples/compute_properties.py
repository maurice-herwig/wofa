from wofa import FiniteAutomata, SubmissionIterator, get_solution
import networkx as nx

REMOVED_UNPRODUCTIVE = 'removed_unproductive'
ORIGINAL = 'original'
LANGUAGE = 'language'

NUM_STATES = 'number_of_states'
NUM_ACC_STATES = 'number_or_accepting_states'
NUM_INITIAL_STATES = 'number_of_initial_states'
NUM_OF_TRANSITIONS = 'number_of_transitions'
USE_NON_ALPHABET_TRANS = 'use_non_alphabet_transitions'
NUM_OF_UN_PROD_STATES = 'number_of_unproductive_states'
DEAD_STATE = 'exist_dead_state'
NUM_SIM_EQ_PAIRS = 'number_of_simulation_equivalent_pairs'
NUM_BI_SIM_EQ_PAIRS = 'number_of_bisimulation_equivalent_pairs'
LENGTH_LONGEST_PATH = 'length_of_longest_path'
CORRECT = 'correct'
IS_SUBSET = 'is_subset'
IS_SUPERSET = 'is_superset'
EMPTY_LANGUAGE = 'empty_language'
SHORTEST_WORDS = 'shortest_accepting_words'
SHORTEST_FALSE_WORDS = 'shortest_false_classified_words'
NUM_NON_DETERMINISTIC_TRANS = 'number_of_non_deterministic_transitions'
LENGTH_OF_SIMPLE_LOOPS = 'length_of_simple_loops'


def get_basic_language_props(submission: FiniteAutomata,
                             solution: FiniteAutomata):
    """
    Compute some language properties of the given submission in contrast to the given solution.

    Args:
        submission: FiniteAutomata
        solution: FiniteAutomata

    Returns:  dict with the properties
    """
    # Check if the automaton language equivalent to the sample solution
    equivalent = submission.equivalence_test(other=solution)

    # Compute some simple language properties
    basic_props = {CORRECT: equivalent,
                   EMPTY_LANGUAGE: submission.is_empty(),
                   SHORTEST_WORDS: submission.get_shortest_accepting_words()
                   }

    # Compute the subset relationship between the submission and the solution
    if equivalent:
        basic_props[IS_SUBSET] = True
        basic_props[IS_SUPERSET] = True
    else:
        sub_sub_solution, solution_sub_submission = submission.subsets_symmetric_difference(other=solution)
        basic_props[IS_SUBSET] = (sub_sub_solution.is_empty())
        basic_props[IS_SUPERSET] = (solution_sub_submission.is_empty())
        basic_props[SHORTEST_FALSE_WORDS] = sub_sub_solution.union(
            solution_sub_submission).get_shortest_accepting_words()

    return basic_props


def get_basic_syntactically_props(automaton: FiniteAutomata,
                                  check_if_use_non_alphabet_transitions=False,
                                  check_num_of_non_productive=False,
                                  check_for_dead_state=False):
    """
    Compute some basic syntactically properties for a given automaton. 
    
    Args:
        automaton: The automaton for that we want to compute theirs properties.
        check_if_use_non_alphabet_transitions: Optionally computation if true
        check_num_of_non_productive: Optionally computation if true
        check_for_dead_state: Optionally computation if true

    Returns: A dict with the properties
    """
    # Compute the transitions of the submission
    transitions = automaton.get_transitions()

    # Compute some simple properties
    basic_props = {
        NUM_STATES: automaton.get_number_of_states(),
        NUM_ACC_STATES: len(automaton.get_finals()),
        NUM_INITIAL_STATES: len(automaton.get_initials()),
        NUM_OF_TRANSITIONS: len(transitions),
        LENGTH_LONGEST_PATH: automaton.get_length_longest_run()}

    # Additionally check if the automaton use non-alphabet transitions
    if check_if_use_non_alphabet_transitions:
        use_non_alphabet_trans = False
        for _, a, _ in transitions:
            if a not in FiniteAutomata.alphabet:
                use_non_alphabet_trans = True
                break
        basic_props[USE_NON_ALPHABET_TRANS] = use_non_alphabet_trans

    # Additionally check the number of unproductive states
    if check_num_of_non_productive:
        basic_props[NUM_OF_UN_PROD_STATES] = (automaton.get_number_of_states() - len(automaton.productive()))

    # Additionally check if a dead state exits
    if check_for_dead_state:

        exists_dead_state = False

        # Check for each state if it is a dead state
        for q in range(automaton.get_number_of_states()):
            if q not in automaton.finals:

                is_dead_state = True
                letters = set()
                for p, a in automaton.get_all_predecessors_with_letter(s=q):
                    if p != q:
                        is_dead_state = False
                        break
                    letters.add(a)

                if is_dead_state:
                    if FiniteAutomata.alphabet.issubset(letters):
                        exists_dead_state = True

            if exists_dead_state:
                break

        basic_props[DEAD_STATE] = exists_dead_state

    # Compute the number of simulation equivalent pairs
    basic_props[NUM_SIM_EQ_PAIRS] = len(automaton.simulation_equivalence_pairs())

    # Compute the number of bisimulation equivalent pairs
    basic_props[NUM_BI_SIM_EQ_PAIRS] = len(automaton.bi_simulation_pairs())

    # Compute the number of nondeterministic transition pairs
    num_non_det_trans = 0
    for q in range(automaton.get_number_of_states()):
        for a in FiniteAutomata.alphabet:
            if len(automaton.get_successors(s=q, a=a)) > 1:
                num_non_det_trans += 1
    basic_props[NUM_NON_DETERMINISTIC_TRANS] = num_non_det_trans

    # Compute the length of all symple loops of the automaton and sort in descending order
    graph = nx.DiGraph()
    graph.add_edges_from([(p, q) for p, _, q in transitions])
    length_of_cycles = [len(c) for c in list(nx.simple_cycles(graph))]
    length_of_cycles.sort(reverse=True)
    basic_props[LENGTH_OF_SIMPLE_LOOPS] = length_of_cycles

    return basic_props


def get_properties(submission, solution):
    """
    Compute some language and syntactically properties of the

    Args:
        submission:
        solution:

    Returns: A dict with the properties
    """
    props = {}
    if submission:
        # Compute some basic properties
        props = {LANGUAGE: get_basic_language_props(submission=submission,
                                                    solution=solution),
                 ORIGINAL: (get_basic_syntactically_props(automaton=submission,
                                                          check_if_use_non_alphabet_transitions=True,
                                                          check_num_of_non_productive=True,
                                                          check_for_dead_state=True))}

        # Remove all non-productive states and non-alphabet transitions
        submission.remove_unproductive_states()
        submission.remove_non_alphabet_transitions()

        props[REMOVED_UNPRODUCTIVE] = get_basic_syntactically_props(automaton=submission,
                                                                    check_if_use_non_alphabet_transitions=False,
                                                                    check_num_of_non_productive=False,
                                                                    check_for_dead_state=True)

    return props


def compute_properties_for_task(task: str):
    """
    Compute for each submission of the given task their properties.

    Args:
        task: The task for that we want to compute the properties.

    Returns: A dict with key = the id of the automaten and value = their properties.
    """
    # Get the solution and set the alphabet
    solution = get_solution(exercise=task)
    FiniteAutomata.set_alphabet(solution.calc_and_get_alphabet())

    # Iterate over all submission and compute for each submission their properties
    properties_dict = {}
    i = 1
    for sub in SubmissionIterator(task=task):
        properties_dict[i] = get_properties(submission=sub, solution=solution)
        i += 1
    return properties_dict


if __name__ == "__main__":
    res = compute_properties_for_task(task='A')

    import pprint

    pprint.pprint(res)
