# Author: Ani Khachatryab
# Date & Time: 12/17/18 9:40 AM

import pandas as pd
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.feature_selection import RFE
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression

df_merged = pd.read_csv('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/df_merged.csv')

df_merged_dummy = pd.get_dummies(df_merged, columns=['Description', 'Type', 'MethodType', 'Origin', 'ReviewStatus'], drop_first=False)
df_merged_dummy.drop(labels=['RCV', 'Version', 'DateLastEvaluated', 'DateUpdated', 'first_file', 'recl_file', 'date_added', 'date_recl', 'age_days', 'age_months', 'age_years'], axis=1, inplace=True)  # not droping reclassified and review status

# df_merged_filtered = pd.read_csv('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/df_merged_filtered.csv', index_col=None)
# X = df_merged_filtered.loc[:, df_merged_filtered.columns != 'Reclassified']
# y = df_merged_filtered['Reclassified']

X = df_merged_dummy.loc[:, df_merged_dummy.columns != 'Reclassified']
y = df_merged_dummy['Reclassified']

print(X.head())
X.shape

kbest = SelectKBest(chi2, k=14)
f = kbest.fit(X,y)
X_new = kbest.fit_transform(X, y)
X_new.shape

# RFE
model = LogisticRegression()
rfe = RFE(model, 1)
fit = rfe.fit(X, y)
print("Num Features:", fit.n_features_)
print("Selected Features:", fit.support_)
print("Feature Ranking:", fit.ranking_)

c = []
for i in [e for (i,e) in enumerate(fit.support_) if e]:
    print(X.columns[i])
    c.append(X.columns[i])


dict_ranking_rfe = {}

# i index
# e ranking
for i,e in sorted([(i,e) for (i,e) in enumerate(fit.ranking_)], key=lambda t: t[1]):
    # print('ranking:', e)
    print(X.columns[i])
    # print('support:', fit.support_[i])
    # c.append(X.columns[i])
    dict_ranking_rfe[X.columns[i]] = e


# X = X.loc[:, c]


# FI
model = ExtraTreesClassifier()
model.fit(X, y)
print(model.feature_importances_)

dict_ranking_etc = {}

j = 1
for i in [(t[0], t[1]) for t in sorted(zip(X.columns, model.feature_importances_), key=lambda t: t[1], reverse=True)]:
    print(i)
    dict_ranking_etc[i[0]] = j
    j += 1


for i in [(t[0], t[1]) for t in sorted(zip(X.columns, f.pvalues_), key=lambda t: t[1])]:
    print('\\textbf{' + i[0] + '} & ' + str(dict_ranking_rfe[i[0]]) + ' & ' + str(dict_ranking_etc[i[0]]) + ' \\\\ \hline')
