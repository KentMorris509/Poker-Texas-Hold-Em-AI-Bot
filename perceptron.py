from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle
from sklearn import metrics

def main():
    perceptrons = [Perceptron(max_iter=100000, eta0=0.25, early_stopping=False, random_state=90), #preflop
    Perceptron(max_iter=100000, eta0=0.25, early_stopping=False, random_state=30), #flop
    Perceptron(max_iter=100000, eta0=0.25, early_stopping=False, random_state=50), #turn
    Perceptron(max_iter=100000, eta0=0.25, early_stopping=False, random_state=50)] #river
    #train machines automatically with assumed data files
    dfs = [pd.read_csv("preflop.csv"),
    pd.read_csv("flop.csv"),
    pd.read_csv("turn.csv"),
    pd.read_csv("river.csv")]

    x_y_data = []

    for round in range(len(dfs)):
        X = dfs[round].iloc[:, :-1].values #takes all values but last column
        y = dfs[round].iloc[:, -1].values  #takes value of last column
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        perceptrons[round].fit(X_train, y_train)
        x_y_data.append((X_train, X_test, y_train, y_test))
    
    for round in range(len(dfs)):
        y_pred = perceptrons[round].predict(x_y_data[round][1]) #test with X_test
        accuracy = metrics.accuracy_score(x_y_data[round][3], y_pred) #compare prediction to y_test
        print(f'Accuracy: {accuracy:.2f}')
    
    save_perceptrons(perceptrons)
        

def save_perceptrons(perceptrons, filename="perceptronObjects"):
    with open(filename, 'wb') as f:
        pickle.dump(perceptrons, f)
        print(f"Perceptrons saved to {filename}")

if __name__ == "__main__":
    main()
    