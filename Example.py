from weight_finite_automata import FiniteAutomata
from weight_finite_automata import weight_diff, weight

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
    print(f'Weight diff. Automata 1 to Solution = {weight_diff(sol, a_1, eta, lam)[2]}')
    print(f'Weight diff. Automata 2 to Solution = {weight_diff(sol, a_2, eta, lam)[2]}')
    print(f'Weight diff. Automata 3 to Solution = {weight_diff(sol, a_3, eta, lam)[2]}')
    print(f'Weight diff. Automata 4 to Solution = {weight_diff(sol, a_4, eta, lam)[2]}')
    print(f'Weight diff. Automata 5 to Solution = {weight_diff(sol, a_5, eta, lam)[2]}')
    print(f'Weight diff. Automata 6 to Solution = {weight_diff(sol, a_6, eta, lam)[2]}')
    print()

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
        
        # Determination of weights and output of results.
        if i < 1: 
            print(f'Weight Solution = {weight(automatas[i].determinize(), eta, lam)}')
        else:
            print(f'Weight Automata {i} = {weight(automatas[i].determinize(), eta, lam)}')
    print()

def example_same_weight():
    """ This example should make clear that the weight of two languages is not an indicator of how far apart they are, but this can only be 
    determined by weighting the symmetrical difference. Here you can see that the languages a^* and b^* have the same weight, but the weight 
    of the symmetric difference is not equal to 0.
    """
    print("Example same weight but weight Symetric difference not 0.")

    # Setting the alphabet.
    FiniteAutomata.set_alphabet({'a', 'b'})

    # Crate the automatas for the languages a^* anb b^*
    a_star = FiniteAutomata.one_symbol_nfa('a').star()
    b_star = FiniteAutomata.one_symbol_nfa('b').star()

    # Determine the parameters.
    eta = 1
    lam = 0.8 

    # Determination of weights and output of results.
    print(f'Weight a^* = {weight(a_star.determinize(), eta, lam)}')
    print(f'Weight b^* = {weight(b_star.determinize(), eta, lam)}')

    # Determination of the weight of the symmetrical difference.
    print(f'Weigt diff. a^* to b^* = {weight_diff(a_star, b_star, eta, lam)[2]}')
    print()

def example_eta():
    """ This example shows the influence of the parameter eta on the resulting weight of a language. In general it can be said that it makes 
    sense to set eta to the pumping constant of the language of the automaton. The language of this example automaton (the language which does 
    not contain the subword "abba") is also an example why it can make sense in some cases to choose eta differently, because up to and including 
    the word length 4 there is only one word above the alphabet which is not in the language.
    """
    print("Example of different values for eta.")
    # Setting the alphabet.
    FiniteAutomata.set_alphabet({'a', 'b'})

    # Crate the automata object
    automat = FiniteAutomata({0}, [(0, 'a', 2), (0, 'b', 0), (2, 'a', 2), (2, 'b', 3), (3, 'a', 2), (3, 'b', 1), (1, 'b', 0)], {0, 1, 2, 3}).determinize()
    
    # In this example, lambda is set to a fixed value.
    lam = 0.8

    # Specify a set of etas for which the weight of the language should be determined.
    eta_values = [i for i in range(0,11)] + [15, 20, 25, 30, 40, 50, 100, 200, 500]
    for eta in eta_values:
        s = f'Weight for eta={eta}'.ljust(20)
        s += f'= {weight(automat, eta, lam)}'
        print(s)
    print()

def example_lamda():
    """ This example shows how the parameter lambda influences the weight of a language. In general, a small value of lambda leads to a higher 
    weighting of shorter word lengths while larger values lead to the fact that also the longer word lengths flow more into the weighting. It is 
    interesting with the example automata (the language which does not contain the subword "abba") used here that for the language for longer 
    word lengths only very few words contain, whereby by a higher value for Lambda the weight strongly decreases.
    """
    print("Example of different values for lambda.")
    # Setting the alphabet.
    FiniteAutomata.set_alphabet({'a', 'b'})

    # Crate the automata object
    automat = FiniteAutomata({0}, [(0, 'a', 2), (0, 'b', 0), (2, 'a', 2), (2, 'b', 3), (3, 'a', 2), (3, 'b', 1), (1, 'b', 0)], {0, 1, 2, 3}).determinize()
    
    # In this example, eta is set to a fixed value.
    eta = automat.get_length_longest_run() +1

    # Specify a set of lambdas for which the weight of the language should be determined.
    lam_values = [i/20 for i in range(1, 20)] + [0.96, 0.97, 0.98, 0.99]
    for lam in lam_values:
        s = f'Weight for lambda={lam}'.ljust(23)
        s += f'= {weight(automat, eta, lam)}'
        print(s)
    print()

if __name__=="__main__":
    """Here you can comment out which examples should be executed when executing this file.
    """

    example_sym_diff()
    example_weight_lang()
    example_same_weight()
    example_eta()
    example_lamda()