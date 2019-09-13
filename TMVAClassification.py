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
# cutStrS = cutStrC+" && ( isTraining == 1 || isTraining == 2 )"
cutStrS = cutStrC+" && ( isTraining == 1 )"
cutStrB = cutStrC


# Default settings for command line arguments
DEFAULT_OUTFNAME = "weights/TMVA.root"
DEFAULT_INFNAME  = "180"
DEFAULT_TREESIG  = "TreeS"
DEFAULT_TREEBKG  = "TreeB"
DEFAULT_METHODS  = "BDT"
# "Cuts,CutsD,CutsPCA,CutsGA,CutsSA,Likelihood,LikelihoodD,LikelihoodPCA,LikelihoodKDE,LikelihoodMIX,PDERS,PDERSD,PDERSPCA,PDEFoam,PDEFoamBoost,KNN,LD,Fisher,FisherG,BoostedFisher,HMatrix,FDA_GA,FDA_SA,FDA_MC,FDA_MT,FDA_GAMT,FDA_MCMT,MLP,MLPBFGS,MLPBNN,CFMlpANN,TMlpANN,SVM,BDT,BDTD,BDTG,BDTB,BDTF,RuleFit"
DEFAULT_NTREES   = "50"
DEFAULT_MDEPTH   = "2"#str(len(varList))
DEFAULT_VARLISTKEY = "BigComb"
#print "Usage: python %s [options]" % sys.argv[2]
# Print usage help
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
    print " "

# Main routine
def main():

    try:
        # retrive command line options
        shortopts  = "m:i:n:d:k:l:t:o:vh?"
        longopts   = ["methods=", "inputfile=", "nTrees=", "maxDepth=", "mass=", "varListKey=", "inputtrees=", "outputfile=", "verbose", "help", "usage"]
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
        elif o in ("-v", "--verbose"):
            verbose = True

    varList = varsList.varList[varListKey]
    nVars = str(len(varList))+'vars'
    Note=methods+'_'+varListKey+'_'+nVars+'_mDepth'+mDepth
    outfname = "dataset/weights/TMVA_"+Note+".root"
    # Print methods
    mlist = methods.replace(' ',',').split(',')
    print "=== TMVAClassification: use method(s)..."
    for m in mlist:
        if m.strip() != '':
            print "=== - <%s>" % m.strip()
			
    # Import ROOT classes
    from ROOT import gSystem, gROOT, gApplication, TFile, TTree, TCut
    
    # check ROOT version, give alarm if 5.18 
    if gROOT.GetVersionCode() >= 332288 and gROOT.GetVersionCode() < 332544:
        print "*** You are running ROOT version 5.18, which has problems in PyROOT such that TMVA"
        print "*** does not run properly (function calls with enums in the argument are ignored)."
        print "*** Solution: either use CINT or a C++ compiled version (see TMVA/macros or TMVA/examples),"
        print "*** or use another ROOT version (e.g., ROOT 5.19)."
        sys.exit(1)
        
    # Import TMVA classes from ROOT
    from ROOT import TMVA

    # Output file
    outputFile = TFile( outfname, 'RECREATE' )
    
    # Create instance of TMVA factory (see TMVA/macros/TMVAClassification.C for more factory options)
    # All TMVA output can be suppressed by removing the "!" (not) in 
    # front of the "Silent" argument in the option string
    factory = TMVA.Factory( "TMVAClassification", outputFile, 
                            "!V:!Silent:Color:DrawProgressBar:Transformations=I;:AnalysisType=Classification" )

    loader = TMVA.DataLoader("dataset")
    
    # Set verbosity
