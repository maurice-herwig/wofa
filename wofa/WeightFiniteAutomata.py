from wofa import FiniteAutomata
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import math
import os
import pathlib


"""=====================================================================================================================
   Methods to determine the weight.
   =====================================================================================================================
"""


def weight_diff(fa_a, fa_b, eta, lam, variant='words'):
    """Method determines the weight of the symmetric difference of two finite automata. 
    The result can be used as a value describing how far apart the languages of the automata are from each other.  

    Args:
        fa_a (FiniteAutomata):      One of the two finite automaton on whose symmetric difference the weight is
                                    to be formed.
        fa_b (FiniteAutomata):      One of the two finite automaton on whose symmetric difference the weight is
                                    to be formed.
        eta (int):                  Threshold value up to which the weight of words should be evaluated constantly.
        lam (float):                Decay rate that describes how much the weighting of the individual words
                                    decreases with increasing word length.
        variant (string, optional): Determines the variant of how the words in the constant part are redistributed.
                                    'words' := All words in the constant part have the same weight.
                                    'wordLengths' := All word lengths in the constant part have the same weight.
                                    Default value 'word'

    Returns:
        float, float, float: 1, 2, 3
                            1: The weight of the language containing the words contained only in fa_a and not in fa_b.
                            2: The weight of the language containing the words contained only in fa_b and not in fa_a.
                            3: The weight of the symmetrical difference.
    """
    sym_diff = fa_a.subsets_symmetric_difference(fa_b)
    weight_a_sub_b = 0
    weight_b_sub_a = 0

    if not sym_diff[0].is_empty():
        weight_a_sub_b = weight(sym_diff[0], eta, lam, variant)

    if not sym_diff[1].is_empty():
        weight_b_sub_a = weight(sym_diff[1], eta, lam, variant)

    return weight_a_sub_b, weight_b_sub_a, (weight_a_sub_b + weight_b_sub_a)


def weight(dfa, eta, lam, variant='words'):
    """ Determining the weight of a language described by a deterministic finite automaton.

    !!!Important!!! The input of the parameter dfa must be a deterministic finite automaton.
                    For not deterministic finite automaton it is not possible to determine the weight.
    Args:
        dfa (FiniteAutomata):       The deterministic finite automaton on which the weight of the language is
                                    to be determined.
        eta (int):                  Threshold value up to which the weight of words should be evaluated constantly.
        lam (float):                Decay rate that describes how much the weighting of the individual words decreases
                                    with increasing word length.
        variant (string, optional): Determines the variant of how the words in the constant part are redistributed.
                                    'words' := All words in the constant part have the same weight.
                                    'wordLengths' := All word lengths in the constant part have the same weight.
                                    Default value 'word'
    """
    w = __explicit_solution(dfa, lam)
    w += __weight_with_matrix(dfa, eta, lam, variant=variant)
    w -= __weight_with_matrix(dfa, 0, lam, eta + 1, variant=variant)

    return w


"""=====================================================================================================================
   Auxiliary methods for determining the weighting.
   =====================================================================================================================
"""


def __explicit_solution(dfa, lam):
    """Explicit solution of the weight by means of a linear equation system. However, the redistribution of the initial
    word lengths is not taken into account.

    Args:
        dfa (FiniteAutomata):   The deterministic finite automaton on which the weight of the language is
                                to be determined.
        lam (float):            Decay rate that describes how much the weighting of the individual words decreases with
                                increasing word length.

    Returns:
        float: The weight of the language of the automaton.
    """
    w_one_trans = lam / len(FiniteAutomata.get_alphabet())
    ls = []
    sol_vec = []

    # Set up the linear system of equations.
    for q in range(dfa.get_number_of_states()):
        slices = []
        number_of_letters = defaultdict(int)
        for (p, _) in dfa.get_all_successors_with_letter(q):
            number_of_letters[p] += 1

        for p in range(dfa.get_number_of_states()):
            if p == q:
                slices.append(number_of_letters[p] * w_one_trans - 1)
            else:
                slices.append(number_of_letters[p] * w_one_trans)

        ls.append(slices)
        if q in dfa.get_finals():
            sol_vec.append(- (1 - lam))
        else:
            sol_vec.append(0)

    # Solving the system of linear equations.
    ls = np.array(ls)
    sol_vec = np.array(sol_vec)
    res = np.linalg.solve(ls, sol_vec)

    return res[min(dfa.get_initials())]


