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

from prose_pre_commit_hooks.check_jupyter_notebook_cells_ran_in_a_row import main

log_level = config('LOG_LEVEL', default='DEBUG')
logging.basicConfig(level=log_level)


@pytest.mark.parametrize(
    ("filename", "expected_retval"),
    (
        ("bad_notebook.ipynb", 0),
        ("good_notebook.ipynb", 1),
        ("broken_notebook.ipynb", 0),
    ),
)
def test_main(filename, expected_retval):
    f_path = get_resource_path(filename)
    ret = main([f_path])
    assert ret == expected_retval
