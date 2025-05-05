import unittest

from wofa import FiniteAutomata
from wofa import get_submission, get_solution


class TestParser(unittest.TestCase):

    def setUp(self):
        # Setting the alphabet
        FiniteAutomata.set_alphabet({'a', 'b'})

    def test_get_submission(self):
        # Assume
        fa = FiniteAutomata({0},
                            [(0, 'b', 0), (0, 'a', 1), (1, 'a', 1), (1, 'b', 2), (2, 'a', 1), (2, 'b', 3), (3, 'a', 4),
                             (3, 'b', 0), (4, 'a', 4), (4, 'b', 4)], {0, 1, 2, 3})

        # Test
        submission = get_submission('B', '1')

        # Asserts
        self.assertTrue(fa.equivalence_test(submission))
        self.assertEqual(fa.get_initials(), submission.get_initials())
        self.assertEqual(fa.get_finals(), submission.get_finals())
        self.assertEqual(fa.get_transitions(), submission.get_transitions())

    def test_get_solution(self):
        # Assume
        fa = FiniteAutomata({0}, [(0, 'a', 1), (0, 'b', 0), (1, 'a', 1), (1, 'b', 2), (2, 'a', 1), (2, 'b', 3),
                                  (3, 'b', 0)], {0, 1, 2, 3})

        # Test
        solution = get_solution('B')

        # Asserts
        self.assertTrue(fa.equivalence_test(solution))
        self.assertEqual(fa.get_initials(), solution.get_initials())
        self.assertEqual(fa.get_finals(), solution.get_finals())
        self.assertEqual(fa.get_transitions(), solution.get_transitions())

    def test_file_not_found(self):
        # Assert
        self.assertRaises(Exception, get_solution('Z'))
        self.assertRaises(Exception, get_submission('A', str(100000)))