def __weight_with_matrix(dfa, eta, lam, up_to=0, variant='words'):
    """ Calculates the weight of the language of the DFA approximately using matrices. Only the word lengths 
    up to max(eta, up_to) are considered and the rest of the weight of the language is considered as imprecision. 
    Therefore, this method is also useful to determine the weight of words in the constant part or the weight up to eta 
    without redistribution.

    Args:
        dfa (FiniteAutomata):       The deterministic finite automaton on which the weight of the language is
                                    to be determined.
        eta (int):                  Threshold value up to which the weight of words should be evaluated constantly.
        lam (float):                Decay rate that describes how much the weighting of the individual words decreases
                                    with increasing word length.
        up_to (int, optional):      Determines up to which word length the calculation is performed. Default value 0
                                    means that the exponential decaying part is not calculated.
        variant (string, optional): Determines the variant of how the words in the constant part are redistributed.
                                    'words' := All words in the constant part have the same weight.
                                    'wordLengths' := All word lengths in the constant part have the same weight.
                                    Default value 'word'
    """
    matrix = Matrix(dfa)
    w = 0
    weight_ex_part = 0

    # Determination of the weight of the part of speech in which the words are evaluated with constant weight.
    sum_w_c_p = 1 - lam ** (eta + 1)

    if variant == 'words':
        # Determination of the number of words by means of the Geometric Series
        max_words_in_c_p = (1 - len(FiniteAutomata.get_alphabet()) ** (eta + 1)) / (
                1 - len(FiniteAutomata.get_alphabet()))

        w_of_one_word_c_p = sum_w_c_p / max_words_in_c_p

        if not dfa.get_initials().isdisjoint(dfa.get_finals()):
            w += w_of_one_word_c_p

        for i in range(1, eta + 1):
            words_of_length_i = round(matrix.get_share(i) * (len(FiniteAutomata.get_alphabet()) ** i))
            w += w_of_one_word_c_p * words_of_length_i

    elif variant == 'wordLengths':
        w_of_wl = sum_w_c_p / (eta + 1)
        if not dfa.get_initials().isdisjoint(dfa.get_finals()):
            w += w_of_wl

        for i in range(1, eta + 1):
            w += matrix.get_share(i) * w_of_wl

    else:
        raise ValueError("Wrong variant for determining the weight")

    # Determination of the weight of the exponentially decaying part.
    for i in range(eta + 1, up_to):
        weight_ex_part += matrix.get_share(i) * (lam ** (i + 1))

    # Divide weight by the limit value of the sum (Geometric series).
    weight_ex_part = weight_ex_part * ((1 - lam) / lam)
    w += weight_ex_part

    return w


"""=====================================================================================================================
   Methods for visualization of various parameters evaluate.
   =====================================================================================================================
"""


def vis_weight(dfa, etas, num_lams, vis_type='heatmap', variant='words'):
    """ Visualize the weight results in a 3 dimensional figure with different values for eta and lambda.
    !!!Important!!! The input of the parameter dfa must be a deterministic finite automaton.
                    For not deterministic finite automaton it is not possible to determine the weight.

    Args:
        dfa (FiniteAutomata):       The deterministic finite automaton on which the weights of the language for
                                    different values is to be determined.
        etas (list of integer):     List with values that eta should accept for the visualisation.
        num_lams (integer):         Number of different values Lambda should take.
        vis_type (str, optional):   Type of the visualisation: 'surface' or 'heatmap'. Defaults to 'heatmap'.
        variant (string, optional): Determines the variant of how the words in the constant part are redistributed.
                                    'words' := All words in the constant part have the same weight.
                                    'wordLengths' := All word lengths in the constant part have the same weight.
                                    Default value 'word'
    """
    # Uniformly distributed selection of the lambda values for which the weight is to be determined.
    lams = np.linspace(0.5, 1, num_lams + 1)[:num_lams]

    # set the size of the figure
    plt.figure(figsize=(len(etas), num_lams))

    # Calculate the weights
    z = weight_values(dfa, etas, lams, variant)

    # create a surface plot
    if vis_type == 'surface':
        x, y = np.meshgrid(etas, lams)
        ax = plt.axes(projection='3d')
        ax.invert_xaxis()
        ax.set_xlabel("eta")
        ax.set_ylabel("lambda")
        ax.set_zlabel('weight')
        ax.plot_surface(x, y, z, cmap='viridis', edgecolor='green')

    # create a heatmap
    elif vis_type == 'heatmap':
        plt.style.use("seaborn")
        ax = sns.heatmap(z, linewidth=1, annot=True, cbar_kws={'label': 'weight'})
        ax.invert_yaxis()
        ax.set_xticklabels(etas)
        ax.set_yticklabels([round(i, 2) for i in lams], rotation=0)
        plt.xlabel("eta")
        plt.ylabel("lambda")

    else:
        raise ValueError("False visualisation type.")

    plt.show()


