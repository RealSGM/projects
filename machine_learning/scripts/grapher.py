import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def graph_knn():
    # Load the CSV files
    knn_df = pd.read_csv('data/KNeighborsClassifier.csv')
    
    # Initialize figure for KNeighborsClassifier parameter analysis
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('Effect of Parameters on Mean Score - KNN')

    # Plotting n_neighbors vs mean_score
    sns.lineplot(data=knn_df, x='n_neighbors', y='mean_score', ax=axs[0])
    axs[0].set_title('n_neighbors vs Mean Score')
    axs[0].set_xlabel('n_neighbors')
    axs[0].set_ylabel('Mean Score')

    # Plotting weights vs mean_score
    sns.boxplot(data=knn_df, x='weights', y='mean_score', ax=axs[1])
    axs[1].set_title('weights vs Mean Score')
    axs[1].set_xlabel('weights')
    axs[1].set_ylabel('Mean Score')

    # Plotting metric vs mean_score
    sns.boxplot(data=knn_df, x='metric', y='mean_score', ax=axs[2])
    axs[2].set_title('metric vs Mean Score')
    axs[2].set_xlabel('metric')
    axs[2].set_ylabel('Mean Score')
    
    plt.savefig('images/knn_graph.png')


def graph_svc():
    svc_df = pd.read_csv('data/SVC.csv')
    # Initialize figure for SVC parameter analysis
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('Effect of Parameters on Mean Score - SVC')

    # Plotting C vs mean_score
    sns.lineplot(data=svc_df, x='C', y='mean_score', ax=axs[0])
    axs[0].set_title('C vs Mean Score')
    axs[0].set_xlabel('C')
    axs[0].set_ylabel('Mean Score')

    # Plotting kernel vs mean_score
    sns.boxplot(data=svc_df, x='kernel', y='mean_score', ax=axs[1])
    axs[1].set_title('kernel vs Mean Score')
    axs[1].set_xlabel('kernel')
    axs[1].set_ylabel('Mean Score')

    # Plotting degree vs mean_score
    sns.lineplot(data=svc_df, x='degree', y='mean_score', ax=axs[2])
    axs[2].set_title('degree vs Mean Score')
    axs[2].set_xlabel('degree')
    axs[2].set_ylabel('Mean Score')
    
    plt.savefig('images/svc_graph.png')


def graph_rf():
    rf_df = pd.read_csv('data/RandomForestClassifier.csv')
    
    # Initialize figure for RandomForestClassifier parameter analysis
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('Effect of Parameters on Mean Score - RandomForestClassifier')
    
    # Plotting n_estimators vs mean_score
    sns.lineplot(data=rf_df, x='n_estimators', y='mean_score', ax=axs[0])
    axs[0].set_title('n_estimators vs Mean Score')
    axs[0].set_xlabel('n_estimators')
    axs[0].set_ylabel('Mean Score')
    
    # Plotting criterion vs mean_score
    sns.boxplot(data=rf_df, x='criterion', y='mean_score', ax=axs[1])
    axs[1].set_title('criterion vs Mean Score')
    axs[1].set_xlabel('criterion')
    axs[1].set_ylabel('Mean Score')
    
    # Plotting max_depth vs mean_score
    sns.lineplot(data=rf_df, x='max_depth', y='mean_score', ax=axs[2])
    axs[2].set_title('max_depth vs Mean Score')
    axs[2].set_xlabel('max_depth')
    axs[2].set_ylabel('Mean Score')
    
    plt.savefig('images/rf_graph.png')


if __name__ == "__main__":
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout to fit the title
    graph_knn()
    # graph_svc()
    # graph_rf()
