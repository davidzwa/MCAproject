#!/bin/bash
outfilename="resultsfile.txt"


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
OUTFILE="$DIR/$outfilename"

MAPARRAY=(*/);
ls >> $MAPARRAY

for dir in "${MAPARRAY[@]}"; do
    cd $dir
    cd results
    echo "$dir" >> $OUTFILE
    
    #timing met ?
    if ! grep -q "All timing constraints were met" timing.txt; then
		echo '!!!!timing was not met!!!!' >> $OUTFILE
    fi
    
    #area
	slices=$(grep -F "Number of Slice Registers:" area.txt | awk -F':' '{ print $2 }' | awk -F'out' '{ print $1 }')
	echo 'slices: '$slices >> $OUTFILE
	
	luts=$(grep -F "Number of Slice LUTs:" area.txt| awk -F':' '{ print $2 }' | awk -F'out' '{ print $1 }')
    echo 'luts: '$luts >> $OUTFILE
    
    ram36=$(grep -F "Number using RAMB36E1 only:" area.txt | awk -F':' '{ print $2 }')
    echo 'ram36: '$ram36 >> $OUTFILE

	ram18=$( grep -F "Number using RAMB18E1 only:" area.txt | awk -F':' '{ print $2 }')
	echo 'ram18: '$ram18 >> $OUTFILE
     
	dsp=$(grep -F "Number of DSP48E1s:" area.txt | awk -F':' '{ print $2 }' | awk -F'out' '{ print $1 }')
	echo 'dsp: '$dsp >> $OUTFILE
	
	#area calculation
	area=$()
	
	#energy
	energy=$(grep -F "Average: " energy.txt |awk -F':' '{ print $2 }')
	echo 'energy: '$energy >> $OUTFILE
	
	#performance
	performance=$(grep -F "Average: " performance.txt >> $OUTFILE|awk -F':' '{ print $2 }')
	echo 'performance: '$performance >> $OUTFILE
	
    cd $DIR
done
