# SYSTEM LIBRARY IMPORT/INSTALLS
import io,os,sys,subprocess
# path to python.exe
python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')
    
# upgrade pip
subprocess.call([python_exe, "-m", "ensurepip"])
subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])


installs = ["math","matplotlib","scipy","tqdm","numba","torch","multiprocessing","importlib"]
for installitem in installs:
    try: exec("import "+installitem)
    except:
        # install required packages
        subprocess.call([python_exe, "-m", "pip", "install", installitem])
        print("DONE")
    else:
        print("Already installed package: ",installitem)