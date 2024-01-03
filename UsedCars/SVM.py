
from sklearn.svm import LinearSVC
from sklearn.metrics import f1_score, precision_score, accuracy_score, recall_score,confusion_matrix
from DBConfig import DBConnection

import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
import pandas as pd


def svm_evaluation(X_train, X_test, y_train, y_test):
    db = DBConnection.getConnection()
    cursor = db.cursor()

    svm_clf = DecisionTreeClassifier()

    svm_clf.fit(X_train, y_train)

    predicted = svm_clf.predict(X_test)


    accuracy = accuracy_score(y_test, predicted)*100

    precision = precision_score(y_test, predicted, average="micro")*100

    recall = recall_score(y_test, predicted, average="micro")*100

    fscore = f1_score(y_test, predicted, average="micro")*100

    
    values = ("SVM", str(accuracy), str(precision), str(recall), str(fscore))
    sql = "insert into evaluations values(%s,%s,%s,%s,%s)"
    cursor.execute(sql, values)
    db.commit()
    print("SVM=", accuracy, precision, recall, fscore)
    return accuracy, precision, recall, fscore




def main():
    df = pd.read_csv("preprocessed_dataset.csv")
    y_train = df['Name']
    del df['Name']
    del df['Sno']
    del df['Location']
    X = df
    y = y_train


    from sklearn.model_selection import train_test_split



    # Split train test: 70 % - 30 %
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=52)
    d=svm_evaluation(X_train, X_test, y_train, y_test)
    return d

