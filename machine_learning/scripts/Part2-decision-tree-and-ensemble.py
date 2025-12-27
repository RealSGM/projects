# Description: Part 2b of the coursework
# Created on: 06/11/2024
# --------------------------------------------------
# Ensemble
# accuracy_score(on test set):  0.7678571428571429
# --------------------------------------------------

import numpy as np
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder
from sklearn import model_selection
from sklearn import tree
import matplotlib.pyplot as plt

SEED = 38

def prepare_data():
    """
    Prepare the breast cancer dataset by loading the data from a file, separating features and labels,
    and filtering out rows with missing values.
    
    Returns:
    X (array): Array of shape (n_samples, n_features) containing the features.
    y (array): Array of shape (n_samples,) containing the labels.
    
    Libraries:
    - numpy
    """
    # Load data from the file
    breast_cancer_data = np.genfromtxt("data/breast-cancer.data", delimiter=",", dtype=str)
    
    # Separate features and labels
    y = breast_cancer_data[:, 0]  # Labels are in the first column
    X = breast_cancer_data[:, 1:]  # Features are in the remaining columns
    
    # Filter out rows with any missing values
    complete_cases = ~np.any((X == "?") | (X == "nan"), axis=1)  # Keep only complete cases
    X = X[complete_cases]
    y = y[complete_cases]  # Filter y using the same index
    
    return X, y


def encode_data(X, y):
    """
    Encode the dataset with a numerical representation using an ordinal encoding approach.

    Parameters:
    X (array): The input features.
    y (array): The target variable.

    Returns:
    X_encoded (array): The encoded input features.
    y_encoded (array): The encoded target variable.
    
    Libraries:
    - sklearn.preprocessing.OrdinalEncoder
    - sklearn.preprocessing.LabelEncoder
    """
    ordinal_encoder = OrdinalEncoder()
    X_encoded = ordinal_encoder.fit_transform(X)
    
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    return X_encoded, y_encoded


def print_data(X, y):
    """
    Prints a summary of the dataset.

    Parameters:
    X (numpy.ndarray): The input data array.
    y (numpy.ndarray): The target variable array.
    """
    print("Dataset summary")
    print(f"Number of cases: {X.shape[0]}")
    print(f"Number of attributes: {X.shape[1]}")
    print(f"Number of classes: {len(np.unique(y))}")
    print(f"Class distribution (cases per class): {np.bincount(y)}")
    print("List attributes and the number of different values")
    for i in range(X.shape[1]):
        print(f"Attribute[{i}]: {len(np.unique(X[:, i]))}")


def split_data(X, y):
    """
    Splits the data into training and testing sets.

    Parameters:
    X (array): The input features.
    y (array): The target variable.

    Returns:
    X_train (array): The training set of input features.
    X_test (array): The testing set of input features.
    y_train (array): The training set of target variable.
    y_test (array): The testing set of target variable.
    """
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2, random_state=SEED, stratify=y)
    return X_train, X_test, y_train, y_test


def train_decision_tree(X_train, y_train):
    """
    Trains a decision tree classifier using the provided training data.

    Parameters:
    - X_train (array): The input features for training.
    - y_train (array): The target labels for training.

    Returns:
    - classifier (DecisionTreeClassifier): The trained decision tree classifier.
    """
    classifier = tree.DecisionTreeClassifier(criterion='entropy', max_depth=5, random_state=SEED)
    classifier.fit(X_train, y_train)
    return classifier


def print_decision_tree(classifier, X_train, y_train, X_test, y_test):
    """
    Prints information about the decision tree classifier.

    Parameters:
    classifier (DecisionTreeClassifier): The decision tree classifier object.
    X_train (array): The training input samples.
    y_train (array): The target values for the training set.
    X_test (array): The test input samples.
    y_test (array): The target values for the test set.
    """
    print("DecisionTreeClassifier")
    print(f"criterion: {classifier.criterion}")
    print(f"max_depth: {classifier.max_depth}")
    print(f"random_state: {classifier.random_state}")
    print(f"accuracy_score(on training set): {classifier.score(X_train, y_train)}")
    print(f"accuracy_score(on test set): {classifier.score(X_test, y_test)}")


def plot_decision_tree(classifier):
    """
    Plots the decision tree classifier.

    Parameters:
    classifier (DecisionTreeClassifier): The decision tree classifier to be plotted.
    """
    plt.figure(figsize=(20, 10))
    tree.plot_tree(classifier, filled=True, feature_names=range(1, 10))
    plt.savefig("Part2-decision-tree-display.png")


def train_ensemble_classifiers(X_train, y_train, max_depth):
    """
    Trains an ensemble of decision tree classifiers.

    Parameters:
    - X_train (array): The input features for training.
    - y_train (array): The target labels for training.
    - max_depth (int): The maximum depth of the decision trees.

    Returns:
    - classifier (DecisionTreeClassifier): The trained decision tree classifier.
    """
    classifier = tree.DecisionTreeClassifier(criterion='gini', max_depth=max_depth, max_features=9, random_state=SEED)
    classifier.fit(X_train, y_train)
    return classifier


def ensemble_voting(X_train, y_train, X_test, y_test):
    """
    Creates 9 decision tree classifiers using gini criterion and different depths.
    Performs ensemble voting using the decision tree classifiers and evaluates the ensemble.
    Stores the predictions in a CSV file.
    

    Parameters:
    - X_train (array): Training data features.
    - y_train (array): Training data labels.
    - X_test (array): Test data features.
    - y_test (array): Test data labels.
    """
    # Create a CSV file to store the predictions
    header = 'case_id,dt1,dt2,dt3,dt4,dt5,dt6,dt7,dt8,dt9,actual_class,ensemble'
    file_name = 'data/Part2-ensemble.csv'
    
    csv_file = open(file_name, 'w')
    csv_file.write(header + '\n')
    
    
    classifiers = [train_ensemble_classifiers(X_train, y_train, i) for i in range(1, 10)]
    
    # Loop through test set and predict using each classifier
    # Store the predictions in a matrix
    predictions = np.array([classifier.predict(X_test) for classifier in classifiers])
    
    for case_id in range(X_test.shape[0]):
        # For each case, get the predictions from all classifiers
        case_predictions = predictions[:, case_id]
        # Count the number of votes for each class
        votes = np.bincount(case_predictions)
        # Find the class with the most votes
        predicted_class = np.argmax(votes)
        
        csv_file.write(f'{case_id+1},{",".join(map(str, case_predictions))},{y_test[case_id]},{predicted_class}\n')

    # Close the file
    csv_file.close()
    
    # Calculate the accuracy of the ensemble
    ensemble_accuracy = np.mean(predictions[-1] == y_test)
    print(f'Ensemble accuracy: {ensemble_accuracy}')


def main():
    """
    Prepare and encode the data, train a decision tree classifier, and evaluate its performance.
    Plot the decision tree and save the plot to a file.
    Create arrays of decision tree classifiers with different depths and train them.
    Perform ensemble voting using the decision tree classifiers and evaluate the ensemble
    """
    X, y = prepare_data()
    X, y = encode_data(X, y)
    # print_data(X, y)
    X_train, X_test, y_train, y_test = split_data(X, y)
    # classifier = train_decision_tree(X_train, y_train)
    # print_decision_tree(classifier, X_train, y_train, X_test, y_test)
    # plot_decision_tree(classifier)
    ensemble_voting(X_train, y_train, X_test, y_test)


if __name__ == "__main__":
    main()