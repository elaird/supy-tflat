import supy
import ROOT as r

class LastBinOverFirstBin(supy.wrappedChain.calculable):
    @property
    def name(self):
        return "LastBinOverBin%d" % self.firstBin

    def __init__(self, dir="", histoName="", firstBin=1):
        self.hPath = "%s/%s" % (dir, histoName)
        self.firstBin = firstBin
        self.value = None

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

    def update(self, _):
        if self.value is not None:
            return

        h = self.histo(self.source["chain"].GetListOfFiles())
        num = h.GetBinContent(h.GetNbinsX())
        den = h.GetBinContent(self.firstBin)
        assert den
        self.value = num / den


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


class one(supy.wrappedChain.calculable):
    @property
    def name(self):
        return "%s%d" % (self.var, self.index)

    def __init__(self, var="", index=None):
        self.var = var
        self.index = index

    def update(self, _):
        self.value = self.source[self.var].at(self.index)
