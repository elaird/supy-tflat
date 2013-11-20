import supy

class LastBinOverFirstBin(supy.wrappedChain.calculable):
    def __init__(self, dir="", histoName=""):
        self.dir = dir
        self.histoName = histoName
        self.value = None

    def update(self, _):
        if self.value is not None:
            return

        nTrees = self.source["chain"].GetNtrees()
        assert nTrees == 1, "Chain has %d trees.  Consider using hadd." % nTrees
        f = self.source["chain"].GetFile()
        assert f
        hPath = "%s/%s" % (self.dir, self.histoName)
        h = f.Get(hPath)
        assert h, "Histogram %s not found." % hPath
        num = h.GetBinContent(h.GetNbinsX())
        den = h.GetBinContent(1)
        assert den
        self.value = num / den
