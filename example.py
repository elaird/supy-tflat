import supy
import displayer
import calculables
import ROOT as r

class example(supy.analysis):
    
    def listOfSteps(self, pars):
        return [supy.steps.printer.progressPrinter(),
                #supy.steps.histos.multiplicity("genTauPt"),
                #supy.steps.filters.multiplicity("genTauPt", min=2, max=2),
                #supy.steps.histos.multiplicity("genBPt"),
                #supy.steps.filters.multiplicity("genBPt", min=2, max=2),

                supy.steps.histos.multiplicity("Js_CSVbtagSorted"),
                supy.steps.filters.multiplicity("Js_CSVbtagSorted", min=2),

                supy.steps.histos.value("Js_CSVbtagSorted_CSVbtag0", 20, 0.0, 1.0),
                supy.steps.filters.value("Js_CSVbtagSorted_CSVbtag0", min=0.679),

                supy.steps.histos.value("Js_CSVbtagSorted_CSVbtag1", 20, 0.0, 1.0),
                supy.steps.filters.value("Js_CSVbtagSorted_CSVbtag1", min=0.244),

                supy.steps.histos.mass("diJetP4", 20, 0.0, 200.0),
                supy.steps.filters.mass("diJetP4", min=100.0, max=140.0),

                supy.steps.histos.multiplicity("pt1"),
                supy.steps.filters.multiplicity("pt1", min=1),

                supy.steps.histos.mass("diTauP4", 20, 0.0, 200.0),
                #supy.steps.histos.pt("diTauP4", 20, 0.0, 200.0),
                #supy.steps.filters.mass("diTauP4", min=50.0, max=130.0),

                supy.steps.histos.mass("svP4", 20, 0.0, 200.0),
                supy.steps.filters.mass("svP4", min=100.0, max=130.0),

                #supy.steps.histos.multiplicity("met"),
                supy.steps.histos.value("met0", 20, 0.0, 200.0),

                #displayer.displayer(),
                ]


    def listOfCalculables(self, pars):
        out = supy.calculables.zeroArgs(supy.calculables)
        #out += supy.calculables.zeroArgs(calculables)
        out += [calculables.jets(var="J", nBranches=4, ptMin=20.0, absEtaMax=2.4,
                                 keys=["CSVbtag"], sortBy="CSVbtag", reverse=True),
                calculables.indexedVar(index=0, var="Js_CSVbtagSorted", key="CSVbtag"),
                calculables.indexedVar(index=1, var="Js_CSVbtagSorted", key="CSVbtag"),
                calculables.diJetP4(var="Js_CSVbtagSorted"),
                calculables.diTauP4(index=0),
                calculables.svP4(index=0),
                calculables.one("met", index=0),
                ]
        return out


    def listOfSampleDictionaries(self):
        h = supy.samples.SampleHolder()
        # xs in pb
        h.add("H300_hh_bbtautau",
              #'["/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_7/src/UWAnalysis/CRAB/LTau/gg/analysis_signal.root"]',
              #'["/scratch/zmao/analysis.root"]',
              'utils.fileListFromDisk("/hdfs/store/user/zmao/H2hh2-SUB-TT/")',
              xs=0.0159)

        h.add("ZZ_2l2q",
              'utils.fileListFromDisk("/hdfs/store/user/zmao/ZZ3-SUB-TT/")',
              xs=2.5)

        h.add("tt_bbll",
              #'["/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_7/src/UWAnalysis/CRAB/LTau/tt/analysis_tt.root"]',
              'utils.fileListFromDisk("/hdfs/store/user/zmao/tt2-SUB-TT/")',
              xs=26.1975)
        return [h]


    def listOfSamples(self, pars):
        from supy.samples import specify

        w = calculables.LastBinOverFirstBin(dir="TT", histoName="results")

        nFilesMax = None
        return (specify(names="H300_hh_bbtautau", color=r.kBlue, weights=w, nFilesMax=nFilesMax) +
                specify(names="ZZ_2l2q", color=r.kRed, weights=w, nFilesMax=nFilesMax) +
                specify(names="tt_bbll", color=28, weights=w, nFilesMax=nFilesMax) +
                []
                )


    def conclude(self, pars):
        org = self.organizer(pars)

        def gopts(name="", color=1):
            return {"name":name, "color":color, "markerStyle":1, "lineWidth":2, "goptions":"ehist"}

        for sample, color in [("H300_hh_bbtautau", r.kBlue),
                              ("ZZ_2l2q", r.kRed),
                              ("tt_bbll", 28)]:
            org.mergeSamples(targetSpec=gopts(sample, color), sources=[sample+".LastBinOverBin1"])

        org.scale(20.0e3) # pb
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


                     samplesForRatios=("H300_hh_bbtautau", "tt_bbll"),
                     sampleLabelsForRatios=("hh", "tt"),
                     foms=[{"value": lambda x, y: x/y,
                            "uncRel": lambda x, y, xUnc, yUnc: ((xUnc/x)**2 + (yUnc/y)**2)**0.5,
                            "label": lambda x, y:"%s/%s" % (x, y),
                            },
                           # #{"value": lambda x,y: x/(y**0.5),
                           # # "uncRel": lambda x, y, xUnc, yUnc: math.sqrt((xUnc/x)**2 + (yUnc/y/2.)**2),
                           # # "label": lambda x,y: "%s/sqrt(%s)" % (x, y),
                           # # },
                           ],
                     ).plotAll()
