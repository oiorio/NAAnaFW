import os, commands
import optparse 


usage = 'usage: %prog -se storage:port/srm/managerv2 -v failed -d 161012 -f samples.txt -p path/On/SE -o localOutputDirectory -V verboseLevel'
parser = optparse.OptionParser(usage)
#Specify the base parameters(default samples are hardcoded in the list below):

#Input/Output options:
parser.add_option('-s', '--storageElement',      dest='se',     type='string',     default = 'storage01.lcg.cscs.ch:8443/srm/managerv2',    help='Remote storaga element to fetch including port and manager version, examples: srm://storage01.lcg.cscs.ch:8443/srm/managerv2, stormfe1.pi.infn.it:8444/srm/managerv2')
parser.add_option('-o', '--outputDir',   dest='outdir',  type='string',     default = './mc/trees/',      help='Directory to create the trees folder')

#String fetching options:
parser.add_option('-d', '--date',      dest='date',     type='string',     default = '',   help='date of the job, in the crab format yymmdd_hhmmss, also accepts partial (e.g: 1610 for october 2016)')
parser.add_option('-v',   '--veto',     dest='veto',    type='string',     default = 'failed',  help='String to veto while fetching')

#If you want to get the samples from a .txt file:
parser.add_option('-f', '--file',      dest='file',     type='string',     default = '',      help='File for samples fetching')

#If you want to get a single sample specifying it directly in the command:
parser.add_option('-S','--singleSample',      dest='singleSample',     type='string',     default = '',    help='force to look for a single sample if specified. Overrides the -f option if both are present.')
parser.add_option('-p','--path',      dest='path',     type='string',     default = '/pnfs/lcg.cscs.ch/cms/trivcat/store/user/oiorio/ttDM/trees/2016/Oct/',    help='local path for the samples, if -f or -S options are specified.')

#Quality of life options:
parser.add_option('-V',   '--verbose',     dest='verbose', type='int', default=0,help="verbose level:0=steps performed, 1=final output list,2= detail from all functions")
parser.add_option('-n', '--dryrun',   dest='dryrun',  action='store_true', default=False, help="dry run: will look for the files, but will not write any list.")

(opt, args) = parser.parse_args()

###This funcTion searches recursively for root files in a remote path, requesting the path contains the word "sampleToFind" and returning an output file list:
def findRootFileInPath(ls_command,srm, initialPath,sampleToFind,extraString="",date="", veto = "failed",verbose=False):
    ls_command_exec = ls_command+srm+initialPath
    if verbose: print "command is: "+ ls_command_exec
    status,ls_la = commands.getstatusoutput( ls_command_exec )
    list = []
    list = ls_la.split(os.linesep)
    outlist =[]
    fetchlist =[]
    pulledlist =[]
    #print list
        
    for l in list:
        if l == initialPath:
#            print " can't search further! "
            continue
#       print "list element is: "+ l
#        print "sampleToFind is: "+ sampleToFind
#       print l
#       print date
#       print extraString 
        if (sampleToFind in l and not "failed" in l and not veto in l and (((extraString == "") or (extraString in l))) and (((date == "") or (("/"+date) in l))) ): 
#            print date
#            print extraString 
#            print " there's  sample in this element! "
#            print l
#            print "veto is " + veto + " is it in l? " + str(veto in l)
        
            if ".root" in l:
                #       print " there's a rootfile in this element! "
                outlist.append(l)
            else:
                fetchlist.append(l)
        else:
            if ".root" in l:
                continue
            else: fetchlist.append(l)

    if(len(outlist)==0):
        for l in fetchlist:
            if verbose: print " fetching now path " + l 
            pulledlist = findRootFileInPath(ls_command=ls_command,srm=srm, initialPath=l,sampleToFind=sampleToFind,extraString = extraString, date = date, veto = veto)

            if verbose: print " pulled list:"
            if verbose: print pulledlist
            for f in pulledlist:
                outlist.append(f)

    if verbose:
        print "path is "+ initialPath
        print " check outlist length "
        print len(outlist)
#    if status: raise RFIOErr('Dir not found')
    return outlist

###This one copies a files in an input list to another directory, returning a list wiht the copied file names:
def copyFilesInList(cp_command,srm, inputList, outputDir, maxSimultaneousCopies=1, verbose=False):
    
    m =0
    command_cp_exec = cp_command+srm
    for p in inputList:
        outName = outputDir
        words = p.split("/")
        for word in words:
            if(".root" in word):
                outName = outputDir+"/"+word
        command_ls_local = "ls "+ outName        

        check_doubles = commands.getstatusoutput(command_ls_local)
        
        print check_doubles
        if check_doubles[0]==512: 
            final=" &"
            m=m+1;
            if (m % maxSimultaneousCopies ==0):
                final = ""
