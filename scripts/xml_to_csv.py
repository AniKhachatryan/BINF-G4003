# Author: Ani Khachatryab
# Date & Time: 12/3/18 5:20 PM

import os
import pandas as pd
import xml.etree.ElementTree as ET


def parse_xml(filepath, outfile):
    if outfile is None:
        outfile = '/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/filtered_csv_cancer/' + os.path.basename(filepath)[:-4] + '.csv'
    # get an iterable
    context = ET.iterparse(filepath, events=("start", "end"))

    # turn it into an iterator
    context = iter(context)

    # get the root element
    event, root = next(context)

    dfs = []

    i = 0
    for event, elem in context:
        if event == 'end' and elem.tag == 'ReferenceClinVarAssertion':
            i += 1
            print(outfile, i)

            RCV = elem.find('ClinVarAccession').attrib['Acc']
            print(RCV)
            Version = elem.find('ClinVarAccession').attrib['Version']
            DateUpdated = elem.find('ClinVarAccession').attrib['DateUpdated']
            Description = elem.find('ClinicalSignificance').find('Description').text
            ReviewStatus = elem.find('ClinicalSignificance').find('ReviewStatus').text

            try:
                Type = elem.find('MeasureSet').find('Measure').attrib['Type']
            except:
                Type = 'NA'

            try:
                DateLastEvaluated = elem.find('ClinicalSignificance').attrib['DateLastEvaluated']
            except KeyError:
                DateLastEvaluated = 'NA'

            try:
                MethodType = elem.find('ObservedIn').find('Method').find('MethodType').text
            except AttributeError:
                MethodType = 'NA'

            try:
                Origin = elem.find('ObservedIn').find('Sample').find('Origin').text
            except AttributeError:
                Origin = 'NA'

            df_ = pd.DataFrame({'RCV': RCV, 'Version': Version, 'Description': Description, 'Type': Type,
                                 'DateUpdated': DateUpdated, 'DateLastEvaluated': DateLastEvaluated,
                                 'MethodType': MethodType, 'ReviewStatus': ReviewStatus, 'Origin': Origin},
                                index=[0])
            dfs.append(df_)
            root.clear()

    df = pd.concat(dfs, ignore_index=True)
    df.to_csv(outfile, index=False)


def main():
    cancer = False
    if cancer:
        data_dir = '/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/filtered_xml_cancer/'
        output_dir = '/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/filtered_csv_cancer/'
        for year in os.listdir(data_dir):
            data_dir_year = os.path.join(data_dir, year)
            for filename in os.listdir(data_dir_year):
                # print(os.path.join(output_dir, filename[:-4]+'.csv'))
                if not os.path.isfile(os.path.join(output_dir, filename[:-4]+'.csv')):
                    # print('parse', filename)
                    parse_xml(os.path.join(data_dir_year, filename))
    else:
        infile = '/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/filtered_non_cancer/filtered_ClinVarFullRelease_2018-11.xml'
        outfile = '/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/filtered_non_cancer/filtered_ClinVarFullRelease_2018-11.csv'
        parse_xml(infile, outfile)


if __name__ == '__main__':
    main()
