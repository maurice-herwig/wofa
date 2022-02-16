import unittest

from wofa import weight_diff, weight, vis_weight, vis_diff, weight_values, surface_to_tikz
from wofa import FiniteAutomata


class TestWeightFiniteAutomata(unittest.TestCase):

    def set_up(self):
        # Setting the alphabet
        FiniteAutomata.set_alphabet({'a', 'b'})

        self.sol = FiniteAutomata({1},
                                  [(1, 'a', 2), (1, 'b', 1), (2, 'a', 2), (2, 'b', 3), (3, 'a', 2), (3, 'b', 4),
                                   (4, 'b', 1)], {1, 2, 3, 4})

        self.automaton1 = FiniteAutomata({1}, [(1, 'a', 3), (1, 'b', 2), (2, 'a', 3), (2, 'b', 2), (3, 'a', 3),
                                               (3, 'b', 4), (4, 'a', 3), (4, 'b', 5), (5, 'b', 3)], {1, 2, 3, 4, 5})
        self.automaton2 = FiniteAutomata({1}, [(1, 'a', 2), (1, 'b', 2), (2, 'a', 2), (2, 'b', 3), (3, 'a', 2),
                                               (3, 'b', 4), (4, 'b', 5), (5, 'a', 2), (5, 'b', 5)], {1, 2, 3, 4, 5})
        self.automaton3 = FiniteAutomata({1}, [(1, 'a', 2), (1, 'b', 1), (2, 'a', 2), (2, 'b', 3), (3, 'a', 2),
                                               (3, 'b', 4), (4, 'b', 4), (4, 'b', 2)], {2, 3, 4})
        self.automaton4 = FiniteAutomata({1}, [(1, 'a', 1), (1, 'b', 2), (2, 'a', 1), (2, 'b', 3), (3, 'b', 2)],
                                         {1, 2, 3})
        self.automaton5 = FiniteAutomata({1}, [(1, 'a', 2), (1, 'b', 1), (2, 'a', 1), (2, 'b', 3), (3, 'a', 1),
                                               (3, 'b', 4), (4, 'b', 1)], {1})
        self.automaton6 = FiniteAutomata({1}, [(1, 'a', 2), (1, 'b', 1), (2, 'a', 2), (2, 'b', 3), (3, 'a', 3),
                                               (3, 'b', 4), (4, 'a', 5), (4, 'b', 4), (5, 'a', 5), (5, 'b', 5)], {5})

    def test_weight(self):
        # Assume
        self.set_up()
        eta = self.sol.get_length_longest_run() + 1

        # Assert for different values
        self.assertEqual(0.9923664122137406, weight(self.sol.determine(), 0, 0.5))
        self.assertEqual(0.9181476622137406, weight(self.sol.determine(), eta, 0.5))
        self.assertEqual(0.7011357784543253, weight(self.sol.determine(), eta, 0.9))

