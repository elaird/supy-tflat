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
                            "isoMax":2.0,
                            },
                "ss": self.vary(dict([("os", {"max": 0.5}),
                                      ("ss", {"min": 0.5}),
                                      ]
                                     )
                                ),
                }

    def listOfSteps(self, pars):
        return [supy.steps.printer.progressPrinter(),
                calculables.LastBinOverBin(dir="TT", histoName="results", iBin=1).onlySim(),

                #supy.steps.histos.multiplicity("genTauPt"),
                #supy.steps.filters.multiplicity("genTauPt", min=2, max=2),
                #supy.steps.histos.multiplicity("genBPt"),
                #supy.steps.filters.multiplicity("genBPt", min=2, max=2),

                supy.steps.histos.value("minimumPt", 40, 0.0, 200.0),
                steps.tauLegsPtEta(**pars["tauLegs"]),

                supy.steps.filters.label("tauPlots"),
                supy.steps.histos.value("pt1_0", 40, 0.0, 200.0),
                supy.steps.histos.value("pt2_0", 40, 0.0, 200.0),
                supy.steps.histos.value("eta1_0", 20, -3.0, 3.0),
                supy.steps.histos.value("eta2_0", 20, -3.0, 3.0),
                supy.steps.histos.value("iso1_0", 20, 0.0, 4.0),
                supy.steps.histos.value("iso2_0", 20, 0.0, 4.0),
                supy.steps.histos.value("sameSign", 2, -0.5, 1.5),
                supy.steps.filters.value("sameSign", **pars["ss"]),
                supy.steps.histos.value("diTauHadTriggerWeight", 20, 0.0, 2.0),
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
                supy.steps.filters.mass("diJetP4", min=100.0, max=140.0),

                supy.steps.filters.label("diTauMass"),
                supy.steps.histos.multiplicity("pt1"),
                supy.steps.filters.multiplicity("pt1", min=1),

                #supy.steps.histos.mass("diTauP4", 20, 0.0, 200.0),
                supy.steps.histos.mass("diTauP4", 25, 0.0, 500.0),
                #supy.steps.histos.pt("diTauP4", 20, 0.0, 200.0),
                #supy.steps.filters.mass("diTauP4", min=50.0, max=130.0),

                supy.steps.filters.label("diTauSvMass"),
                #supy.steps.histos.mass("svP4", 20, 0.0, 200.0),
                supy.steps.histos.mass("svP4", 25, 0.0, 500.0),
                supy.steps.filters.mass("svP4", min=100.0, max=130.0),

                #supy.steps.histos.multiplicity("met"),
                #supy.steps.histos.value("met_0", 20, 0.0, 200.0),

                supy.steps.histos.mass("sumP4_diJetP4_diTauP4", 20, 0.0, 400.0),
                supy.steps.histos.mass("sumP4_diJetP4_svP4", 20, 0.0, 400.0),

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
                ]
        return out


    def listOfSampleDictionaries(self):
        h = supy.samples.SampleHolder()
        hdfs = 'utils.fileListFromDisk("/hdfs/store/user/%s/")'

        # xs in pb
        h.add("H300_hh_bbtautau", hdfs % 'zmao/H2hh300_new-SUB-TT', xs=0.0159)
        h.add("H350_hh_bbtautau", hdfs % 'zmao/H2hh350_new-SUB-TT', xs=0.0159)
        h.add("H260_hh_bbtautau", hdfs % 'zmao/H2hh260_new3-SUB-TT', xs=0.0159)
        print "fix xs 260,350"

        h.add("ZZ_2l2q", hdfs % 'zmao/ZZ_noSign-SUB-TT', xs=2.5)
        #h.add("tt_bbll", hdfs % 'zmao/tt_new-SUB-TT', xs=26.1975)
        h.add("tt_bblnln", hdfs % 'zmao/tt_new_moreGenInfo-SUB-TT', xs=26.1975)
        h.add("tt_bblnqq", hdfs % 'zmao/tt_SemiLep_noSign-SUB-TT', xs=109.281)
        h.add('dy_ll',     hdfs % 'zmao/DYJetsToLL-SUB-TT', xs=3504.)
        h.add('w_ln_2j',   hdfs % 'zmao/W2JetsToLNu-SUB-TT', xs=1750.)

        h.add('dataA', hdfs % 'zmao/Tau_Run2012A-SUB-TT-data',          lumi=1.0e3)
        h.add('dataB', hdfs % 'elaird/TauParked_Run2012B-SUB-TT-data/', lumi=6.0e3)
        h.add('dataC', hdfs % 'elaird/TauParked_Run2012C-SUB-TT-data/', lumi=6.0e3)
        h.add('dataD', hdfs % 'elaird/TauParked_Run2012D-SUB-TT-data/', lumi=6.0e3)
        print "fix lumi ABCD"

        return [h]


    def listOfSamples(self, pars):
        from supy.samples import specify
        n = None
        kMc = {"weights": ['LastBinOverBin1', 'diTauHadTriggerWeight'],
               "nFilesMax": n,
               }

        return (#specify(names="H260_hh_bbtautau", color=r.kRed, **kMc) +
                #specify(names="H300_hh_bbtautau", color=r.kBlue, **kMc) +
                #specify(names="H350_hh_bbtautau", color=r.kCyan, **kMc) +

                specify(names="ZZ_2l2q",   color=r.kYellow,    **kMc) +
                specify(names="tt_bblnln", color=r.kMagenta,   **kMc) +
                specify(names="tt_bblnqq", color=r.kBlue,      **kMc) +
                specify(names="dy_ll",     color=r.kGreen,     **kMc) +
                specify(names="w_ln_2j",   color=r.kMagenta+2, **kMc) +
                
                specify(names="dataA", nFilesMax=n) +
                specify(names="dataB", nFilesMax=n) +
                specify(names="dataC", nFilesMax=n) +
                specify(names="dataD", nFilesMax=n) +
                []
                )


    def conclude(self, pars):
        org = self.organizer(pars)

        def gopts(name="", color=1):
            return {"name":name, "color":color, "markerStyle":1, "lineWidth":2, "goptions":"ehist"}

        org.mergeSamples(targetSpec={"name": "Data"}, allWithPrefix="data")

        weightString = ".".join(["", "LastBinOverBin1", "diTauHadTriggerWeight"])
        for sample, color in [("H260_hh_bbtautau", r.kOrange),
                              ("H300_hh_bbtautau", r.kBlue),
                              ("H350_hh_bbtautau", r.kCyan),
                              ("ZZ_2l2q",   r.kYellow,   ),
                              ("tt_bblnln", r.kMagenta,  ),
                              ("tt_bblnqq", r.kBlue,     ),
                              ("dy_ll",     r.kGreen,    ),
                              ("w_ln_2j",   r.kMagenta+2,),
                              ]:
            org.mergeSamples(targetSpec=gopts(sample, color), sources=[sample + weightString])


        org.mergeSamples(targetSpec=gopts("EWK", r.kRed),
                         keepSources=True,
                         sources=["ZZ_2l2q", "tt_bblnln", "tt_bblnqq", "dy_ll", "w_ln_2j"])

        org.scale()  # to data
        #org.scale(20.0e3) # /pb
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
