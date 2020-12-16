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
                with open(inputfile, "r") as fh:
                    print(f"{pythonfile}: ", end="")
                    sys.stdout.flush()
                    sys.stdin = fh
                    execstart = time.time()
                    exec(pythonfile.read_text())
                    exectime = time.time() - execstart
                    print(f"    ({exectime:.3f} s)")
        sys.path.pop()
