# Author: Ani Khachatryab
# Date & Time: 12/15/18 2:14 PM

import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import OrderedDict
import numpy as np


def plot_version_hist(version_value_counts, n, png):
    version_dict = OrderedDict()
    # n = 8
    opacity = .75

    for index, row in version_value_counts.iteritems():
        # print(index, row)
        if int(index ) < n:
            version_dict[index] = row
        else:
            if version_dict.get(n, False):
                version_dict[n] += row
            else:
                version_dict[n] = row

    df = pd.DataFrame(version_dict, index=[0])
    df = df.transpose()
    df.reset_index(inplace=True)
    df['index'] = pd.to_numeric(df['index'])

    fig, ax = plt.subplots()
    plt.bar(df['index'], df[0], alpha=opacity)
    plt.ylabel('Count', fontsize=20, fontweight='bold')
    plt.xlabel('Version', fontsize=20, fontweight='bold')
    ax.set_xticks(range(0,n+1))
    ax.set_xticklabels([''] + list(map(str,range(1,n))) + ['>'+str(n-1)])

    ax.tick_params(labelsize=18)

    plt.show()
    # plt.savefig(png)
    # plt.close()


def plot_types_of_changes(change_value_counts):
    change_dict = OrderedDict()

    for index, row in change_value_counts.iteritems():
        # print(index, row)
        if row > 100:
            change_dict[index] = row
        else:
            if change_dict.get('other', False):
                change_dict['other'] += row
            else:
                change_dict['other'] = row

    df = pd.DataFrame(change_dict, index=[0])
    df = df.transpose()
    df.reset_index(inplace=True)
    # df['index'] = pd.to_numeric(df['index'])


    # styles = ['_classic_test', 'seaborn-white', 'seaborn-talk', 'seaborn-dark', 'fast', 'seaborn-whitegrid',
    #           'grayscale', 'seaborn-ticks', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-notebook', \
    #           'seaborn-dark-palette', 'tableau-colorblind10', 'fivethirtyeight', 'classic', 'bmh', 'seaborn-darkgrid',
    #           'dark_background', 'Solarize_Light2', 'seaborn', 'seaborn-muted', 'seaborn-poster', \
    #           'seaborn-pastel', 'seaborn-deep', 'ggplot', 'seaborn-paper']
    #
    plt.style.use('tableau-colorblind10')
    labels = change_dict.keys()
    # labels = ['uncertain significance to likely benign',
    #           'uncertain significance to conflicting interpretations of pathogenicity', \
    #           'benign to benign/likely benign', 'likely benign to benign', 'uncertain significance to benign']
    # sizes = [88.4, 10.6, 0.7, 0.3]
    # colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    def default_value(x):
        return x[0]
    patches, texts, autotextx = plt.pie(list(change_dict.values()), autopct='', startangle=90)
    for i, a in enumerate(autotextx):
        a.set_text("{}".format(list(change_dict.values())[i]))
    plt.legend(patches, labels, loc="best", fontsize=10)
    # Set aspect ratio to be equal so that pie is drawn as a circle.

    plt.axis('equal')
    plt.tight_layout()


    plt.show()
    # plt.savefig(png)
    # plt.close()


def hist(df, xticklabels=None, png=None, ylabel='Count', xlabel='Clinical Significance', xticks=None):
    if xticks is None:
        xticks = range(len(df) + 1)
    fig, ax = plt.subplots()
    opacity = .75
    plt.bar(df.index, df, alpha=opacity)
    plt.ylabel(ylabel, fontsize=20, fontweight='bold')
    plt.xlabel(xlabel, fontsize=20, fontweight='bold')
    ax.set_xticks(xticks)
    if xticklabels is not None:
        ax.set_xticklabels(xticklabels)

    ax.tick_params(labelsize=18)
    plt.show()
    # plt.savefig(png)
    # plt.close()


