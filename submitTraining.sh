#!/bin/bash

date

nTrees=1000

#for mass in Low Med High 180 200 220 250 300 350 400 500 800 1000 2000 3000; do
for method in BDT; do
	for mass in Low Med 800 1000 2000 3000; do
		for vListKey in MAY25; do
			for mDepth in 3; do # 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16; do
				echo 'Submitting '$method' '$vListKey' mDepth'$mDepth' '$mass
				nohup python -u TMVAClassification.py -m $method -k $mass -l $vListKey -n $nTrees \
				-d $mDepth >& weights/${method}_${vListKey}_33vars_mDepth${mDepth}_M${mass}.log &
				sleep 5
			done
		done
	done
done

#for mass in Low Med High 180 200 220 250 300 350 400 500 800 1000 2000 3000; do
# for method in BDTG; do
# 	for mass in Low 180; do #180 200 220 250 300 350 400 500 800 1000 2000 3000; do #Low Med High; do
# 		for vListKey in BigComb; do
# 			for mDepth in 2 3; do # 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16; do
# 				for fld in 123 231 312; do
# 					echo 'Submitting '$method' '$vListKey' mDepth'$mDepth' '$mass
# 					nohup python -u TMVAClassification_folds.py -m $method -k $mass -l $vListKey -n $nTrees \
# 					-d $mDepth -f $fld >& weights/${method}_fold${fld}_${vListKey}_30vars_mDepth${mDepth}_M${mass}.log &
# 					sleep 5
# 				done
# 			done
# 		done
# 	done
# done

echo "DONE"

date
