import cPickle
import math
import supy
import ROOT as r


class LastBinOverBin(supy.calculables.secondary):
    '''
    When this step is run and the cache file does not exist, it will
    (a) retrieve the necessary numbers from the TChain files;
    (b) reject all events (preventing further processing);
    (c) sum the numbers retrieved from the files in each slice;
    (d) store them in a cache file.

    When this step is run and the cache file does exist, it will compute
    a ratio of histogram bin contents, and assign that to self.value.
    '''

    @property
    def name(self):
        return "LastBinOverBin%d" % self.iBin

    def __init__(self, dir="", histoName="", iBin=None):
        self.hPath = "%s/%s" % (dir, histoName)
        assert type(iBin) is int
        self.iBin = iBin
        self.value = 1.0
        self._continueProcessing = False
        self._varNames = ["nFiles", "nEventsBinI", "nEventsLastBin"]

    def checkCache(self, tag=None):
        # disable warning inherited from supy.calculables.secondary
        pass

    def deSliced(self, s):
        fileName = s[:-len(self.outputSuffix())]
        fileName = "_".join(fileName.split("_")[:-2]) # remove nSlices_iSlice from name
        return fileName + self.outputSuffix()

    def deWeighted(self, s):
        fileName = s[:-len(self.outputSuffix())]
        if fileName.count("."):
            print "FIXME: fileName hack"
            fileName = fileName[:fileName.find(".")] # remove weights from name
        return fileName + self.outputSuffix()

    def cacheFileName(self):
        fileName = self.deSliced(self.inputFileName)
        return self.deWeighted(fileName)

    def select(self, _):
        # if cache file has not been created, do not process event further
        return self._continueProcessing

    def update(self, _):
        # self.value is computed in self.setup()
        pass

    def setup(self, chain, fileDir):
        try:
            d = cPickle.load(open(self.cacheFileName()))
            assert d["nEventsBinI"]
            self.value = d["nEventsLastBin"] / d["nEventsBinI"]
            self._continueProcessing = True
        except IOError, e:
            assert e.errno == 2, e
            print e
            print "%s will reject all events and produce that file." % self.name

            self.varsToPickle = lambda: self._varNames
            elements = chain.GetListOfFiles()
            self.nFiles = elements.GetEntries()
            h = self.histo(elements)
            self.nEventsBinI = h.GetBinContent(self.iBin)
            self.nEventsLastBin = h.GetBinContent(h.GetNbinsX())

    def mergeFunc(self, products):
        d = {}
        for key in self._varNames:
            if key not in products:  # do not overwrite cache file
                return
            d[key] = sum(products[key])

        outputFileName = self.deWeighted(self.outputFileName)
        cPickle.dump(d, open(outputFileName, "w"))
        # NOTE: self.outputFileName (when not sliced) ==
        #       self.cacheFileName (when sliced)
        print "PAT-tuple skim-efficiency file %s\n" % self.outputFileName +\
            " was created from %d input files." % d["nFiles"]

    def histo(self, elements):
        # http://root.cern.ch/root/html/TChain.html#TChain:AddFile
        out = None
        for iElement in range(elements.GetEntries()):
            element = elements.At(iElement)
            f = r.TFile(element.GetTitle())
            assert f
            h = f.Get(self.hPath)
            assert h, "Histogram %s not found." % self.hPath
            if out:
                out.Add(h)
            else:
                out = h.Clone()
                out.SetDirectory(0)
            f.Close()
        return out