def plot_comparison_barplot(class1, class2, labels, ylabel='Count', xlabel='Clinical Significance', class1_label='Before reclassification', class2_label='After reclassification'):
    # data to plot
    n_groups = len(labels)

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = .75

    rects1 = plt.bar(index, class1, bar_width,
                     alpha=opacity,
                     color='#1f77b4',
                     label=class1_label)

    rects2 = plt.bar(index + bar_width, class2, bar_width,
                     alpha=opacity,
                     color='orange',
                     label=class2_label)

    plt.xlabel(xlabel, fontsize=20, fontweight='bold')
    plt.ylabel(ylabel, fontsize=20, fontweight='bold')
    # plt.title('Scores by person')
    plt.xticks(index + bar_width/2, labels)
    plt.legend(fontsize=18)

    ax.tick_params(labelsize=18)

    plt.tight_layout()
    plt.show()


def main():
    # Fig 1
    df_latest = pd.read_csv(
        '/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/processed_filtered_csv_cancer/filtered_ClinVarFullRelease_2018-11.csv')
    version_value_counts = df_latest['Version'].value_counts()
    plot_version_hist(version_value_counts, 8, '/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/plots/versions_8.png')
    plot_version_hist(version_value_counts, 2, '/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/plots/versions_2.png')



    # Fig 2b
    df_version_change = pd.read_csv('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/df_version_change.csv', index_col=None)
    # df_version_change['change'] = df_version_change['firstVersion'] + ' to ' + df_version_change['lastVersion']

    change_value_counts = df_version_change['change'].value_counts()
    plot_types_of_changes(change_value_counts)

    # Fig 2a
    before_counts = df_version_change['firstVersion'].value_counts()
    after_counts = df_version_change['lastVersion'].value_counts()
    sum_counts = before_counts + after_counts
    sum_counts = sum_counts.fillna(0)

    some_set = list(set(df_version_change['firstVersion'].unique().tolist() + df_version_change['lastVersion'].unique().tolist()))
    some_set = sorted(some_set, key=lambda s: sum_counts.loc[s])
    before = []
    after = []

    for k in some_set:
        if k in before_counts.index:
            before.append(before_counts.loc[k])
        else:
            before.append(0)

        if k in after_counts.index:
            after.append(after_counts.loc[k])
        else:
            after.append(0)

    # some_set[some_set.index('conflicting interpretations of pathogenicity')] = 'conflicting interpretations\nof pathogenicity'
    # labels = ['pathogenic/likely\npathogenic', 'other', 'likely\npathogenic', 'pathogenic', 'conflicting\ninterpretations', 'benign', 'likely\nbenign', 'uncertain\nsignificance']
    labels = ['other', 'likely\npathogenic', 'pathogenic', 'conflicting\ninterpretations', 'benign', 'likely\nbenign', 'uncertain\nsignificance']
    plot_comparison_barplot(before, after, labels)


    # Fig 3
    # shows the distribution of clinical significance in the negative dataset
    df_merged = pd.read_csv('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/df_merged.csv', index_col=None)

    df = df_merged[df_merged['Reclassified'] == 0]['Description'].value_counts()
    #df
    xticklabels = ['uncertain\nsignificance', 'likely\nbenign', 'pathogenic',
       'likely\npathogenic', 'benign', 'conflicting\nterpretations', 'other']

    hist(df, xticklabels, '/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/plots/clin_sig_negative.png')



    # Fig 4
    # the distribution of clinical significance among the non-cancer dataset
    clinvar_non_cancer = pd.read_csv(
        '/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/filtered_non_cancer/filtered_ClinVarFullRelease_2018-11.csv',
        index_col=None)
    df = clinvar_non_cancer['Description'].value_counts()
    #df
    xticklabels = ['uncertain\nsignificance', 'likely\nbenign', 'pathogenic', 'benign',
       'likely\npathogenic', 'conflicting\ninterpretations',
       'other']
    hist(df, xticklabels)


    # Exploratory analysis
    df_merged = pd.read_csv('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/df_merged.csv', index_col=None)

    recl_value_counts = df_merged[df_merged['Reclassified'] == 1]['age_years'].value_counts()
    not_recl_value_counts = df_merged[df_merged['Reclassified'] == 0]['age_years'].value_counts()
    hist(recl_value_counts, xlabel='Years', xticks=range(7))
    hist(not_recl_value_counts, xlabel='Years', xticks=range(7))

    # visual differences


    cols = ['Description', 'Type', 'MethodType', 'ReviewStatus', 'Origin'] # ,'age_years']  # ? age_months
    df_merged_recl = df_merged[df_merged['Reclassified'] == 1]
    df_merged_not_recl = df_merged[df_merged['Reclassified'] == 0]

    num_recl = df_merged_recl.shape[0]
    num_not_recl = df_merged_not_recl.shape[0]

    for col in cols:

        df_merged_recl_vc = df_merged_recl[col].value_counts()
        df_merged_not_recl_vc = df_merged_not_recl[col].value_counts()

        labels = set(df_merged_recl_vc.index.tolist() + df_merged_not_recl_vc.index.tolist())

        class1 = [df_merged_recl_vc.loc[label]/num_recl if label in df_merged_recl_vc.index else 0 for label in labels]
        class2 = [df_merged_not_recl_vc.loc[label]/num_not_recl if label in df_merged_not_recl_vc.index else 0 for label in labels]

        if col == 'Description':
            labels = ['benign', 'pathogenic', 'other', 'likely\npathogenic', 'likely\nbenign', 'conflicting\ninterpretations', 'uncertain\nsignificance']
        elif col == 'Type':
            labels =  ['duplication', 'single nucleotide\nvariant', 'indel', 'cnv']
        elif col == 'MethodType':
            labels = ['literature\nonly', 'clinical\ntesting', 'research', 'curation']
        elif col == 'ReviewStatus':
            labels = ['no assertion\ncriteria', 'single\nsubmitter', 'expert\npanel', 'multiple\nsubmitters', 'conflicting\ninterpretations']
        elif col == 'Origin':
            labels = ['germline', 'somatic', 'unknown']

        plot_comparison_barplot(class1, class2, labels, ylabel='Proportion', xlabel=col, class1_label='Reclassified', class2_label='Not reclassified')

        # time projection
        df_merged_dummy = pd.get_dummies(df_merged,
                                         columns=['Description', 'Type', 'MethodType', 'Origin', 'ReviewStatus'],
                                         drop_first=False)
        df_merged_dummy.drop(
            labels=['RCV', 'Version', 'DateLastEvaluated', 'DateUpdated', 'first_file', 'recl_file', 'date_added',
                    'date_recl', 'age_days', 'age_months'], axis=1, # age_years
            inplace=True)  # not droping reclassified and review status

        # x = df_merged_dummy[(df_merged_dummy['Description_uncertain significance'] == 1) & (df_merged_dummy['Reclassified'] == 0)]['age_years'].value_counts() / df_merged_dummy[df_merged_dummy['Reclassified'] == 0]['age_years'].value_counts()
        x = df_merged_dummy[(df_merged_dummy['Description_uncertain significance'] == 1) & (df_merged_dummy['Reclassified'] == 0)]['age_years'].value_counts()
        # x = df_merged_dummy[(df_merged_dummy['Description_uncertain significance'] == 1) & (df_merged_dummy['Reclassified'] == 1)]['age_years'].value_counts() / df_merged_dummy[df_merged_dummy['Reclassified'] == 0]['age_years'].value_counts()
        x = df_merged_dummy[(df_merged_dummy['Description_uncertain significance'] == 1) & (df_merged_dummy['Reclassified'] == 1)]['age_years'].value_counts()
        hist(x, xlabel='Years', xticks=range(7))

        x = df_merged_dummy['age_years'].value_counts()


        # x = df_merged_dummy[(df_merged_dummy['ReviewStatus_reviewed by expert panel'] == 1) & (df_merged_dummy['Reclassified'] == 0)]['age_years'].value_counts() / df_merged_dummy[df_merged_dummy['Reclassified'] == 0]['age_years'].value_counts()
        x = df_merged_dummy[(df_merged_dummy['ReviewStatus_reviewed by expert panel'] == 1) & (df_merged_dummy['Reclassified'] == 0)]['age_years'].value_counts()
        # x = df_merged_dummy[(df_merged_dummy['ReviewStatus_reviewed by expert panel'] == 1) & (df_merged_dummy['Reclassified'] == 1)]['age_years'].value_counts() / df_merged_dummy['age_years'].value_counts()
        x = df_merged_dummy[(df_merged_dummy['ReviewStatus_reviewed by expert panel'] == 1) & (df_merged_dummy['Reclassified'] == 1)]['age_years'].value_counts()
        hist(x, xlabel='Years', xticks=range(7))


if __name__ == '__main__':
    main()