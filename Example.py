import random

import matplotlib.pyplot as plt
import numpy as np

from wofa import FiniteAutomata
from wofa import get_submission, get_solution
from wofa import grading_weight, grading_subsets, grading_test_words
from wofa import weight_diff, weight, vis_weight, vis_diff, weight_values, surface_to_tikz

""" This file contains various examples that illustrate how the calculation of the weighting of a language works. 
    The various examples are briefly described at the point of implementation. 
    At the end of this file you can comment out the corresponding methods which examples should be executed when running
    this program.
"""

"""The task was to specify a finite automaton that describes the language that does not contain the subword "abba". 
The automaton 1 to 6 are different submissions of students for this task and sol represented a typically correct 
solution (In docs/ExampleAutomates.pdf are graphical representations of these finite automata). 
"""
sol = FiniteAutomata({0},
                     [(0, 'a', 1), (0, 'b', 0), (1, 'a', 1), (1, 'b', 2), (2, 'a', 1), (2, 'b', 3), (3, 'b', 0)],
                     {0, 1, 2, 3})

automaton1 = FiniteAutomata({0}, [(0, 'a', 2), (0, 'b', 1), (1, 'a', 2), (1, 'b', 1), (2, 'a', 2), (2, 'b', 3),
                                  (3, 'a', 2), (3, 'b', 4), (4, 'b', 2)], {0, 1, 2, 3, 4})
automaton2 = FiniteAutomata({0}, [(0, 'a', 1), (0, 'b', 1), (1, 'a', 1), (1, 'b', 2), (2, 'a', 3), (2, 'b', 3),
                                  (3, 'b', 4), (4, 'a', 1), (4, 'b', 4)], {0,1, 2, 3, 4})
automaton3 = FiniteAutomata({0}, [(0, 'a', 1), (0, 'b', 0), (1, 'a', 1), (1, 'b', 2), (2, 'a', 1), (2, 'b', 3),
                                  (3, 'b', 3), (3, 'b', 1)], {1, 2, 3})
automaton4 = FiniteAutomata({0}, [(0, 'a', 0), (0, 'b', 1), (1, 'a', 0), (1, 'b', 2), (2, 'b', 1)], {0, 1, 2})
automaton5 = FiniteAutomata({0}, [(0, 'a', 1), (0, 'b', 0), (1, 'a', 0), (1, 'b', 2), (2, 'a', 0), (2, 'b', 3),
                                  (3, 'b', 0)], {0})
automaton6 = FiniteAutomata({0}, [(0, 'a', 1), (0, 'b', 0), (1, 'a', 1), (1, 'b', 2), (2, 'a', 2), (2, 'b', 3),
                                  (3, 'a', 4), (3, 'b', 4), (4, 'a', 4), (4, 'b', 4)], {4})


def example_sym_diff(variant):
    """ This is an example of how weighting regular languages can be used in teaching. This example should clarify that
    with the weighting of the symmetrical difference between the submission and a sample solution, the quality of the
    submission can be determined. It should be noted that the lower the weight, the closer the language of the
    submission is to the language of the solution.

    Args:
        variant (string):   Determines the variant of how the words in the constant part are redistributed.
                            'words' := All words in the constant part have the same weight.
                            'wordLengths' := All word lengths in the constant part have the same weight.
    """
    print(f'Example weight of the symmetrical difference. Variant = {variant}:')

    # Determine the parameters. x is the proportion of the weight to be allocated to the constant part.
    x = 0.5
    eta = sol.get_length_longest_run() + 1
    lam = (1 - x) ** (1 / eta)

    # Determine the weight of the symmetrical difference and then print the result.
    print(f'Weight diff. Automata 1 to Solution = {weight_diff(sol, automaton1, eta, lam, variant)[2]}')
    print(f'Weight diff. Automata 2 to Solution = {weight_diff(sol, automaton2, eta, lam, variant)[2]}')
    print(f'Weight diff. Automata 3 to Solution = {weight_diff(sol, automaton3, eta, lam, variant)[2]}')
    print(f'Weight diff. Automata 4 to Solution = {weight_diff(sol, automaton4, eta, lam, variant)[2]}')
    print(f'Weight diff. Automata 5 to Solution = {weight_diff(sol, automaton5, eta, lam, variant)[2]}')
    print(f'Weight diff. Automata 6 to Solution = {weight_diff(sol, automaton6, eta, lam, variant)[2]}')
    print()


