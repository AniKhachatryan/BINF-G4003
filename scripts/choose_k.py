# Author: Ani Khachatryab
# Date & Time: 12/18/18 11:21 AM


import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import average_precision_score
from sklearn.feature_selection import SelectKBest, chi2
import matplotlib.pyplot as plt


def fit_logistic_regression(X, y, k):
    kbest = SelectKBest(chi2, k=k)
    f = kbest.fit(X, y)
    X_new = kbest.fit_transform(X, y)
    X_new.shape

    X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size=0.3, random_state=0)
    model2 = LogisticRegression()
    model2.fit(X_train, y_train)

    # predict class labels for the test set
    predicted = model2.predict(X_test)
    # print(predicted)

    # generate class probabilities
    probs = model2.predict_proba(X_test)
    # print(probs)

    # generate evaluation metrics
    accuracy = metrics.accuracy_score(y_test, predicted)
    roc_auc = metrics.roc_auc_score(y_test, probs[:, 1])

    average_precision = average_precision_score(y_test, predicted)

    return accuracy, roc_auc, average_precision


def plot_k_dependency(k_list, some_list, ylabel, title, xlabel='k'):
    fig, ax = plt.subplots()

    ax.plot(k_list, some_list)
    plt.ylabel(ylabel, fontsize=20, fontweight='bold')
    plt.xlabel(xlabel, fontsize=20, fontweight='bold')
    plt.title(title, fontsize=20, fontweight='bold')
    ax.tick_params(labelsize=18)

    ax.grid()

    plt.show()


def main():
    df_merged = pd.read_csv('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/df_merged.csv')

    df_merged_dummy = pd.get_dummies(df_merged, columns=['Description', 'Type', 'MethodType', 'Origin', 'ReviewStatus'],
                                     drop_first=False)
    df_merged_dummy.drop(
        labels=['Version', 'DateLastEvaluated', 'DateUpdated', 'first_file', 'recl_file', 'date_added', 'date_recl',
                'age_days', 'age_months', 'age_years'], axis=1,
        inplace=True)  # not droping reclassified and review status

    X = df_merged_dummy.loc[:, df_merged_dummy.columns != 'Reclassified']
    y = df_merged_dummy['Reclassified']

    accuracy_list = []
    roc_auc_list = []
    pr_auc_list = []

    for k in range(1,X.shape[1]+1):
        accuracy, roc_auc, pr_auc = fit_logistic_regression(X, y, k)
        accuracy_list.append(accuracy)
        roc_auc_list.append(roc_auc)
        pr_auc_list.append(pr_auc)

    plot_k_dependency(range(1,X.shape[1]+1), accuracy_list, ylabel='Accuracy', title = 'k vs Accuracy')
    plot_k_dependency(range(1,X.shape[1]+1), roc_auc_list, ylabel='ROC-AUC', title = 'k vs ROC-AUC')
    plot_k_dependency(range(1,X.shape[1]+1), pr_auc_list, ylabel='PR-AUC', title = 'k vs PR-AUC')


if __name__ == '__main__':
    main()