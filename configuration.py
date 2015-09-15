from supy.defaults import *
import supy


def mainTree():
    return ("/", "Ntuple")

def useCachedFileLists():
    return False

def leavesToBlackList():
    return ["weight"]

def cppFiles():
    return ["cpp/linkdef.cxx"]

def initializeROOT(r, cppFiles=[]):
    r.gStyle.SetPalette(1)
    r.TH1.SetDefaultSumw2(True)
    r.gErrorIgnoreLevel = 2000
    r.gROOT.SetBatch(True)
    for sourceFile in cppFiles:
        r.gROOT.LoadMacro(sourceFile + "+")

def cppROOTDictionariesToGenerate():
    return [#("pair<string,bool>", "string"),
            ]

def experiment():
    return "cms"
