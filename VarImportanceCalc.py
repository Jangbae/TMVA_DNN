#!/usr/bin/env python
import glob, os, math
import varsList

outPath = '/user_data/jlee/TTTT/test/CMSSW_9_4_6_patch1/src/TTTT/TMVA/condor_log/'

outPath = os.getcwd()
outFile = os.listdir(outPath+'/condor_log/')
seedList = []
for Files in outFile:
    if "Subseed_" not in Files and ".out" in Files:
        seedList.append(Files.split("_Seed_")[1].split(".out")[0])
        
os.chdir(outPath+'/condor_log/')

seedDict = {}
for indx, seed in enumerate(seedList):
    if indx > 100: break
    seedDict[seed] = glob.glob('BDT_BigComb_53vars_mDepth2_Seed_'+seed+'_Subseed_*.out')

importances = {}
for indx in range(0,53):
    importances[indx] = 0
    
for seeds in seedDict:
    l_seed = long(seeds)
    print "seed : ", seeds
    for line in open('BDT_BigComb_53vars_mDepth2_Seed_'+seeds+'.out').readlines():
        if 'ROC-integral' in line: 
            SROC = float(line[:-1].split(' ')[-1])
    for subseedout in seedDict[seeds]:
        subseed = subseedout.split("_Subseed_")[1].split(".out")[0]
        l_subseed = long(subseed)
        varIndx = math.log(l_seed - l_subseed)/0.693147
        for line in open('BDT_BigComb_53vars_mDepth2_Seed_'+seeds+'_Subseed_'+subseed+'.out').readlines():        
            if 'ROC-integral' in line: 
                SSROC = float(line[:-1].split(' ')[-1])
                importances[int(varIndx)] += SROC-SSROC

normalization = 0;
for indx in range(0,53):
    normalization += importances[indx]
for indx in range(0,53):
    print "importance : ", 100*importances[indx]/normalization, "        variable : ",varsList.varList['BigComb'][indx][0]
        