def example_weight_lang(variant):
    """ This example shows how to calculate for different automata the weight of their language. 
        The same automata are used here as in the previous example. 
        In docs/ExampleAutomates.pdf are graphical representations of these finite automata

    Args:
        variant (string):   Determines the variant of how the words in the constant part are redistributed.
                            'words' := All words in the constant part have the same weight.
                            'wordLengths' := All word lengths in the constant part have the same weight.
    """
    print(f'Example weight of a language. Variant = {variant}:')

    # Setting the alphabet.
    FiniteAutomata.set_alphabet({'a', 'b'})

    # Put the automatas in a list
    automatas = [automaton1, automaton2, automaton3, automaton4, automaton5, automaton6]

    # x is the proportion of the weight to be allocated to the constant part.
    x = 0.5

    for i in range(len(automatas)):
        # Determine the parameters. 
        eta = automatas[i].get_length_longest_run() + 1
        lam = (1 - x) ** (1 / eta)

        # Determination of weights and output of results.
        if i < 1:
            print(f'Weight Solution = {weight(automatas[i].determine(), eta, lam, variant)}')
        else:
            print(f'Weight Automata {i} = {weight(automatas[i].determine(), eta, lam, variant)}')
    print()


def example_same_weight():
    """ This example should make clear that the weight of two languages is not an indicator of how far apart they are,
        but this can only be determined by weighting the symmetrical difference. Here you can see that the languages
        a^* and b^* have the same weight, but the weight of the symmetric difference is not equal to 0.
    """
    print("Example same weight but weight Symmetric difference not 0.")

    # Setting the alphabet.
    FiniteAutomata.set_alphabet({'a', 'b'})

    # Crate the automatas for the languages a^* anb b^*
    a_star = FiniteAutomata.one_symbol_nfa('a').star()
    b_star = FiniteAutomata.one_symbol_nfa('b').star()

    # Determine the parameters.
    eta = 1
    lam = 0.8

    # Determination of weights and output of results.
    print(f'Weight a^* = {weight(a_star.determine(), eta, lam)}')
    print(f'Weight b^* = {weight(b_star.determine(), eta, lam)}')

    # Determination of the weight of the symmetrical difference.
    print(f'Weight diff. a^* to b^* = {weight_diff(a_star, b_star, eta, lam)[2]}')
    print()


def example_eta(variant):
    """ This example shows the influence of the parameter eta on the resulting weight of a language. In general it can
    be said that it makes sense to set eta to the pumping constant of the language of the automaton. The language of
    this example automaton (the language which does not contain the subword "abba") is also an example why it can make
    sense in some cases to choose eta differently, because up to and including the word length 4 there is only one word
    above the alphabet which is not in the language.

    Args:
        variant (string):   Determines the variant of how the words in the constant part are redistributed.
                            'words' := All words in the constant part have the same weight.
                            'wordLengths' := All word lengths in the constant part have the same weight.
    """
    print(f'Example of different values for eta. Variant = {variant}:')
    # Setting the alphabet.
    FiniteAutomata.set_alphabet({'a', 'b'})

    # Crate the automata object
    automaton = FiniteAutomata({0}, [(0, 'a', 2), (0, 'b', 0), (2, 'a', 2), (2, 'b', 3), (3, 'a', 2), (3, 'b', 1),
                                     (1, 'b', 0)], {0, 1, 2, 3}).determine()

    # In this example, lambda is set to a fixed value.
    lam = 0.8

    # Specify a set of etas for which the weight of the language should be determined.
    eta_values = [i for i in range(0, 11)] + [15, 20, 25, 30, 40, 50, 100, 200, 500]
    for eta in eta_values:
        s = f'Weight for eta={eta}'.ljust(20)
        s += f'= {weight(automaton, eta, lam, variant)}'
        print(s)
    print()


