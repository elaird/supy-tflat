import supy


class tauLegsPtEta(supy.analysisStep):
    def __init__(self, ptMin=None, absEtaMax=None, index=None):
        assert index is not None
        self.index = index
        self.ptMin = ptMin
        self.absEtaMax = absEtaMax
        self.moreName = "%g < pT; |eta| < %g" % (self.ptMin, self.absEtaMax)
    
    def select(self, eventVars):
        for i in [1, 2]:
            if (self.ptMin is not None) and (eventVars["pt%d" % i].at(self.index) < self.ptMin):
                return False
            if (self.absEtaMax is not None) and (self.absEtaMax < abs(eventVars["eta%d" % i].at(self.index))):
                return False
        return True
