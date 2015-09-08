import os
import supy
import ROOT as r
import taufit


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
        self.value.SetCoordinates(s["t1GenPt"], s["t1GenEta"], s["t1GenPhi"], s["t1GenMass"])


class gt2(supy.wrappedChain.calculable):
    """gen tau 2"""
    def __init__(self):
        self.value = supy.utils.LorentzV()
    def update(self, _):
        s = self.source
        self.value.SetCoordinates(s["t2GenPt"], s["t2GenEta"], s["t2GenPhi"], s["t2GenMass"])


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
    """gen nu 1"""
    def __init__(self):
        self.value = supy.utils.LorentzV()
    def update(self, _):
        s = self.source
        self.value.SetCoordinates(s["t1GenVisPt"], s["t1GenVisEta"], s["t1GenVisPhi"], s["t1GenVisMass"])


class gv2(supy.wrappedChain.calculable):
    """gen nu 2"""
    def __init__(self):
        self.value = supy.utils.LorentzV()
    def update(self, _):
        s = self.source
        self.value.SetCoordinates(s["t2GenVisPt"], s["t2GenVisEta"], s["t2GenVisPhi"], s["t2GenVisMass"])


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
        self.value.SetCoordinates(s["t1Pt"], s["t1Eta"], s["t1Phi"], s["t1Mass"])


class rv2(supy.wrappedChain.calculable):
    """reco vis 2"""
    def __init__(self):
        self.value = supy.utils.LorentzV()
    def update(self, _):
        s = self.source
        self.value.SetCoordinates(s["t2Pt"], s["t2Eta"], s["t2Phi"], s["t2Mass"])


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
        self.value = taufit.tmatrix(met_cov, sym=self.sym)


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


class measured_tau_leptons(supy.wrappedChain.calculable):
    def __init__(self):
        r.gSystem.Load("libTauAnalysisSVfitStandalone.so")
        r.SVfitStandaloneAlgorithm  # hack

    def update(self, _):
        s = self.source
        met = self.fixes[0]
        ml = r.svFitStandalone.MeasuredTauLepton

        m_elec = 0.51100e-3
        m_muon = 0.10566
        m_pion = 0.13957

        self.value = r.std.vector('svFitStandalone::MeasuredTauLepton')()
        for pdgId, pt, eta, phi, mass, dm in [(abs(s["t1PdgId"]), s["rv1"].pt(), s["rv1"].eta(), s["rv1"].phi(), s["rv1"].mass(), int(s["t1DecayMode"])),
                                              (abs(s["t2PdgId"]), s["rv2"].pt(), s["rv2"].eta(), s["rv2"].phi(), s["rv2"].mass(), int(s["t2DecayMode"])),
                                              ]:
            if pdgId == 11:
                lep = ml(r.svFitStandalone.kTauToElecDecay, pt, eta, phi, m_elec)
            elif pdgId == 13:
                lep = ml(r.svFitStandalone.kTauToMuDecay, pt, eta, phi, m_muon)
            elif pdgId == 15:
                lep = ml(r.svFitStandalone.kTauToHadDecay, pt, eta, phi, mass if dm else m_pion, dm)
            else:
                continue  # requires filter later
            self.value.push_back(lep)


class has_hadronic_taus(supy.wrappedChain.calculable):
    def update(self, _):
        s = self.source
        one = abs(s["t1PdgId"]) == 15 and s["t1DecayMode"] != 5 and s["t1DecayMode"] != 6
        two = abs(s["t2PdgId"]) == 15 and s["t2DecayMode"] != 5 and s["t2DecayMode"] != 6
        self.value = one or two


class svfitter(supy.wrappedChain.calculable):
    def __init__(self, met="", verbosity=2):
        self.verbosity = verbosity
        self.fixes = (met, "")

    def update(self, _):
        s = self.source
        met = self.fixes[0]
        # note that relevant setup is done in measured_tau_leptons.__init__
        self.value = r.SVfitStandaloneAlgorithm(s["measured_tau_leptons"], s[met].px(), s[met].py(), s["%scov" % met], self.verbosity)


class svs(supy.wrappedChain.calculable):
    def __init__(self, met=""):
        self.fixes = (met, "")
        self.resFileName = "%s/src/TauAnalysis/SVfitStandalone/data/svFitVisMassAndPtResolutionPDF.root" % os.environ["CMSSW_BASE"]

    def update(self, _):
        s = self.source
        self.value = {"mc_dm_leaf": (s["t1_t2_SVfit"].M(), None, None)}

        sv = s["%ssvfitter" % self.fixes[0]]
        sv.addLogM(False)

        sv.integrateVEGAS()  # NOTE! shiftVisPt crashes vegas
        self.value["vg"] = (sv.mass(), sv.mass() - sv.massUncert(), sv.mass() + sv.massUncert())
        # vglm = sv.massLmax()

        # sv.shiftVisPt(s["has_hadronic_taus"], r.TFile(self.resFileName))
        sv.integrateMarkovChain()
        self.value["mc"] = (sv.mass(), sv.mass() - sv.massUncert(), sv.mass() + sv.massUncert())
        # mclm = sv.massLmax()

        sv.fit()
        self.value["pl"] = (sv.mass(), sv.mass() - sv.massUncert(), sv.mass() + sv.massUncert())

