from sklearn.ensemble import RandomForestClassifier
import pickle



def train_model(features, values):
    clf = RandomForestClassifier()
    clf = clf.fit(features, values)
    return clf
    #     X = [[0, 0], [1, 1]]
    # Y = [0, 1]
    # clf = RandomForestClassifier()
    # clf = clf.fit(X, Y)
        
    
    
def main():
    with open('data.pkl', 'rb') as f:
        data = pickle.load(f)
        model = train_model(data['first_innings_features'], data['first_innings_values'])
     
    
    
if __name__ == "__main__":
    main()   
    