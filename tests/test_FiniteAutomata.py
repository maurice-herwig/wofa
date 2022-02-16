import unittest

from wofa import FiniteAutomata


class TestFiniteAutomata(unittest.TestCase):

    def setUp(self):
        FiniteAutomata.set_alphabet({'a', 'b'})

    def test_accepts_word(self):
        # Automaton for language 'ab'
        fa = FiniteAutomata([0], [(0, 'a', 1), (1, 'b', 2)], [2])
        self.assertTrue(fa.accepts_word('ab'))
        self.assertFalse(fa.accepts_word(''))
        self.assertFalse(fa.accepts_word('a'))
        self.assertFalse(fa.accepts_word('b'))
        self.assertFalse(fa.accepts_word('ba'))
        self.assertFalse(fa.accepts_word('aa'))
        self.assertFalse(fa.accepts_word('aba'))
        self.assertFalse(fa.accepts_word('aab'))

        # Automaton for language 'a+b'
        fa = FiniteAutomata([0, 2], [(0, 'a', 1), (2, 'b', 3)], [1, 3])
        self.assertTrue(fa.accepts_word('a'))
        self.assertTrue(fa.accepts_word('b'))
        self.assertFalse(fa.accepts_word(''))
        self.assertFalse(fa.accepts_word('ab'))
        self.assertFalse(fa.accepts_word('aa'))
        self.assertFalse(fa.accepts_word('ab'))
        self.assertFalse(fa.accepts_word('bab'))
        self.assertFalse(fa.accepts_word('aaaa'))

    def test_complement(self):
        # Automaton for language 'a*'
        fa = FiniteAutomata([0], [(0, 'a', 0)], [0])
        fa.set_alphabet(['a', 'b'])
        complement = fa.complement()
        self.assertTrue(fa.accepts_word('aaa'))
        self.assertFalse(complement.accepts_word('aaa'))
        self.assertFalse(fa.accepts_word('abaa'))
        self.assertTrue(complement.accepts_word('abaa'))

        # Automaton for language 'ab'
        fa = FiniteAutomata([0], [(0, 'a', 1), (1, 'b', 2)], [2])
        complement = fa.complement()
        self.assertTrue(complement.accepts_word(''))
        self.assertTrue(complement.accepts_word('a'))
        self.assertTrue(complement.accepts_word('b'))
        self.assertTrue(complement.accepts_word('ba'))
        self.assertFalse(complement.accepts_word('ab'))

    def test_empty(self):
        # Assert
        self.assertTrue(FiniteAutomata.empty_nfa().is_empty())

        # Assert
        self.assertFalse(FiniteAutomata.full_nfa().is_empty())

    def test_equivalence(self):
        # Assume
        fa_a = FiniteAutomata.one_symbol_nfa('a')
        fa_b = FiniteAutomata.univ_symbol_nfa().star()
        fa_c = FiniteAutomata.full_nfa()

        # Assert
        self.assertTrue(fa_a.equivalence_test(fa_a)[0])
        self.assertFalse(fa_a.equivalence_test(fa_b)[0])
        self.assertTrue(fa_b.equivalence_test(fa_c)[0])

    def test_concatenation(self):
        # Assume
        fa_a = FiniteAutomata.one_symbol_nfa('a')
        fa_b = FiniteAutomata.one_symbol_nfa('b')

        # Assert
        self.assertTrue(fa_a.concatenate(fa_b).accepts_word('ab'))

    def test_union(self):
        # Assume
        fa_a = FiniteAutomata.one_symbol_nfa('a')
        fa_b = FiniteAutomata.one_symbol_nfa('b')
        fa_union = FiniteAutomata.univ_symbol_nfa()
        FiniteAutomata.set_minimization_engine(1)

        # Asset
        self.assertTrue(fa_a.union(fa_b).equivalence_test(fa_union)[0])

    def test_symmetric_difference(self):
        # Assume
        fa_a = FiniteAutomata.one_symbol_nfa('a')
        fa_b = FiniteAutomata.one_symbol_nfa('b')
        fa_diff = FiniteAutomata.univ_symbol_nfa()
        FiniteAutomata.set_minimization_engine(1)

        # Asset
        self.assertTrue(fa_a.union(fa_b).equivalence_test(fa_diff)[0])
        