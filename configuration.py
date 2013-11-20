from supy.defaults import *
import supy


def mainTree():
    return ("ttTreeFinal", "eventTree")


def useCachedFileLists():
    return False


def LorentzVectorType():
    return ('PtEtaPhiM4D', 'double')


def experiment():
    return "cms"
