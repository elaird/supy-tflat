import supy
import configuration
import displayer
import steps
import calculables
import calculables.sv
import ROOT as r


ss = supy.steps
sshv = ss.histos.value

class look(supy.analysis):
    def listOfSteps(self, pars):
        mMax = 500.0
        return [ss.printer.progressPrinter(),
                # sshv("t1ByCombinedIsolationDeltaBetaCorrRaw3Hits", 100, 0.0, 10.0, xtitle="isolation (GeV)"),
                # sshv("t2ByCombinedIsolationDeltaBetaCorrRaw3Hits", 100, 0.0, 10.0, xtitle="isolation (GeV)"),
                # ss.filters.value("t1GenMass", min=0.0),
                # ss.filters.value("t2GenMass", min=0.0),
                ss.histos.pt("rv1", 100, 0.0, 100.0, xtitle="reco vis 1 p_{T}"),
                ss.histos.pt("rv2", 100, 0.0, 100.0, xtitle="reco vis 2 p_{T}"),
                # ss.filters.pt("rv1", min=35.0),
                # ss.filters.pt("rv2", min=35.0),
                ss.filters.value("DR1", max=0.4),
                ss.filters.value("DR2", max=0.4),
                sshv("CDT1", 150, -1.0, 2.0, xtitle="cos(#Delta#theta_{1})"),
                sshv("CDT2", 150, -1.0, 2.0, xtitle="cos(#Delta#theta_{2})"),
                sshv("DR1", 100, 0.0, 10.0, xtitle="#DeltaR_{1} (gen,reco)"),
                sshv("DR2", 100, 0.0, 10.0, xtitle="#DeltaR_{2} (gen,reco)"),
                sshv("gDPhi12", 20, -r.TMath.Pi(), r.TMath.Pi(), xtitle="gen. taus' #Delta#phi"),
                sshv("rDPhi12", 20, -r.TMath.Pi(), r.TMath.Pi(), xtitle="reco. taus' #Delta#phi"),
                sshv("gv1_gt1", 60, 0.0, 2.0, xtitle="gen. vis. p_{T} 1 (#mu/e/h_{1}) / gen. tau p_{T}"),
                sshv("gv2_gt2", 60, 0.0, 2.0, xtitle="gen. vis. p_{T} 2 (h_{2}/h/e) / gen. tau p_{T}"),
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

                # ss.filters.multiplicity("measured_tau_leptons", min=2, max=2),
                # ss.other.touchstuff(["nSelected"]),
                # ss.other.touchstuff(["pfmetsvfitter"]),
                # ss.other.touchstuff(["pfmetsvs"]),
                # steps.svHistos(),

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
                calculables.sv.measured_tau_leptons(),
                calculables.sv.has_hadronic_taus(),
                calculables.sv.svfitter(met="pfmet", verbosity=2),
                calculables.sv.svs(met="pfmet", mc=True, vg=False, pl=False),
                ]
        return out


    def listOfSampleDictionaries(self):
        h = supy.samples.SampleHolder()
        # xs in pb

        # h.add('dy_ll', 'utils.fileListFromDisk("/home/elaird/v3/DY_all_SYNC_tt.root", pruneList=False, isDirectory=False)', xs=3504.)
        # d = 'utils.fileListFromDisk("/user_data/zmao/13TeV_samples_25ns/%s_inclusive.root", pruneList=False, isDirectory=False)'
        d = 'utils.fileListFromDisk("/user_data/elaird/svSkim-sep18/%s_inclusive.root", pruneList=False, isDirectory=False)'

        h.add('dy_tt', d % 'DY_all_ZTT_SYNC_tt', xs=3504.)
        h.add('dy_mt', d % 'DY_all_ZTT_SYNC_mt', xs=3504.)
        h.add('dy_et', d % 'DY_all_ZTT_SYNC_et', xs=3504.)
        h.add('dy_em', d % 'DY_all_ZTT_SYNC_em', xs=3504.)
        return [h]


    def listOfSamples(self, pars):
        from supy.samples import specify
        n = 1000
        return (specify(names="dy_tt", nEventsMax=n) +
                specify(names="dy_mt", nEventsMax=n) +
                specify(names="dy_et", nEventsMax=n) +
                specify(names="dy_em", nEventsMax=n) +
                []
                )


    def conclude(self, pars):
        org = self.organizer(pars, verbose=True)

        def gopts(name="", color=1):
            return {"name": name, "color": color, "markerStyle": 1, "lineWidth": 2, "goptions": "ehist"}

        for new, old, color in [("DY->tt", "dy_tt", r.kBlue),
                                ("DY->mt", "dy_mt", r.kRed),
                                ("DY->et", "dy_et", r.kOrange + 3),
                                ("DY->em", "dy_em", r.kGreen),
                                ]:
            org.mergeSamples(targetSpec=gopts(new, color), sources=[old])

        # org.scale()  # to data
        org.scale(lumiToUseInAbsenceOfData=4.0e3) # /pb
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
