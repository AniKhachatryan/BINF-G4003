# Author: Ani Khachatryab
# Date & Time: 12/3/18 7:41 PM

import os
import pandas as pd
import pickle
from collections import defaultdict


def main():
    df_first_versions = pd.read_csv('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/first_versions.csv', index_col='RCV')
    # df_latest = pd.read_csv('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/filtered_csv_cancer/filtered_ClinVarFullRelease_2018-11.csv')
    df_latest = pd.read_csv('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/processed_filtered_csv_cancer/filtered_ClinVarFullRelease_2018-11.csv')
    # df = pd.DataFrame(
    #     columns=['RCV', 'Version', 'Description', 'Type', 'DateUpdated', 'DateLastEvaluated', 'MethodType',
    #              'ReviewStatus', 'Origin', 'Reclassified'])

    # df_first_versions['Description'] = df_first_versions['Description'].str.lower()
    # df_latest['Description'] = df_latest['Description'].str.lower()

    dfs = []
    recl_dict = {}
    # creating the dataframe with the ones that are not reclassified and keeping track of reclassified
    i = 0
    for index, row in df_latest.iterrows():
        i += 1
        print(i)
        RCV = row['RCV']
        if df_first_versions.loc[RCV].shape[0] == 0:
            continue
        if df_first_versions.loc[RCV]['Description'] == row['Description']:
            # TODO change this bs way of making _df, just add a new Reclassified column
            _df = pd.DataFrame({'RCV': row['RCV'], 'Version': row['Version'], 'Description': row['Description'], \
                                'Type': row['Type'], 'DateUpdated': row['DateUpdated'], 'DateLastEvaluated': row['DateLastEvaluated'], \
                                'MethodType': row['MethodType'], 'ReviewStatus': row['ReviewStatus'], 'Origin': row['Origin'], 'Reclassified': 0}, index=[0])

            # row['Reclassified'] = 0
            dfs.append(_df)
        else:
            # print('first version:', df_first_versions.loc[RCV]['Description'])
            # print('last version:', row['Description'])
            recl_dict[RCV] = df_first_versions.loc[RCV]['filename']


    df = pd.concat(dfs)
    df.to_csv('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/not_reclassified_filtered_ClinVarFullRelease_2018-11.csv', index=False)
    # df = pd.read_csv('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/not_reclassified_filtered_ClinVarFullRelease_2018-11.csv', index_col=None)

    with open('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/recl_dict.pickle', 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(recl_dict, f, pickle.HIGHEST_PROTOCOL)

    # pulling the data for reclassified
    recl_dict_reverse = defaultdict(list)

    for k, v in recl_dict.items():
        recl_dict_reverse[v].append(k)

    filtered_csv_dir = '/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/processed_filtered_csv_cancer'
    dfs = []
    for k in recl_dict_reverse.keys():
        print(k)
        df_ = pd.read_csv(os.path.join(filtered_csv_dir, k))
        for RCV in recl_dict_reverse[k]:
            print(RCV)
            _df = df_[df_['RCV'] == RCV]
            _df.loc[:, 'Reclassified'] = [1]
            dfs.append(_df)
            # print('first version:', _df[_df['RCV' == RCV]]['Description'])
            # print('last version:', df_latest[df_latest['RCV'] == RCV]['Description'])

    df_2 = pd.concat(dfs)
    df_2['Description'] = df_2['Description'].str.lower()

    df_merged = pd.concat([df, df_2])
    df_merged.to_csv('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/df_merged.csv', index=False)


if __name__ == '__main__':
    main()
