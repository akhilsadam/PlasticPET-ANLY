from analyzeOptions import Options


class histogramOptions:
    processBreak = False
    photocomptonbreak = False
    byElectronProcess = False
    subfigs = False
    plot_opt = ""

    QE = Options.QE

    detMax = 500 if QE else 1000
    detSumMax = 1500 if QE else 1500
    doiSumMax = 800 if QE else 1500
    binwidth_0 = 20
    binwidth_1 = 20
    binwidth_2 = 20
    def reset():
        histogramOptions.plot_opt = ""