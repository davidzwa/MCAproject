#!/bin/bash
outfilename="resultsfile.txt"


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
OUTFILE="$DIR/$outfilename"
#clear previous output file
rm $OUTFILE

MAPARRAY=(*/);
ls >> $MAPARRAY

#header row
echo -n "Architecture name,LUTS,Sliceregisters,ram36,ram18,dsp,area,energy,performance" >> $OUTFILE
for i in {0..16}
do
   echo -n ",core-programname, cycles, imiss, drmiss, dwmiss" >>$OUTFILE
done
echo '' >> $OUTFILE
#done



for dir in "${MAPARRAY[@]}"; do
    cd $dir
    cd results
    echo  -n "$dir" >> $OUTFILE
    
    #timing met ?
    if ! grep -q "All timing constraints were met" timing.txt; then
		echo -n'!!!!timing was not met!!!!' >> $OUTFILE
		echo '!!!!timing was not met!!!!'
    fi
    
	slices=$(grep -F "Number of Slice Registers:" area.txt | awk -F':' '{ print $2 }' | awk -F'out' '{ print $1 }'| tr -d ',')
	luts=$(grep -F "Number of Slice LUTs:" area.txt| awk -F':' '{ print $2 }' | awk -F'out' '{ print $1 }'| tr -d ',')
    ram36=$(grep -F "Number using RAMB36E1 only:" area.txt | awk -F':' '{ print $2 }'| tr -d ',')
	ram18=$( grep -F "Number using RAMB18E1 only:" area.txt | awk -F':' '{ print $2 }'| tr -d ',')
	dsp=$(grep -F "Number of DSP48E1s:" area.txt | awk -F':' '{ print $2 }' | awk -F'out' '{ print $1 }'| tr -d ',')
	energy=$(grep -F "Average: " energy.txt |awk -F':' '{ print $2 }')
	performance=$(grep -F "Average: " performance.txt |awk -F':' '{ print $2 }')
	
	#area calculation
	area="$(( ($luts/8)+($slices/16)+(50*(($dsp)+($ram36)+(($ram18)/2))) ))"
	
	echo -n ','$luts >> $OUTFILE
	echo -n ','$slices >> $OUTFILE
    echo -n ','$ram36 >> $OUTFILE
	echo -n ','$ram18 >> $OUTFILE
	echo -n ','$dsp >> $OUTFILE
	
	echo -n ','$area >> $OUTFILE
	echo -n ','$energy >> $OUTFILE
	echo -n ','$performance >> $OUTFILE

	#cycles and misses
	LOGARRAY=($(ls run1* | grep '\.log$'))
	echo $dir
	
	#for each log file
	for thislog in "${LOGARRAY[@]}"; do
	
		#echo $thislog
		core=$(echo $thislog | awk -F '.' '{ print $1 }'|awk -F '-' '{ print $2 }')
		csplit -s $thislog /^$/ {*}
		
		#for each part of each log file
		LOGPARTS=($(ls xx*))
		initcyc=0;
		for part in "${LOGPARTS[@]}"; do
		
			#dont run on empty files
			if [[ $(wc -l <$part) -ge 2 ]]; then
			
			program=$(grep -B 1 "CYC" $part|head -1)
			cyc=0;
			
			#if it is the init program set the init cyc
			if [ "$program" = "init" ]; then
				initcyc=$(grep -F "CYC" $part | awk -F':' '{ print $2 }')
				cyc=$initcyc
			else
				cyc=$((  $(grep -F "CYC" $part | awk -F':' '{ print $2 }') - $initcyc ))
			fi
			imiss=$(grep -F "IMISS" $part | awk -F':' '{ print $2 }')
			drmiss=$(grep -F "DRMISS" $part | awk -F':' '{ print $2 }')
			dwmiss=$(grep -F "DWMISS" $part | awk -F':' '{ print $2 }')
			echo -n ','$core$program			>> $OUTFILE
			echo -n ','$cyc		>> $OUTFILE
			echo -n ','$imiss		>> $OUTFILE
			echo -n ','$drmiss		>> $OUTFILE
			echo -n ','$dwmiss		>> $OUTFILE
			#echo '  cyc:'$cyc			>> $OUTFILE
			#echo '  imiss:'$imiss		>> $OUTFILE
			#echo '  drmiss:'$drmiss		>> $OUTFILE
			#echo '  dwmiss:'$dwmiss		>> $OUTFILE
			
			fi
		
		done
		rm -rf xx*
 
	done
	echo '' >> $OUTFILE
    cd $DIR
done
