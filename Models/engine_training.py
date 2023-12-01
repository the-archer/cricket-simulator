# Data Processing
import pandas as pd
import numpy as np

# Modelling
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import randint

# Tree Visualisation
from sklearn.tree import export_graphviz
from IPython.display import Image
import graphviz
import pickle



def get_data():
    data = {}
    with open('data.pkl', 'rb') as f:
        data = pickle.load(f)
    return data    

def clean_data(df):
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df = df.dropna()        
    return df

def train_model(X_train, y_train):
    clf = RandomForestClassifier()
    clf = clf.fit(X_train, y_train)
    return clf

def get_accuracy(clf, X_test, y_test):
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)

def save_model(model):
    model_pkl_file = "cricket_simulator_model.pkl"  
    with open(model_pkl_file, 'wb') as file:  
        pickle.dump(model, file)
    print("Successfully saved model in .pkl file")    
        
def main():
    data = get_data()
    features, values = data['first_innings_features'], data['first_innings_values']
    df = pd.DataFrame(features)
    df['values'] = values
    df = clean_data(df)
    X = df.drop('values',axis=1)
    y = df['values'].astype(str)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    clf = train_model(X_train, y_train)
    get_accuracy(clf, X_test, y_test)
    save_model(clf)
    

if __name__ == "__main__":
    main()
