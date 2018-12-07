#!/usr/bin/python3.6
#http://nbviewer.jupyter.org/gist/justmarkham/6d5c061ca5aee67c4316471f8c2ae976

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import average_precision_score

df_merged_filtered = pd.read_csv('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/df_merged_filtered.csv', index_col=None)
X = df_merged_filtered.loc[:, df_merged_filtered.columns != 'Reclassified']
y = df_merged_filtered['Reclassified']
print(X.head())


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


model.coef_.tolist()
model.coef_.tolist()[0]
coefs = model.coef_.tolist()[0]
coefs_features = list(zip(coefs, X.columns))
coefs_features = sorted(coefs_features, key=lambda t: t[0])
print(coefs_features)