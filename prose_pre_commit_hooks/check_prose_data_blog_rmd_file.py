import argparse
import os.path as op
import re
from typing import Optional, Sequence

REGEX_BLOG_REPORT = r"^([2]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))-ch\d+-.*\.Rmd$"


def _validate_filename(fname: str) -> int:
    rmd_filename = op.basename(fname)

    m = re.match(REGEX_BLOG_REPORT, rmd_filename)
    if not m:
        print(  # noqa T001
            f"'{rmd_filename}' doesnt not follow the pattern yyyy-mm-dd-chXXXX-Title.Rmd"
        )
        return 1

    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Filenames to fix")

    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        retv |= _validate_filename(filename)

    return retv


if __name__ == "__main__":
    exit(main())
