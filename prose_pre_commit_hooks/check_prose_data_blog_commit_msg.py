import re
import sys

examples = """+ 61c8ca9 blog: shampoo satisfaction analysis [sc-1234]
+ b818120 feat: add overall satisfaction per segment [ch1234]
+ b818120 feat(capucine): add overall satisfaction per segment [ch1234]
+ d65ayu3 review: according to camille feedback [ch1234]
+ c6e9a97 fix: report date range [ch1234]
"""


ALLOWED_PREFIX = (
    'blog',
    'build',
    'data',
    'docs',
    'feat',
    'fix',
    'perf',
    'refactor',
    'style',
    'test',
    'chore',
    'revert',
    'review',
)


def _validate_commit_msg(msg: str) -> int:
    # example:
    # feat(apikey): added the ability to add api key to configuration
    pattern = rf'({"|".join(ALLOWED_PREFIX)})(\([\w\-]+\))?:\s.*'
    m = re.match(pattern, msg)
    if not m:
        print('\nCOMMIT FAILED!')
        print(
            f'\nPrefix must be specified, and found among: {", ".join(ALLOWED_PREFIX)}.'
        )
        print(
            "\nPlease enter commit message in the conventional format and try to commit again. Examples:"
        )
        print("\n" + examples)
        return 1

    # raise Exception if missing clubhouse ticket number
    pattern = r'(blog|data|feat|fix|review)(\([\w\-]+\))?:\s.*'
    m = re.match(pattern, msg)
    if not m:
        return 0

    m = re.match(rf'{pattern}\s\[(ch|sc\-)\d+\]', msg)
    if not m:
        print("\nCOMMIT FAILED!")
        print(
            "\nPlease enter the clubhouse ticket for blog, feat, fix, review prefixes."
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