def example_lambda(variant):
    """ This example shows how the parameter lambda influences the weight of a language. In general, a small value of
    lambda leads to a higher weighting of shorter word lengths while larger values lead to the fact that also the longer
    word lengths flow more into the weighting. It is interesting with the example automata (the language which does not
    contain the subword "abba") used here that for the language for longer word lengths only very few words contain,
    whereby by a higher value for Lambda the weight strongly decreases.

    Args:
        variant (string):   Determines the variant of how the words in the constant part are redistributed.
                            'words' := All words in the constant part have the same weight.
                            'wordLengths' := All word lengths in the constant part have the same weight.
    """
    print(f'Example of different values for lambda. Variant = {variant}:')
    # Setting the alphabet.
    FiniteAutomata.set_alphabet({'a', 'b'})

    # Crate the automata object
    automaton = FiniteAutomata({0}, [(0, 'a', 2), (0, 'b', 0), (2, 'a', 2), (2, 'b', 3), (3, 'a', 2), (3, 'b', 1),
                                     (1, 'b', 0)], {0, 1, 2, 3}).determine()

    # In this example, eta is set to a fixed value.
    eta = automaton.get_length_longest_run() + 1

    # Specify a set of lambdas for which the weight of the language should be determined.
    lam_values = [i / 20 for i in range(1, 20)] + [0.96, 0.97, 0.98, 0.99]
    for lam in lam_values:
        s = f'Weight for lambda={lam}'.ljust(23)
        s += f'= {weight(automaton, eta, lam, variant)}'
        print(s)
    print()


def example_visualisation(variant):
    """ This method shows with a visualization how the weight is changed by the parameters. For the automaton used as a
    solution in the previous examples, the weight is calculated for different combinations of eta and lambda and
    displayed graphically.

    Args:
        variant (string):   Determines the variant of how the words in the constant part are redistributed.
                            'words' := All words in the constant part have the same weight.
                            'wordLengths' := All word lengths in the constant part have the same weight.
    """
    print("Wait a moment please for creating the visualisation....")

    # Visualisation of the weight for difference eta and lambda
    vis_weight(sol.determine(), np.arange(0, 11), 20, 'heatmap', variant)


def example_visualisation_diff(variant):
    """ This method shows with a visualization how the weight is changed by the parameters. For the automaton used as
    solution in the previous examples and the automaton named automaton 3, the weight of the symmetric difference for
    the different combination of eta and lambda is calculated and displayed graphically.

    Args:
        variant (string):   Determines the variant of how the words in the constant part are redistributed.
                            'words' := All words in the constant part have the same weight.
                            'wordLengths' := All word lengths in the constant part have the same weight.
    """
    print("Wait a moment please for creating the visualisation....")

    # Visualisation of the weight for difference eta and lambda
    vis_diff(sol, automaton3, np.arange(0, 11), 20, 'surface', variant)


