import supy
import calculables
import calculables.sv
import ROOT as r
import plots_cfg


class svSkim(supy.analysis):
    channels = ["tt", "mt", "et", "em"]

    def parameters(self):
        return {"met": "pfmet",
                "sv": ["mc"],
                "svKeys": ["mass", "massUncert", "massLmax", "pt", "eta", "phi"],
                "histoNames": {"eventCountWeighted": "initWeightedEvents", "eventCount": "initEvents"},
                }

    def listOfSteps(self, pars):
        met = pars["met"]
        extraVars = sorted(pars["histoNames"].values())
        for sv in pars["sv"]:
            for key in pars["svKeys"]:
                extraVars.append("%s_sv%s_%s" % (met, sv, key))

        return [supy.steps.printer.progressPrinter(),
                supy.steps.filters.multiplicity("measured_tau_leptons", min=2, max=2),
                supy.steps.other.skimmer(mainChain=True, extraVars=extraVars, haddOutput=True),
                ]

    def listOfCalculables(self, pars):
        met = pars["met"]
        svl = pars["sv"]
        out = supy.calculables.zeroArgs(supy.calculables)
        out += [calculables.pfmet(),
                calculables.cov(met, sym=False),
                calculables.sv.measured_tau_leptons(),
                calculables.sv.has_hadronic_taus(),
                calculables.sv.svfitter(met=met, verbosity=0),
                calculables.sv.svs(met=met, mc=("mc" in svl), vg=("vg" in svl), pl=("pl" in svl)),
                ]
        for sv in svl:
            for key in pars["svKeys"]:
                out += [calculables.sv.sv_access(met=met, sv=sv, key=key)]

        for hName, leafName in pars["histoNames"].iteritems():
            out.append(calculables.histo_bin1(hName, leafName))

        return out


    def listOfSampleDictionaries(self):
        d = "/user_data/elaird/13TeV_samples_25ns_Spring15_eletronID2"

        h = supy.samples.SampleHolder()
        zm = 'utils.fileListFromDisk("%s/%s_%s_inclusive.root", pruneList=False, isDirectory=False)'
        for name, stem, _ in plots_cfg.dataCardSamplesList:
            for dm in self.channels:
                h.add("%s_%s" % (name, dm), zm % (d, stem.replace(plots_cfg.dir, ""), dm), xs=1.0)  # dummy XS
        return [h]


    def listOfSamples(self, pars):
        test = False

        from supy.samples import specify
        out = []
        for name, _, _ in plots_cfg.dataCardSamplesList:
            for dm in self.channels:
                if test and name != "ZTT": continue
                out += specify(names="%s_%s" % (name, dm), nEventsMax=(2 if test else None))
        return tuple(out)
