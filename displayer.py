import ROOT as r
import supy

class displayer(supy.steps.displayer):
    def __init__(self,
                 scale=200.0,
                 jets=[{"fixes":("J", "Gen"), "nMax":4, "color":r.kBlack, "width":2, "style":2},
                       {"fixes":("J", ""), "nMax":4, "color":r.kBlue, "width":1, "style":1},
                       ],
                 nMaxParticles=4,
                 particles=[("b", r.kRed),
                            ("tau", r.kCyan),
                            ],
                 nMaxTaus=4,
                 ):
        self.moreName = "(see below)"

        for item in ["scale", "jets", "nMaxParticles", "particles", "nMaxTaus"]:
            setattr(self, item, eval(item))

        self.titleSizeFactor = 1.0
        
        self.legendDict = {}
        self.legendList = []

        self.ellipse = r.TEllipse()
        self.ellipse.SetFillStyle(0)

        self.line = r.TLine()
        self.arrow = r.TArrow()
        self.text = r.TText()
        self.latex = r.TLatex()

    def prepareText(self, params, coords) :
        self.text.SetTextSize(params["size"])
        self.text.SetTextFont(params["font"])
        self.text.SetTextColor(params["color"])
        self.textSlope = params["slope"]

        self.textX = coords["x"]
        self.textY = coords["y"]
        self.textCounter = 0

    def printText(self, message, color=r.kBlack):
        self.text.SetTextColor(color)
        self.text.DrawText(self.textX, self.textY - self.textCounter * self.textSlope, message)
        self.textCounter += 1
        self.text.SetTextColor(r.kBlack)

    def printEvent(self, eventVars, params, coords):
        self.prepareText(params, coords)

        self.printText("Event %10d" % eventVars["EVENT"])
        self.printText("Weight %9.2f" % eventVars["weight"])

        self.printText("")
        #self.printText("rho   %10.1f" % eventVars["rho"])
        self.printText("")

        #met = eventVars["MissingET"][0]
        #self.printText("MET   %10.1f (phi %4.1f)" % (met.MET, met.Phi))
        self.printText("")


    def printJets(self, eventVars=None, params=None, coords=None, fixes=None, nMax=None, highlight=False):
        def j(s="", iJet=None):
            return eventVars["%s%d%s%s" % (fixes[0], 1+iJet, fixes[1], s)]

        self.prepareText(params, coords)
        self.printText(str(fixes))
        headers = "   csv    pT   eta   phi  mass"
        self.printText(headers)
        self.printText("-" * len(headers))

        for iJet in range(nMax):
            if nMax <= iJet:
                self.printText("[%d more not listed]" % (nJets - nMax))
                break

            out = ""
            out += "%6s %5.0f %5.1f %5.1f %5.0f" % ("   " if fixes[1] else "%6.2f" % j("CSVbtag", iJet),
                                                    j("Pt", iJet),
                                                    j("Eta", iJet),
                                                    j("Phi", iJet),
                                                    j("Mass", iJet),
                                                    )
            self.printText(out, r.kBlack)

    def printGenParticles(self, eventVars=None, params=None, coords=None,
                          nMax=None, particles=None, color=r.kBlack):
        def g(s="", iJet=None):
            return eventVars["%s%s" % (particles, s)].at(iJet)

        self.prepareText(params, coords)
        self.printText("gen "+particles)
        headers = "   pT   eta   phi  mass"
        self.printText(headers)
        self.printText("-" * len(headers))

        nParticles = eventVars["%sPt" % particles].size()
        for iParticle in range(nParticles):
            if nMax <= iParticle:
                self.printText("[%d more not listed]" % (nParticles - nMax))
                break
            self.printText("%5.0f %5.1f %5.1f %5.1f" % (g("Pt", iParticle),
                                                        g("Eta", iParticle),
                                                        g("Phi", iParticle),
                                                        g("Mass", iParticle),
                                                        ),
                           color=color)
        return


    def printTaus(self, eventVars=None, params=None, coords=None,
                  nMax=None, color=r.kBlack, ptMin=None):
        self.prepareText(params, coords)

        self.printText("taus")
        headers = "   pT  eta  phi  iso"
        self.printText(headers)
        self.printText("-" * len(headers))

        for iLepton in range(nLeptons):
            if nMax <= iLepton:
                self.printText("[%d more not listed]" % (nLeptons - nMax))
                break

            lepton = eventVars[leptons][iLepton]
            iso = "%4.1f" % lepton.IsolationVar if hasattr(lepton, "IsolationVar") else "    "
            self.printText("%5.0f %s %4.1f %s" % (lepton.PT,
                                                  lepton.Phi,
                                                  iso,
                                                  ),
                           color=color)
        return


    def drawSkeleton(self, coords, color) :
        r.gPad.AbsCoordinates(False)
        
        self.ellipse.SetLineColor(color)
        self.ellipse.SetLineWidth(1)
        self.ellipse.SetLineStyle(1)
        self.ellipse.DrawEllipse(coords["x0"], coords["y0"], coords["radius"], coords["radius"], 0.0, 360.0, 0.0, "")

        self.line.SetLineColor(color)
        self.line.DrawLine(coords["x0"]-coords["radius"], coords["y0"]                 , coords["x0"]+coords["radius"], coords["y0"]                 )
        self.line.DrawLine(coords["x0"]                 , coords["y0"]-coords["radius"], coords["x0"]                 , coords["y0"]+coords["radius"])

    def drawScale(self, color, size, scale, point) :
        self.latex.SetTextSize(size)
        self.latex.SetTextColor(color)
        self.latex.DrawLatex(point["x"], point["y"],"radius = "+str(scale)+" GeV p_{T}")

    def drawP4(self,
               rhoPhiPad=None,
               etaPhiPad=None,
               coords=None,
               p4=None,
               lineColor=None,
               lineWidth=1,
               lineStyle=1,
               arrowSize=1.0,
               circleRadius=1.0,
               b=None,
               tau=None):

        c = coords
        x0 = c["x0"]
        y0 = c["y0"]
        x1 = x0 + p4.px()*c["radius"]/c["scale"]
        y1 = y0 + p4.py()*c["radius"]/c["scale"]

        rhoPhiPad.cd()
        self.arrow.SetLineColor(lineColor)
        self.arrow.SetLineWidth(lineWidth)
        self.arrow.SetLineStyle(lineStyle)
        self.arrow.SetArrowSize(arrowSize)
        self.arrow.SetFillColor(lineColor)
        self.arrow.DrawArrow(x0, y0, x1, y1)

        etaPhiPad.cd()
        self.ellipse.SetLineColor(lineColor)
        self.ellipse.SetLineWidth(lineWidth)
        self.ellipse.SetLineStyle(lineStyle)
        self.ellipse.DrawEllipse(p4.eta(), p4.phi(), circleRadius, circleRadius, 0.0, 360.0, 0.0, "")

        if b:
            self.ellipse.SetLineColor(r.kRed)
            self.ellipse.SetLineStyle(3)
            self.ellipse.DrawEllipse(p4.eta(), p4.phi(), circleRadius, circleRadius, 0.0, 360.0, 0.0, "")

        if tau:
            self.ellipse.SetLineColor(r.kCyan)
            self.ellipse.SetLineStyle(2)
            self.ellipse.DrawEllipse(p4.eta(), p4.phi(), circleRadius, circleRadius, 0.0, 360.0, 0.0, "")

    def legendFunc(self, lineColor=None, lineStyle=1, name="", desc=""):
        if name not in self.legendDict:
            self.legendDict[name] = True
            self.legendList.append((lineColor, lineStyle, desc, "l"))

    def drawGenParticles(self, eventVars=None, indices="",
                         coords=None, lineColor=None,
                         lineWidth=1, lineStyle=1,
                         arrowSize=-1.0, circleRadius=None):

        self.legendFunc(lineColor=lineColor,
                        lineStyle=lineStyle,
                        name=indices,
                        desc=indices)

        for iParticle in eventVars[indices]:
            particle = eventVars["genP4"].at(iParticle)
            if circleRadius is None:
                self.drawP4(coords=coords,
                            p4=particle,
                            lineColor=lineColor,
                            lineWidth=lineWidth,
                            arrowSize=arrowSize)
            else :
                self.drawCircle(p4=particle,
                                lineColor=lineColor,
                                lineWidth=lineWidth,
                                circleRadius=circleRadius)


    def drawJets(self, eventVars=None, fixes=None, nMax=None, vec=False, bVar="",
                 coords=None, lineColor=None, lineWidth=1, lineStyle=1,
                 arrowSize=-1.0, circleRadius=None, rhoPhiPad=None, etaPhiPad=None):

        def j(s="", iJet=None):
            if vec:
                return eventVars["%s%s" % (fixes[0], s)].at(iJet)
            else:
                return eventVars["%s%d%s%s" % (fixes[0], 1+iJet, fixes[1], s)]
        
        self.legendFunc(lineColor=lineColor,
                        lineStyle=lineStyle,
                        name="".join(fixes), desc="".join(fixes))

        for iJet in range(nMax):
            if not j("Pt", iJet):
                continue
            self.drawP4(rhoPhiPad=rhoPhiPad,
                        etaPhiPad=etaPhiPad,
                        coords=coords,
                        p4=supy.utils.LorentzV(j("Pt", iJet), j("Eta", iJet), j("Phi", iJet), j("Mass", iJet)),
                        b=False if (fixes[1] or not bVar) else (j(bVar, iJet) > 0.679),
                        tau=False,
                        lineColor=lineColor,
                        lineWidth=lineWidth,
                        lineStyle=lineStyle,
                        arrowSize=arrowSize,
                        circleRadius=circleRadius)


    def etaPhiPad(self, eventVars, corners):
        pad = r.TPad("etaPhiPad", "etaPhiPad",
                     corners["x1"], corners["y1"],
                     corners["x2"], corners["y2"])
        pad.cd()
        pad.SetTickx()
        pad.SetTicky()

        etaPhiPlot = r.TH2D("etaPhi", ";#eta;#phi;",
                            1, -r.TMath.Pi(), r.TMath.Pi(),
                            1, -r.TMath.Pi(), r.TMath.Pi())
        etaPhiPlot.SetStats(False)
        etaPhiPlot.Draw()
        return pad, etaPhiPlot


    def rhoPhiPad(self, eventVars, coords, corners):
        pad = r.TPad("rhoPhiPad", "rhoPhiPad", corners["x1"], corners["y1"], corners["x2"], corners["y2"])
        pad.cd()

        skeletonColor = r.kYellow+1
        self.drawSkeleton(coords, skeletonColor)
        self.drawScale(color=skeletonColor, size=0.03, scale=coords["scale"],
                       point={"x":0.0, "y":coords["radius"]+coords["y0"]+0.03})
        return pad

    def drawObjects(self, eventVars=None, etaPhiPad=None, rhoPhiPad=None, rhoPhiCoords=None):
        defArrowSize=0.5*self.arrow.GetDefaultArrowSize()
        defWidth=1

        arrowSize = defArrowSize
        for particles, color in self.particles:
            self.drawJets(eventVars=eventVars,
                          fixes=(particles, ""),
                          vec=True,
                          nMax=eventVars["%sPt" % particles].size(),
                          coords=rhoPhiCoords,
                          lineColor=color,
                          arrowSize=arrowSize,
                          circleRadius=0.15,
                          rhoPhiPad=rhoPhiPad,
                          etaPhiPad=etaPhiPad,
                          )
            arrowSize *= 0.8

        for d in self.jets:
            self.drawJets(eventVars=eventVars,
                          fixes=d["fixes"],
                          nMax=d["nMax"],
                          bVar="CSVbtag",
                          coords=rhoPhiCoords,
                          lineColor=d["color"],
                          lineWidth=d["width"],
                          lineStyle=d["style"],
                          arrowSize=arrowSize,
                          circleRadius=0.5,
                          rhoPhiPad=rhoPhiPad,
                          etaPhiPad=etaPhiPad,
                          )
            arrowSize *= 0.8


    def drawLegend(self, corners) :
        pad = r.TPad("legendPad", "legendPad", corners["x1"], corners["y1"], corners["x2"], corners["y2"])
        pad.cd()
        
        legend = r.TLegend(0.0, 0.0, 1.0, 1.0)
        for color, style, desc, gopts in self.legendList:
            self.line.SetLineColor(color)
            self.line.SetLineStyle(style)
            someLine = self.line.DrawLine(0.0, 0.0, 0.0, 0.0)
            legend.AddEntry(someLine, desc, gopts)
        legend.Draw("same")
        self.canvas.cd()
        pad.Draw()
        return [pad,legend]

    def printText1(self, eventVars, corners):
        pad = r.TPad("textPad", "textPad",
                     corners["x1"], corners["y1"],
                     corners["x2"], corners["y2"])
        pad.cd()

        defaults = {}
        defaults["size"] = 0.035
        defaults["font"] = 80
        defaults["color"] = r.kBlack
        defaults["slope"] = 0.017
        s = defaults["slope"]

        smaller = {}
        smaller.update(defaults)
        smaller["size"] = 0.034

        yy = 0.98
        x0 = 0.01
        x1 = 0.51
        self.printEvent(eventVars, params=defaults, coords={"x": x0, "y": yy})

        y = yy - 7*s
        for d in self.jets:
            self.printJets(eventVars,
                           params=smaller,
                           coords={"x": x0, "y": y},
                           fixes=d["fixes"],
                           nMax=d["nMax"],
                           highlight=False)
            y -= s*(5 + d["nMax"])

        for (particles, color) in self.particles:
            self.printGenParticles(eventVars,
                                   params=smaller,
                                   particles=particles,
                                   color=color,
                                   coords={"x": x0, "y": y},
                                   nMax=self.nMaxParticles)
            y -= s*(5 + self.nMaxParticles)

        self.canvas.cd()
        pad.Draw()
        return [pad]


    def printText2(self, eventVars, corners):
        pad = r.TPad("textPad2", "textPad2",
                     corners["x1"], corners["y1"],
                     corners["x2"], corners["y2"])
        pad.cd()

        defaults = {}
        defaults["size"] = 0.08
        defaults["font"] = 80
        defaults["color"] = r.kBlack
        defaults["slope"] = 0.03
        s = defaults["slope"]

        y = 0.98 - 2*s
        x0 = 0.01

        self.printTaus(eventVars,
                       params=defaults,
                       coords={"x": x0, "y": y},
                       nMax=self.nMaxTaus)
        y -= s*(5 + self.nMaxTaus)

        self.canvas.cd()
        pad.Draw()
        return [pad]


    def display(self, eventVars):
        rhoPhiPadYSize = 0.50*self.canvas.GetAspectRatio()
        rhoPhiPadXSize = 0.50
        radius = 0.4

        rhoPhiCoords = {"scale":self.scale, "radius":radius,
                        "x0":radius, "y0":radius+0.05}

        rhoPhiCorners = {"x1":0.0,
                         "y1":0.0,
                         "x2":rhoPhiPadXSize,
                         "y2":rhoPhiPadYSize}

        etaPhiCorners = {"x1":rhoPhiPadXSize - 0.18,
                         "y1":rhoPhiPadYSize - 0.08*self.canvas.GetAspectRatio(),
                         "x2":rhoPhiPadXSize + 0.12,
                         "y2":rhoPhiPadYSize + 0.22*self.canvas.GetAspectRatio()}

        legendCorners = {"x1":0.0,
                         "y1":rhoPhiPadYSize,
                         "x2":1.0-rhoPhiPadYSize,
                         "y2":1.0}

        textCorners1 =  {"x1":rhoPhiPadXSize + 0.11,
                         "y1":0.0,
                         "x2":1.0,
                         "y2":1.0}

        textCorners2 = {"x1":rhoPhiPadXSize - 0.08,
                        "y1":0.0,
                        "x2":rhoPhiPadXSize + 0.11,
                        "y2":0.55}

        rhoPhiPad = self.rhoPhiPad(eventVars, rhoPhiCoords, rhoPhiCorners)
        etaPhiPad, etaPhiPlot = self.etaPhiPad(eventVars, etaPhiCorners)
        
        keep = [rhoPhiPad, etaPhiPad, etaPhiPlot]
        self.drawObjects(eventVars, etaPhiPad, rhoPhiPad, rhoPhiCoords)
        
        self.canvas.cd()
        rhoPhiPad.Draw()
        etaPhiPad.Draw()

        keep.append(self.drawLegend(corners=legendCorners))
        keep.append(self.printText1(eventVars, corners=textCorners1))
        #keep.append(self.printText2(eventVars, corners=textCorners2))
        return keep
