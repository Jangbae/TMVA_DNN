#!/usr/bin/env python
# @(#)root/tmva $Id$
# ------------------------------------------------------------------------------ #
# Project      : TMVA - a Root-integrated toolkit for multivariate data analysis #
# Package      : TMVA                                                            #
# Python script: TMVAClassification.py                                           #
#                                                                                #
# This python script provides examples for the training and testing of all the   #
# TMVA classifiers through PyROOT.                                               #
#                                                                                #
# The Application works similarly, please see:                                   #
#    TMVA/macros/TMVAClassificationApplication.C                                 #
# For regression, see:                                                           #
#    TMVA/macros/TMVARegression.C                                                #
#    TMVA/macros/TMVARegressionpplication.C                                      #
# and translate to python as done here.                                          #
#                                                                                #
# As input data is used a toy-MC sample consisting of four Gaussian-distributed  #
# and linearly correlated input variables.                                       #
#                                                                                #
# The methods to be used can be switched on and off via the prompt command, for  #
# example:                                                                       #
#                                                                                #
#    python TMVAClassification.py --methods Fisher,Likelihood                    #
#                                                                                #
# The output file "TMVA.root" can be analysed with the use of dedicated          #
# macros (simply say: root -l <../macros/macro.C>), which can be conveniently    #
# invoked through a GUI that will appear at the end of the run of this macro.    #
#                                                                                #
# for help type "python TMVAClassification.py --help"                            #
# ------------------------------------------------------------------------------ #

# --------------------------------------------
# Standard python import
import os,sys  # exit
import time   # time accounting
import getopt # command line parser
import ROOT as r
import varsList

# --------------------------------------------
#weight and cut strings below are used for both background and signals!
weightStrC = "pileupWeight*lepIdSF*EGammaGsfSF*MCWeight_singleLepCalc/abs(MCWeight_singleLepCalc)"
weightStrS = weightStrC
weightStrB = weightStrC

cutStrC = "(NJets_JetSubCalc >= 5 && NJetsCSV_JetSubCalc >= 2) && ((leptonPt_singleLepCalc > 35 && isElectron) || (leptonPt_singleLepCalc > 30 && isMuon))"
cutStrS = cutStrC+" && ( isTraining == 1 || isTraining == 2 )"
cutStrB = cutStrC


# Default settings for command line arguments
DEFAULT_OUTFNAME = "weights/TMVA.root"
DEFAULT_INFNAME  = "180"
DEFAULT_TREESIG  = "TreeS"
DEFAULT_TREEBKG  = "TreeB"
DEFAULT_METHODS  = "BDT"
DEFAULT_NTREES   = "50"
DEFAULT_MDEPTH   = "2"#str(len(varList))
DEFAULT_VARLISTKEY = "BigComb"
DEFAULT_SEED     = "0"
def usage():
    print " "
    print "Usage: python %s [options]" % sys.argv[0]
    print "  -m | --methods    : gives methods to be run (default: all methods)"
    print "  -i | --inputfile  : name of input ROOT file (default: '%s')" % DEFAULT_INFNAME
    print "  -o | --outputfile : name of output ROOT file containing results (default: '%s')" % DEFAULT_OUTFNAME
    print "  -n | --nTrees : amount of trees for BDT study (default: '%s')" %DEFAULT_NTREES 
    print "  -d | --maxDepth : maximum depth for BDT study (default: '%s')" %DEFAULT_MDEPTH 
    print "  -l | --varListKey : BDT input variable list (default: '%s')" %DEFAULT_VARLISTKEY 
    print "  -t | --inputtrees : input ROOT Trees for signal and background (default: '%s %s')" \
          % (DEFAULT_TREESIG, DEFAULT_TREEBKG)
    print "  -v | --verbose"
    print "  -? | --usage      : print this help message"
    print "  -h | --help       : print this help message"
    print "  -s | --seed       : input seed for variable importance (default: '%s')" %DEFAULT_SEED 
    print " "

