import unittest
import numpy as np

from wofa import weight_diff, weight, vis_weight, vis_diff, weight_values, surface_to_tikz
from wofa import FiniteAutomata


class TestWeightFiniteAutomata(unittest.TestCase):

    def setUp(self):
        # Setting the alphabet
        FiniteAutomata.set_alphabet({'a', 'b'})

    def test_weight(self):
        # Assume
        fa = FiniteAutomata.one_symbol_nfa('a').star()

        # Assert for different values
        self.assertEqual(0.6666666666666665, weight(fa.determine(), 0, 0.5))
        self.assertEqual(0.09391276041666663, weight(fa.determine(), 5, 0.5))
        self.assertEqual(0.18181818181818177, weight(fa.determine(), 0, 0.9))

    def test_sym_diff(self):
        # Assume
        fa_a = FiniteAutomata.one_symbol_nfa('a').star()
        fa_b = FiniteAutomata.one_symbol_nfa('b').star()

        # Assert
        self.assertEqual((0, 0, 0),
                         weight_diff(fa_a, fa_a, 0, 0.5))
        self.assertEqual((0.16666666666666666, 0.16666666666666666, 0.3333333333333333),
                         weight_diff(fa_a, fa_b, 0, 0.5))

    def test_weight_other_variant(self):
        # Assume
        fa_a = FiniteAutomata.one_symbol_nfa('a').star()

        # Assert
        self.assertEqual(0.15525569744318177, weight(fa_a.determine(), 5, 0.9, 'wordLengths'))
        self.assertRaises(ValueError, weight,  fa_a.determine(), 5, 0.9, 'abc')

    def test_visualisations(self):
        # Assume
        fa_a = FiniteAutomata.one_symbol_nfa('a').star().determine()
        fa_b = FiniteAutomata.one_symbol_nfa('b').star()

        # Currently only control if the graphics are created without errors not if they are correct.
        vis_weight(fa_a, np.arange(0, 3), 3, 'heatmap', 'words')
        vis_weight(fa_a, np.arange(0, 3), 3, 'surface', 'words')
        vis_diff(fa_a, fa_b, np.arange(0, 3), 3, 'heatmap', 'wordLengths')
        vis_diff(fa_a, fa_b, np.arange(0, 3), 3, 'surface', 'wordLengths')

    def test_false_vis_type(self):
        # Assume
        fa_a = FiniteAutomata.one_symbol_nfa('a').star().determine()
        fa_b = FiniteAutomata.one_symbol_nfa('b').star()

        # Assert
        self.assertRaises(ValueError, vis_weight, fa_a, np.arange(0, 3), 3, 'abc', 'words')
        self.assertRaises(ValueError, vis_diff, fa_a, fa_b, np.arange(0, 3), 3, 'abc', 'wordLengths')





