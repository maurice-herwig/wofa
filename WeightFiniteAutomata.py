from FiniteAutomata import FiniteAutomata
from collections import defaultdict
import numpy as np

def weight_diff(fa_a, fa_b, eta, lam):
    """Method determines the weight of the symmetric difference of two finite automata. 
    The result can be used as a value describing how far apart the languages of the automata are from each other.  

    Args:
        fa_a (FiniteAutomata):  One of the two finite automaton on whose symmetric difference the weight is to be formed.
        fa_b (FiniteAutomata):  One of the two finite automaton on whose symmetric difference the weight is to be formed.
        eta (int):              Threshold value up to which the weight of words should be evaluated constantly.
        lam (float):            Decay rate that describes how much the weighting of the individual words decreases with increasing word length.

    Returns:
        float, float, float: 1, 2, 3
                                1: The weight of the language containing the words contained only in fa_a and not in fa_b. 
                                2: The weight of the language containing the words contained only in fa_b and not in fa_a. 
                                3: The weight of the symmetrical difference.
    """
    sym_diff = fa_a.symetrical_difference(fa_b)

    if not sym_diff[0].is_empty():
        weight_a_sub_b = weight(sym_diff[0], eta, lam)
    else:
       weight_a_sub_b = 0

    if not sym_diff[1].is_empty():
        weight_b_sub_a = weight(sym_diff[1], eta, lam)
    else:
       weight_b_sub_a = 0

    return weight_a_sub_b, weight_b_sub_a, (weight_a_sub_b + weight_b_sub_a)

def weight(dfa, eta, lam):
    """ Determining the weight of a language described by a deterministic finite automaton.

    !!!Important!!! The input of the parameter dfa must be a deterministic finite automaton.
                    For not deterministic finite automaton it is not possible to determine the weight.
    Args:
        dfa (FiniteAutomata):   The deterministic finite automaton on which the weight of the language is to be determined.
        eta (int):              Threshold value up to which the weight of words should be evaluated constantly.
        lam (float):            Decay rate that describes how much the weighting of the individual words decreases with increasing word length.

    Returns:
        float: [description]
    """
    weight = __explicit_solution(dfa, lam) 
    weight += __weight_with_matrix(dfa, eta, lam) 
    weight -= __weight_with_matrix(dfa, 0, lam, eta + 1) 

    return weight
    
def __explicit_solution(dfa, lam):
    """Explicit solution of the weight by means of a linear equation system. However, the redistribution of the initial word lengths is not taken 
    into account.

    Args:
        dfa (FiniteAutomata):   The deterministic finite automaton on which the weight of the language is to be determined.
        lam (float):            Decay rate that describes how much the weighting of the individual words decreases with increasing word length.

    Returns:
        float: The weight of the language of the automaton.
    """
    w_one_trans = lam/len(FiniteAutomata.get_alphabet()) 
    ls = []   
    sol_vec = []

    # Set up the linear system of equations.
    for q in range(dfa.get_number_of_states()):
        slice = []
        number_of_letters = defaultdict(int)
        for (p,_ ) in dfa.get_all_succesors_with_letter(q):
            number_of_letters[p] += 1

        for p in range(dfa.get_number_of_states()):
            if p == q:
                slice.append(number_of_letters[p] * w_one_trans -1)
            else:
                slice.append(number_of_letters[p] * w_one_trans)

        ls.append(slice)
        if q in dfa.get_finals():
            sol_vec.append(- (1 - lam))
        else:
            sol_vec.append(0)

    # Solving the system of linear equations.
    ls = np.array(ls)
    sol_vec = np.array(sol_vec)
    res = np.linalg.solve(ls, sol_vec)

    return res[min(dfa.get_initials())]

def __weight_with_matrix(dfa, eta, lam, up_to = 0): 
    """ Calculates the weight of the language of the DFA approximately using matrices. Only the worlengths up to max(eta, up_to) are considered 
    and the rest of the weight of the language is considered as imprecision. Therefore, this method is also useful to determine the weight of 
    words in the constant part or the weight up to eta without redistribution.

    Args:
        dfa (FiniteAutomata):   The deterministic finite automaton on which the weight of the language is to be determined.
        eta (int):              Threshold value up to which the weight of words should be evaluated constantly.
        lam (float):            Decay rate that describes how much the weighting of the individual words decreases with increasing word length.
        up_to (int, optional):  Determines up to which word length the calculation is performed. Default value 0 means that the exponential decaying 
                                part is not calculated.
    """
    matrix = Matrix(dfa)
    size_of_alpabet = len(FiniteAutomata.get_alphabet())
    weight = 0
    weight_ex_part = 0

    # Determination of the weight of the part of speech in which the words are evaluated with constant weight. 
    max_words_in_c_p = (1-size_of_alpabet**(eta + 1))/(1-size_of_alpabet)
    sum_w_c_p = 1 - lam**(eta + 1)
    w_of_one_word_c_p = sum_w_c_p/max_words_in_c_p

    if not dfa.get_initials().isdisjoint(dfa.get_finals()):
        weight += w_of_one_word_c_p

    for i in range(1, eta + 1):
        words_of_length_i = round(matrix.get_share(i) * (size_of_alpabet**i))
        weight += w_of_one_word_c_p * words_of_length_i
    
    # Determination of the weight of the exponentially decaying part.
    for i in range(eta + 1,  up_to):
        weight_ex_part += matrix.get_share(i)  * (lam**(i+1))

    # Divide weight by the limit value of the sum (Geometric series).
    weight_ex_part = weight_ex_part * ((1-lam)/(lam))
    weight += weight_ex_part
    
    return weight

class Matrix:
    """Class that contains the matrices needed to calculate the weight of a language and if needed determines the matrices for further word lengths.
    """
    def __init__(self, fa):
        """ Constructor of the matrix class.

        Args:
            fa (FiniteAutomata): Finite automaton for which the matrices are created.
        """
        self.fa = fa
        self.dimension = fa.get_number_of_states()
        self.size_of_alpabet = len(FiniteAutomata.get_alphabet())
        self.matrixs = {}
        self.__initial_matrix()

    def __initial_matrix(self):
        """Creating the initial matrix for the word length 1.
        """
        matrix = []
        for i in range(self.dimension):
            number_of_letters = defaultdict(int)
            this_dimension = []
            
            for (j, _) in self.fa.get_all_succesors_with_letter(i):
                number_of_letters[j] +=1

            for j in range(self.dimension):
                this_dimension.append(number_of_letters[j]/self.size_of_alpabet)

            matrix.append(this_dimension)

        self.matrixs[1] = np.array(matrix)

    def get_matrix(self, i):
        """ Returns the matrix for the word length i and if this has not yet been calculated, the method also determines the matrix for this word length.

        Args:
            i (int): Word length.

        Returns:
            Matrix: The matrix of the word length i.
        """
        if i in self.matrixs.keys():
            return self.matrixs[i]

        elif i-1 in self.matrixs.keys():
            before = self.matrixs[i-1]
            first = self.matrixs[1]
            new_matrix = np.matmul(before, first)
            self.matrixs[i] = new_matrix
            return new_matrix

        else:
            self.get_matrix(i-1)

    def get_share(self, i):	
        """ Returns the proportion of language accepting words of length i relative to all words of length i. 

        Args:
            i (int): Word length.

        Returns:
            float: Proportion of accepting words of length i.
        """
        if i < 1:
            return 0

        matrix = self.get_matrix(i)
        share = 0
        for initial in self.fa.get_initials():
            for final in self.fa.get_finals():
                share += matrix[initial][final]

        return share