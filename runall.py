import pathlib
import sys
import time


if __name__ == "__main__":
    rootdir = pathlib.Path(__file__).parent
    for yeardir in sorted(rootdir.glob("2*")):
        sys.path.append(str(yeardir))
        inputdir = yeardir / "input"
        for inputfile in sorted(inputdir.glob("*")):
            for pythonfile in sorted(yeardir.glob(f"{inputfile.name}*.py")):
                print(f"{pythonfile}: ")
                sys.argv[0] = str(pythonfile)
                execstart = time.time()
                exec(pythonfile.read_text())
                exectime = time.time() - execstart
                print(f"({exectime:.3f} s)")
        # Pop path and modules loaded from it to avoid clashes with next year
        path = sys.path.pop()
        for name, m in sys.modules.copy().items():
            if hasattr(m, "__file__") and m.__file__.startswith(path):
                sys.modules.pop(name)
