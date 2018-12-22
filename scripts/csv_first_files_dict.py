# Author: Ani Khachatryan
# Date & Time: 12/3/18 11:59 PM

# get the file where the RCV first occured
# output: data frame (.csv) with corresponding file names for each RCV

import os
import pandas as pd
import pickle


def main():
    # csv_dir = '/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/filtered_csv_cancer'
    csv_dir = '/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/processed_filtered_csv_cancer'
    # df = pd.DataFrame(columns=['RCV', 'Description', 'filename'])
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
            if not d.get(RCV, False):
                d[RCV] = (Description, filename)
                # df = df.append({'RCV': RCV, 'Descripion': Description, 'filename': filename}, ignore_index=True)
    # print(d)
    with open('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/first_versions.pickle', 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(d, f, pickle.HIGHEST_PROTOCOL)
    # df.to_csv('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/rcv_first_files.csv')
    df_first_versions = pd.DataFrame.from_dict(d, orient='index', columns=['Description', 'filename'])
    df_first_versions.to_csv('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/first_versions.csv', index_label='RCV')


    # with open('/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/first_versions.pickle', 'rb') as f:
    #     # Pickle the 'data' dictionary using the highest protocol available.
    #     d = pickle.load(f)

if __name__ == '__main__':
    main()
