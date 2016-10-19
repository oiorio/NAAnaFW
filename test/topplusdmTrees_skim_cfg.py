import commands, os
### *****************************************************************************************
### Usage:
###
### cmsRun topplusdmanaEDMntuples_cfg.py maxEvts=N sample="mySample/sample.root" version="1"7 outputLabel="myoutput"
### cmsRun topplusdmTrees_cfg.py maxEvts=-1 sample="file:/afs/cern.ch/work/w/wajid/NapoliFW/CMSSW_8_0_16/src/Analysis/B2GAnaFW/test/B2GEDMNtuple.root" outputLabel='ntuple.root'
### Default values for the options are set:
### maxEvts     = -1
### sample      = 'file:/scratch/decosa/ttDM/testSample/tlbsm_53x_v3_mc_10_1_qPV.root'
### outputLabel = 'analysisTTDM.root'
### *****************************************************************************************
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as opts



options = opts.VarParsing ('analysis')

options.register('maxEvts',
                 -1,# default value: process all events
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.int,
                 'Number of events to process')

SingleElTriggers = []
SingleMuTriggers = []
hadronTriggers = []


chan = "MET_Prompt"
chan = "TTbarDMJets_scalar_Mchi-50_Mphi-50"
#chan = "TTbarDMJets_scalar_Mchi-1_Mphi-50"
#chan = "TTbarDMJets_scalar_Mchi-10_Mphi-50"
chan = "DY"
chan = "WJ"
filedir= "/tmp/oiorio/"
cmd = "ls "+filedir+"/"+chan+"/"

status,ls_la = commands.getstatusoutput( cmd )
listFiles = ls_la.split(os.linesep)
files = []
#files = ["file:re-MiniAOD_17Jul/"+l for l in listFiles]
#files = ["file:"+filedir+"MET_Prompt/"+l for l in listFiles]
files = ["file:"+filedir+"/"+chan+"/"+l for l in listFiles]
options.register('sample',
                 #root://xrootd.ba.infn.it
                 #or 
                 #root://xrootd.unl.edu
                 #or
                 #root://xrootd.cern.ch
                 'root://xrootd.ba.infn.it//store/user/oiorio/ttDM/samples/2016/Oct/ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/crab_STt-channeltop4finclusiveDecays13TeV-powhegV2-madspin-pythia8TuneCUETP8M1/161011_132502/0000/B2GEDMNtuple_212.root',
#                 'file:../../B2GAnaFW/test/B2GEDMNtuple.root',
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 'Sample to analyze')

options.register('version',
                 #'53',
                 '71',
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 'ntuple version (53 or 71)')

options.register('outputLabel',
                 #                 'treesTTJetsNew_ttDMMCChangeJECs.root',
                 #'treesTTJetsNew_ttDMMCChangeJECs_DirectV4_MCCorr.root',
                 'treesTTJets.root',
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 'Output label')

options.register('isData',
                 False,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.bool,
                 'Is data?')

options.register('applyRes',
                 False,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.bool,
                 'ApplyResiduals?')

options.register('addPartonInfo',
                 True,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.bool,
                 'Add parton info??')



options.register('changeJECs',
                 False,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.bool,
                 'Apply new JECs?')

options.register('LHE',
                 False,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.bool,
                 'Keep LHEProducts')

options.register('lhesource',
                 'externalLHEProducer',
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 'LHEProducts source')

options.register('channel',
                 'ttDM',
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 'channel for weight evaluation'
                 )

options.parseArguments()

if(options.isData):options.LHE = False
options.LHE = False 
if(not options.isData): options.applyRes = False

l = ["singleTrigger"+str(s) for s in xrange(15)]
l = l + ["trigger2"+str(s) for s in xrange(15)]

#SingleElTriggers = ["HLT_Ele27_WPTight_Gsf_v2"]
#SingleElTriggers = SingleElTriggers + ["HLT_Ele32_eta2p1_WPTight_Gsf_v3"]
SingleElTriggers = ["HLT_Ele32_eta2p1_WPTight_Gsf_v"+str(s) for s in range(2,4)]
SingleElTriggers = SingleElTriggers + ["HLT_Ele27_eta2p1_WPTight_Gsf_v"+str(s) for s in xrange(2,4)]
#SingleElTriggers = SingleElTriggers + ["HLT_Ele27_eta2p1_WPLoose_Gsf_v"+str(s) for s in xrange(2,4)]

PhotonTriggers = [""]

#SingleMuTriggers = ["HLT_IsoMu22_v3","HLT_IsoTkMu22_v3"]
SingleMuTriggers = ["HLT_IsoMu22_v"+str(s) for s in range(2,4)]
SingleMuTriggers = SingleMuTriggers + ["HLT_IsoMu24_v"+str(s) for s in range(2,4)]
#SingleMuTriggers = SingleMuTriggers + ["HLT_IsoTkMu22_v"+str(s) for s in range(2,3)]

#SingleMuTriggers = SingleMuTriggers + ["HLT_IsoMu24_v2","HLT_IsoTkMu24_v2"]
#SingleMuTriggers = SingleMuTriggers + ["HLT_IsoTkMu24_v"+str(s) for s in range(2,3)]

hadronTriggers = [""]