#     factory.SetVerbose( verbose )
    
    # If you wish to modify default settings 
    # (please check "src/Config.h" to see all available global options)
    #    gConfig().GetVariablePlotting()).fTimesRMS = 8.0
    (TMVA.gConfig().GetIONames()).fWeightFileDir = "weights/"+Note

    # Define the input variables that shall be used for the classifier training
    # note that you may also use variable expressions, such as: "3*var1/var2*abs(var3)"
    # [all types of expressions that can also be parsed by TTree::Draw( "expression" )]


    for iVar in varList:
        if iVar[0]=='NJets_JetSubCalc': loader.AddVariable(iVar[0],iVar[1],iVar[2],'I')
        else: loader.AddVariable(iVar[0],iVar[1],iVar[2],'F')

    # You can add so-called "Spectator variables", which are not used in the MVA training, 
    # but will appear in the final "TestTree" produced by TMVA. This TestTree will contain the 
    # input variables, the response values of all trained MVAs, and the spectator variables

    inputDir = varsList.inputDir
    infname = "TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_hadd.root"
    iFileSig = TFile.Open(inputDir+infname)
    sigChain = iFileSig.Get("ljmet")

    loader.AddSignalTree(sigChain)
    bkg_list = []
    bkg_trees_list = []
    hist_list = []
    weightsList = []
    bkgList = varsList.bkg
    
    for i in range(len(bkgList)):
        bkg_list.append(TFile.Open(inputDir+bkgList[i]))
        print inputDir+bkgList[i]
        bkg_trees_list.append(bkg_list[i].Get("ljmet"))
        bkg_trees_list[i].GetEntry(0)

        if bkg_trees_list[i].GetEntries() == 0:
            continue
        loader.AddBackgroundTree( bkg_trees_list[i], 1)

    signalWeight = 1 #0.0159/sigChain.GetEntries() #xs (pb)


    # ====== register trees ====================================================
    # To give different trees for training and testing, do as follows:
    #    loader.AddSignalTree( signalTrainingTree, signalTrainWeight, "Training" )
    #    loader.AddSignalTree( signalTestTree,     signalTestWeight,  "Test" )
    
    # Use the following code instead of the above two or four lines to add signal and background 
    # training and test events "by hand"
    # NOTE that in this case one should not give expressions (such as "var1+var2") in the input 
    #      variable definition, but simply compute the expression before adding the event
    #
    #    # --- begin ----------------------------------------------------------
    #    
    # ... *** please lookup code in TMVA/macros/TMVAClassification.C ***
    #    
    #    # --- end ------------------------------------------------------------
    #
    # ====== end of register trees ==============================================    
            
    # Set individual event weights (the variables must exist in the original TTree)
    #    for signal    : loader.SetSignalWeightExpression    ("weight1*weight2");
    #    for background: loader.SetBackgroundWeightExpression("weight1*weight2");
    loader.SetSignalWeightExpression( weightStrS )
    loader.SetBackgroundWeightExpression( weightStrB )

    # Apply additional cuts on the signal and background sample. 
    # example for cut: mycut = TCut( "abs(var1)<0.5 && abs(var2-0.5)<1" )
    mycutSig = TCut( cutStrS )
    mycutBkg = TCut( cutStrB ) 

    # Here, the relevant variables are copied over in new, slim trees that are
    # used for TMVA training and testing
    # "SplitMode=Random" means that the input events are randomly shuffled before
    # splitting them into training and test samples
    loader.PrepareTrainingAndTestTree( mycutSig, mycutBkg,
                                        "nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V" )

    # --------------------------------------------------------------------------------------------------

    # ---- Book MVA methods
    #
    # please lookup the various method configuration options in the corresponding cxx files, eg:
    # src/MethoCuts.cxx, etc, or here: http://tmva.sourceforge.net/optionRef.html
    # it is possible to preset ranges in the option string in which the cut optimisation should be done:
    # "...:CutRangeMin[2]=-1:CutRangeMax[2]=1"...", where [2] is the third input variable

    # Cut optimisation

# bdtSetting for "BDT" 
    bdtSetting = '!H:!V:NTrees=%s:MaxDepth=%s' %(nTrees,mDepth)
    bdtSetting += ':MinNodeSize=2.5%:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20'
    bdtSetting += ':IgnoreNegWeightsInTraining=True'
# bdtSetting for "BDTMitFisher" 
    bdtFSetting = '!H:!V:NTrees=%s' %nTrees
    bdtFSetting += ':MinNodeSize=2.5%:UseFisherCuts:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:SeparationType=GiniIndex:nCuts=20'
    bdtFSetting += ':IgnoreNegWeightsInTraining=True'
# bdtSetting for "BDTG" 
    bdtGSetting = '!H:!V:NTrees=%s:MaxDepth=%s' %(nTrees,mDepth)
    bdtGSetting += ':MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20'
    bdtGSetting += ':Pray' #Pray takes into account the effect of negative bins in BDTG
    #bdtGSetting += ':IgnoreNegWeightsInTraining=True'
# bdtSetting for "BDTB" 
    bdtBSetting = '!H:!V:NTrees=%s' %nTrees
    bdtBSetting += ':MinNodeSize=2.5%:BoostType=Bagging:SeparationType=GiniIndex:nCuts=20'
    bdtBSetting += ':IgnoreNegWeightsInTraining=True'
# bdtSetting for "BDTD" 
    bdtDSetting = '!H:!V:NTrees=%s' %nTrees
    bdtDSetting += ':MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=20:VarTransform=Decorrelate'
    bdtDSetting += ':IgnoreNegWeightsInTraining=True'
#Note also that explicitly setting *nEventsMin* so far OVERWRITES the option recomeded ^[[0m


#BOOKING AN ALGORITHM
#     if methods=="BDT": factory.BookMethod( TMVA.Types.kBDT, "BDT",bdtSetting)
    if methods=="BDT": factory.BookMethod( loader, TMVA.Types.kBDT, "BDT",bdtSetting)    
    if methods=="BDTG": factory.BookMethod( TMVA.Types.kBDT, "BDTG",bdtGSetting)
    if methods=="BDTMitFisher": factory.BookMethod( TMVA.Types.kBDT, "BDTMitFisher",bdtFSetting)
    if methods=="BDTB": factory.BookMethod( TMVA.Types.kBDT, "BDTB",bdtBSetting)
    if methods=="BDTD": factory.BookMethod( TMVA.Types.kBDT, "BDTD",bdtDSetting)
    # --------------------------------------------------------------------------------------------------
            
    # ---- Now you can tell the loader to train, test, and evaluate the MVAs. 

    # Train MVAs
    print "train all method"
    factory.TrainAllMethods()

    print "test all method"
    # Test MVAs
    factory.TestAllMethods()
    
    # Evaluate MVAs
    factory.EvaluateAllMethods()    

    # Save the output.
    outputFile.Close()
    # save plots:
    os.chdir('dataset/weights/'+Note)

    if not gROOT.IsBatch(): TMVA.TMVAGui( outfname )
    print "DONE"

if __name__ == "__main__":
    main()
