import supy
import configuration
import calculables
import calculables.sv
import ROOT as r


class svSkim(supy.analysis):
    def parameters(self):
        return {"met": "pfmet",
                "sv": ["mc"],
                }

    def listOfSteps(self, pars):
        met = pars["met"]
        extraVars = []
        for sv in pars["sv"]:
            extraVars.append("%ssvMass%s" % (met, sv))

        return [supy.steps.printer.progressPrinter(),
                supy.steps.filters.multiplicity("measured_tau_leptons", min=2, max=2),
                supy.steps.other.skimmer(mainChain=True, extraVars=extraVars),
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
            out += [calculables.sv.svMass(met=met, sv=sv)]

        return out


    def listOfSampleDictionaries(self):
        h = supy.samples.SampleHolder()
        # xs in pb

        zm = 'utils.fileListFromDisk("/user_data/zmao/13TeV_samples_25ns/%s_inclusive.root", pruneList=False, isDirectory=False)'
        h.add('dy_tt', zm % 'DY_all_ZTT_SYNC_tt', xs=3504.)
        h.add('dy_mt', zm % 'DY_all_ZTT_SYNC_mt', xs=3504.)
        h.add('dy_et', zm % 'DY_all_ZTT_SYNC_et', xs=3504.)
        h.add('dy_em', zm % 'DY_all_ZTT_SYNC_em', xs=3504.)
        h.add('m160_tt', zm % 'SUSY_all_SYNC_tt', xs=3504.)
        h.add('m160_mt', zm % 'SUSY_all_SYNC_mt', xs=3504.)
        h.add('m160_et', zm % 'SUSY_all_SYNC_et', xs=3504.)
        h.add('m160_em', zm % 'SUSY_all_SYNC_em', xs=3504.)
        return [h]


    def listOfSamples(self, pars):
        from supy.samples import specify
        n = 2
        return (# specify(names="dy_tt", nEventsMax=n) +
                # specify(names="dy_mt", nEventsMax=n) +
                # specify(names="dy_et", nEventsMax=n) +
                specify(names="dy_em", nEventsMax=n) +
                # specify(names="m160_tt", nEventsMax=n) +
                # specify(names="m160_mt", nEventsMax=n) +
                # specify(names="m160_et", nEventsMax=n) +
                # specify(names="m160_em", nEventsMax=n) +
                []
                )