def vis_diff(fa_a, fa_b, etas, num_lams, vis_type='heatmap', variant='words'):
    """ Visualize the weight of the symmetric difference of two finite automata in a 3 dimensional figure with different
    values for eta and lambda.

    Args:
        fa_a (FiniteAutomata):      One of the two finite automaton on whose symmetric difference the weight is
                                    to be formed.
        fa_b (FiniteAutomata):      One of the two finite automaton on whose symmetric difference the weight is
                                    to be formed.
        etas (list of integer):     List with values that eta should accept for the visualisation.
        num_lams (integer):         Number of different values Lambda should take.
        vis_type (str, optional):   Type of the visualisation: 'surface' or 'heatmap'. Defaults to 'heatmap'.
        variant (string, optional): Determines the variant of how the words in the constant part are redistributed.
                                    'words' := All words in the constant part have the same weight.
                                    'wordLengths' := All word lengths in the constant part have the same weight.
                                    Default value 'word'
    """
    # Uniformly distributed selection of the lambda values for which the weight is to be determined.
    lams = np.linspace(0.5, 1, num_lams + 1)[:num_lams]

    lams = np.append(lams, 0.99)
    lams = np.append(lams, 0.995)
    num_lams += 2

    # set the size of the figure
    plt.figure(figsize=(len(etas), num_lams))

    # create a surface plot
    if vis_type == 'surface':
        # Determine the x, y and z values.
        x, y = np.meshgrid(etas, lams)
        z1, z2, z3 = __weight_sym_values(fa_a, fa_b, etas, lams)

        # Labeling and settings of the axes.
        ax = plt.axes(projection='3d')
        ax.invert_yaxis()
        ax.set_xlabel("eta")
        ax.set_ylabel("lambda")
        ax.set_zlabel('weight')

        # Add the surfaces.
        ax.plot_surface(x, y, z1, cmap='Greens', edgecolor='green')
        ax.plot_surface(x, y, z2, cmap='Oranges', edgecolor='orange')
        ax.plot_surface(x, y, z3, cmap='Greys', edgecolor='grey')

        # Add the legend.
        fake2_d_line1 = mpl.lines.Line2D([0], [0], linestyle="none", c='grey', marker='o')
        fake2_d_line2 = mpl.lines.Line2D([0], [0], linestyle="none", c='green', marker='o')
        fake2_d_line3 = mpl.lines.Line2D([0], [0], linestyle="none", c='orange', marker='o')
        ax.legend([fake2_d_line1, fake2_d_line2, fake2_d_line3],
                  ['Weight of symmetrical difference', 'Weight of words only in FA a', 'Weight of words only in FA a'],
                  numpoints=1)

    # create a heatmap
    elif vis_type == 'heatmap':
        # Determine the symmetrical difference of the two finite automata
        dfa = fa_a.symmetric_difference(fa_b)

        # Calculate the weights
        z = weight_values(dfa, etas, lams, variant)

        # Create the heatmap
        plt.style.use("seaborn")
        ax = sns.heatmap(z, linewidth=1, annot=True, cbar_kws={'label': 'weight'})
        ax.invert_yaxis()
        ax.set_xticklabels(etas)
        ax.set_yticklabels([round(i, 3) for i in lams], rotation=0)
        plt.xlabel("eta")
        plt.ylabel("lambda")

    else:
        raise ValueError("False visualisation type.")

    plt.show()


