import multiprocessing
try: AnalyzeOptions
except: AnalyzeOptions = True
if(AnalyzeOptions):
    #------------------------------------------------------------------------------------
    PYTHONIOENCODING="UTF-8"  #sys.setdefaultencoding("ISO-8859-1")
    #------------------------------------------------------------------------------------
    try: datadir
    except NameError: datadir = "../data/current/"
    else: pass
    try: plotDIR
    except NameError: plotDIR = "../plot/current/"
    else: pass
    reflectplotDIR = plotDIR + "reflect/"
    ML_PATH = "tools/ML/"
    #------------------------------------------------------------------------------------ CPU/GPU/TPU SETUP ------------->/v<--- ---------- ------- ------>------/  - - - - - |
    cpus = multiprocessing.cpu_count()
    print("CPU Count:",cpus)
    if(cpus>16):
        num_cores = 48 #48
        MaxEventLimit = False
        import matplotlib
        matplotlib.use('AGG')
    else:
        num_cores = cpus
        MaxEventLimit = False
        import matplotlib
        #matplotlib.use('AGG')
    #----------------------------
    import matplotlib.pyplot as plt
    import matplotlib.colors as mpt_col
    from matplotlib.colors import ListedColormap,LinearSegmentedColormap
    import matplotlib.cm as cm
    import matplotlib.markers as mk
    import matplotlib.ticker as mticker
    #------------------------------------------------------------------------------------ Event / Main SETUP ------------->^/<--- ---------- ------- ------>------/  - - - - - |
    MaxEventLimit = False #manual override
    MaxEvents = 50 #int(input("Number of Events:"))
    #--------------------------
    COMPLETEDETECTOR = True
    #--------------------------
    firstPhoton = 0
    try: photoLen
    except NameError: photoLen = 5
    else: pass
    # ------------------------------------------ RECONSTRUCTION SETUP ---->/=<--- ---------- ------- ------>------/  - - - - - |----------------------_|
    # - \---------------------------------
    Process_Based_Breakdown = False
    Strip_Based_Reconstruction = False #otherwise uses only endcount data
    SiPMTime_Based_Reconstruction = False
    SiPM_Based_Reconstruction = False #a binning method, massages data to use only binned SiPM counts #unrealistic!
    ML_DRES = True #(turn off SiPMTime_Based_Reconstruction)

    #--------------- --------- --------- -------- ML SETUP ------\\-->^/v<--- ---------- ------- ------>------/  - - - - - |
    DRES_Train = True #Train or Test/VIS?
    #---CNN
    warmstart=True # warmstart the CNN
    #---KNN
    KNN = True #using KNN OR CNN ? 
    MLOPT = [] #options "PCA" "STD" "MAHA" "DISABLE-ZT" (note MAHA,STD requires PCA)
    #options "RUNONE" "RUN" "OPTNUM" "ERR" "VIS" "False" "PICKLE" #nearest neighbor output visualization?
    try: KVIS
    except: KVIS = "PICKLE"

    knn_neighbors = 4 #set value

    #--------------- --------- --------- -------- TESTS ------------->^/v<--- ---------- ------- ------>------/  - - - - - |
    # Reflection Tests \---------------------------------
    ReflectionTest = False
    ReflectOPT = [] #options "DISABLE-VK"
    boundaryinteract = True
    Ropt = ""
    # SIPM TIMING Tests \---------------------------------
    # (number of photons to count in SiPM timing) (needs SiPMTime_Based_Reconstruction)
    SiPMtimeRES = False
    SiPMtimeVSatt = False
    SiPMtimePOSRES = False #multilateration style x,y,z positioning for visualization?.

    #--------------- --------- --------- -------- ADDITIONAL RESOLUTION PLOTS/HISTOGRAMS ------------->/=<--- ---------- ------- ------>------/  - - - - - |
    # Production/Detection Histograms \---------------------------------
    STRIPHIST = False
    #subdefines - needs striphist, Process_Based_Breakdown True and SiPM_Based_Reconstruction False
    STRIP_OPT = ["process_breakdown","electron_processes"] #options "process_breakdown" "photocompton_breakdown" "electron_processes" "subfigures" (#2 requires #1) (#3 - default is gamma_processes) (#4 ~requires #3)
    Creation = True
    Detection = True
    PD = False
    #------------------------------------------------------------------_|
    POSRES = False
    RES_ADD = False #additional resolution plots
    SIGRES = False #needs Strip_Based_Reconstruction
    SUBSTRIP = False #needs SiPM_Based_Reconstruction False
    SUBSTRIP_RECONSTRUCT = False #needs SiPM_Based_Reconstruction False
    #---------------
    TIMERES = False
    #------------------------------------------------------------------_|
    AnalyzeOptions = False