import pytest

from prose_pre_commit_hooks.utils import cmd_output


@pytest.fixture
def temp_git_dir(tmpdir):
    git_dir = tmpdir.join("gits")
    cmd_output("git", "init", "--", str(git_dir))
    yield git_dir
