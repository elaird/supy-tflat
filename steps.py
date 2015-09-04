import supy


class visHistos(supy.analysisStep):
    def uponAcceptance(self, s):
        for i in [1, 2]:
            m = s["t%dDecayMode" % i]
            x = s["rv%d_gv%d" % (i, i)]
            self.book.fill(x, "taus_ptVisVisRatio_%d" % m, 100, 0.0, 3.0, title=";reco. vis. p_{T} / gen. vis. p_{T} (decay mode %d);Events / bin" % m)
