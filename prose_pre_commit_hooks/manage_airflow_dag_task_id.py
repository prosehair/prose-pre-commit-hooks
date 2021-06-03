import argparse
import os
import os.path as op
import re
from typing import List, Optional, Sequence

REGEX_SEMVER_V = r"(v([0-9]+)\.([0-9]+)\.([0-9]+)(?:-([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?)(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?"


def _validate_filename(fname: str) -> int:
    dag_id_fn = op.splitext(op.basename(fname))[0]

    m = re.match(rf"(.*){REGEX_SEMVER_V}", dag_id_fn)
    if not m:
        print(f"'{dag_id_fn}' doesnt not contain a properly formatted version.")
        return 1

    return 0


def _update_dag_file(fname: str, fcontent: list, do_correct: bool, inplace: bool):
    if not do_correct:
        return

    if inplace:
        out_name = fname
    else:
        f_dir = op.dirname(fname)
        out_name = f"{op.join(f_dir, op.splitext(op.basename(fname))[0])}.lintres"

    with open(out_name, "w") as f:
        for line in fcontent:
            f.write(line)


def _update_dag_id(fname: str, fcontent: List[str]) -> int:
    dag_id_fn = op.splitext(op.basename(fname))[0]
    retv = 0

    r = re.compile(r"(.*dag_id\s*\=\s*)(?:\'|\")(.*)(?:\'|\")(.*)")

    out = []

    for line in fcontent:
        m = r.match(line)
        if not m:
            out.append(line)
            continue

        line_prefix = m.group(1)
        dag_id = m.group(2)
        line_suffix = m.group(3)

        # Extract function argument name (avoiding confusion between task_id & external_task_id)
        argument_name_reg = re.compile(r"[^_]+dag_id\s*\=")
        argument_name = argument_name_reg.findall(line_prefix)
        if not argument_name:
            out.append(line)
            continue

        if dag_id != dag_id_fn:
            retv = 1
            print(
                f"Mismatch between dag_id from filename and from DAG definition\n => Updating to {dag_id_fn}"
            )
            line = f"{line_prefix}'{dag_id_fn}'{line_suffix}{os.linesep}"
        out.append(line)

    return retv, out


def _update_task_id(fname: str, fcontent: List[str]) -> int:
    dag_id = op.splitext(op.basename(fname))[0]

    retv = 0

    # Extract version fom dag_id
    m = re.match(rf"(.*){REGEX_SEMVER_V}", dag_id)
    version = m.group(2)

    r = re.compile(r"^(.*task_id\s*\=\s*)(?:\'|\")(.*)(?:\'|\")\s*(\,)?(.*)")

    out = []
    for line in fcontent:
        m = r.match(line)
        if not m:
            out.append(line)
            continue

        line_prefix = m.group(1)
        task_id = m.group(2)
        line_suffix = ''.join([m.group(i) for i in range(3, 5) if m.group(i)])

        # Extract function argument name (avoiding confusion between task_id & external_task_id)
        argument_name_reg = re.compile(r"[^_]+task_id\s*\=")
        argument_name = argument_name_reg.findall(line_prefix)
        if not argument_name:
            out.append(line)
            continue

        # detect version in task_id
        m = re.match(rf"(.*)-{REGEX_SEMVER_V}", task_id)

        if not m:
            retv = 1
            task_id_updated = f"'{task_id}-{version}'"
            print(
                f"Version not detected for {task_id}. \n  => Updating to {task_id_updated}"
            )
            line = f"{line_prefix}{task_id_updated}{line_suffix}{os.linesep}"
            out.append(line)
            continue

        task_id_base = m.group(1)
        task_id_version = m.group(2)

        if task_id_version != version:
            retv = 1
            task_id_updated = f"'{task_id_base}-{version}'"
            print(
                f"Version mismatch for {task_id}. \n  => Updating to {task_id_updated} (from {line_prefix})"
            )
            line = f"{line_prefix}{task_id_updated}{line_suffix}{os.linesep}"
            out.append(line)
            continue

        out.append(line)

    return retv, out


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Filenames to fix")
    parser.add_argument("--dry-run", help="do not modify files", action="store_true")
    parser.add_argument(
        "--no-inplace",
        help="create a new file instead of inplace modification (*.lintres)",
        action="store_true",
    )
    args = parser.parse_args(argv)

    if args.dry_run:
        do_correct = False
    else:
        do_correct = True

    if args.no_inplace:
        inplace = False
    else:
        inplace = True

    retv = 0

    for filename in args.filenames:
        retv_fname = _validate_filename(filename)
        valid_fname = bool(1 - retv_fname)
        retv |= retv_fname

        if not valid_fname:
            continue

        with open(filename) as f:
            fcontent = f.readlines()

        retv_tmp, fcontent = _update_dag_id(filename, fcontent)
        retv |= retv_tmp

        retv_tmp, fcontent = _update_task_id(filename, fcontent)
        retv |= retv_tmp

        _update_dag_file(
            fname=filename, fcontent=fcontent, do_correct=do_correct, inplace=inplace
        )

    return retv


if __name__ == "__main__":
    exit(main())
