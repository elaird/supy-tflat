import cPickle
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

    def cacheFileName(self):
        fileName = self.inputFileName[:-len(self.outputSuffix())]
        fileName = "_".join(fileName.split("_")[:-2]) # remove nSlices_iSlice from name
        return fileName + self.outputSuffix()

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

        cPickle.dump(d, open(self.outputFileName, "w"))
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
    def __init__(self, vars=[]):
        self.vars = vars
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
