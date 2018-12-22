# Author: Ani Khachatryab
# Date & Time: 12/4/18 11:34 PM

import pandas as pd
from collections import OrderedDict
import matplotlib.pyplot as plt



df_merged = pd.read_csv('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/df_merged.csv', index_col=None)

df_latest = pd.read_csv('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/processed_filtered_csv_cancer/filtered_ClinVarFullRelease_2018-11.csv', index_col=None)

df_version_change = pd.DataFrame(columns=['RCV', 'firstVersion', 'lastVersion'], index=range(0, df_merged[df_merged['Reclassified'] == 1].shape[0]))
df_version_change.loc[:,'RCV'] = df_merged[df_merged['Reclassified'] == 1]['RCV'].reset_index(drop=True)
df_version_change['firstVersion'] = df_merged[df_merged['Reclassified'] == 1]['Description'].reset_index(drop=True)


i = 0
for index, row in df_version_change.iterrows():
    i += 1
    print(i)
    latestDescription = df_latest[df_latest['RCV'] == row['RCV']]['Description'].item()
    print(row['firstVersion'], latestDescription)
    df_version_change.loc[df_version_change['RCV'] == row['RCV'], 'lastVersion'] = latestDescription

df_version_change['change'] = df_version_change['firstVersion']+' to '+df_version_change['lastVersion']

df_version_change.to_csv('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/df_version_change.csv', index=False)
df_version_change = pd.read_csv('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/df_version_change.csv', index_col=None)




x = df_version_change['change'].value_counts()


# plots
change_dict = OrderedDict()

for index, row in x.iteritems():
    print(index, row)
    if row > 400:
        change_dict[index] = row
    # else:
    #     if change_dict.get('other', False):
    #         change_dict['other'] += row
    #     else:
    #         change_dict['other'] = row


df = pd.DataFrame(change_dict, index=[0])
df = df.transpose()
df.reset_index(inplace=True)
# df['index'] = pd.to_numeric(df['index'])

fig, ax = plt.subplots()
plt.bar(df['index'], df[0])
plt.ylabel('Count')
plt.xlabel('Change')
# ax.set_xticks(range(0,9))
# ax.set_xticklabels(['', '1', '2', '3', '4', '5', '6', '7', '>7'])

ax.set_xticks(range(0,3))
ax.set_xticklabels(['', '1', '>1'])


styles = ['_classic_test', 'seaborn-white', 'seaborn-talk', 'seaborn-dark', 'fast', 'seaborn-whitegrid', 'grayscale', 'seaborn-ticks', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-notebook', \
          'seaborn-dark-palette', 'tableau-colorblind10', 'fivethirtyeight', 'classic', 'bmh', 'seaborn-darkgrid', 'dark_background', 'Solarize_Light2', 'seaborn', 'seaborn-muted', 'seaborn-poster', \
          'seaborn-pastel', 'seaborn-deep', 'ggplot', 'seaborn-paper']



plt.style.use('tableau-colorblind10')
labels = ['uncertain significance to likely benign', 'uncertain significance to conflicting interpretations of pathogenicity', \
          'benign to benign/likely benign', 'likely benign to benign', 'uncertain significance to benign']
# sizes = [88.4, 10.6, 0.7, 0.3]
# colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
patches, texts = plt.pie(list(change_dict.values()), startangle=90)
plt.legend(patches, labels, loc="best")
# Set aspect ratio to be equal so that pie is drawn as a circle.
plt.axis('equal')
plt.tight_layout()
plt.show()


#####

x = df_version_change['firstVersion'].value_counts()
first_dict = OrderedDict()

for index, row in x.iteritems():
    print(index, row)
    first_dict[index] = row

df = pd.DataFrame(first_dict, index=[0])
df = df.transpose()
df.reset_index(inplace=True)
# df['index'] = pd.to_numeric(df['index'])

fig, ax = plt.subplots()
plt.bar(df['index'], df[0])
plt.ylabel('Count')
plt.xlabel('Clinical Significance')



plt.style.use('tableau-colorblind10')
labels = list(first_dict.keys())
# sizes = [88.4, 10.6, 0.7, 0.3]
# colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
patches, texts = plt.pie(list(first_dict.values()), startangle=90)
plt.legend(patches, labels, loc="best")
# Set aspect ratio to be equal so that pie is drawn as a circle.
plt.axis('equal')
plt.tight_layout()
plt.show()


######
x = df_version_change['lastVersion'].value_counts()

last_dict = OrderedDict()

for index, row in x.iteritems():
    print(index, row)
    if row > 200:
        last_dict[index] = row
    else:
        if last_dict.get('other', False):
            last_dict['other'] += row
        else:
            last_dict['other'] = row


for index, row in x.iteritems():
    print(index, row)
    if row > 400:
        change_dict[index] = row


df = pd.DataFrame(last_dict, index=[0])
df = df.transpose()
df.reset_index(inplace=True)
# df['index'] = pd.to_numeric(df['index'])

fig, ax = plt.subplots()
plt.bar(df['index'], df[0])
plt.ylabel('Count')
plt.xlabel('Clinical Significance')


plt.style.use('tableau-colorblind10')
labels = list(last_dict.keys())
# sizes = [88.4, 10.6, 0.7, 0.3]
# colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
patches, texts = plt.pie(list(last_dict.values()), startangle=90)
plt.legend(patches, labels, loc="best")
# Set aspect ratio to be equal so that pie is drawn as a circle.
plt.axis('equal')
plt.tight_layout()
plt.show()



##
x = df_merged[df_merged['Reclassified'] == 0]['Description'].value_counts()

desc_dict = OrderedDict()

for index, row in x.iteritems():
    print(index, row)
    desc_dict[index] = row


df = pd.DataFrame(last_dict, index=[0])
df = df.transpose()
df.reset_index(inplace=True)
# df['index'] = pd.to_numeric(df['index'])

fig, ax = plt.subplots()
plt.bar(df['index'], df[0])
plt.ylabel('Count')
plt.xlabel('Clinical Significance')

plt.style.use('tableau-colorblind10')
labels = list(desc_dict.keys())
# sizes = [88.4, 10.6, 0.7, 0.3]
# colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
patches, texts = plt.pie(list(desc_dict.values()), startangle=90)
plt.legend(patches, labels, loc="best")
# Set aspect ratio to be equal so that pie is drawn as a circle.
plt.axis('equal')
plt.tight_layout()
plt.show()

