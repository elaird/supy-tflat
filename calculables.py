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
