# Description: Part 3 of the coursework
# Created on: 6th November 2024
# --------------------------------------------------

from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
from sklearn.model_selection import KFold

import time
import os
from itertools import product

os.environ["LOKY_MAX_CPU_COUNT"] = "4" 

SEED = 38

rf_param_grid = {
    'n_estimators': [100, 200, 400],
    'max_depth': [None, 10, 25],
    'criterion': ['gini', 'entropy']
}

knn_param_grid = {
    'n_neighbors': [5, 15, 30],
    'weights': ['uniform', 'distance'],
    'metric': ['euclidean', 'manhattan', 'chebyshev', 'minkowski']
}

svc_param_grid = {
    'C': [0.1, 1, 10],
    'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
    'degree': [2, 3, 4],
}

def load_data():
    """
    Load the digit dataset from sklearn and return the data and target

    Returns:
    X (array): The feature matrix containing the input data.
    y (array): The target vector containing the corresponding labels.
    """
    start_time = time.time()
    digits = load_digits()
    X = digits.data
    y = digits.target
    print(f"Time taken to load data: {time.time() - start_time:.2f} seconds")
    return X, y


def split_data(X, y):
    """
    Split the data into training and testing sets at a 85/15 ratio.

    Parameters:
    X (array): The input features.
    y (array): The target variable.

    Returns:
    X_train (array): The training set of input features.
    X_test (array): The testing set of input features.
    y_train (array): The training set of target variable.
    y_test (array): The testing set of target variable.
    """
    start_time = time.time()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, stratify=y, random_state=SEED)
    print(f"Time taken to split data: {time.time() - start_time:.2f} seconds")
    return X_train, X_test, y_train, y_test


def optimise_model(X_train, y_train, model_class, param_grid):
    """
    optimises the given model by checking all possible combinations of the parameters in the parameter grid.
    Performs 5 fold cross-validation to evaluate the model.
    Stores the best model, best score, and best parameters found.
    
    Parameters:
        X_train (array): The training data.
        y_train (array): The target values.
        model_class (class): The class of the model to optimise.
        param_grid (dict): The parameter grid to search over.
        
    Returns:
        tuple: A tuple containing the optimised model, the best score achieved, and the best parameters found.
    """
    start_time = time.time()
    print(f"Optimizing {model_class.__name__}...")
    
    data = {}
    count = 0
    
    best_score = 0
    best_params = {}
    worst_score = 1
    worst_params = {}

    param_names = list(param_grid.keys())
    param_combinations = list(product(*param_grid.values()))

    for param_values in param_combinations:
        # Create parameter dictionary for current combination
        params = dict(zip(param_names, param_values)) 
        # Store the parameters in the data dictionary
        data[count] = params.copy() 
        
        # Add the random_state parameter if it's supported by the model
        if 'random_state' in model_class().get_params().keys(): 
            params['random_state'] = SEED

        # Instantiate model with current parameters
        model = model_class(**params) 
        # Create a 5-fold cross-validation object
        cv = KFold(n_splits=5, shuffle=False) 
        # Perform cross-validation using KFold
        scores = cross_val_score(model, X_train, y_train, cv=cv) 
        
        mean_score = round(scores.mean(), 6)
        std_score = round(scores.std(), 6)
        
        best_score, best_params = (mean_score, params) if mean_score > best_score else (best_score, best_params)
        worst_score, worst_params = (mean_score, params) if mean_score < worst_score else (worst_score, worst_params)
        
        print(f"{params}, mean_score: {mean_score}")
            
        data[count]['mean_score'] = mean_score
        data[count]['std_score'] = std_score
        count += 1
        
    # Save the data to a file
    # Columns: ID and a column for each parameter, mean_score, std_score
    with open(f"data/{model_class.__name__}.csv", "w") as f:
        f.write("ID,")
        f.write(",".join(param_names + ["mean_score", "std_score"]) + "\n")
        for i in range(count):
            f.write(f"{i},")
            f.write(",".join(str(data[i][param]) for param in param_names + ["mean_score", "std_score"]) + "\n")

    print(f"Time taken to optimise {model_class.__name__}: {time.time() - start_time:.2f} seconds\n")
    return model_class(**best_params), best_score, best_params, worst_score, worst_params


def main():
    X, y = load_data()
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    rf_model, rf_score, rf_params, rf_worst_score, rf_worst_params = optimise_model(X_train, y_train, RandomForestClassifier, rf_param_grid)
    knn_model, knn_score, knn_params, knn_worst_score, knn_worst_params = optimise_model(X_train, y_train, KNeighborsClassifier, knn_param_grid)
    svc_model, svc_score, svc_params, svc_worst_score, svc_worst_params = optimise_model(X_train, y_train, SVC, svc_param_grid)
    
    rf_model.fit(X_train, y_train)
    knn_model.fit(X_train, y_train)
    svc_model.fit(X_train, y_train)
    
    # Test the models
    rf_test_score = rf_model.score(X_test, y_test)
    knn_test_score = knn_model.score(X_test, y_test)
    svc_test_score = svc_model.score(X_test, y_test)
    
    # Print best parameters and its score during training
    print(f"Random Forest: Best score: {rf_score}, Best params: {rf_params}")
    print(f"KNN: Best score: {knn_score}, Best params: {knn_params}")
    print(f"SVC: Best score: {svc_score}, Best params: {svc_params}")
    
    # Print worst parameters and its score during training
    print(f"Random Forest: Worst score: {rf_worst_score}, Worst params: {rf_worst_params}")
    print(f"KNN: Worst score: {knn_worst_score}, Worst params: {knn_worst_params}")
    print(f"SVC: Worst score: {svc_worst_score}, Worst params: {svc_worst_params}")
    
    # Print test scores
    print(f"Random Forest test score: {rf_test_score}")
    print(f"KNN test score: {knn_test_score}")
    print(f"SVC test score: {svc_test_score}")
    
    


if __name__ == "__main__":
    main()