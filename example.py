import supy
import displayer
import calculables
import ROOT as r

class example(supy.analysis):
    
    def listOfSteps(self, pars):
        return [supy.steps.printer.progressPrinter(),
                #supy.steps.histos.multiplicity("genTauPt"),
                #supy.steps.filters.multiplicity("genTauPt", min=2, max=2),
                supy.steps.histos.multiplicity("genBPt"),
                #supy.steps.filters.multiplicity("genBPt", min=2, max=2),
                #displayer.displayer(),
                ]


    def listOfCalculables(self, pars):
        out = supy.calculables.zeroArgs(supy.calculables)
        #out += supy.calculables.zeroArgs(calculables)
        return out


    def listOfSampleDictionaries(self):
        h = supy.samples.SampleHolder()
        # xs in pb
        h.add("H300_hh_bbtautau",
              #'["/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_7/src/UWAnalysis/CRAB/LTau/gg/analysis_signal.root"]',
              #'["/scratch/zmao/analysis.root"]',
              'utils.fileListFromDisk("/hdfs/store/user/zmao/H2hh-SUB-TT/")',
              xs=0.0159)

        h.add("ZZ_2l2q",
              'utils.fileListFromDisk("/hdfs/store/user/zmao/ZZ2-SUB-TT/")',
              xs=2.5)

        h.add("tt_bbll",
              #'["/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_7/src/UWAnalysis/CRAB/LTau/tt/analysis_tt.root"]',
              'utils.fileListFromDisk("/hdfs/store/user/zmao/tt-SUB-TT/")',
              xs=26.1975)
        return [h]


    def listOfSamples(self, pars):
        from supy.samples import specify

        w = calculables.LastBinOverFirstBin(dir="TT", histoName="results")

        kargs = {"weights": w,
                 "nFilesMax": 10,
                 }
        return (specify(names="H300_hh_bbtautau", color=r.kBlue, **kargs) +
                specify(names="ZZ_2l2q", color=r.kRed, **kargs) +
                specify(names="tt_bbll", color=28, **kargs) +
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
                     pegMinimum=0.3,
                     showStatBox=False,
                     latexYieldTable=False,
                     ).plotAll()
