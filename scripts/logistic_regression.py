#!/usr/bin/python3.6
#http://nbviewer.jupyter.org/gist/justmarkham/6d5c061ca5aee67c4316471f8c2ae976

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import average_precision_score
from sklearn.feature_selection import SelectKBest, chi2

def main():
    df_merged = pd.read_csv('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/df_merged.csv')

    df_merged_dummy = pd.get_dummies(df_merged, columns=['Description', 'Type', 'MethodType', 'Origin', 'ReviewStatus'], drop_first=False)
    df_merged_dummy.drop(labels=['RCV', 'Version', 'DateLastEvaluated', 'DateUpdated', 'first_file', 'recl_file', 'date_added', 'date_recl', 'age_days', 'age_months', 'age_years'], axis=1, inplace=True)  # not droping reclassified and review status # 'DateLastEvaluated'

    # df_merged_filtered = df_merged_dummy[~((df_merged_dummy['Reclassified'] == 0) & (df_merged_dummy['Description_uncertain significance'] == 1))]

    X = df_merged_dummy.loc[:, df_merged_dummy.columns != 'Reclassified']
    y = df_merged_dummy['Reclassified']

    # X = df_merged_filtered.loc[:, df_merged_filtered.columns != 'Reclassified']
    # y = df_merged_filtered['Reclassified']

    print(X.head())

    kbest = SelectKBest(chi2, k=8)
    f = kbest.fit(X,y)
    X = kbest.fit_transform(X, y)
    X.shape


    # instantiate a logistic regression model, and fit with X and y
    model = LogisticRegression()
    model = model.fit(X, y)

    # check the accuracy on the training set
    model.score(X, y)


    # evaluate the model by splitting into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    model2 = LogisticRegression()
    model2.fit(X_train, y_train)

    # predict class labels for the test set
    predicted = model2.predict(X_test)
    print(predicted)


    # generate class probabilities
    probs = model2.predict_proba(X_test)
    print(probs)


    # generate evaluation metrics
    print(metrics.accuracy_score(y_test, predicted))
    print(metrics.roc_auc_score(y_test, probs[:, 1]))

    average_precision = average_precision_score(y_test, predicted)
    print(average_precision)

    print(metrics.confusion_matrix(y_test, predicted))
    print(metrics.classification_report(y_test, predicted))


if __name__ == '__main__':
    main()
