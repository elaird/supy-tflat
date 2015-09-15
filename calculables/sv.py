import os
import supy
import ROOT as r


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

        if "mPt" in s:
            self.value.push_back(ml(r.svFitStandalone.kTauToMuDecay, s["mPt"], s["mEta"], s["mPhi"], m_muon))
        if "ePt" in s:
            self.value.push_back(ml(r.svFitStandalone.kTauToElecDecay, s["ePt"], s["eEta"], s["ePhi"], m_elec))

        # hadronic taus
        for p in ["t1", "t2", "t"]:
            if ("%sPt" % p) not in s:
                continue
            dm = int(s["%sDecayMode" % p])
            m = s["%sMass" % p] if dm else m_pion
            self.value.push_back(ml(r.svFitStandalone.kTauToHadDecay, s["%sPt" % p], s["%sEta" % p], s["%sPhi" % p], m, dm))


class has_hadronic_taus(supy.wrappedChain.calculable):
    def update(self, _):
        bad = [None, 5, 6]  # FIXME (floats)
        s = self.source
        self.value = (s.get("t1DecayMode") not in bad) and (s.get("t2DecayMode") not in bad)


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
    def __init__(self, met="", vg=False, mc=False, pl=False):
        self.fixes = (met, "")
        self.resFileName = "%s/src/TauAnalysis/SVfitStandalone/data/svFitVisMassAndPtResolutionPDF.root" % os.environ["CMSSW_BASE"]
        self.vg = vg
        self.mc = mc
        self.pl = pl

    def store(self, key, sv):
        self.value[key] = {}
        for prefix in ["mass", "pt", "eta", "phi"]:
            for suffix in ["", "Uncert", "Lmax"]:
                f = prefix + suffix
                self.value[key][f] = getattr(sv, f)()

    def update(self, _):
        s = self.source
        self.value = {}

        sv = s["%ssvfitter" % self.fixes[0]]
        sv.addLogM(False)

        if self.vg:
            sv.integrateVEGAS()  # NOTE! shiftVisPt crashes vegas
            self.store("vg", sv)

        if self.mc:
            # sv.shiftVisPt(s["has_hadronic_taus"], r.TFile(self.resFileName))
            sv.integrateMarkovChain()
            self.store("mc", sv)

        if self.pl:
            sv.fit()
            self.store("pl", sv)


class sv_access(supy.wrappedChain.calculable):
    @property
    def name(self):
        return "%s_sv%s_%s" % (self.met, self.sv, self.key)

    def __init__(self, key="", met="", sv=""):
        self.key = key
        self.met = met
        self.sv = sv

    def update(self, _):
        d = self.source["%ssvs" % self.met][self.sv]
        self.value = d[self.key]
