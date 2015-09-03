import supy


class osIsoMin(supy.analysisStep):
    def __init__(self, index=None, isoMin=2.0):
        assert type(index) is int, index
        for item in ["index", "isoMin"]:
            setattr(self, item, eval(item))
        self.moreName = "%g GeV < max(iso1, iso2) when pair %d is OS" % (self.isoMin, self.index)

    def select(self, eventVars):
        isos = [eventVars["iso1"].at(self.index),
                eventVars["iso2"].at(self.index)]
        os = eventVars["charge1"].at(self.index) != eventVars["charge2"].at(self.index)
        if os:
            return self.isoMin < max(isos)
        else:
            return True


class blind(osIsoMin):
    pass


class tauLegsPtEta(supy.analysisStep):
    def __init__(self,
                 ptMin=None,
                 absEtaMax=None,
                 isoMin=None,
                 isoMax=None,
                 index=None,
                 ):
        assert type(index) is int, index
        for item in ["index", "ptMin", "absEtaMax", "isoMin", "isoMax"]:
            setattr(self, item,  eval(item))
        self._setName()

    def _setName(self):
        self.moreName = ""
        if self.ptMin is not None:
            self.moreName += "%g < pT" % self.ptMin
        if self.absEtaMax is not None:
            self.moreName += "; |eta| < %g" % self.absEtaMax

        iso = "iso"
        if self.isoMin is not None:
            iso = "%g < %s" (self.isoMin, iso)
        if self.isoMax is not None:
            iso = "%s < %g" % (iso, self.isoMax)
        if set([self.isoMin, self.isoMax]) != set([None]):
            self.moreName += "; "+iso

    def select(self, eventVars):
        for i in [1, 2]:
            if (self.ptMin is not None) and (eventVars["pt%d" % i].at(self.index) < self.ptMin):
                return False
            if (self.absEtaMax is not None) and (self.absEtaMax < abs(eventVars["eta%d" % i].at(self.index))):
                return False
            if (self.isoMin is not None) and (eventVars["iso%d" % i].at(self.index) < self.isoMin):
                return False
            if (self.isoMax is not None) and (self.isoMax < eventVars["iso%d" % i].at(self.index)):
                return False
        return True