def example_find_best_parameters(variant):
    """This example shows how the automates from example_sym_diff behave with different parameter values.
    This example can help to find the best parameters for the use case of evaluating student submissions.

    Args:
        variant (string):   Determines the variant of how the words in the constant part are redistributed.
                            'words' := All words in the constant part have the same weight.
                            'wordLengths' := All word lengths in the constant part have the same weight.
    """
    print("Wait a moment please for creating the visualisation....")

    # Determine the different parameters that eta and lambda should take.
    etas = np.arange(0, 11)
    lams = np.linspace(0.5, 1, 11)[:10]

    # Set the size of the figure.
    plt.figure(figsize=(len(etas), len(lams)))

    # Create the meshgrid for x and y dimension.
    x, y = np.meshgrid(etas, lams)

    # Labeling and settings of the axes.
    ax = plt.axes(projection='3d')
    ax.invert_yaxis()
    ax.set_xlabel("eta")
    ax.set_ylabel("lambda")
    ax.set_zlabel('weight')

    # Create the surfaces for the weights of the symmetrical difference between the solution and the 6 different
    # automatas from students submissions.
    ax.plot_surface(x, y, weight_values(sol.symmetric_difference(automaton1), etas, lams, variant), cmap='Greys',
                    edgecolor='grey')
    ax.plot_surface(x, y, weight_values(sol.symmetric_difference(automaton2), etas, lams, variant), cmap='Purples',
                    edgecolor='purple')
    ax.plot_surface(x, y, weight_values(sol.symmetric_difference(automaton3), etas, lams, variant), cmap='Greens',
                    edgecolor='green')
    ax.plot_surface(x, y, weight_values(sol.symmetric_difference(automaton4), etas, lams, variant), cmap='Oranges',
                    edgecolor='orange')
    ax.plot_surface(x, y, weight_values(sol.symmetric_difference(automaton5), etas, lams, variant), cmap='BuPu',
                    edgecolor='blue')
    ax.plot_surface(x, y, weight_values(sol.symmetric_difference(automaton6), etas, lams, variant), cmap='BuGn',
                    edgecolor='green')

    plt.show()
    print()


def example_tikz(variant):
    """This example shows how to create the graphical representation as surface from the previous examples
    as tikz picture.

    Args:
        variant (string):   Determines the variant of how the words in the constant part are redistributed.
                            'words' := All words in the constant part have the same weight.
                            'wordLengths' := All word lengths in the constant part have the same weight.
    """
    print("Please wait a moment the file will be created")
    surface_to_tikz(sol.symmetric_difference(automaton4), etas=np.arange(0, 15), num_lams=30, directory="tmp",
                    file_name='example', variant=variant, log_scale_fac=4,
                    labels=[0, 0.02, 0.05, 0.1, 0.2, 0.4, 0.7, 1])
    print("The file was created.")
    print()


def example_parser():
    """ So far, we have always explicitly determined our automata in this example file. However, we can also use an
    already collected dataset of student submissions. The dataset is explained in ./assets/README.
    """
    print("Example of the use of the parser")
    # Outputs the solution on the console
    print(get_solution('B'))

    # Outputs a random submission to the console for this task.
    print(get_submission('B', str(random.randint(0, 165))))
    print()


def example_grading_weight(variant):
    """  For the evaluation of student assignments, it can be useful that you do not get a weight as a result but a
    concrete score that this submission should receive. We use the grading schemata from ./docs/gradingsSchemes.
    """
    print("Example to use the weighting for concrete gradings with a point schemata based on the weight of the "
          "symmetrical difference.")

    # Determine the parameters. x is the proportion of the weight to be allocated to the constant part.
    x = 0.5
    eta = sol.get_length_longest_run() + 1
    lam = (1 - x) ** (1 / eta)

    # Set the maximum number of points and the linear displacement.
    max_po = 5
    lin_dis = 5

    # Determination of the scores
    print(f'With {float(max_po)} possible points, a suggested score for automaton1 would be: '
          f'{grading_weight(sol, automaton1, eta, lam, max_po, lin_dis, variant)}')
    print(f'With {float(max_po)} possible points, a suggested score for automaton2 would be: '
          f'{grading_weight(sol, automaton2, eta, lam, max_po, lin_dis, variant)}')
    print(f'With {float(max_po)} possible points, a suggested score for automaton3 would be: '
          f'{grading_weight(sol, automaton3, eta, lam, max_po, lin_dis, variant)}')
    print(f'With {float(max_po)} possible points, a suggested score for automaton4 would be: '
          f'{grading_weight(sol, automaton4, eta, lam, max_po, lin_dis, variant)}')
    print(f'With {float(max_po)} possible points, a suggested score for automaton5 would be: '
          f'{grading_weight(sol, automaton5, eta, lam, max_po, lin_dis, variant)}')
    print(f'With {float(max_po)} possible points, a suggested score for automaton5 would be: '
          f'{grading_weight(sol, automaton6, eta, lam, max_po, lin_dis, variant)}')
    print()


