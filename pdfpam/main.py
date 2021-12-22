import subprocess
import shlex
import sys
from tempfile import NamedTemporaryFile as NTF
from pathlib import Path
from typing import Dict
import click


def abort(message: str, code: int = 1):
    print(message, file=sys.stderr)
    exit(code)


def get_file_range_map(files: str, directory: str) -> Dict[str, str]:
    dir_p = Path(directory)
    if not dir_p.exists():
        raise Exception(f"directory: {directory} does not exist")

    with open(files, "r") as f:
        frange = f.readlines()

    files_and_ranges = {}

    for f in frange:
        fno, page_range = f.split(":")
        page_range = page_range.strip()
        globbed = list(dir_p.glob(f"{fno}-*.pdf"))
        if len(globbed) != 1:
            raise Exception(f"expected 1 file starting with {fno}, got {len(globbed)}")
        thefile = globbed[0]
        files_and_ranges[thefile] = page_range
    return files_and_ranges


@click.command()
@click.argument("config", type=click.Path(exists=True))
@click.argument(
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True),
)
@click.argument("output", type=click.Path(exists=False))
def main(config, directory, output):
    """Pick n' Mix to select and combine pages from multiple PDFs into one"""
    try:
        fr = get_file_range_map(config, directory)
    except Exception as e:
        abort(e)

    out = Path(output)
    if out.exists():
        abort(f"warning: {out} already exists. Aborting to prevent overwriting data")

    tmp1 = NTF(suffix=".pdf")
    tmp2 = NTF(suffix=".pdf")

    for idx, (file, page_range) in enumerate(fr.items()):
        # extract the requested pages from the pdf and store either in
        # tmp file or output depending if first run
        subprocess.run(
            shlex.split(
                f"pdftk {file} cat {page_range} output {tmp1.name if out.exists() else out}"  # noqa
            )
        )
        if idx == 0:
            continue
        # combine previous extracted and new into one
        subprocess.run(shlex.split(f"cp {out} {tmp2.name}"))
        subprocess.run(shlex.split(f"pdftk {tmp2.name} {tmp1.name} cat output {out}"))

    tmp1.close()
    tmp2.close()


if __name__ == "__main__":
    main()
