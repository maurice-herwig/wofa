from wofa import weight, weight_diff
from wofa import FiniteAutomata
from wofa import Constants


def grading_weight(solution, test_obj, eta, lam, max_po, lin_dis, variant=Constants.VARIANT_WORDS,
                   grading_variant=Constants.GRADING_VARIANT_HARMONIC):
    """ Determining a score for a submitted student solution, using the grading schemata presented in docs.
    !!! In contrast to the determination of the weight, point function is no longer symmetrical!!!

    Args:
        solution (FiniteAutomata):  A sample solution of the concrete task.
        test_obj (FiniteAutomata):  Finite automaton of a given student submission for this task.
        eta (int):                  Threshold value up to which the weight of words should be evaluated constantly.
        lam (float):                Decay rate that describes how much the weighting of the individual words
                                    decreases with increasing word length.
        max_po (float):               Maximum points to be awarded.
        lin_dis (float):              linear displacement of the grading.
        variant (string, optional): Determines the variant of how the words in the constant part are redistributed.
                                    'words' := All words in the constant part have the same weight.
                                    'wordLengths' := All word lengths in the constant part have the same weight.
                                    Default value 'word'
        grading_variant (string, optional): Determines the variant of how the points are computed by the grading
                                            function.
                                            'harmonic' := Use the harmonic mean.
                                            'weighted' := Use the weighting of the solution and there complement.

    Returns:
        int:  Points proposal for the submitted solution.
    """

    # Add the linear displacement of the grading points.
    max_po = max_po + lin_dis

    # Use the harmonic grading schemata.
    if grading_variant == Constants.GRADING_VARIANT_HARMONIC:

        # Compute the harmonic mean.
        h_mean = harmonic_mean(solution=solution, test_obj=test_obj, lam=lam, eta=eta, variant=variant)
        points = (h_mean * max_po) - lin_dis

    # Use the weighted grading schemata
    elif grading_variant == Constants.GRADING_VARIANT_WEIGHTED:

        # Determination of the weight of the language of the solution.
        w_sol = weight(solution.determine(), eta, lam, variant)

        # Determination of the weight of the complement language of the solution.
        w_sol_com = 1 - w_sol

        # Determination of the sub-scores.
        po_sol = w_sol * max_po
        po_sol_com = w_sol_com * max_po

        # Determination of the weight of the symmetric difference.
        weight_d = weight_diff(solution, test_obj, eta, lam, variant)

        # Computation of the factors.
        if w_sol == 0:
            fac_sup = 0
        else:
            fac_sup = ((w_sol - weight_d[0]) / w_sol)

        if w_sol_com == 0:
            fac_sub = 0
        else:
            fac_sub = ((w_sol_com - weight_d[1]) / w_sol_com)

        # Compute the points.
        points = (fac_sub * po_sol_com) + (fac_sup * po_sol) - lin_dis

    else:
        assert "No match for the grading_variant parameter."
        return

    # Map all points less than zero to zero.
    if points < 0:
        return 0

    # Return the points as integer rounded to whole points.
    return int(round(points, 0))


def grading_subsets(solution, test_obj, max_po):
    """ Determines the score by looking at the subset relationships between the sample solution and submitted
    submission, for each of the two correct inclusion directions half the points are awarded.

    Args:
        solution (FiniteAutomata):  A sample solution of the concrete task.
        test_obj (FiniteAutomata):  Finite automaton of a given student submission for this task.
        max_po (float):               Maximum points to be awarded.

    Returns:
        float:  Points proposal for the submitted solution
    """
    points = 0

    s_sub_o, o_sub_s = solution.subsets_symmetric_difference(test_obj)

    # Check if the subset relationships are present
    if s_sub_o.is_empty():
        points += max_po/2

    if o_sub_s.is_empty():
        points += max_po/2

    return points


def grading_test_words(test_obj, max_po, containing_words, not_included_words):
    """ Determines the number of points awarded by testing certain test words that should be correctly categorized
    (accepted/rejected) by the testing automaton.

    Args:
        test_obj (FiniteAutomata):              Finite automaton of a given student submission for this task.
        max_po (float):                           Maximum points to be awarded.
        containing_words (list of strings):     List of words that should be accepted by the test automaton.
        not_included_words (list of strings):   List of words that reject be accepted by the test automaton.

    Returns:
        float:  Points proposal for the submitted solution.
    """

    points = 0
    points_per_word = max_po / (len(containing_words) + len(not_included_words))

    # check the words the test object should include.
    for word in containing_words:
        if test_obj.accepts_word(word):
            points += points_per_word

    # check the words the test object should not include.
    for word in not_included_words:
        if not test_obj.accepts_word(word):
            points += points_per_word

    return points


def harmonic_mean(solution, test_obj, eta, lam, variant='words'):
    """ Compute the harmonic mean of the two frachtions: first the weight of the intersection of the solution and the
        submission normalized with weight of the solution. Or in other words the fraction that the submission classified
        correct as words in the solution language. Second the weight of the intersection of the complement of the
        solution and the complement of the submission.

    Args:
        solution (FiniteAutomata):  A sample solution of the concrete task.
        test_obj (FiniteAutomata):  Finite automaton of a given student submission for this task.
        eta (int):                  Threshold value up to which the weight of words should be evaluated constantly.
        lam (float):                Decay rate that describes how much the weighting of the individual words
                                    decreases with increasing word length.
        variant (string, optional): Determines the variant of how the words in the constant part are redistributed.
                                    'words' := All words in the constant part have the same weight.
                                    'wordLengths' := All word lengths in the constant part have the same weight.
                                    Default value 'word'

    Returns:
        float: The calculated harmonic mean.
    """

    # Compute the weight of the solution
    w_sol = weight(solution.determine(), eta, lam, variant)
    w_sol_com = 1 - w_sol

    # Compute the weight of the symmetrical difference
    weight_d = weight_diff(solution, test_obj, eta, lam, variant)

    # Compute the fraction of words that are correct classified as word in the language.
    if w_sol == 0:
        fac_1 = 1
    else:
        fac_1 = (w_sol - weight_d[0]) / w_sol

    # Compute the fraction of words that are correct classified as word not in the language.
    if w_sol_com == 0:
        fac_2 = 1
    else:
        fac_2 = (w_sol_com - weight_d[1]) / w_sol_com

    # Compute the harmonic mean of both factors.
    return 2 * fac_1 * fac_2 / (fac_1 + fac_2)
