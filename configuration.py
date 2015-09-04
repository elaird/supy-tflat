from supy.defaults import *
import supy


def mainTree():
    return ("/", "Ntuple")

def useCachedFileLists():
    return False

def leavesToBlackList():
    return ["weight"]

def LorentzVectorType():
    return ('PtEtaPhiM4D', 'float')

def cppFiles() :
    return ["cpp/linkdef.cxx"]

def cppROOTDictionariesToGenerate():
    return [#("pair<string,bool>", "string"),
            ]

def experiment():
    return "cms"
