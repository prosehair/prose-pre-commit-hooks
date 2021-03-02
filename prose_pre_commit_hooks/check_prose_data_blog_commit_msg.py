import re
import sys

examples = """+ 61c8ca9 blog: shampoo satisfaction analysis [ch1234]
+ b818120 feat: add overall satisfaction per segment [ch1234]
+ b818120 feat(capucine): add overall satisfaction per segment [ch1234]
+ d65ayu3 review: according to camille feedback [ch1234]
+ c6e9a97 fix: report date range [ch1234]
"""


def _validate_commit_msg(msg: str) -> int:
    # example:
    # feat(apikey): added the ability to add api key to configuration
    pattern = r'(blog|build|docs|feat|fix|perf|refactor|style|test|chore|revert|review)(\([\w\-]+\))?:\s.*'
    m = re.match(pattern, msg)
    if not m:
        print("\nCOMMIT FAILED!")
        print(
            "\nPlease enter commit message in the conventional format and try to commit again. Examples:"
        )
        print("\n" + examples)
        return 1

    pattern = r'(blog|feat|fix|review)(\([\w\-]+\))?:\s.*'
    m = re.match(pattern, msg)
    if not m:
        return 0

    # raise Exception if missing clubhouse ticket number
    m = re.match(rf'{pattern}\s\[ch\d+\]', msg)
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
