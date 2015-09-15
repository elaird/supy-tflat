import supy
import ROOT as r


def tmatrix(met_cov, sym=False):
    assert len(met_cov) == 2, met_cov
    assert met_cov[0][1] == met_cov[1][0]
    if sym:
        out = r.TMatrixDSym(2)
    else:
        out = r.TMatrixD(2, 2)
    for i in range(2):
        assert len(met_cov[i]) == 2
        for j in range(2):
            # out[i][j] = met_cov[i][j]  # ROOT 5
            out[i, j] = met_cov[i][j]
    return out


class histo_bin1(supy.wrappedChain.calculable):
    @property
    def name(self):
        return self.hName

    def __init__(self, hName):
        self.hName = hName
        self.value = None

    def update(self, _):
        if self.value is None:
            h = self.histo(self.source["chain"].GetListOfFiles())
            self.value = h.GetBinContent(1)

    def histo(self, elements):
        # http://root.cern.ch/root/html/TChain.html#TChain:AddFile
        out = None
        for iElement in range(elements.GetEntries()):
            element = elements.At(iElement)
            f = r.TFile(element.GetTitle())
            assert f
            h = f.Get(self.hName)
            assert h, "Histogram %s not found." % self.hName
            if out:
                out.Add(h)
            else:
                out = h.Clone()
                out.SetDirectory(0)
            f.Close()
        return out


class nus(supy.wrappedChain.calculable):
    """global (including neutrinos not from taus)"""
    def __init__(self):
        self.value = supy.utils.LorentzV()
    def update(self, _):
        s = self.source
        self.value.SetCoordinates(s["genNuPt"], s["genNuEta"], s["genNuPhi"], s["genNuMass"])


class nus_pt(supy.wrappedChain.calculable):
    def update(self, _):
        self.value = self.source["nus"].pt()


class gt1(supy.wrappedChain.calculable):
    """gen tau 1"""
    def __init__(self):
        self.value = supy.utils.LorentzV()
    def update(self, _):
        s = self.source

        for p in ["mGenTau", "eGenTau", "t1Gen"]:
            if "%sPt" % p in s:
                break
        self.value.SetCoordinates(s["%sPt" % p], s["%sEta" % p], s["%sPhi" % p], s["%sMass" % p])


class gt2(supy.wrappedChain.calculable):
    """gen tau 2"""
    def __init__(self):
        self.value = supy.utils.LorentzV()
    def update(self, _):
        s = self.source

        for p in ["t2Gen", "tGen", "eGenTau"]:
            if "%sPt" % p in s:
                break

        self.value.SetCoordinates(s["%sPt" % p], s["%sEta" % p], s["%sPhi" % p], s["%sMass" % p])


class gn1(supy.wrappedChain.calculable):
    """gen nu 1"""
    def __init__(self):
        self.value = supy.utils.LorentzV()
    def update(self, _):
        s = self.source
        self.value.SetCoordinates(s["t1GenNuPt"], s["t1GenNuEta"], s["t1GenNuPhi"], s["t1GenNuMass"])


class gn2(supy.wrappedChain.calculable):
    """gen nu 2"""
    def __init__(self):
        self.value = supy.utils.LorentzV()
    def update(self, _):
        s = self.source
        self.value.SetCoordinates(s["t2GenNuPt"], s["t2GenNuEta"], s["t2GenNuPhi"], s["t2GenNuMass"])


class gtMass(supy.wrappedChain.calculable):
    """gen mass"""
    def update(self, _):
        s = self.source
        self.value = (s["gt1"] + s["gt2"]).mass()


class gv1(supy.wrappedChain.calculable):
    """gen vis 1"""
    def __init__(self):
        self.value = supy.utils.LorentzV()
    def update(self, _):
        s = self.source

        for p in ["mGen", "eGen", "t1GenVis"]:
            if "%sPt" % p in s:
                break
        self.value.SetCoordinates(s["%sPt" % p], s["%sEta" % p], s["%sPhi" % p], s["%sMass" % p])


class gv2(supy.wrappedChain.calculable):
    """gen vis 2"""
    def __init__(self):
        self.value = supy.utils.LorentzV()
    def update(self, _):
        s = self.source

        for p in ["t2GenVis", "tGenVis", "eGen"]:
            if "%sPt" % p in s:
                break

        self.value.SetCoordinates(s["%sPt" % p], s["%sEta" % p], s["%sPhi" % p], s["%sMass" % p])


class gvMass(supy.wrappedChain.calculable):
    """gen mass"""
    def update(self, _):
        s = self.source
        self.value = (s["gv1"] + s["gv2"]).mass()


class rv1(supy.wrappedChain.calculable):
    """reco vis 1"""
    def __init__(self):
        self.value = supy.utils.LorentzV()
    def update(self, _):
        s = self.source

        for p in ["m", "e", "t1"]:
            if "%sPt" % p in s:
                break
        self.value.SetCoordinates(s["%sPt" % p], s["%sEta" % p], s["%sPhi" % p], s["%sMass" % p])


class rv2(supy.wrappedChain.calculable):
    """reco vis 2"""
    def __init__(self):
        self.value = supy.utils.LorentzV()
    def update(self, _):
        s = self.source

        for p in ["t2", "t", "e"]:
            if "%sPt" % p in s:
                break

        self.value.SetCoordinates(s["%sPt" % p], s["%sEta" % p], s["%sPhi" % p], s["%sMass" % p])


