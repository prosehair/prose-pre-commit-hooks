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

from prose_pre_commit_hooks.check_prose_data_blog_rmd_file import main

log_level = config('LOG_LEVEL', default='DEBUG')
logging.basicConfig(level=log_level)


@pytest.mark.parametrize(
    ("filename", "expected_retval"),
    (
        ("content/blog/2021-01-01-ch000000-test-rmd_ok01.Rmd", 0),
        ("content/blog/2021-01-01-sc-000000-test-rmd_ok01.Rmd", 0),
        ("content/blog/2021-01-01-test-rmd_ok01.Rmd", 1),
    ),
)
def test_main(filename, expected_retval):
    f_path = get_resource_path(filename)
    ret = main([f_path])
    assert ret == expected_retval
