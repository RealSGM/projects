# Description: Part 2a of the coursework
# Created on: 31st October 2024
# --------------------------------------------------
# Root Entropy = 0.95
# Root Gini = 0.47
# --------------------------------------------------
# Attribute: Headache
# Contingency table:
# [3 0]
# [2 3]
# --------------------------------------------------
# Information Gain
# Gain(root, Headache) = 0.35
# get_gain(spot_contingency_table, root_entropy)
# --------------------------------------------------
# Gini
# get_gini(spot_contingency_table, root_gini)
# Gini(root, Headache) = 0.17
# --------------------------------------------------
# Chi-square
# get_chi(spot_contingency_table)
# Chi (root, Headache) = 2.88
# --------------------------------------------------

# --------------------------------------------------
# Attribute: Spots
# Contingency table:
# [[4 1]
#  [1 2]]
# --------------------------------------------------
# Information Gain
# get_gain(spot_contingency_table, root_entropy)
# Gain(root, Spots) = 0.16
# --------------------------------------------------
# Gini
# get_gini(spot_contingency_table, root_gini)
# Gini(root, Spots) = 0.1
# --------------------------------------------------
# Chi-square
# get_chi(spot_contingency_table)
# Chi (root, Spots) = 1.74
# --------------------------------------------------

# --------------------------------------------------
# Attribute: Stiff-neck
# Contingency table:
# [[4 1]
#  [1 2]]
# --------------------------------------------------
# Information Gain
# get_gain(stiff_neck_contingency_table, root_entropy)
# Gain(root, Stiff-neck) = 0.16
# --------------------------------------------------
# Gini
# get_gini(stiff_neck_contingency_table, root_gini)
# Gini(root, Stiff-neck) = 0.1
# --------------------------------------------------
# Chi-square
# get_chi(stiff_neck_contingency_table)
# Chi (root, Stiff-neck) = 1.74

import numpy as np

def process_contingency_table(contingency_table):
    """
    Process a contingency table and calculate various measures.

    Parameters:
    contingency_table (array): A 2x2 contingency table.

    Returns:
    tuple: A tuple containing the total number of cases and the values of a, b, c, d.
    
    Libraries:
    numpy as np

    """
    # Check if the input is a 2x2 array
    if contingency_table.shape != (2, 2):
        raise ValueError("The input should be a 2x2 array.")
    
    
    # Calculate the total number of cases
    total_cases = np.sum(contingency_table)
    
    a = contingency_table[0][0] # True Positive
    b = contingency_table[0][1] # True Negative
    c = contingency_table[1][0] # False Positive
    d = contingency_table[1][1] # False Negative
    
    return total_cases, a, b, c, d


def get_gain(contingency_table, root_entropy):
    """
    Calculate the information gain based on a contingency table.

    Parameters:
    contingency_table (arrau): The contingency table containing the counts of true positive, true negative,
    false positive, and false negative.
    root_entropy (float): The entropy of the root node.

    Returns:
    float: The information gain.
    
    Libraries:
    numpy as np

    """
    total_cases, true_positive, true_negative, false_positive, false_negative = process_contingency_table(contingency_table)
    true_sum = true_positive + true_negative
    false_sum = false_positive + false_negative
    
    # Calculate the entropy for yes and no, set it to 0 if the sum is 0, to prevent a division by 0 error
    entropy_true = 0 if (true_positive == 0 or true_negative == 0 ) else -((true_positive / true_sum) * np.log2(true_positive / true_sum) + (true_negative / true_sum) * np.log2(true_negative / true_sum))
    entropy_false = 0 if (false_positive == 0 or false_negative == 0) else -((false_positive / false_sum) * np.log2(false_positive / false_sum) + (false_negative / false_sum) * np.log2(false_negative / false_sum))
    weighted_gain = (true_sum / total_cases) * entropy_true + (false_sum / total_cases) * entropy_false
    gain = root_entropy - weighted_gain
    
    return round(gain, 2)