if(options.isData):

    SingleElTriggers = ["HLT_Ele27_WPTight_Gsf","HLT_Ele32_eta2p1_WPTight_Gsf"]
    SingleElTriggers = SingleElTriggers + ["HLT_Ele27_WPTight_Gsf_v"+str(s) for s in xrange(10)]
    SingleElTriggers = SingleElTriggers + ["HLT_Ele32_eta2p1_WPTight_Gsf_v"+str(s) for s in xrange(10)]

    #Muons
    SingleMuTriggers = ["HLT_IsoMu22","HLT_IsoTkMu22"]
    SingleMuTriggers = SingleMuTriggers + ["HLT_IsoMu22_v"+str(s) for s in xrange(10)]
    SingleMuTriggers = SingleMuTriggers + ["HLT_IsoTkMu22_v"+str(s) for s in xrange(10)]

    SingleMuTriggers = SingleMuTriggers + ["HLT_IsoMu24","HLT_IsoTkMu24"]
    SingleMuTriggers = SingleMuTriggers + ["HLT_IsoMu24_v"+str(s) for s in xrange(10)]
    SingleMuTriggers = SingleMuTriggers + ["HLT_IsoTkMu24_v"+str(s) for s in xrange(10)]

    hadronTriggers = hadronTriggers+ [""]
    


process = cms.Process("ttDManalysisTrees")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.MessageLogger.categories.append('HLTrigReport')
### Output Report
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True)
                #,SkipEvent = cms.untracked.vstring('ProductNotFound') 
                )
### Number of maximum events to process
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvts) )
### Source file
process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
        options.sample
        )
)

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

from Configuration.AlCa.GlobalTag import GlobalTag as customiseGlobalTag
#process.GlobalTag = customiseGlobalTag(process.GlobalTag, globaltag = 'auto:run2_mc_50nsGRun')
#process.GlobalTag = customiseGlobalTag(process.GlobalTag, globaltag = '76X_mcRun2_asymptotic_v12')
process.GlobalTag = customiseGlobalTag(process.GlobalTag, globaltag = '80X_mcRun2_asymptotic_2016_miniAODv2')
#process.GlobalTag.connect   = 'frontier://FrontierProd/CMS_COND_31X_GLOBALTAG'
process.GlobalTag.pfnPrefix = cms.untracked.string('frontier://FrontierProd/')

### Rootplizer

process.TFileService = cms.Service("TFileService", fileName = cms.string(options.outputLabel))

process.load("Analysis.NAAnaFW.topplusdmedmRootTreeMaker_skim_cff")
#process.load("ttDM.treeDumper.topplusdmedmRootTreeMaker_with_cat_cff")
#process.load("B2GAnaFW.B2GAnaFW.topplusdmedmRootTreeMaker_cff")

process.DMTreesDumper.channelInfo.SingleElTriggers=cms.vstring(SingleElTriggers)
process.DMTreesDumper.channelInfo.SingleMuTriggers=cms.vstring(SingleMuTriggers)
process.DMTreesDumper.channelInfo.hadronicTriggers=cms.vstring(hadronTriggers)



if options.addPartonInfo:
    if options.isData: #G
        process.DMTreesDumper.channelInfo.getPartonW=cms.untracked.bool(True)
        process.DMTreesDumper.channelInfo.getPartonTop=cms.untracked.bool(True)
        process.DMTreesDumper.channelInfo.doWReweighting=cms.untracked.bool(True)
        process.DMTreesDumper.channelInfo.doTopReweighting=cms.untracked.bool(True)

    if not options.isData: #G                                                                                                                            
        process.DMTreesDumper.channelInfo.getPartonW=cms.untracked.bool(True)
        process.DMTreesDumper.channelInfo.getPartonTop=cms.untracked.bool(True)
        process.DMTreesDumper.channelInfo.doWReweighting=cms.untracked.bool(True)
        process.DMTreesDumper.channelInfo.doTopReweighting=cms.untracked.bool(True)
#process.DMTreesDumper.lhes =cms.InputTag("externalLHEProducer")
process.DMTreesDumper.lhes =cms.InputTag(options.lhesource)
#process.DMTreesDumper.lhes =cms.InputTag(options.lhesource)
process.DMTreesDumper.changeJECs = cms.untracked.bool(options.changeJECs)
process.DMTreesDumper.isData = cms.untracked.bool(options.isData)#This adds the L2L3Residuals
process.DMTreesDumper.applyRes = cms.untracked.bool(options.applyRes)#This adds the L2L3Residuals

#G
process.DMTreesDumper.channelInfo.useLHE = cms.untracked.bool(True)
#G
process.DMTreesDumper.channelInfo.useLHEWeights = cms.untracked.bool(True)


if options.channel == "ttbar":
    process.DMTreesDumper.getPartonTop  = cms.untracked.bool(True)

if options.channel == "wzjets":
    print "channel is " + options.channel 
    process.DMTreesDumper.channelInfo.getPartonW  = cms.untracked.bool(True)
    process.DMTreesDumper.channelInfo.getParticleWZ  = cms.untracked.bool(True)

if options.isData:
    process.DMTreesDumper.channelInfo.useLHE = cms.untracked.bool(False)
    process.DMTreesDumper.channelInfo.useLHEWeights = cms.untracked.bool(False)

if not options.isData:
    process.DMTreesDumper.channelInfo.useLHE = cms.untracked.bool(True)
    process.DMTreesDumper.channelInfo.useLHEWeights = cms.untracked.bool(True)

#if(options.isData): del process.DMTreesDumper.physicsObjects[-1]
process.analysisPath = cms.Path(
    process.DMTreesDumper
    )


#if(options.isData):
for p in process.DMTreesDumper.physicsObjects:
    if(p.prefix == cms.string("el")):
        p.variablesF.append(cms.InputTag("electrons","elvidVeto"))
        p.variablesF.append(cms.InputTag("electrons","elvidLoose"))
        p.variablesF.append(cms.InputTag("electrons","elvidMedium"))
        p.variablesF.append(cms.InputTag("electrons","elvidTight"))
            #print "yes"
        p.toSave.append("elvidVeto")
        p.toSave.append( "elvidLoose")
        p.toSave.append("elvidMedium")
        p.toSave.append("elvidTight")
            
