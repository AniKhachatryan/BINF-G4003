# Author: Ani Khachatryab
# Date & Time: 12/17/18 1:20 PM

import os
import pandas as pd
import datetime


def main():
    df_merged = pd.read_csv('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/df_merged.csv', index_col='RCV')

    last_date = datetime.datetime(2018, 11, 1)
    df_merged['DateLastEvaluated'] = pd.to_datetime(df_merged['DateLastEvaluated'])
    df_merged.dropna(axis=0, subset=['DateLastEvaluated'], inplace=True)
    df_merged['DLE'] = df_merged['DateLastEvaluated'].apply(lambda d: round((last_date - d).days / (12 * 30)))
    df_version_change = pd.read_csv('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/df_version_change.csv', index_col='RCV')
    df_first_versions = pd.read_csv('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/first_versions.csv', index_col='RCV')

    # for each RCV get the first file
    df_merged['first_file'] = df_first_versions.loc[df_merged.index]['filename']

    # make a rclassified rcv set
    recl_rcv_set = set(df_merged[df_merged['Reclassified']==1].index.tolist())

    csv_dir = '/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/processed_filtered_csv_cancer'

    d = {}

    l = os.listdir(csv_dir)
    l = sorted(l, key=lambda s: (int(s.split('_')[2].split('.')[0].split('-')[0]), int(s.split('_')[2].split('.')[0].split('-')[1][:2]), s.split('_')[2].split('.')[0].split('-')[1][2:]))

    i = 0
    for filename in l:
        i += 1
        print(filename, i)
        filepath = os.path.join(csv_dir, filename)
        df_ = pd.read_csv(filepath, index_col=None)

        for index, row in df_.iterrows():
            RCV = row['RCV']
            Description = row['Description']
            # print(RCV)
            if RCV in recl_rcv_set:
                if not d.get(RCV, False):
                    if Description == df_version_change.loc[RCV]['lastVersion']:
                        d[RCV] = filename

    # add the dictionary info to df_merged
    df_merged['recl_file'] = 'NA'

    # calculate age (im months and years)
    # for recl: date recl - date added
    # for w/o recl: Nov 2018 - date added

    recl_files_df = pd.DataFrame.from_dict(d, orient='index')
    df_merged.loc[recl_files_df.index, 'recl_file'] = recl_files_df[0]

    df_merged['date_added'] = df_merged['first_file'].apply(lambda f: datetime.date(int(f.split('_')[2].split('.')[0].split('-')[0]), \
                                                                                    int(f.split('_')[2].split('.')[0].split('-')[1]), 1))
    last_file = l[-1]
    last_date = datetime.date(int(last_file.split('_')[2].split('.')[0].split('-')[0]), int(last_file.split('_')[2].split('.')[0].split('-')[1]), 1)
    df_merged['date_recl'] = df_merged['recl_file'].apply(lambda f: last_date if f == 'NA' else \
        datetime.date(int(f.split('_')[2].split('.')[0].split('-')[0]), \
        int(f.split('_')[2].split('.')[0].split('-')[1]), 1))

    df_merged['age_days'] = df_merged['date_recl'] - df_merged['date_added']
    df_merged['age_months'] = df_merged['age_days'].apply(lambda td: int(round(td.days/30)))
    df_merged['age_years'] = df_merged['age_months'].apply(lambda m: int(m/12))

    df_merged.to_csv('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/df_merged.csv')


if __name__ == '__main__':
    main()