class rvMass(supy.wrappedChain.calculable):
    """reco vis mass"""
    def update(self, _):
        s = self.source
        self.value = (s["rv1"] + s["rv2"]).mass()


class DR1(supy.wrappedChain.calculable):
    def update(self, _):
        s = self.source
        self.value = r.Math.VectorUtil.DeltaR(s["gt1"], s["rv1"])


class DR2(supy.wrappedChain.calculable):
    def update(self, _):
        s = self.source
        self.value = r.Math.VectorUtil.DeltaR(s["gt2"], s["rv2"])

class CDT1(supy.wrappedChain.calculable):
    def update(self, _):
        s = self.source
        self.value = r.Math.VectorUtil.CosTheta(s["gt1"], s["rv1"])

class CDT2(supy.wrappedChain.calculable):
    def update(self, _):
        s = self.source
        self.value = r.Math.VectorUtil.CosTheta(s["gt2"], s["rv2"])

class gDPhi12(supy.wrappedChain.calculable):
    def update(self, _):
        s = self.source
        self.value = r.Math.VectorUtil.DeltaPhi(s["gt1"], s["gt2"])

class rDPhi12(supy.wrappedChain.calculable):
    def update(self, _):
        s = self.source
        self.value = r.Math.VectorUtil.DeltaPhi(s["rv1"], s["rv2"])

class rv1_gt1(supy.wrappedChain.calculable):
    def update(self, _):
        s = self.source
        self.value = s["rv1"].pt() / s["gt1"].pt()

class rv2_gt2(supy.wrappedChain.calculable):
    def update(self, _):
        s = self.source
        self.value = s["rv2"].pt() / s["gt2"].pt()

class rv1_gv1(supy.wrappedChain.calculable):
    def update(self, _):
        s = self.source
        self.value = s["rv1"].pt() / s["gv1"].pt()

class rv2_gv2(supy.wrappedChain.calculable):
    def update(self, _):
        s = self.source
        self.value = s["rv2"].pt() / s["gv2"].pt()

class gv1_gt1(supy.wrappedChain.calculable):
    def update(self, _):
        s = self.source
        self.value = s["gv1"].pt() / s["gt1"].pt()

class gv2_gt2(supy.wrappedChain.calculable):
    def update(self, _):
        s = self.source
        self.value = s["gv2"].pt() / s["gt2"].pt()

class pt_two_nu(supy.wrappedChain.calculable):
    def __init__(self):
        self.lv = supy.utils.LorentzV()

    def update(self, _):
        s = self.source
        self.lv.SetCoordinates(0.0, 0.0, 0.0, 0.0)
        self.lv += s["gt1"]
        self.lv -= s["gv1"]
        self.lv += s["gt2"]
        self.lv -= s["gv2"]
        self.value = self.lv.pt()

class genmet(supy.wrappedChain.calculable):
    def __init__(self):
        self.value = supy.utils.LorentzV()

    def update(self, _):
        s = self.source
        self.value.SetCoordinates(s["genMetEt"], 0.0, s["genMetPhi"], 0.0)


class pfmet(supy.wrappedChain.calculable):
    def __init__(self):
        self.value = supy.utils.LorentzV()

    def update(self, _):
        s = self.source
        self.value.SetCoordinates(s["pfMetEt"], 0.0, s["pfMetPhi"], 0.0)


class cov(supy.wrappedChain.calculable):
    def __init__(self, prefix="", sym=None):
        assert sym is not None
        self.fixes = (prefix, "sym" if sym else "")
        self.sym = sym

    def update(self, _):
        s = self.source
        met = self.fixes[0]
        met_cov = [(s["%sCovariance_00" % met], s["%sCovariance_01" % met]),
                   (s["%sCovariance_10" % met], s["%sCovariance_11" % met]),
                   ]
        self.value = tmatrix(met_cov, sym=self.sym)


class gaus(supy.wrappedChain.calculable):
    def __init__(self, fixes=(["genmet", "nus"][0], "pfmet")):
        self.fixes = fixes

    def update(self, _):
        s = self.source
        gen, met = self.fixes
        mux = r.RooRealVar("%sx" % gen, "%sx" % gen, s[gen].px())
        muy = r.RooRealVar("%sy" % gen, "%sy" % gen, s[gen].py())

        metx = r.RooRealVar("%sx" % met, "%sx" % met, s[met].px())
        mety = r.RooRealVar("%sy" % met, "%sy" % met, s[met].py())
        gaus = r.RooMultiVarGaussian(self.name, self.name,
                                     r.RooArgList(metx, mety),
                                     r.RooArgList(mux, muy),
                                     s["%scovsym" % met])
        self.value = r.TMath.Sqrt(-2.0 * r.TMath.Log(gaus.getVal()))


class rho_xy(supy.wrappedChain.calculable):
    def __init__(self, prefix=""):
        self.fixes = (prefix, "")

    def update(self, _):
        s = self.source
        f = self.fixes[0]
        self.value = s["%sCovariance_01" % f] / r.TMath.Sqrt(s["%sCovariance_00" % f] * s["%sCovariance_11" % f])


class nSelected(supy.wrappedChain.calculable):
    def __init__(self):
        self.value = 0

    def update(self, _):
        self.value += 1
        print
        print "nSelected =", self.value


