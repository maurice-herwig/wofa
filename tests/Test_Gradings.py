import unittest

import wofa
from wofa import FiniteAutomata
from wofa import grading_weight, grading_subsets, grading_test_words


class TestGradings(unittest.TestCase):

    def setUp(self):
        # Setting the alphabet
        FiniteAutomata.set_alphabet({'a', 'b'})

    def test_grading_weight_1(self):
        # Assume
        sol = FiniteAutomata({1},
                             [(1, 'a', 2), (1, 'b', 1), (2, 'a', 2), (2, 'b', 3), (3, 'a', 2), (3, 'b', 4),
                              (4, 'b', 1)], {1, 2, 3, 4})
        test_obj = FiniteAutomata({1}, [(1, 'a', 2), (1, 'b', 2), (2, 'a', 2), (2, 'b', 3), (3, 'a', 2), (3, 'b', 4),
                                        (4, 'b', 5), (5, 'a', 2), (5, 'b', 5)], {1, 2, 3, 4, 5})

        # Test
        points = grading_weight(sol, test_obj, sol.get_length_longest_run(), 0.8, 10, 6,
                                grading_variant=wofa.GRADING_VARIANT_WEIGHTED)

        # Asserts
        self.assertEqual(9, points)

    def test_grading_weight_2(self):
        # Assume
        sol = FiniteAutomata.one_symbol_nfa('a').union(FiniteAutomata.one_symbol_nfa('b'))
        test_obj = FiniteAutomata.one_symbol_nfa('a').union(FiniteAutomata.one_symbol_nfa('b')).star()

        # Test
        points = grading_weight(sol, test_obj, sol.get_length_longest_run(), 0.8, 10, 5)

        # Asserts
        self.assertEqual(0, points)

    def test_grading_weight_3(self):
        # Assume
        sol = FiniteAutomata.one_symbol_nfa('a').union(FiniteAutomata.one_symbol_nfa('b'))
        test_obj = FiniteAutomata.one_symbol_nfa('a').union(FiniteAutomata.one_symbol_nfa('b')).star()

        # Test
        points = grading_weight(sol, test_obj, sol.get_length_longest_run(), 0.8, 10, 5,
                                grading_variant=wofa.GRADING_VARIANT_HARMONIC)

        # Asserts
        self.assertEqual(0, points)

    def test_grading_false_variant(self):
        # Assume
        sol = FiniteAutomata.one_symbol_nfa('a').union(FiniteAutomata.one_symbol_nfa('b'))
        test_obj = FiniteAutomata.one_symbol_nfa('a').union(FiniteAutomata.one_symbol_nfa('b')).star()

        # Test
        points = grading_weight(sol, test_obj, sol.get_length_longest_run(), 0.8, 10, 5, grading_variant='')

        # Asserts
        self.assertEqual(None, points)

    def test_grading_subsets(self):
        # Assume
        sol = FiniteAutomata.one_symbol_nfa('a').star().union(FiniteAutomata.one_symbol_nfa('b'))
        test_obj = FiniteAutomata.one_symbol_nfa('a').union(FiniteAutomata.one_symbol_nfa('b'))

        # Tests and Asserts
        self.assertEqual(1, grading_subsets(sol, test_obj, 2))
        self.assertEqual(1, grading_subsets(test_obj, sol, 2))

    def test_grading_test_words(self):
        # Assume
        test_obj = FiniteAutomata.one_symbol_nfa('a').star().union(FiniteAutomata.one_symbol_nfa('b'))
        containing_words = ['b', 'a', 'aaaaaaaa' '']
        not_included_words = ['bb']

        # Tests and Asserts
        self.assertEqual(5, grading_test_words(test_obj, 5, containing_words, not_included_words))
