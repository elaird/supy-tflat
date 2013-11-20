import supy
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
        # xs in pb  (hacked to accommodate PAT skim)
        h.add("H300_hh_bbtautau",
              '["/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_7/src/UWAnalysis/CRAB/LTau/gg/analysis_signal.root"]',
              xs=0.0159 * 1932./8100.)
        h.add("ZZ_2l2q",
              '["/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_7/src/UWAnalysis/CRAB/LTau/zz/analysis_zz.root"]',
              xs=2.5 * 1760./6226.)
        h.add("tt_bbll",
              '["/afs/hep.wisc.edu/home/zmao/CMSSW_5_3_7/src/UWAnalysis/CRAB/LTau/tt/analysis_tt.root"]',
              xs=26.1975 * 4052./10832.)
        return [h]


    def listOfSamples(self, pars):
        from supy.samples import specify
        return (specify(names="H300_hh_bbtautau", color=r.kBlue, nFilesMax=None) +
                specify(names="ZZ_2l2q", color=r.kRed, nFilesMax=None) +
                specify(names="tt_bbll", color=28, nFilesMax=None) +
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
