import subprocess
import shlex
import sys
from tempfile import NamedTemporaryFile as NTF
from pathlib import Path


def get_file_range_dispatch(files, directory):
    dir_p = Path(directory)
    if not dir_p.exists():
        raise Exception(f"directory: {directory} does not exist")

    with open(files, "r") as f:
        frange = f.readlines()

    frd = {}

    for f in frange:
        fno, page_range = f.split(":")
        page_range = page_range.strip()
        globbed = list(dir_p.glob(f"{fno}-*.pdf"))
        if len(globbed) != 1:
            raise Exception(f"expected 1 file starting with {fno}, got {len(globbed)}")
        thefile = globbed[0]
        frd[thefile] = page_range
    return frd


def main():
    args = sys.argv[1:]
    if len(args) < 3:
        print("usage: pdfpam input directory output", file=sys.stderr)
        exit(1)
    file, dirr, output = args[0], args[1], args[2]

    try:
        frd = get_file_range_dispatch(file, dirr)
    except Exception as e:
        print(e, file=sys.stderr)
        exit(1)

    out = Path(output)
    if out.exists():
        print(
            f"warning: {out} already exists. Aborting to prevent overwriting data",
            file=sys.stderr,
        )
        exit(1)

    tmp1 = NTF(suffix=".pdf")
    tmp2 = NTF(suffix=".pdf")

    for file, page_range in frd.items():
        if not out.exists():  # first run
            subprocess.run(shlex.split(f"pdftk {file} cat {page_range} output {out}"))
        else:
            subprocess.run(
                shlex.split(f"pdftk {file} cat {page_range} output {tmp1.name}")
            )
            subprocess.run(shlex.split(f"cp {out} {tmp2.name}"))
            subprocess.run(
                shlex.split(f"pdftk {tmp2.name} {tmp1.name} cat output {out}")
            )
    tmp1.close()
    tmp2.close()


if __name__ == "__main__":
    main()
