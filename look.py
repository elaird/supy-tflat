import supy
import displayer
import steps
import calculables
import ROOT as r
import os


ss = supy.steps
sshv = ss.histos.value

class look(supy.analysis):
    def parameters(self):
        return {"svs": ["mc", "vg", "pl"],
                "tf": True,
                }

    def listOfSteps(self, pars):
        mMax = 500.0
        return [ss.printer.progressPrinter(),
                sshv("t1ByCombinedIsolationDeltaBetaCorrRaw3Hits", 100, 0.0, 10.0, xtitle="isolation (GeV)"),
                sshv("t2ByCombinedIsolationDeltaBetaCorrRaw3Hits", 100, 0.0, 10.0, xtitle="isolation (GeV)"),
                ss.filters.value("t1GenMass", min=0.0),
                ss.filters.value("t2GenMass", min=0.0),
                ss.filters.value("DR1", max=0.4),
                ss.filters.value("DR2", max=0.4),
                sshv("CDT1", 150, -1.0, 2.0, xtitle="cos(#Delta#theta_{1})"),
                sshv("CDT2", 150, -1.0, 2.0, xtitle="cos(#Delta#theta_{2})"),
                sshv("DR1", 100, 0.0, 10.0, xtitle="#DeltaR_{1} (gen,reco)"),
                sshv("DR2", 100, 0.0, 10.0, xtitle="#DeltaR_{2} (gen,reco)"),
                sshv("gDPhi12", 20, -r.TMath.Pi(), r.TMath.Pi(), xtitle="gen. taus' #Delta#phi"),
                sshv("rDPhi12", 20, -r.TMath.Pi(), r.TMath.Pi(), xtitle="reco. taus' #Delta#phi"),
                sshv("gv1_gt1", 100, 0.0, 3.0, xtitle="gen. vis. p_{T} / gen. tau p_{T}"),
                sshv("gv2_gt2", 100, 0.0, 3.0, xtitle="gen. vis. p_{T} / gen. tau p_{T}"),
                steps.visHistos(),
                ss.histos.pt("nus", 100, 0.0, 100.0, xtitle="(sum nu) pT (GeV)"),

                sshv("pfmetrho_xy", 100, -1.0, 1.0, xtitle="correlation of METx and METy"),
                sshv("genmetgauspfmet", 100, 0.0, 5.0, xtitle="Gaus(PF MET, genmet, cov.) (#sigma)"),
                sshv("nusgauspfmet", 100, 0.0, 5.0, xtitle="Gaus(PF MET, nus, cov.) (#sigma)"),

                sshv(("gvMass", "rvMass"), (100, 100), (0.0, 0.0), (mMax, mMax), xtitle="gen visible mass (GeV);reco visible mass (GeV)"),
                sshv(("gtMass", "rvMass"), (100, 100), (0.0, 0.0), (mMax, mMax), xtitle="gen mass (GeV);reco visible mass (GeV)"),

                sshv(("genMetEt", "pt_two_nu"), (100, 100), (0.0, 0.0), (mMax, mMax), xtitle="gen met (GeV);pt two nu (GeV)"),
                sshv(("nus_pt", "pt_two_nu"), (100, 100), (0.0, 0.0), (mMax, mMax), xtitle="(sum nu) pT (GeV);pt two nu (GeV)"),
                sshv(("genMetEt", "nus_pt"), (100, 100), (0.0, 0.0), (mMax, mMax), xtitle="gen met (GeV);(sum nu) pT (GeV)"),

                sshv(("genMetEt", "pfMetEt"), (100, 100), (0.0, 0.0), (mMax, mMax), xtitle="gen met (GeV);pf met (GeV)"),
                sshv(("nus_pt", "pfMetEt"), (100, 100), (0.0, 0.0), (mMax, mMax), xtitle="(sum nu) pT (GeV);pf met (GeV)"),

                # ss.other.touchstuff(["nSelected"]),
                ss.filters.multiplicity("measured_tau_leptons", min=2, max=2),
                ss.other.touchstuff(["pfmetsvfitter"]),
                # ss.other.touchstuff(["pfmetsvs"]),

                # ss.filters.label("tauPlots"),
                # #ss.other.skimmer(mainChain=False, extraVars=pars["extraVars"]),
                # #displayer.displayer(),
                ]

    def listOfCalculables(self, pars):
        out = supy.calculables.zeroArgs(supy.calculables)
        # out += supy.calculables.zeroArgs(calculables) # fixme
        out += [calculables.nus(),
                calculables.nus_pt(),
                calculables.pt_two_nu(),
                calculables.DR1(),
                calculables.DR2(),
                calculables.CDT1(),
                calculables.CDT2(),
                calculables.gDPhi12(),
                calculables.rDPhi12(),
                calculables.gt1(),
                calculables.gt2(),
                calculables.gv1(),
                calculables.gv2(),
                calculables.gv1_gt1(),
                calculables.gv2_gt2(),
                calculables.rv1_gv1(),
                calculables.rv2_gv2(),
                calculables.rv1(),
                calculables.rv2(),
                calculables.gtMass(),
                calculables.gvMass(),
                calculables.rvMass(),
                calculables.genmet(),
                calculables.pfmet(),
                calculables.nSelected(),
                calculables.cov("pfmet", sym=True),
                calculables.cov("pfmet", sym=False),
                calculables.rho_xy("pfmet"),
                calculables.gaus(("genmet", "pfmet")),
                calculables.gaus(("nus", "pfmet")),
                calculables.measured_tau_leptons(),
                calculables.has_hadronic_taus(),
                calculables.svfitter(met="pfmet"),
                calculables.svs(met="pfmet"),
                ]
        return out


    def listOfSampleDictionaries(self):
        h = supy.samples.SampleHolder()
        # xs in pb

        if True:
            v3 = 'utils.fileListFromDisk("/home/elaird/v3/DY_all_SYNC_tt.root", pruneList=False, isDirectory=False)'
            h.add('dy_ll', v3, xs=3504.)
        else:
            zm = 'utils.fileListFromDisk("/user_data/zmao/13TeV_samples_25ns/%s_inclusive.root", pruneList=False, isDirectory=False)'
            h.add('dy_ll', zm % 'DY_all_ZTT_SYNC_tt', xs=3504.)
        return [h]


    def listOfSamples(self, pars):
        from supy.samples import specify
        n = None
        return (specify(names="dy_ll", nFilesMax=n) +
                []
                )


    def conclude(self, pars):
        org = self.organizer(pars, verbose=True)

        def gopts(name="", color=1):
            return {"name": name, "color": color, "markerStyle": 1, "lineWidth": 2, "goptions": "ehist"}

        for new, old, color in [("DY->ll", "dy_ll", r.kBlue),
                                ]:
            org.mergeSamples(targetSpec=gopts(new, color), sources=[old])

        # org.scale()  # to data
        org.scale(lumiToUseInAbsenceOfData=20.0e3) # /pb
        # org.scale(toPdf=True)

        supy.plotter(org,
                     pdfFileName=self.pdfFileName(org.tag),
                     printImperfectCalcPageIfEmpty=False,
                     printXs=True,
                     blackList=["lumiHisto", "xsHisto", "nJobsHisto"],
                     rowColors=[r.kBlack, r.kViolet+4],
                     doLog=False,
                     # pegMinimum=0.1,
                     ).plotAll()
