from FiniteAutomata import FiniteAutomata
from WeightFiniteAutomata import weight_diff, weight
""" This file contains various examples that illustrate how the calculation of the weighting of a language works. 
    The various examples are briefly described at the point of implementation. 
    At the end of this file you can comment out the corresponding methods which examples should be executed when running this program.
"""

def example_sym_diff():
    """ This is an example of how weighting regular languages can be used in teaching. The task was to specify a finite automaton that 
        describes the language that does not contain the subword "abba". The automata a_1 to a_6 are different submissions of students for this 
        task. This example should clarify that with the weighting of the symmetrical difference between the submission and a sample solution, 
        the quality of the submission can be determined. It should be noted that the lower the weight, the closer the language of the submission 
        is to the language of the solution. 
    """
    print("Example weight of the symmetrical difference:")

    # Setting the alphabet.
    FiniteAutomata.set_alphabet({'a', 'b'})

    # Create a solution object.
    sol = FiniteAutomata({0}, [(0, 'a', 2), (0, 'b', 0), (2, 'a', 2), (2, 'b', 3), (3, 'a', 2), (3, 'b', 1), (1, 'b', 0)], {0, 1, 2, 3})

    # Determine the parameters. x is the proportion of the weight to be allocated to the constant part.
    x = 0.5
    eta = sol.get_length_longest_run() + 1
    lam = (1-x)**(1/eta)

    # Loading of different finite automata over the same alphabet. 
    a_1 = FiniteAutomata({0}, [(0, 'a', 5), (0, 'b', 7), (5, 'a', 5), (5, 'b', 1), (1, 'a', 5), (1, 'b', 4), (4, 'b', 5), (7, 'a', 3), (7, 'b', 7), (3, 'a', 3), (3, 'b', 6), (6, 'a', 3), (6, 'b', 2), (2, 'b', 3)], {0, 1, 2, 3, 4, 5, 6, 7})
    a_2 = FiniteAutomata({0}, [(0, 'a', 2), (0, 'b', 2), (2, 'a', 2), (2, 'b', 3), (3, 'a', 2), (3, 'b', 4), (4, 'b', 1), (1, 'b', 1), (1, 'a', 2)], {0, 1, 2, 3, 4})
    a_3 = FiniteAutomata({0}, [(0, 'b', 0), (0, 'a', 3), (3, 'a', 3), (3, 'b', 2), (2, 'a', 3), (2, 'b', 1), (1, 'a', 4), (1, 'b', 1), (1, 'b', 3)], {1, 2, 3})
    a_4 = FiniteAutomata({0}, [(0, 'a', 0), (0, 'b', 2), (2, 'a', 0), (2, 'b', 1), (1, 'b', 2), (1, 'a', 3)], {0, 1, 2})
    a_5 = FiniteAutomata({0}, [(0, 'b', 0), (0, 'a', 1), (1, 'a', 0), (1, 'b', 2), (2, 'a', 0), (2, 'b', 3), (3, 'a', 4), (3, 'b', 0)] ,{0})
    a_6 = FiniteAutomata({0}, [(0, 'b', 0), (0, 'a', 2), (2, 'a', 2), (2, 'b', 3), (3, 'a', 3), (3, 'b', 4), (4, 'b', 4), (4, 'a', 1), (1, 'a', 1), (1, 'b', 1)], {1})

    # Determine the weight of the symmetrical difference and then print the result.
    print(f'Automata 1 diff. to Solution = {weight_diff(sol, a_1, eta, lam)[2]}')
    print(f'Automata 2 diff. to Solution = {weight_diff(sol, a_2, eta, lam)[2]}')
    print(f'Automata 3 diff. to Solution = {weight_diff(sol, a_3, eta, lam)[2]}')
    print(f'Automata 4 diff. to Solution = {weight_diff(sol, a_4, eta, lam)[2]}')
    print(f'Automata 5 diff. to Solution = {weight_diff(sol, a_5, eta, lam)[2]}')
    print(f'Automata 6 diff. to Solution = {weight_diff(sol, a_6, eta, lam)[2]}')

def example_weight_lang():
    """ This example shows how to calculate for different automata the weight of their language. 
        The same automata are used here as in the previous example.
    """
    print("Example weight of a language:")

    # Setting the alphabet.
    FiniteAutomata.set_alphabet({'a', 'b'})

    # Loading of different finite automata over the same alphabet. 
    automatas = []
    automatas.append(FiniteAutomata({0}, [(0, 'a', 2), (0, 'b', 0), (2, 'a', 2), (2, 'b', 3), (3, 'a', 2), (3, 'b', 1), (1, 'b', 0)], {0, 1, 2, 3}))
    automatas.append(FiniteAutomata({0}, [(0, 'a', 5), (0, 'b', 7), (5, 'a', 5), (5, 'b', 1), (1, 'a', 5), (1, 'b', 4), (4, 'b', 5), (7, 'a', 3), (7, 'b', 7), (3, 'a', 3), (3, 'b', 6), (6, 'a', 3), (6, 'b', 2), (2, 'b', 3)], {0, 1, 2, 3, 4, 5, 6, 7}))
    automatas.append(FiniteAutomata({0}, [(0, 'a', 2), (0, 'b', 2), (2, 'a', 2), (2, 'b', 3), (3, 'a', 2), (3, 'b', 4), (4, 'b', 1), (1, 'b', 1), (1, 'a', 2)], {0, 1, 2, 3, 4}))
    automatas.append(FiniteAutomata({0}, [(0, 'b', 0), (0, 'a', 3), (3, 'a', 3), (3, 'b', 2), (2, 'a', 3), (2, 'b', 1), (1, 'a', 4), (1, 'b', 1), (1, 'b', 3)], {1, 2, 3}))
    automatas.append(FiniteAutomata({0}, [(0, 'a', 0), (0, 'b', 2), (2, 'a', 0), (2, 'b', 1), (1, 'b', 2), (1, 'a', 3)], {0, 1, 2}))
    automatas.append(FiniteAutomata({0}, [(0, 'b', 0), (0, 'a', 1), (1, 'a', 0), (1, 'b', 2), (2, 'a', 0), (2, 'b', 3), (3, 'a', 4), (3, 'b', 0)] ,{0}))
    automatas.append(FiniteAutomata({0}, [(0, 'b', 0), (0, 'a', 2), (2, 'a', 2), (2, 'b', 3), (3, 'a', 3), (3, 'b', 4), (4, 'b', 4), (4, 'a', 1), (1, 'a', 1), (1, 'b', 1)], {1}))
    
    #x is the proportion of the weight to be allocated to the constant part.
    x = 0.5

    for i in range(len(automatas)):
        # Determine the parameters. 
        eta = automatas[i].get_length_longest_run() + 1
        lam = (1-x)**(1/eta)
        
        if i < 1: 
            print(f'Weight Solution = {weight(automatas[i].determinize(), eta, lam)}')
        else:
            print(f'Weight Automata {i} = {weight(automatas[i].determinize(), eta, lam)}')

if __name__=="__main__":
    """ Here you can comment out which examples should be executed when executing this file.
    """
    example_sym_diff()
    example_weight_lang()