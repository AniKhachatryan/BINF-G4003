import os
import re
import argparse
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser('takes as input xml file, writes a filtered xml file containing just the ReferenceClinVarAssertion nodes relating to breast cancer/cancer')
parser.add_argument('-f', '--filename', dest='filename', help='input file path')
args = parser.parse_args()

args_filename = args.filename
if args_filename[-3:] == '.gz':
    args_filename = args_filename[:-3]


data_dir = '/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/'
filtered_dir = os.path.join(data_dir, 'filtered_xml_cancer')
# filtered_dir = os.path.join(data_dir, 'filtered_xml_breast_cancer')


def filter_xml(filepath, year, month):
    filtered_year_dir = os.path.join(filtered_dir, year)
    if not os.path.isdir(filtered_year_dir):
        os.mkdir(filtered_year_dir)
    out_filename = os.path.join(filtered_year_dir, 'filtered_' + os.path.basename(filepath))

    with open(out_filename, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<dummy_root>\n')

    # https://stackoverflow.com/questions/324214/what-is-the-fastest-way-to-parse-large-xml-docs-in-python
    # get an iterable
    context = ET.iterparse(filepath, events=("start", "end"))

    # turn it into an iterator
    context = iter(context)

    # get the root element
    event, root = next(context)

    i = 0
    cnt = 0
    for event, elem in context:
        # cnt += 1
        # print(cnt)
        if event == "end" and elem.tag == "ReferenceClinVarAssertion":
            elem_traitset = elem.find('TraitSet')
            if elem_traitset is None or elem_traitset.attrib['Type'] != "Disease":
                continue
            traitset_text = re.sub(r"\s+", ' ', ' '.join(elem_traitset.itertext())).strip()
            # del
            # print(traitset_text)
            # TODO add carcinoma or neoplasm?
            if 'cancer' in traitset_text:
            # if 'breast' in traitset_text and 'cancer' in traitset_text:
                # del
                i += 1
                print('cancer record found #', i, sep='')
                with open(out_filename, 'a') as f:
                    f.write(ET.tostring(elem).decode('utf-8'))
            root.clear()

    with open(out_filename, 'a') as f:
        f.write('</dummy_root>')
    # print('done')
    print(year+'-'+month+':', i, 'cancer records found')


def main():
    # os.chdir(filtered_dir)
    filename = os.path.basename(args_filename)
    year, month = filename.split('_')[1].split('.')[0].split('-')
    filter_xml(args_filename, year, month)


if __name__ == '__main__':
    main()