class jets(supy.wrappedChain.calculable):
    @property
    def name(self):
        return self.__name

    def __init__(self, var="", keys=[], sortBy="", nBranches=None, reverse=False, ptMin=None, absEtaMax=None):
        self.var = var
        self.keys = keys
        self.nBranches = nBranches
        self.lvs = [{"p4": supy.utils.LorentzV()} for i in range(self.nBranches)]
        assert self.var

        self.ptMin = ptMin
        self.absEtaMax = absEtaMax
        self.moreName = "%g < pT; |eta| < %g" % (self.ptMin, self.absEtaMax)

        self.sortBy = sortBy
        self.reverse = reverse

        self.__name = self.var + "s"
        if self.sortBy:
            self.__name += "_%sSorted" % self.sortBy

    def update(self, _):
        self.value = []
        for iJet in range(self.nBranches):
            coords = [self.source["%s%d%s" % (self.var, 1+iJet, s)] for s in ["Pt", "Eta", "Phi", "Mass"]]
            self.lvs[iJet]["p4"].SetCoordinates(*tuple(coords))
            if self.ptMin and (coords[0] < self.ptMin):
                continue
            if self.absEtaMax and (self.absEtaMax < abs(coords[1])):
                continue

            for key in self.keys:
                self.lvs[iJet][key] = self.source["%s%d%s" % (self.var, 1+iJet, key)]
            self.value.append(self.lvs[iJet])

        if self.sortBy:
            self.value = sorted(self.value, key=lambda x:x[self.sortBy], reverse=self.reverse)


class maximumJetPt(supy.wrappedChain.calculable):
    def __init__(self, jets=""):
        self.jets = jets

    def update(self, _):
        pts = [jet["p4"].pt() for jet in self.source[self.jets]]
        self.value = max(pts) if pts else None


class indexedVar(supy.wrappedChain.calculable):
    @property
    def name(self):
        return "%s_%s%d" % (self.var, self.key, self.index)

    def __init__(self, var="", key="", index=None):
        self.var = var
        self.key = key
        self.index = index
        assert self.index is not None

    def update(self, _):
        self.value = self.source[self.var][self.index][self.key]


class diJetP4(supy.wrappedChain.calculable):
    def __init__(self, var=""):
        self.var = var

    def update(self, _):
        self.value = self.source[self.var][0]["p4"]+self.source[self.var][1]["p4"]


class diTauP4(supy.wrappedChain.calculable):
    def __init__(self, index=None):
        self.index = index
        self.lvs = [supy.utils.LorentzV(), supy.utils.LorentzV()]

    def update(self, _):
        for i in range(2):
            coords = [self.source["%s%d" % (s, 1+i)].at(self.index) for s in ["pt", "eta", "phi", "m"]]
            self.lvs[i].SetCoordinates(*tuple(coords))
        self.value = self.lvs[0] + self.lvs[1]


class svP4(supy.wrappedChain.calculable):
    def __init__(self, index=None):
        self.index = index
        self.value = supy.utils.LorentzV()

    def update(self, _):
        self.value.SetCoordinates(0.0, 0.0, 0.0, self.source["svMass"].at(self.index))


class sumP4(supy.wrappedChain.calculable):
    @property
    def name(self):
        return self._name

    def __init__(self, vars=[]):
        self.vars = vars
        self._name = "_".join(["sumP4"] + self.vars)
        self.value = supy.utils.LorentzV()

    def update(self, _):
        self.value.SetCoordinates(0.0, 0.0, 0.0, 0.0)
        for var in self.vars:
            self.value += self.source[var]


class one(supy.wrappedChain.calculable):
    @property
    def name(self):
        return "%s_%d" % (self.var, self.index)

    def __init__(self, var="", index=None):
        self.var = var
        self.index = index

    def update(self, _):
        self.value = self.source[self.var].at(self.index)


class maximumPt(supy.wrappedChain.calculable):
    def __init__(self, index=None):
        self.index = index

    def update(self, _):
        pt1 = self.source["pt1"].at(self.index)
        pt2 = self.source["pt2"].at(self.index)
        self.value = max([pt1, pt2])


class minimumPt(supy.wrappedChain.calculable):
    def __init__(self, index=None):
        self.index = index

    def update(self, _):
        pt1 = self.source["pt1"].at(self.index)
        pt2 = self.source["pt2"].at(self.index)
        self.value = min([pt1, pt2])