def example_grading_subsets():
    """ Another trivial approach to evaluating student solutions is to consider the subset relationships between the
    language of the sample solution and a student submission. Half of the points are awarded for each correct inclusion
    direction. This variant has the disadvantage, for example, the trivial deliveries of the full language or the empty
    language, so already half of the points are assigned.
    """
    print("Example around student submissions using the subset relationships between the submitted language and "
          "a sample solution. ")

    # Set the maximum number of points
    max_po = 2

    # Determination of the scores
    print(f'With {float(max_po)} possible points, a suggested score for automaton1 would be: '
          f'{grading_subsets(sol, automaton1, max_po)}')
    print(f'With {float(max_po)} possible points, a suggested score for automaton2 would be: '
          f'{grading_subsets(sol, automaton2, max_po)}')
    print(f'With {float(max_po)} possible points, a suggested score for automaton3 would be: '
          f'{grading_subsets(sol, automaton3, max_po)}')
    print(f'With {float(max_po)} possible points, a suggested score for automaton4 would be: '
          f'{grading_subsets(sol, automaton4, max_po)}')
    print(f'With {float(max_po)} possible points, a suggested score for automaton5 would be: '
          f'{grading_subsets(sol, automaton5, max_po)}')
    print(f'With {float(max_po)} possible points, a suggested score for automaton6 would be: '
          f'{grading_subsets(sol, automaton6, max_po)}')
    print()


def example_grading_test_words():
    """ The third approach to evaluating student submissions is that we determine for a set of test words whether they
    are categorized (accepted/rejected) in correctly by the submission.
    """
    # set the test words
    containing_words = ['a', 'ab', 'abbba', 'abbbbbb', 'aaaaabbbbbb', '']
    not_included_words = ['abba', 'ababba', 'abbabb', 'bbaabbabb']

    print(f'For example, by testing test words, we use the test words that should not be in the language: '
          f'{not_included_words} respectively that should be in the language: {containing_words}.')

    # Set the maximum number of points
    max_po = 10

    print(f'With {float(max_po)} possible points, a suggested score for automaton1 would be: '
          f'{grading_test_words(automaton1, max_po, containing_words, not_included_words)}')
    print(f'With {float(max_po)} possible points, a suggested score for automaton2 would be: '
          f'{grading_test_words(automaton2, max_po, containing_words, not_included_words)}')
    print(f'With {float(max_po)} possible points, a suggested score for automaton3 would be: '
          f'{grading_test_words(automaton3, max_po, containing_words, not_included_words)}')
    print(f'With {float(max_po)} possible points, a suggested score for automaton4 would be: '
          f'{grading_test_words(automaton4, max_po, containing_words, not_included_words)}')
    print(f'With {float(max_po)} possible points, a suggested score for automaton5 would be: '
          f'{grading_test_words(automaton5, max_po, containing_words, not_included_words)}')
    print(f'With {float(max_po)} possible points, a suggested score for automaton6 would be: '
          f'{grading_test_words(automaton6, max_po, containing_words, not_included_words)}')
    print()


if __name__ == "__main__":
    # Setting the alphabet. Important all current examples have the alphabet {a, b}.
    FiniteAutomata.set_alphabet({'a', 'b'})

    """Here you can comment out which examples should be executed when executing this file.
    """

    example_sym_diff('words')
    example_sym_diff('wordLengths')

    example_weight_lang('words')
    example_weight_lang('wordLengths')

    example_same_weight()

    example_eta('words')
    example_eta('wordLengths')

    example_lambda('words')
    example_lambda('wordLengths')

    # example_visualisation('words')
    example_visualisation('wordLengths')

    example_visualisation_diff('words')
    # example_visualisation_diff('wordLengths')

    example_find_best_parameters('words')
    # example_find_best_parameters('wordLengths')

    example_tikz('words')
    # example_tikz('wordLengths')

    example_parser()

    example_grading_weight('words')
    # example_grading('wordLengths')

    example_grading_subsets()
    example_grading_test_words()
