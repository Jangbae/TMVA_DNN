import os,sys  # exit
import time   # time accounting
import getopt # command line parser
import ROOT as r
from ROOT import TMVA

outfname = "/user_data/jlee/TTTT/test/CMSSW_9_4_6_patch1/src/TTTT/TMVA/dataset/weights/TMVA_BDT_BigComb_53vars_mDepth2.root"
# outfname = "/user_data/jlee/TTTT/CMSSW_9_4_6_patch1/src/TMVA/dataset/weights/TMVA_Keras_BigComb_3vars_mDepth2.root"
TMVA.mvaeffs( 'dataset', outfname ) #Classifier Cut Efficiencies
TMVA.efficiencies('dataset', outfname, 1)
TMVA.correlations('dataset', outfname ) #Input Variable Linear Correlation Coefficients
TMVA.variables('dataset', outfname ) #Input variables (training sample)
TMVA.mvas( 'dataset', outfname, 0 )
TMVA.mvas( 'dataset', outfname, 3 )