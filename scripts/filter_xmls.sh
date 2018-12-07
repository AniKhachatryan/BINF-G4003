#!/bin/bash

cd /media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/xml
dir=`pwd`
git_dir=/media/ani/DATA/Columbia/BINFG4003/BINF-G4003
filtered_dir=/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/filtered_xml_cancer
echo $dir

declare -a arr=("2012" "2013" "2014" "2015" "2016" "2017" "2018")

for i in "${arr[@]}"; do
            echo item: $i
	    cur_dir=$dir/$i
	    if [ -d "$cur_dir" ]; then
		for f in $cur_dir/*
		do
			bf=$(basename $f)
			if [ ${bf: -3} == '.gz' ]; then
				if [ ! -f $filtered_dir/$i/filtered_${bf::-3} ]; then
                                	gunzip $f
					python3.6 $git_dir/scripts/filter_xml_breast_cancer.py -f $f
					gzip ${f::-3}
				fi
			else
				if [ ! -f $filtered_dir/$i/filtered_${bf} ]; then
					python3.6 $git_dir/scripts/filter_xml_breast_cancer.py -f $f
					gzip $f
				fi
			fi
		done

	    fi
        done
