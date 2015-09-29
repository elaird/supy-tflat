import supy


class visHistos(supy.analysisStep):
    def uponAcceptance(self, s):
        for i in [1, 2]:
            dm = "t%dDecayMode" % i
            m = s[dm] if (dm in s) else -1
            x = s["rv%d_gv%d" % (i, i)]
            self.book.fill(x, "taus_ptVisVisRatio_%d" % m, 100, 0.0, 3.0, title=";reco. vis. p_{T} / gen. vis. p_{T} (decay mode %d);Events / bin" % m)


class svHistos(supy.analysisStep):
    def __init__(self, met="", sv=""):
        self.met = met
        self.sv = sv

    def uponAcceptance(self, s):
        mMin = 0.0
        mMax = 400.0

        prefix = "%s_sv%s" % (self.met, self.sv)
        best = s["%s_mass" % prefix]
        uncSym = s["%s_massUncert" % prefix]
        uncSymRel = uncSym / best
        gen = s["gtMass"]
        pull = (best - gen) / uncSym

        self.book.fill(best, "%s_best" % prefix, 100, mMin, mMax, title=";%s fit mass (GeV);Events / bin" % prefix)
        self.book.fill((gen, best), "%s_best_vs_gen" % prefix, (100, 100), (mMin, mMin), (mMax, mMax), title="gen mass (GeV);%s fit mass (GeV);Events / bin" % prefix)
        self.book.fill(uncSymRel, "%s_reluncsym" % prefix, 100, 0.0, 2.0, title=";%s rel. unc. sym.;Events / bin" % prefix)
        self.book.fill(pull, "%s_pull" % prefix, 40, -5.0, 5.0, title=";%s:  (m - gen) / uncSym;Events / bin" % prefix)

        profBins = [0] + range(5, 125, 10) + range(125, 250, 25) + range(250, 450, 50)
        self.book.fillVarBin((gen, best), "%s_best_vs_gen_prof" % prefix, profBins, title=";gen mass (GeV);%s fit mass (GeV)" % prefix)
        self.book.fillVarBin((gen, best), "%s_best_vs_gen_profs" % prefix, profBins, title=";gen mass (GeV);%s fit mass (GeV)  (spread)" % prefix, options="s")

        self.book.fillVarBin((gen, pull), "%s_pull_vs_gen_prof" % prefix, profBins, title=";gen mass (GeV);%s:  (m - gen) / uncSym" % prefix)
        self.book.fillVarBin((gen, pull), "%s_pull_vs_gen_profs" % prefix, profBins, title=";gen mass (GeV);%s:  (m - gen) / uncSym  (spread)" % prefix, options="s")
