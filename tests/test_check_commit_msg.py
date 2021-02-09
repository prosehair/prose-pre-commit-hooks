import pytest
from prose_pre_commit_hooks.check_prose_data_blog_commit_msg import _validate_commit_msg


PREFIX = (
    'blog',
    'feat',
    'fix',
    'review',
    'build',
    'docs',
    'perf',
    'refactor',
    'style',
    'test',
    'chore',
    'revert',
)


@pytest.mark.parametrize("prefix", PREFIX)
def test_ok(prefix):
    msg = f'{prefix}: add xxxx [ch0000]'
    retv = _validate_commit_msg(msg)
    assert retv == 0


def test_wrong_prefix():
    msg = 'abc: wjdkwjedj'
    retv = _validate_commit_msg(msg)
    assert retv == 1
