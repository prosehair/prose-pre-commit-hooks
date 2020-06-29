from testing.utils import get_resource_path
import os
import os.path as op
import shutil
import tempfile
import filecmp

import pytest
import difflib

from prose_pre_commit_hooks.manage_airflow_dag_task_id import main


def create_temporary_copy(path):
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, op.basename(path))
    shutil.copy2(path, temp_path)
    return temp_path


@pytest.mark.parametrize(
    ("filename", "expected_retval"),
    (
        ("dag_ok-v0.0.1.py", 0),
        ("dag_ko_correct_task_dag_id-v0.0.2.py", 1),
        ("dag_ko_wrong_case_version-V0.0.1.py", 1),
    ),
)
def test_main(filename, expected_retval):
    f_path = get_resource_path(filename)
    tmp_file = create_temporary_copy(f_path)
    ret = main([tmp_file])
    assert ret == expected_retval

    comp_file = get_resource_path(f"{op.basename(filename)}.ref")

    if op.exists(comp_file):
        assert filecmp.cmp(tmp_file, comp_file)


@pytest.mark.parametrize(
    ("filename", "expected_retval"),
    (("dag_ok-v0.0.1.py", 0), ("dag_ko_correct_task_dag_id-v0.0.2.py", 1),),
)
def test_dry_run(filename, expected_retval):
    f_path = get_resource_path(filename)
    tmp_file = create_temporary_copy(f_path)
    ret = main([tmp_file, "--dry-run"])
    assert ret == expected_retval
    assert filecmp.cmp(tmp_file, f_path)


@pytest.mark.parametrize(
    ("filename", "expected_retval"),
    (("dag_ok-v0.0.1.py", 0), ("dag_ko_correct_task_dag_id-v0.0.2.py", 1),),
)
def test_no_inplace(filename, expected_retval):
    f_path = get_resource_path(filename)
    tmp_file = create_temporary_copy(f_path)
    ret = main([tmp_file, "--no-inplace"])

    comp_file = get_resource_path(f"{op.basename(filename)}.ref")
    tmp_file_lintres = f"{op.splitext(tmp_file)[0]}.lintres"

    assert ret == expected_retval
    if op.exists(comp_file):
        assert filecmp.cmp(tmp_file_lintres, comp_file)
