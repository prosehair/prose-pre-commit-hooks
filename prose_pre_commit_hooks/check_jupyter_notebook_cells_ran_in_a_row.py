import argparse
import json
from typing import Optional, Sequence


def _check_code_cell_executed(notebook_path: str):
    print(f"Checking {notebook_path}")
    with open(notebook_path) as f:
        json_nb = json.load(f)

    try:
        is_ok = _check_nb_dict(json_nb)
    except KeyError:
        print(f"The file {notebook_path} does not seems to be a jupyter notebook")
        print('ok')
        return 1
    if is_ok:
        return 0
    else:
        print(f"The notebook {notebook_path} code cells were not executed in sequence")
        return 1


def _check_nb_dict(nb_dict):
    execution_count = 1
    for cell in nb_dict['cells']:
        if cell['cell_type'] == 'code':
            if cell['execution_count'] == execution_count:
                execution_count += 1
            elif cell['execution_count'] is None:
                pass
            else:
                print(
                    f"code cell no {execution_count-1} is followed by code cell no {cell['execution_count']}"
                )
                return False
    return True


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Filenames to fix")

    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        retv |= _check_code_cell_executed(filename)

    return retv


if __name__ == "__main__":
    exit(main())
