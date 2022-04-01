from testing.utils import get_resource_path
import os
import os.path as op
import shutil
import tempfile
import filecmp
import logging

import pytest
import difflib

from decouple import config

from prose_pre_commit_hooks.check_jupyter_notebook_cells_ran_in_a_row import (
    get_exit_status,
)

log_level = config('LOG_LEVEL', default='DEBUG')
logging.basicConfig(level=log_level)


@pytest.mark.parametrize(
    ("filename", "expected_status_code"),
    (
        ("bad_notebook.ipynb", 1),
        ("good_notebook.ipynb", 0),
        ("broken_notebook.ipynb", 1),
    ),
)
def test_get_exit_status(filename, expected_status_code):
    f_path = get_resource_path(filename)
    ret = get_exit_status([f_path])
    assert ret == expected_status_code