def weight_values(dfa, etas, lams, variant='words'):
    """ Determines the weight for all combinations of eta and lambda of a given determinate finite automaton.
    !!!Important!!! The input of the parameter dfa must be a deterministic finite automaton.
                    For not deterministic finite automaton it is not possible to determine the weight.

    Args:
        dfa (FiniteAutomata):       The deterministic finite automaton on which the weights of the language for
                                    different values is to be determined.
        etas (list of integer):     List with values that eta should accept for he calculation of weights.
        lams (list of floats):      List of values that lambda should accept for the calculation of weights.
        variant (string, optional): Determines the variant of how the words in the constant part are redistributed.
                                    'words' := All words in the constant part have the same weight.
                                    'wordLengths' := All word lengths in the constant part have the same weight.
                                    Default value 'word'

    Returns:
        numpy.array: A numpy array containing the weight for all lambda and eta combinations. 
    """
    res = []
    for lam in lams:
        i_res = []
        for eta in etas:
            i_res.append(weight(dfa, eta, lam, variant))
        res.append(i_res)

    return np.array(res)


def __weight_sym_values(fa_a, fa_b, etas, lams, variant='words'):
    """ Determines all weights of the symmetric difference as well as the weights of the two disjoint subsets
    for the given values of eta and lambda.

    Args:
        fa_a (FiniteAutomata):      One of the two finite automaton on whose symmetric difference the weight is
                                    to be formed.
        fa_b (FiniteAutomata):      One of the two finite automaton on whose symmetric difference the weight is
                                    to be formed.
        etas (list of integer):     List with values that eta should accept for he calculation of weights.
        lams (list of floats):      List of values that lambda should accept for the calculation of weights.
        variant (string, optional): Determines the variant of how the words in the constant part are redistributed.
                                    'words' := All words in the constant part have the same weight.
                                    'wordLengths' := All word lengths in the constant part have the same weight.
                                    Default value 'word'

    Returns:
        numpy.array, numpy.array, numpy.array: 1, 2, 3
                        1: The weights of the language containing the words contained only in fa_a and not in fa_b.
                        2: The weights of the language containing the words contained only in fa_b and not in fa_a.
                        3: The weights of the symmetrical difference.
    """
    res_a_sub_b = []
    res_b_sub_a = []
    res_w = []

    for lam in lams:
        i_res_a_sub_b = []
        i_res_b_sub_a = []
        i_res_w = []
        for eta in etas:
            w0, w1, w2 = weight_diff(fa_a, fa_b, eta, lam, variant)
            i_res_a_sub_b.append(w0)
            i_res_b_sub_a.append(w1)
            i_res_w.append(w2)

        res_a_sub_b.append(i_res_a_sub_b)
        res_b_sub_a.append(i_res_b_sub_a)
        res_w.append(i_res_w)

    return np.array(res_a_sub_b), np.array(res_b_sub_a), np.array(res_w)


