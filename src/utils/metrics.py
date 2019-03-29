import numpy as np
import math
from scipy.stats import binom


def accuracy(actual, predictions):
    """Calculate and print accuracy and number of guesses.
    :param actual real classes
    :param predictions predicted classes
    """
    true_positive_negative = sum(1 if a == b else 0 for a, b in zip(actual, predictions))
    print(f"correct guesses: {true_positive_negative}")
    print(f"total guesses: {len(predictions)}")
    print("Accuracy:", true_positive_negative / len(predictions))


def permutation_test(actual_classes, a_predictions, b_predictions):
    """Perform the permutation test and print its result.
    The permutation test is a statistical significance test to check whether two models come from significantly
    different distributions. It works by checking the ratio of mean difference of mean results between models when one
    of them is (in this case) randomly permuted.
    :param actual_classes real classes of the predictions.
    :param a_predictions predictions made by model A
    :param b_predictions predictions made by model B, the model being compared to A.
    """
    a_correct = []
    b_correct = []
    for i, actual in enumerate(actual_classes):
        if actual == a_predictions[i]:
            a_correct.append(1)
        else:
            a_correct.append(0)
        if actual == b_predictions[i]:
            b_correct.append(1)
        else:
            b_correct.append(0)

    R = 5000    # Monte Carlo sampling constant
    s = 0       # Number of mean differences >= unpermuted mean difference
    D_0 = abs(np.mean(a_correct) - np.mean(b_correct))
    indecies = [i for i in range(0, len(a_correct))]
    for i in range(0, R):
        ind_perm = indecies
        a_perm = a_correct
        b_perm = b_correct
        # choose to permute between none and all elements
        number_of_pairs_permuted = np.random.randint(0, len(a_perm) + 1)
        ind_perm = np.random.choice(ind_perm, number_of_pairs_permuted)
        for index in ind_perm:
            temp = a_perm[index]
            a_perm[index] = b_perm[index]
            b_perm[index] = temp
        D_i = abs(np.mean(a_perm) - np.mean(b_perm))
        s += 1 if D_i >= D_0 else 0
    p = (s+1) / (R + 1)
    print(f"Prob that Null Hypothesis is true for the two models: {p}\n")


def sign_test(actual_classes, a_predictions, b_predictions, features):
    """Perform the sign test and print its results.
    The sign test is a statistical test checking whether two models come from significantly different distributions. It
    is performed by calculating the ratio of same and differnet results to their total number. It's a weaker test
    compared with the permutation test.
    :param actual_classes real classes for the predictions.
    :param a_predictions predictions of model A.
    :param b_predictions predictions of model B, compared to model A.
    :param features text to be printed when presenting the results.
    :return sign test results (p value)
    """
    average_sum_p = 0
    for fold in range(0, len(actual_classes)):
        actual = actual_classes[fold]
        a_pred = a_predictions[fold]
        b_pred = b_predictions[fold]

        a_better = sum(1 for i, a in enumerate(actual) if
                       (a == a_pred[i]) and (not a == b_pred[i]))
        b_better = sum(1 for i, a in enumerate(actual) if
                       (a == b_pred[i]) and (not a == a_pred[i]))
        both_same = sum(1 for i, a in enumerate(actual) if (a_pred[i] == b_pred[i]))

        print("NB better: %d" % a_better)
        print("SVM better: %d" % b_better)
        print("Both same: %d" % both_same)

        big_n = 2 * math.ceil(both_same / 2) + a_better + b_better
        k = math.ceil(both_same / 2) + min(a_better, b_better)
        p = 2 * sum(binom(big_n, i) * math.pow(0.5, i) * math.pow(0.5, big_n - i) for i in range(0, k))
        print("The probability for fold %d that the models are the same is %f" % (fold, p*100))
        average_sum_p += p

    average_p = average_sum_p / len(actual_classes)
    print("***")
    print("Average probability across folds that the models with %s are the same is %f" % (features, average_p*100))
    print("***")

    return average_p