class differencePt(supy.wrappedChain.calculable):
    def __init__(self, index=None):
        self.index = index

    def update(self, _):
        pt1 = self.source["pt1"].at(self.index)
        pt2 = self.source["pt2"].at(self.index)
        self.value = pt1 - pt2


class sameSign(supy.wrappedChain.calculable):
    def __init__(self, index=None):
        self.index = index

    def update(self, _):
        c1 = self.source["charge1"].at(self.index)
        c2 = self.source["charge2"].at(self.index)
        self.value = c1 == c2


class diTauHadTriggerWeight(supy.wrappedChain.calculable):
    """
    See AN 13-189, appendix A
    -------------------------
            tag: HLT_IsoMu24_eta2p1
          probe: HLT_IsoMu18_eta2p1_MediumIsoPFTau25_Trk1_eta2p1
                 also req. HLT: 25 --> 35
                 also req.  L1: tau-jet w/ 44uc < pT; abs(eta) < 2.1
                                         (~30c tau pT)
                                OR
                                cen-jet w/ 64uc < pT; abs(eta) < 3.0
                                         (~44c tau pT)
     applied to: HLT_DoubleMediumIsoPFTau35_Trk{1,5}_eta2p1_v*
                 (L1: two tau-jet as above OR two cen/tau-jet as above)
    """

    def __init__(self, fitStart=25, hltThreshold=35, data=True, tauPairIndex=None):
        self.tauPairIndex = tauPairIndex
        self.fitStart = fitStart
        assert hltThreshold == 35
        #    fitStart: (epsil,   x0, sigma),
        le14_da = {20: (0.898, 44.3, 1.02),
                   25: (0.866, 43.1, 0.86),
                   30: (0.839, 42.3, 0.73),
                   35: (0.846, 42.4, 0.78),
                   }
        le14_mc = {20: (0.837, 43.6, 1.09),
                   25: (0.832, 40.4, 0.80),
                   30: (0.829, 40.4, 0.74),
                   35: (0.833, 40.1, 0.86),
                   }
        ge16_da = {20: (0.81, 43.6, 1.09),
                   25: (0.76, 41.8, 0.86),
                   30: (0.74, 41.2, 0.75),
                   35: (0.74, 41.2, 0.79),
                   }
        ge16_mc = {20: (0.70, 39.7, 0.95),
                   25: (0.69, 38.6, 0.74),
                   30: (0.69, 38.7, 0.61),
                   35: (0.69, 38.8, 0.61),
                   }

        self.le14 = le14_da if data else le14_mc
        self.ge16 = ge16_da if data else ge16_mc
        self.moreName = ", ".join(["fitStart=%d" % self.fitStart,
                                   "hltThreshold=%d" % hltThreshold,
                                   "data" if data else "MC",
                                   "index=%d" % self.tauPairIndex,
                                   ])
        self.moreName = "(%s)" % self.moreName

    def params(self, eta=None):
        if abs(eta) < 1.4:
            d = self.le14
        elif 1.6 < abs(eta):
            d = self.ge16
        else:
            #assert False, abs(eta)
            d = self.ge16
        return d[self.fitStart]

    def Phi(self, e=None, x=None, x0=None, sigma=None):
        #y = r.TMath.Erf((x-x0)/sigma/math.sqrt(2.0))  # AN Eq. 5
        y = r.TMath.Erf((x-x0)/2.0/sigma/math.sqrt(x))  # https://github.com/rmanzoni/HTT/blob/master/CMGTools/H2TauTau/interface/TriggerEfficiency.h
        return (1+y)*e/2.0

    def effOneLeg(self, eta=None, pt=None):
        e, x0, sigma = self.params(eta)
        return self.Phi(e=e, x=pt, x0=x0, sigma=sigma)

    def update(self, _):
        self.value = 1.0
        for i in range(1, 3):
            self.value *= self.effOneLeg(eta=self.source["eta%d" % i].at(self.tauPairIndex),
                                         pt=self.source["pt%d" % i].at(self.tauPairIndex))