# Main routine
def main():

    try:
        # retrive command line options
        shortopts  = "m:i:n:d:k:l:t:o:s:vh?"
        longopts   = ["methods=", "inputfile=", "nTrees=", "maxDepth=", "mass=", "varListKey=", "inputtrees=", "outputfile=", "seed=", "verbose", "help", "usage"]
        opts, args = getopt.getopt( sys.argv[1:], shortopts, longopts )

    except getopt.GetoptError:
        # print help information and exit:
        print "ERROR: unknown options in argument %s" % sys.argv[1:]
        usage()
        sys.exit(1)

    infname     = DEFAULT_INFNAME
    treeNameSig = DEFAULT_TREESIG
    treeNameBkg = DEFAULT_TREEBKG
    outfname    = DEFAULT_OUTFNAME
    methods     = DEFAULT_METHODS
    nTrees      = DEFAULT_NTREES
    mDepth      = DEFAULT_MDEPTH
    varListKey  = DEFAULT_VARLISTKEY
    verbose     = True
    SeedN = DEFAULT_SEED
    for o, a in opts:
        if o in ("-?", "-h", "--help", "--usage"):
            usage()
            sys.exit(0)
        elif o in ("-m", "--methods"):
            methods = a
        elif o in ("-d", "--maxDepth"):
        	mDepth = a
        elif o in ("-l", "--varListKey"):
        	varListKey = a
        elif o in ("-i", "--inputfile"):
            infname = a
        elif o in ("-n", "--nTrees"):
            nTrees = a
        elif o in ("-o", "--outputfile"):
            outfname = a
        elif o in ("-t", "--inputtrees"):
            a.strip()
            trees = a.rsplit( ' ' )
            trees.sort()
            trees.reverse()
            if len(trees)-trees.count('') != 2:
                print "ERROR: need to give two trees (each one for signal and background)"
                print trees
                sys.exit(1)
            treeNameSig = trees[0]
            treeNameBkg = trees[1]
        elif o in ("-s", "--seed"):
            SeedN = long(a)
        elif o in ("-v", "--verbose"):
            verbose = True


    varList = varsList.varList[varListKey]
    nVars = str(len(varList))+'vars'
    Note=methods+'_'+varListKey+'_'+nVars+'_mDepth'+mDepth
    outfname = "dataset/weights/TMVA_"+Note+".root"
			
    # Import ROOT classes
    from ROOT import gSystem, gROOT, gApplication, TFile, TTree, TCut,TRandom3
    
    # check ROOT version, give alarm if 5.18 
    if gROOT.GetVersionCode() >= 332288 and gROOT.GetVersionCode() < 332544:
        print "*** You are running ROOT version 5.18, which has problems in PyROOT such that TMVA"
        print "*** does not run properly (function calls with enums in the argument are ignored)."
        print "*** Solution: either use CINT or a C++ compiled version (see TMVA/macros or TMVA/examples),"
        print "*** or use another ROOT version (e.g., ROOT 5.19)."
        sys.exit(1)
        
    # Import TMVA classes from ROOT
    from ROOT import TMVA
    
    fClassifier = TMVA.Factory( "VariableImportance", "!V:!ROC:!ModelPersistence:Silent:Color:!DrawProgressBar:AnalysisType=Classification" )
    str_xbitset = '{:053b}'.format(SeedN)
    
    seeddl = TMVA.DataLoader(str_xbitset)

    bdtSetting = '!H:!V:NTrees=%s:MaxDepth=%s' %(nTrees,mDepth)
    bdtSetting += ':MinNodeSize=2.5%:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20'
    bdtSetting += ':IgnoreNegWeightsInTraining=True'
    
    index = 52
    
    for iVar in varList:
        if (str_xbitset[index]=='1'): 
            seeddl.AddVariable(iVar[0],iVar[1],iVar[2],'F')
            print iVar[0]
        index = index - 1

    (TMVA.gConfig().GetIONames()).fWeightFileDir = "weights/"+Note

    inputDir = varsList.inputDir
    infname = "TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_hadd.root"
    iFileSig = TFile.Open(inputDir+infname)
    sigChain = iFileSig.Get("ljmet")

    seeddl.AddSignalTree(sigChain)
    bkg_list = []
    bkg_trees_list = []
    bkgList = varsList.bkg
    
    for i in range(len(bkgList)):
        bkg_list.append(TFile.Open(inputDir+bkgList[i]))
        bkg_trees_list.append(bkg_list[i].Get("ljmet"))
        bkg_trees_list[i].GetEntry(0)

        if bkg_trees_list[i].GetEntries() == 0:
            continue
        seeddl.AddBackgroundTree( bkg_trees_list[i], 1)

    signalWeight = 1

    seeddl.SetSignalWeightExpression( weightStrS )
    seeddl.SetBackgroundWeightExpression( weightStrB )

    mycutSig = TCut( cutStrS )
    mycutBkg = TCut( cutStrB ) 

    seeddl.PrepareTrainingAndTestTree( mycutSig, mycutBkg,
                                        "nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V" )

    fClassifier.BookMethod(seeddl,TMVA.Types.kBDT,"BDT",bdtSetting)
    fClassifier.TrainAllMethods()
    fClassifier.TestAllMethods()
    fClassifier.EvaluateAllMethods()

    SROC = fClassifier.GetROCIntegral(str_xbitset, "BDT")
    print "ROC-integral : ",str_xbitset, " ", SROC    
    print "SEED "+str_xbitset+" DONE"
    fClassifier.DeleteAllMethods()
    fClassifier.fMethodsMap.clear()
    print "==================================================================" 
    print "=================================================================="             

if __name__ == "__main__":
    main()
