import os, glob

sampleList = [
'TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_hadd.root'
# 'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8_hadd.root',
# 'QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8_hadd.root',
# 'QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8_hadd.root',
# 'QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8_hadd.root',
# 'QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8_hadd.root',
# 'QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8_hadd.root',
# 'QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8_hadd.root',
# 'ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_hadd.root',
# 'ST_t-channel_antitop_5f_TuneCP5_PSweights_13TeV-powheg-madspin-pythia8_vtd_vts_prod_hadd.root',
# 'ST_t-channel_top_5f_TuneCP5_PSweights_13TeV-powheg-madspin-pythia8_vtd_vts_prod_hadd.root',
# 'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8_hadd.root',
# 'ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8_hadd.root',
# 'SingleElectron_Mar2018_hadd.root',
# 'SingleMuon_Mar2018_hadd.root',
# 'TTTT_TuneCP5_13TeV-amcatnlo-pythia8_hadd.root',
# 'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt0to700_hadd.root',
# 'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt1000toInf_hadd.root',
# 'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt700to1000_hadd.root',
# 'TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt0to700_hadd.root',
# 'TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt1000toInf_hadd.root',
# 'TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt700to1000_hadd.root',
# 'TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt0to700_hadd.root',
# 'TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt1000toInf_hadd.root',
# 'TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt700to1000_hadd.root',
# 'TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8_hadd.root',
# 'TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8_hadd.root',
# 'TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8_hadd.root',
# 'TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8_hadd.root',
# 'WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root',
# 'WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root',
# 'WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root',
# 'WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root',
# 'WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root'

]
shift = 'nominal'
runDir=os.getcwd()
inputPath = "/mnt/hadoop/store/user/jblee/TTTT/LJMet94X_1lepTT_013019_step2/"+shift+"/"
outputPath = "/mnt/hadoop/store/user/jblee/TTTT/LJMet94X_1lepTT_013019_step2_BDT/"+shift+"/"
weightPath = "/user_data/jlee/TTTT/test/CMSSW_9_4_6_patch1/src/TTTT/TMVA/dataset/weights/Keras_BigComb_53vars_mDepth2/TMVAClassification_PyKeras.weights.xml"
jobFileName_List = []

for sample in sampleList:
    print "#########"*10
    print sample
    os.chdir(runDir)
    pathInput = glob.glob(inputPath+sample)

    for file in pathInput:
        print "file : ", file
        outputFileName = file
        outputFileName = outputFileName.split(inputPath)[1]
        oFileP = outputPath+outputFileName       
        dict={'iFile':file,'oFile':oFileP,'wFile':weightPath,'outName':outputFileName}    
        jdf=open('condor_log/condor_'+outputFileName+'.job','w')
        jdf.write(
"""
executable = DNNapplication.sh
output = condor_log/condor_%(outName)s.out
error = condor_log/condor_%(outName)s.err
log = condor_log/condor_%(outName)s.log
arguments = %(iFile)s %(oFile)s %(wFile)s
+JobFlavour = "workday"
queue 1"""%dict)
        jdf.close()
        os.system('condor_submit condor_log/condor_'+outputFileName+'.job')