#            print "final is: " + final
            command_cp_exec = cp_command+srm+p + " "+ outName +final
            print "command cp is :" +command_cp_exec
            os.system(command_cp_exec)

###This one copies a files in an input list to another directory, returning a list wiht the copied file names:
def printFilesInList(inputList, path, nameOut, outputDir, option = 'w',verbose=False):
 
    filename = outputDir+"list"+nameOut+".py"
    if (option == 'a'):
        filename = outputDir+"listAllSamples.py"
        
    f = open(filename, option)
    

#    f.write("import FWCore.ParameterSet.Config as cms \n")
    if(option == 'a'): f.write("filelist"+nameOut.replace("-","_")+" = [")
    if(option == 'w'): f.write("filelist = [")
    for l in inputList:
        for lsplit in l.split(path):
            if verbose: print lsplit
            if (".root" in lsplit): f.write("'root://xrootd.ba.infn.it//"+lsplit+"', \n")
    f.write("]\n")        

def listFromSamples(f,p,verbose=False):
    fopen = open(f,'r')
    sp = {}
#
    for l in fopen.readlines():
#        if verbose: print "reading line" +l
#        print l 
        parts = l.split("/")
        if len(parts)<2: continue
        sp[parts[1]] = p
        if verbose: print sp
    return sp
        
###MAIN###

cmdls = "lcg-ls"
cmdcp = "lcg-cp"
#srmLocal = "  -b -D srmv2 srm://storage01.lcg.cscs.ch:8443/srm/managerv2\?SFN="

srmLocal = "  -b -D srmv2 srm://"+ opt.se + "\?SFN="

#samplesAndPaths = {"TTJets":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/decosa/ttDM/Phys14_Tree_v2/"}

samplesAndPaths = {
    "ST_t-channel_top":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/oiorio/ttDM/trees/2016/Oct/",
    "ST_t-channel_antitop":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/oiorio/ttDM/trees/2016/Oct/",
    "TT_Tune":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/oiorio/ttDM/trees/2016/Oct/",
    "ST_tW_top":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/oiorio/ttDM/trees/2016/Oct/",
    "ST_tW_antitop":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/oiorio/ttDM/trees/2016/Oct/",
    "ST_s-channel":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/oiorio/ttDM/trees/2016/Oct/",
    "WJetsToLNu":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/oiorio/ttDM/trees/2016/Oct/",
    "DYJetsToLL":"/pnfs/lcg.cscs.ch/cms/trivcat/store/user/oiorio/ttDM/trees/2016/Oct/",
    }


outDir = opt.outdir
print "output directory is: ", outDir, " , fetching se: ", opt.se

if not opt.file == '':
    if not opt.singleSample=='':
        print "using file: ", opt.file, " through path: ", opt.path
        samplesAndPaths = listFromSamples(opt.file, opt.path)
    else: print "!!!WARNING!!! both -f and -S options are present! The latter will override the former, be sure this is what you intended!"

if not opt.singleSample=='':
    samplesAndPaths ={opt.singleSample,opt.path}

def writeSamplesAndPaths(sap, outputDir=outDir, option = 'w'):
    filename = outputDir+"samplesAndPaths.py"
        
    f = open(filename, option)
    
    f.write("samplesAndPaths = {")

    for sample in sap:
        f.write("'"+str(sample)+"':'"+str(sap[sample])+"',")
    f.write("}")  
  


os.system("mkdir "+outDir)
os.system("rm "+outDir+"/listAllSamples.py")
writeSamplesAndPaths(samplesAndPaths)

for sample in samplesAndPaths:
    path = samplesAndPaths[sample]

#    outputList = []
    outputListJES = []
    #print path
    outputListJES= findRootFileInPath(cmdls,srmLocal,path,sample,extraString ="",date=opt.date, veto = opt.veto, verbose=opt.verbose>1)
    if opt.verbose>0:
        print "final output list for "+sample+" is : "
        print outputListJES

    if not opt.dryrun:
        printFilesInList(outputListJES, "/pnfs/lcg.cscs.ch/cms/trivcat/", sample,outDir,"w",verbose=opt.verbose>1)
        printFilesInList(outputListJES, "/pnfs/lcg.cscs.ch/cms/trivcat/", sample,outDir,"a",verbose=opt.verbose>1)
    