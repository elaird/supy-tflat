import supy
import calculables
import ROOT as r

class example(supy.analysis):
    
    def listOfSteps(self, pars):
        return [supy.steps.printer.progressPrinter(),
                supy.steps.histos.multiplicity("tauPt"),
                supy.steps.filters.multiplicity("tauPt", min=2, max=2),
                supy.steps.histos.multiplicity("bPt"),
                supy.steps.filters.multiplicity("bPt", min=2, max=2),
                ]


    def listOfCalculables(self, pars):
        out = supy.calculables.zeroArgs(supy.calculables)
        #out += supy.calculables.zeroArgs(calculables)
        return out


    def listOfSampleDictionaries(self):
        h = supy.samples.SampleHolder()
        # xs in pb
        h.add("H300_hh_bbtautau",
              '["/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_7/src/UWAnalysis/CRAB/LTau/gg/analysis_signal.root"]',
              xs=0.0159)
        h.add("ZZ_2l2q",
              '["/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_7/src/UWAnalysis/CRAB/LTau/zz/analysis_zz.root"]',
              xs=2.5)
        h.add("tt_bbll",
              '["/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_7/src/UWAnalysis/CRAB/LTau/tt/analysis_tt.root"]',
              xs=26.1975)
        return [h]


    def listOfSamples(self, pars):
        from supy.samples import specify

        w = calculables.LastBinOverFirstBin(dir="TT", histoName="results")

        return (specify(names="H300_hh_bbtautau", weights=w, color=r.kBlue, nFilesMax=None) +
                specify(names="ZZ_2l2q", weights=w, color=r.kRed, nFilesMax=None) +
                specify(names="tt_bbll", weights=w, color=28, nFilesMax=None) +
                []
                )


    def conclude(self, pars):
        org = self.organizer(pars)
        org.scale(1.0e3) # pb
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
