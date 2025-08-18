from wofa import FiniteAutomata, SubmissionIterator, get_solution

REMOVED_UNPRODUCTIVE = 'removed_unproductive'
ORIGINAL = 'original'

NUM_STATES = 'number_of_states'
NUM_ACC_STATES = 'number_or_accepting_states'
NUM_INITIAL_STATES = 'number_of_initial_states'
NUM_OF_TRANSITIONS = 'number_of_transitions'
USE_NON_ALPHABET_TRANS = 'use_non_alphabet_transitions'
NUM_OF_UN_PROD_STATES = 'number_of_unproductive_states'
DEAD_STATE = 'exist_dead_state'


def get_basic_props(submission: FiniteAutomata,
                    check_if_use_non_alphabet_transitions=False,
                    check_num_of_non_productive=False,
                    check_for_dead_state=False):
    # Compute the transitions of the submission
    transitions = submission.get_transitions()

    # Compute some simple properties
    basic_props = {NUM_STATES: submission.get_number_of_states(),
                   NUM_ACC_STATES: len(submission.get_finals()),
                   NUM_INITIAL_STATES: len(submission.get_initials()),
                   NUM_OF_TRANSITIONS: len(transitions)}

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
        basic_props[NUM_OF_UN_PROD_STATES] = (submission.get_number_of_states() - len(submission.productive()))

    # Additionally check if a dead state exits
    if check_for_dead_state:

        exists_dead_state = False

        # Check for each state if it is a dead state
        for q in range(submission.get_number_of_states()):
            if q not in submission.finals:

                is_dead_state = True
                letters = set()
                for p, a in submission.get_all_predecessors_with_letter(s=q):
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

    return basic_props


def check_for_properties(task: str):
    # Get the solution and set the alphabet
    solution = get_solution(exercise=task)
    FiniteAutomata.set_alphabet(solution.calc_and_get_alphabet())

    res = {}

    i = 1

    for sub in SubmissionIterator(task=task):
        props = {ORIGINAL: (get_basic_props(submission=sub,
                                            check_if_use_non_alphabet_transitions=True,
                                            check_num_of_non_productive=True,
                                            check_for_dead_state=True))}

        # Remove all non-productive states and non-alphabet transitions
        sub.remove_unproductive_states()
        sub.remove_non_alphabet_transitions()

        props[REMOVED_UNPRODUCTIVE] = get_basic_props(submission=sub,
                                                      check_if_use_non_alphabet_transitions=False,
                                                      check_num_of_non_productive=False,
                                                      check_for_dead_state=True)

        # Add the properties of this automaton to the res dict
        res[i] = props
        i += 1

        # TODO wieder weg
        import pprint
        pprint.pprint(props)
        break


if __name__ == "__main__":
    check_for_properties(task='A')
