#!/bin/bash

dir='/media/ani/DATA/Columbia/BINFG4003/BINF-G4003/data/xml'
declare -a arr=("2012" "2013" "2014" "2015" "2016" "2017" "2018")

for i in "${arr[@]}"; do
            echo $i
	    cur_dir=$dir/$i
	    if [ -d "$cur_dir" ]; then
  		echo $i exists
	    else
		mkdir $cur_dir
		cd $cur_dir
		wget -r -nd ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/xml/archive/$i/
		rm *.md5
	    fi
	done