def surface_to_tikz(dfa, etas, num_lams, directory, file_name, variant='words', log_scale_fac=0, labels=np.linspace(0, 1, 11)):
    """ Creates a tikzpicture in a separate file to include it in an existing LaTex project. This will create a 3
    dimensional graph of the weighting of the given deterministic finite automaton for different values of
    eta and lambda.
    !!!Important!!! The input of the parameter dfa must be a deterministic finite automaton.
                    For not deterministic finite automaton it is not possible to determine the weight.

    Args:
        dfa (FiniteAutomata):       The deterministic finite automaton on which the weights of the language for
                                    different values is to be determined.
        etas (list of integer):     List with values that eta should accept for he calculation of weights.
        num_lams (integer):         Number of different values Lambda should take.
        directory (string):         Directory in which the file should be written.
        file_name (string):         Name of the .tex File.
        variant (string, optional): Determines the variant of how the words in the constant part are redistributed.
                                    'words' := All words in the constant part have the same weight.
                                    'wordLengths' := All word lengths in the constant part have the same weight.
                                    Default value 'word'
        log_scale_fac(integer):     Specifies how strong the logarithmic consumption of the z axis should be.
                                    Default value 0 means that no consumption is made.
        labels(list of floats):     Labels to be placed on the z axis.
                                    Default value [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

    """

    # Uniformly distributed selection of the lambda values for which the weight is to be determined.
    lams = np.linspace(0.5, 1, num_lams + 1)[:num_lams]

    # Create the directory if it does not exist.
    path_dir = os.path.join(pathlib.Path(__file__).parent.parent.resolve(), directory)
    if not os.path.exists(path_dir):
        os.mkdir(path_dir)

    # Crate a new .tex file.
    path_file = os.path.join(path_dir, file_name)
    f = open(f'{path_file}.tex', 'w')

    # Write the begin of the tikzpicture definition in the file.
    f.write(r'\begin{tikzpicture}' + "\n" + "\n" +
            r'\begin{axis}' + "[" + "\n" +
            "\t" + "view = {25}{30}, %Here you can set the angles of the axes 1: orizontal angle 2: vertical angle" + "\n" +
            "\t" + "colormap/jet, " + "\n" +
            "\t" + "colorbar left," + "\n" +
            "\t" + "xlabel={$\eta$}," + "\n" +
            "\t" + "ylabel={$\lambda$}," + "\n" +
            "\t" + "zlabel={weight}," + "\n" +
            "\t" + "zmin=0," + "\n" +
            "\t" + f'zmax=1.0,' + "\n")

    # Map the new values to the original label values.
    s_labels = 'zticklabels={'
    s_values = 'ztick={'
    for i in range(len(labels)):
        s_labels += str(labels[i])
        w = labels[i]

        for _ in range(log_scale_fac):
            w = math.log2(w + 1)

        s_values += str(w)

        if (i + 1) < len(labels):
            s_labels += ', '
            s_values += ', '

    s_labels += '},'
    s_values += '},'

    f.write("\t" + s_values + "\n" +
            "\t" + s_labels + "\n" +
            "\t" + "grid," + "\n" +
            "]" + "\n" +
            r'\addplot3[' + "\n" +
            "\t" + "mesh," + "\n" +
            "]" + "\n" +
            "coordinates {"
            )

    # Determine the coordinates.
    for eta in etas:
        s_labels = ""
        for lam in lams:
            w = weight(dfa, eta, lam, variant)

            # Scaling the weight
            for _ in range(log_scale_fac):
                w = math.log2(w + 1)

            s_labels += f'({eta}, {lam}, {w})'
        f.write(s_labels + "\n \n")

    # Write the end of the tikzpicture definition in the file.
    f.write("};" + "\n" +
            r'\end{axis}' + "\n" +
            r'\end{tikzpicture}')

    # close the file
    f.close()


"""=====================================================================================================================
    Matrix class
   =====================================================================================================================
"""


class Matrix:
    """Class that contains the matrices needed to calculate the weight of a language and if needed determines the
    matrices for further word lengths.
    """

    def __init__(self, fa):
        """ Constructor of the Matrix class.

        Args:
            fa (FiniteAutomata): Finite automaton for which the matrices are created.
        """
        self.fa = fa
        self.dimension = fa.get_number_of_states()
        self.size_of_alphabet = len(FiniteAutomata.get_alphabet())
        self.matrices = {}
        self.__initial_matrix()

    def __initial_matrix(self):
        """Creating the initial matrix for the word length 1.
        """
        matrix = []
        for i in range(self.dimension):
            number_of_letters = defaultdict(int)
            this_dimension = []

            for (j, _) in self.fa.get_all_successors_with_letter(i):
                number_of_letters[j] += 1

            for j in range(self.dimension):
                this_dimension.append(number_of_letters[j] / self.size_of_alphabet)

            matrix.append(this_dimension)

        self.matrices[1] = np.array(matrix)

    def get_matrix(self, i):
        """ Returns the matrix for the word length i and if this has not yet been calculated, the method also determines
        the matrix for this word length.

        Args:
            i (int): Word length.

        Returns:
            Matrix: The matrix of the word length i.
        """
        if i in self.matrices.keys():
            return self.matrices[i]

        elif i - 1 in self.matrices.keys():
            before = self.matrices[i - 1]
            first = self.matrices[1]
            new_matrix = np.matmul(before, first)
            self.matrices[i] = new_matrix
            return new_matrix

        else:
            self.get_matrix(i - 1)

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
