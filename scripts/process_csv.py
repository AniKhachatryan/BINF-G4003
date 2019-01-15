# Author: Ani Khachatryab
# Date & Time: 12/14/18 8:05 PM

import os
import pandas as pd
import datetime


def process_csv(file, indir, outdir):
    df = pd.read_csv(os.path.join(indir, file))
    df.dropna(axis=0, subset=['RCV', 'Description', 'Type', 'MethodType', 'ReviewStatus', 'Origin', 'DateLastEvaluated'], inplace=True)
    df = df.applymap(lambda s: s.lower().strip() if type(s) == str else s)

    # Description
    likely_pathogenic_list = ['probably pathogenic', 'likely pathogenic, other', 'likely pathogenic, risk factor', 'pathogenic/likely pathogenic', 'pathogenic/likely pathogenic, other', 'pathogenic/likely pathogenic, risk factor']
    likely_benign_list = ['probably not pathogenic', 'likely benign, risk factor', 'likely benign, other', 'benign/likely benign', 'benign/likely benign, other', 'benign/likely benign, affects']
    other_list = ['not provided', 'affects, other']
    pathogenic_list = ['pathogenic, risk factor', 'pathogenic, other', 'pathogenic, association', 'pathogenic, affects']
    uncertain_significance_list = ['no known pathogenicity', 'variant of unknown significance', 'uncertain significance, risk factor', 'uncertain significance, other', 'uncertain significance, affects']
    conflicting_list = ['conflicting interpretations of pathogenicity, affects, other', 'conflicting interpretations of pathogenicity, other', 'conflicting interpretations of pathogenicity, risk factor', 'conflicting data from submitters']
    benign_list = ['benign, other']
    remove_description = ['association', 'drug response', 'protective', 'risk factor', 'affects']

    df['Description'] = df['Description'].apply(
        lambda d: 'likely pathogenic' if d in likely_pathogenic_list else ('likely benign' if d in likely_benign_list
        else ('other' if d in other_list else ('pathogenic' if d in pathogenic_list else (
                'uncertain significance' if d in uncertain_significance_list else ('conflicting interpretations of pathogenicity'
                if d in conflicting_list else ('benign' if d in benign_list else d)))))))
    df = df[~df['Description'].isin(remove_description)]

    # Type

    indel_list = ['deletion', 'insertion']
    CNV_list = ['copy number gain', 'copy number loss']
    remove_type = ['microsatellite', 'complex', 'inversion', 'variation', 'protein only', 'translocation', 'fusion']

    df['Type'] = df['Type'].apply(
        lambda t: 'indel' if t in indel_list else ('cnv' if t in CNV_list else t))
    df = df[~df['Type'].isin(remove_type)]

    # MethodType

    remove_methodtype = ['not provided', 'phenotyping only', 'provider interpretation', 'in vitro',
                         'reference population', 'case-control', 'in vivo']
    df = df[~df['MethodType'].isin(remove_methodtype)]

    # ReviewStatus
    single_submitter_list = ['classified by single submitter']
    # TODO ???? if description is in conflict list -> 'criteria provided, conflicting interpretations'
    # else -> 'criteria provided, multiple submitters, no conflicts'
    multiple_submitters_list = ['classified by multiple submitters']
    remove_reviewstatus = ['no assertion provided', 'not classified by submitter', 'practice guideline']

    df['ReviewStatus'] = df['ReviewStatus'].apply(lambda r: 'criteria provided, single submitter' if r in single_submitter_list else ('criteria provided, multiple submitters, no conflicts' if r in CNV_list else r))
    df = df[~df['ReviewStatus'].isin(remove_reviewstatus)]

    df['ReviewStatus'] = df[['ReviewStatus', 'Description']].apply(lambda t: 'criteria provided, conflicting interpretations' if (t[0] in multiple_submitters_list) & (t[1] in conflicting_list) else ('criteria provided, multiple submitters, no conflicts' if (t[0] in multiple_submitters_list) & (t[1] not in conflicting_list) else t), axis=1)

    # Origin
    germline_list = ['maternal', 'paternal', 'inherited', 'uniparental', 'biparental']
    somatic_list = ['de novo']
    unknown_list = ['not provided', 'not-reported', 'not applicable', 'uncertain', 'tested-inconclusive']

    df['Origin'] = df['Origin'].apply(
        lambda o: 'germline' if o in germline_list else ('somatic' if o in somatic_list else ('unknown' if o in unknown_list else o)))

    print(os.path.join(outdir, file))
    df.to_csv(os.path.join(outdir, file), index=False)


def main():
    csv_dir = '/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/filtered_csv_cancer/'
    outdir = '/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/processed_filtered_csv_cancer/'
    file_list = os.listdir(csv_dir)

    for file in file_list:
        filepath = os.path.join(csv_dir,file)
        process_csv(file, csv_dir, outdir)

    # process_csv('filtered_ClinVarFullRelease_2018-11.csv', '/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/filtered_non_cancer/', '/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/filtered_non_cancer/')


if __name__ == '__main__':
    main()