import supy


class visHistos(supy.analysisStep):
    def uponAcceptance(self, s):
        for i in [1, 2]:
            dm = "t%dDecayMode" % i
            m = s[dm] if (dm in s) else -1
            x = s["rv%d_gv%d" % (i, i)]
            self.book.fill(x, "taus_ptVisVisRatio_%d" % m, 100, 0.0, 3.0, title=";reco. vis. p_{T} / gen. vis. p_{T} (decay mode %d);Events / bin" % m)


class svHistos(supy.analysisStep):
    def __init__(self, met="", svs=[]):
        self.met = met
        self.svs = svs

    def uponAcceptance(self, s):
        mMin = 0.0
        mMax = 400.0

        for sv in self.svs:
            prefix = "%s_sv%s" % (self.met, sv)
            best = s["%s_mass" % prefix]
            uncSym = s["%s_massUncert" % prefix]
            uncSymRel = uncSym / best
            gen = s["gtMass"]
            pull = (best - gen) / uncSym

            self.book.fill(best, "sv_best_%s" % sv, 100, mMin, mMax, title=";%s sv fit mass (GeV);Events / bin" % sv)
            self.book.fill((gen, best), "sv_best_%s_vs_gen" % sv, (100, 100), (mMin, mMin), (mMax, mMax), title="gen mass (GeV);%s sv fit mass (GeV);Events / bin" % sv)
            self.book.fill(uncSymRel, "sv_reluncsym_%s" % sv, 100, 0.0, 2.0, title=";%s sv rel. unc. sym.;Events / bin" % sv)
            self.book.fill(pull, "sv_pull_%s" % sv, 40, -5.0, 5.0, title=";%s sv:  (m - gen) / uncSym;Events / bin" % sv)

            profBins = [0] + range(5, 125, 10) + range(125, 250, 25) + range(250, 450, 50)
            self.book.fillVarBin((gen, best), "sv_best_%s_vs_gen_prof" % sv, profBins, title=";gen mass (GeV);%s sv fit mass (GeV)" % sv)
