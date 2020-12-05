import pathlib
import sys
import time


if __name__ == "__main__":
    rootdir = pathlib.Path(__file__).parent
    inputdir = rootdir / "input"
    for inputfile in sorted(inputdir.glob("*")):
        for pythonfile in sorted(rootdir.glob(f"{inputfile.name}*.py")):
            with open(inputfile, "r") as fh:
                print(f"{pythonfile}: ", end="")
                sys.stdout.flush()
                sys.stdin = fh
                execstart = time.time()
                exec(pythonfile.read_text())
                exectime = time.time() - execstart
                print(f"    ({exectime:.3f} s)")
