import os
import re
import sys
from typing import List, Match, Optional, Pattern, Tuple

from git import Repo

REGEX_CLUBHOUSE_BRANCH = r'^(ch\d+)-(.*)$'
REGEX_CLUBHOUSE_COMMIT_MSG = r'^(.*)(\[ch\d+\])(.*)$'
REGEX_SHORTCUT_BRANCH = r'^(sc\-\d+)-(.*)$'
REGEX_SHORTCUT_COMMIT_MSG = r'^(.*)(\[sc-\d+\])(.*)$'

REGEX_CH_SC_BRANCH = (REGEX_SHORTCUT_BRANCH, REGEX_CLUBHOUSE_BRANCH)
REGEX_CH_SC_COMMIT_MSG = (REGEX_SHORTCUT_COMMIT_MSG, REGEX_CLUBHOUSE_COMMIT_MSG)


def _get_arg(i: int) -> Optional[str]:
    try:
        return sys.argv[i]
    except IndexError:
        return None


def _get_prepare_commit_msg_arg() -> Tuple[str]:
    return _get_arg(1), _get_arg(2), _get_arg(3)


def _match_multiple_regex(
    regex: List[Pattern[str]], string: str
) -> Optional[Match[str]]:
    m = [re.match(r, string) for r in regex]
    m = [e for e in m if e]
    if not m:
        return None
    return m[0]


def main() -> int:

    commit_msg_file, commit_source, commit_sha1 = _get_prepare_commit_msg_arg()

    if commit_source:
        print('Skip !')
        return 0

    repo = Repo(os.getcwd())
    try:
        branch = repo.active_branch.name
    except TypeError:
        print('Cannot get branch name.\n=> Skipping addition.')
        return 0

    if branch in ('master', 'main'):
        print(f'Do not commit on the {branch} branch')
        return 1

    m = _match_multiple_regex(regex=REGEX_CH_SC_BRANCH, string=branch)
    if not m:
        print(f'No clubhouse/shortcut ticket detected in {branch}')
        return 0

    ch_ticket = m.group(1)
    print(f'Clubhouse ticket {ch_ticket} detected.')

    with open(commit_msg_file) as f:
        lines = f.readlines()

    m = _match_multiple_regex(REGEX_CH_SC_COMMIT_MSG, lines[0])
    if m:
        print(
            'Shortcut / Clubhouse ticket(s) already in the commit message.\n=> Skip addition.'
        )
        return 0

    lines[0] = f'{lines[0].rstrip()} [{ch_ticket}]\n'

    with open(commit_msg_file, "w") as f:
        f.writelines(lines)
    print(f'=> New commit message: {lines[0].rstrip()}')

    return 0


if __name__ == "__main__":
    exit(main())
