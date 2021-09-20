import pytest
from prose_pre_commit_hooks.check_prose_data_blog_commit_msg import _validate_commit_msg


PREFIX_NEED_CH_SC = ('blog', 'feat', 'fix', 'review')
PREFIX = ('build', 'docs', 'perf', 'refactor', 'style', 'test', 'chore', 'revert')


@pytest.mark.parametrize("prefix", PREFIX_NEED_CH_SC + PREFIX)
def test_ok(prefix):
    msg = f'{prefix}: add xxxx [ch0000]'
    retv = _validate_commit_msg(msg)
    assert retv == 0

    msg = f'{prefix}: add xxxx [sc-0000]'
    retv = _validate_commit_msg(msg)
    assert retv == 0


@pytest.mark.parametrize("prefix", PREFIX)
def test_missing_ch_sc_ok(prefix):
    msg = f'{prefix}: add xxxx'
    retv = _validate_commit_msg(msg)
    assert retv == 0


@pytest.mark.parametrize("prefix", PREFIX_NEED_CH_SC)
def test_missing_ch_sc_ko(prefix):
    msg = f'{prefix}: add xxxx'
    retv = _validate_commit_msg(msg)
    assert retv == 1


def test_wrong_prefix():
    msg = 'abc: wjdkwjedj'
    retv = _validate_commit_msg(msg)
    assert retv == 1