def get_gini(contingency_table, root_gini):
    """
    Calculate the Gini index based on a contingency table.

    Parameters:
    contingency_table (array): The contingency table containing the counts of true positive, true negative,
    false positive, and false negative.
    root_gini (float): The Gini index of the root node.

    Returns:
    float: The Gini index.

    """
    total_cases, true_positive, true_negative, false_positive, false_negative = process_contingency_table(contingency_table)
    true_sum = true_positive + true_negative
    false_sum = false_positive + false_negative
    
    gini_true = 1 - ((true_positive / true_sum) ** 2 + (true_negative / true_sum) ** 2)
    gini_false = 1 - ((false_positive / false_sum) ** 2 + (false_negative / false_sum) ** 2)
    weighted_gini = (true_sum / total_cases) * gini_true + (false_sum / total_cases) * gini_false
    gini = root_gini - weighted_gini
    
    return round(gini, 2)


def get_chi(contingency_table):
    """
    Calculate the Chi-square statistic based on a contingency table.

    Parameters:
    contingency_table (array): The contingency table containing the counts of true positive, true negative,
    false positive, and false negative.

    Returns:
    float: The Chi-square statistic.

    """
    total_cases, true_positive, true_negative, false_positive, false_negative = process_contingency_table(contingency_table)
    true_sum = true_positive + true_negative
    false_sum = false_positive + false_negative
    
    expected_true_positive = (true_sum / total_cases) * (true_positive + false_positive)
    expected_true_negative = (true_sum / total_cases) * (true_negative + false_negative)
    expected_false_positive = (false_sum / total_cases) * (true_positive + false_positive)
    expected_false_negative = (false_sum / total_cases) * (true_negative + false_negative)
    
    x2 = ((true_positive - expected_true_positive) ** 2 / expected_true_positive +
           (true_negative - expected_true_negative) ** 2 / expected_true_negative +
           (false_positive - expected_false_positive) ** 2 / expected_false_positive +
           (false_negative - expected_false_negative) ** 2 / expected_false_negative)
    
    return round(x2, 2)


def run_analysis(contingency_table, root_entropy, root_gini, attribute):
    """
    Run the analysis for a given contingency table.

    Parameters:
    contingency_table (array): The contingency table containing the counts of true positive, true negative,
    false positive, and false negative.
    root_entropy (float): The entropy of the root node.
    root_gini (float): The Gini index of the root node.

    """
    
    print("-" * 50)
    print("Attribute:", attribute)
    print("Contingency table:")
    print(contingency_table)
    print("-" * 50)
    
    print("Information Gain")
    print("get_gain(contingency_table, root_entropy)")
    print(f"Gain(root, {attribute}) = {get_gain(contingency_table, root_entropy)}")
    print("-" * 50)
    
    print("Gini")
    print("get_gini(contingency_table, root_gini)")
    print(f"Gini(root, {attribute}) = {get_gini(contingency_table, root_gini)}")
    print("-" * 50)
    
    print("Chi-square")
    print("get_chi(contingency_table)")
    print(f"Chi (root, {attribute}) = {get_chi(contingency_table)}")
    print("-" * 50)


def main():
    """
    Calculate the root entropy and Gini index and run the analysis for the three attributes.
    
    Libraries:
    numpy as np 
    """
    
    root_table = np.array([5, 3]) # [Positive, Negative]
    headache_contingency_table = np.array([[3, 0], [2, 3]])
    spot_contingency_table = np.array([[4, 1], [1, 2]])
    stiff_neck_contingency_table = np.array([[4, 1], [1, 2]])
    
    # Calculate the entropy for the root node
    root_entropy = -((root_table[0] / np.sum(root_table)) * np.log2(root_table[0] / np.sum(root_table)) + (root_table[1] / np.sum(root_table)) * np.log2(root_table[1] / np.sum(root_table)))
    # Calculate the Gini index for the root node
    root_gini = 1 - ((root_table[0] / np.sum(root_table)) ** 2 + (root_table[1] / np.sum(root_table)) ** 2)    

    run_analysis(headache_contingency_table, root_entropy, root_gini, "Headache")
    run_analysis(spot_contingency_table, root_entropy, root_gini, "Spots")
    run_analysis(stiff_neck_contingency_table, root_entropy, root_gini, "Stiff-neck")


if __name__ == "__main__":
    main()