import re
import sys

examples = """+ 61c8ca9 fix: navbar not responsive on mobile
+ 479c48b test: prepared test cases for user authentication
+ a992020 chore: moved to semantic versioning
+ b818120 fix: button click even handler firing twice
+ c6e9a97 fix: login page css
+ dfdc715 feat(auth): added social login using twitter
"""

ALLOWED_PREFIX = (
    'build',
    'ci',
    'docs',
    'feat',
    'fix',
    'perf',
    'refactor',
    'style',
    'test',
    'chore',
    'revert',
)


def _validate_commit_msg(msg: str) -> int:
    # example:
    # feat(apikey): added the ability to add api key to configuration
    pattern = rf'({"|".join(ALLOWED_PREFIX)})(\([\w\-]+\))?:\s.*'
    filename = sys.argv[1]
    ss = open(filename, 'r').read()
    m = re.match(pattern, ss)
    if not m:
        print("\nCOMMIT FAILED!")
        print(
            f'\nPrefix must be specified, and found among: {", ".join(ALLOWED_PREFIX)}.'
        )
        print(
            "\nPlease enter commit message in the conventional format and try to commit again. Examples:"
        )
        print("\n" + examples)
        return 1

    return 0


def main() -> int:
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        return _validate_commit_msg(f.read())


if __name__ == "__main__":
    sys.exit(main())
