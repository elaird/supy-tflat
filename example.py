import supy
import displayer
import steps
import calculables
import ROOT as r

class example(supy.analysis):
    def parameters(self):
        return {"extraVars": ["diTauHadTriggerWeight",
                              #"LastBinOverBin1",
                              ],
                "tauLegs": {"ptMin": 45.0,
                            "absEtaMax": 2.1,
                            "index": 0,
                            "isoMax": 1.5,
                            },
                "ss": self.vary(dict([("os", {"max": 0.5}),
                                      ("ss", {"min": 0.5}),
                                      ]
                                     )
                                ),
                }

    def listOfSteps(self, pars):
        return [supy.steps.printer.progressPrinter(),
                #calculables.LastBinOverBin(dir="TT", histoName="results", iBin=1).onlySim(),
                calculables.LastBinOverBin(dir="/", histoName="preselection", iBin=1).onlySim(),

                #supy.steps.histos.multiplicity("genTauPt"),
                #supy.steps.filters.multiplicity("genTauPt", min=2, max=2),
                #supy.steps.histos.multiplicity("genBPt"),
                #supy.steps.filters.multiplicity("genBPt", min=2, max=2),

                supy.steps.histos.value("minimumPt", 40, 0.0, 200.0),
                steps.tauLegsPtEta(**pars["tauLegs"]),
                supy.steps.histos.multiplicity("pt1"),
                supy.steps.filters.multiplicity("pt1", min=1),

                supy.steps.filters.label("tauPlots"),
                supy.steps.histos.value("pt1_0", 40, 0.0, 200.0),
                supy.steps.histos.value("pt2_0", 40, 0.0, 200.0),
                supy.steps.histos.value("eta1_0", 20, -3.0, 3.0),
                supy.steps.histos.value("eta2_0", 20, -3.0, 3.0),
                supy.steps.histos.value("iso1_0", 20, 0.0, 4.0),
                supy.steps.histos.value("iso2_0", 20, 0.0, 4.0),
                supy.steps.histos.value("sameSign", 2, -0.5, 1.5),
                supy.steps.filters.value("sameSign", **pars["ss"]),
                supy.steps.histos.value("diTauHadTriggerWeight", 20, 0.0, 2.0).onlySim(),
                steps.blind(index=pars["tauLegs"]["index"]).onlyData(),

                #supy.steps.other.skimmer(mainChain=False, extraVars=pars["extraVars"]),

                supy.steps.filters.label("jetPlots"),
                supy.steps.histos.multiplicity("Js_CSVbtagSorted"),
                supy.steps.filters.multiplicity("Js_CSVbtagSorted", min=2),

                #supy.steps.histos.value("maximumJetPt", 20, 0.0, 100.0),  # ntuple max of 4 to be fixed
                #supy.steps.filters.value("maximumJetPt", min=50.0),


                supy.steps.histos.value("Js_CSVbtagSorted_CSVbtag0", 20, 0.0, 1.0),
                supy.steps.filters.value("Js_CSVbtagSorted_CSVbtag0", min=0.679),

                supy.steps.histos.value("Js_CSVbtagSorted_CSVbtag1", 20, 0.0, 1.0),
                supy.steps.filters.value("Js_CSVbtagSorted_CSVbtag1", min=0.244),

                supy.steps.filters.label("diJetMass"),
                #supy.steps.histos.mass("diJetP4", 20, 0.0, 200.0),
                supy.steps.histos.mass("diJetP4", 25, 0.0, 500.0),
                supy.steps.filters.mass("diJetP4", min=100.0, max=150.0),

                supy.steps.filters.label("diTauMasses"),
                #supy.steps.histos.mass("diTauP4", 20, 0.0, 200.0),
                supy.steps.histos.mass("diTauP4", 25, 0.0, 500.0),
                #supy.steps.histos.pt("diTauP4", 20, 0.0, 200.0),
                #supy.steps.filters.mass("diTauP4", min=50.0, max=130.0),

                #supy.steps.filters.label("diTauSvMass"),
                #supy.steps.histos.mass("svP4", 20, 0.0, 200.0),
                supy.steps.histos.mass("svP4", 25, 0.0, 500.0),
                supy.steps.filters.mass("svP4", min=100.0, max=150.0),

                #supy.steps.histos.multiplicity("met"),
                #supy.steps.histos.value("met_0", 20, 0.0, 200.0),

                supy.steps.histos.mass("sumP4_diJetP4_diTauP4", 25, 0.0, 500.0),
                supy.steps.histos.mass("sumP4_diJetP4_svP4", 25, 0.0, 500.0),

                #displayer.displayer(),
                ]


    def listOfCalculables(self, pars):
        out = supy.calculables.zeroArgs(supy.calculables)
        #out += supy.calculables.zeroArgs(calculables)
        out += [calculables.jets(var="J", nBranches=4, ptMin=30.0, absEtaMax=2.4,
                                 keys=["CSVbtag"], sortBy="CSVbtag", reverse=True),
                calculables.maximumJetPt(jets="Js_CSVbtagSorted"),
                calculables.indexedVar(index=0, var="Js_CSVbtagSorted", key="CSVbtag"),
                calculables.indexedVar(index=1, var="Js_CSVbtagSorted", key="CSVbtag"),
                calculables.diJetP4(var="Js_CSVbtagSorted"),
                calculables.diTauP4(index=0),
                calculables.svP4(index=0),
                calculables.sumP4(vars=["diJetP4", "diTauP4"]),
                calculables.sumP4(vars=["diJetP4", "svP4"]),
                calculables.one("met", index=0),
                calculables.one("pt1", index=0),
                calculables.one("pt2", index=0),
                calculables.one("eta1", index=0),
                calculables.one("eta2", index=0),
                calculables.one("iso1", index=0),
                calculables.one("iso2", index=0),
                calculables.maximumPt(index=0),
                calculables.minimumPt(index=0),
                calculables.sameSign(index=0),
                calculables.differencePt(index=0),
                calculables.diTauHadTriggerWeight(tauPairIndex=0),
                supy.calculables.other.fixedValue(label="x100", value=100.0),
                ]
        return out


    def listOfSampleDictionaries(self):
        h = supy.samples.SampleHolder()
        hdfs = 'utils.fileListFromDisk("/hdfs/store/user/%s/")'
        # xs in pb
        #h.add("H260_hh_bbtautau", hdfs % 'zmao/H2hh260_noSign_relaxed7-SUB-TT', xs=0.0159)
        #h.add("H300_hh_bbtautau", hdfs % 'zmao/H2hh300_noSign_relaxed7-SUB-TT', xs=0.0159)
        #h.add("H350_hh_bbtautau", hdfs % 'zmao/H2hh350_noSign_relaxed7-SUB-TT', xs=0.0159)
        print "fix xs 260,350"

        #h.add("ZZ_llqq",   hdfs % 'zmao/ZZ_noSign_relaxed4-SUB-TT',         xs=2.5)
        #h.add("tt_bblnln", hdfs % 'zmao/tt_new_noSign_relaxed3-SUB-TT',     xs=26.1975)
        #h.add("tt_bblnqq", hdfs % 'zmao/tt_SemiLep_noSign_relaxed6-SUB-TT', xs=109.281)
        #h.add('dy_ll',     hdfs % 'zmao/DYJetsToLL_relaxed3-SUB-TT',        xs=3504.)
        #h.add('w_ln_2j',   hdfs % 'zmao/W2JetsToLNu_relaxed3-SUB-TT',       xs=1750.)

        #h.add('dataA', hdfs % 'zmao/Tau_Run2012A_relaxed3-SUB-TT-data',        lumi=1.0e3)
        #h.add('dataB', hdfs % 'zmao/TauParked_Run2012B_relaxed3-SUB-TT-data/', lumi=6.0e3)
        #h.add('dataC', hdfs % 'zmao/TauParked_Run2012C_relaxed3-SUB-TT-data/', lumi=6.0e3)
        #h.add('dataD', hdfs % 'zmao/TauParked_Run2012D_relaxed3-SUB-TT-data/', lumi=6.0e3)
        print "fix lumi ABCD"

        zd = 'utils.fileListFromDisk("/scratch/zmao/relaxed_new/%s_all.root", isDirectory=False)'
        h.add("H260_hh_bbtautau", zd % 'H2hh260', xs=0.0159)
        h.add("H300_hh_bbtautau", zd % 'H2hh300', xs=0.0159)
        h.add("H350_hh_bbtautau", zd % 'H2hh350', xs=0.0159)
        h.add("ZZ_llqq",   zd % 'ZZ_eff',  xs=2.5)
        h.add("tt_bblnln", zd % 'tt_eff',  xs=26.1975)
        h.add("tt_bblnqq", zd % 'tt_semi_eff',  xs=109.281)
        h.add('dy_ll',     zd % 'DYJetsToLL_eff',  xs=3504.)
        h.add('w_ln_1j',   zd % 'W1JetsToLNu_eff',  xs=5400.)
        h.add('w_ln_2j',   zd % 'W2JetsToLNu_eff',  xs=1750.)
        h.add('w_ln_3j',   zd % 'W3JetsToLNu_eff',  xs=519.)
        h.add('Data',      zd % 'dataTotal', lumi=19.0e3)

        return [h]


    def listOfSamples(self, pars):
        from supy.samples import specify
        n = None
        mc = ['LastBinOverBin1', 'diTauHadTriggerWeight']
        sig = mc + ['x100']

        return (specify(names="H260_hh_bbtautau", color=r.kRed,  nFilesMax=n, weights=sig) +
                specify(names="H300_hh_bbtautau", color=r.kBlue, nFilesMax=n, weights=sig) +
                specify(names="H350_hh_bbtautau", color=r.kCyan, nFilesMax=n, weights=sig) +

                specify(names="ZZ_llqq",   color=r.kYellow,    nFilesMax=n, weights=mc) +
                specify(names="tt_bblnln", color=r.kMagenta,   nFilesMax=n, weights=mc) +
                specify(names="tt_bblnqq", color=r.kBlue,      nFilesMax=n, weights=mc) +
                specify(names="dy_ll",     color=r.kGreen,     nFilesMax=n, weights=mc) +
                specify(names="w_ln_1j",   color=r.kMagenta+2, nFilesMax=n, weights=mc) +
                specify(names="w_ln_2j",   color=r.kMagenta+2, nFilesMax=n, weights=mc) +
                specify(names="w_ln_3j",   color=r.kMagenta+2, nFilesMax=n, weights=mc) +

                specify(names="Data", nFilesMax=n) +
                #specify(names="dataA", nFilesMax=n) +
                #specify(names="dataB", nFilesMax=n) +
                #specify(names="dataC", nFilesMax=n) +
                #specify(names="dataD", nFilesMax=n) +
                []
                )


    def conclude(self, pars):
        org = self.organizer(pars, verbose=True)

        def gopts(name="", color=1):
            return {"name":name, "color":color, "markerStyle":1, "lineWidth":2, "goptions":"ehist"}

        org.mergeSamples(targetSpec={"name": "Data"}, allWithPrefix="data")

        mc = ".".join(["", "LastBinOverBin1", "diTauHadTriggerWeight"])
        sig = mc + ".x100"
        for sample, color, ws in [("H260_hh_bbtautau", r.kOrange,    sig),
                                  ("H300_hh_bbtautau", 28,           sig),
                                  ("H350_hh_bbtautau", 44,           sig),
                                  ("ZZ_llqq",          r.kYellow,    mc),
                                  ("tt_bblnln",        r.kMagenta,   mc),
                                  ("tt_bblnqq",        r.kBlue,      mc),
                                  ("dy_ll",            r.kGreen,     mc),
                                  ]:
            name = sample
            if ws.endswith(".x100"):
                name = sample[:4] + ".x100"
            org.mergeSamples(targetSpec=gopts(name, color), sources=[sample + ws])

        org.mergeSamples(targetSpec=gopts("w_ln_123j", r.kMagenta+2), allWithPrefix="w_ln")

        org.mergeSamples(targetSpec=gopts("EWK", r.kRed),
                         keepSources=True,
                         sources=["ZZ_llqq", "tt_bblnln", "tt_bblnqq", "dy_ll", "w_ln_123j"])

        org.scale()  # to data
        #org.scale(lumiToUseInAbsenceOfData=20.0e3) # /pb
        #org.scale(toPdf=True)

        supy.plotter(org,
                     pdfFileName=self.pdfFileName(org.tag),
                     printImperfectCalcPageIfEmpty=False,
                     printXs=True,
                     blackList=["lumiHisto", "xsHisto", "nJobsHisto"],
                     rowColors=[r.kBlack, r.kViolet+4],

                     doLog=True,
                     pegMinimum=0.1,
                     showStatBox=False,
                     latexYieldTable=False,

                     #samplesForRatios=("H300_hh_bbtautau", "tt_bbll"),
                     #sampleLabelsForRatios=("hh", "tt"),
                     #foms=[{"value": lambda x, y: x/y,
                     #       "uncRel": lambda x, y, xUnc, yUnc: ((xUnc/x)**2 + (yUnc/y)**2)**0.5,
                     #       "label": lambda x, y:"%s/%s" % (x, y),
                     #       },
                     #      #{"value": lambda x,y: x/(y**0.5),
                     #      # "uncRel": lambda x, y, xUnc, yUnc: math.sqrt((xUnc/x)**2 + (yUnc/y/2.)**2),
                     #      # "label": lambda x,y: "%s/sqrt(%s)" % (x, y),
                     #      # },
                     #      ],
                     ).plotAll()
