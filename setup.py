# -*- coding: utf-8 -*-

import os
import sys

from setuptools import find_packages, setup
from setuptools.command.install import install

import versioneer

cmdclass = versioneer.get_cmdclass()

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()  # noqa A001

with open('requirements.in') as f:
    requirements = f.read().splitlines()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""

    description = 'verify that the git tag matches our version'

    def run(self):
        _version = versioneer.get_version()
        tag = os.getenv('CIRCLE_TAG')
        if not tag:
            sys.exit(0)
        if tag != _version:
            info = f'Git tag: {tag} does not match the version of this app: {_version}'
            sys.exit(info)


cmdclass['verify'] = VerifyVersionCommand


setup(
    name='prose-pre_commit_hooks',
    version=versioneer.get_version(),
    description='Implement custom prose pre-commit hooks',
    long_description=readme,
    author='Morgan Durand',
    author_email='morgan.durand@prosehair.com',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=requirements,
    cmdclass=cmdclass,
    entry_points={
        'console_scripts': [
            'manage-airflow-dag-task-id = prose_pre_commit_hooks.manage_airflow_dag_task_id:main',
            'add-clubhouse-ticket = prose_pre_commit_hooks.add_clubhouse_ticket_num:main',
            'check-commit-msg = prose_pre_commit_hooks.check_commit_msg:main',
            'check-prose-data-blog-rmd-file-pattern = prose_pre_commit_hooks.check_prose_data_blog_rmd_file:main',
            'check-prose-data-blog-commit-msg = prose_pre_commit_hooks.check_prose_data_blog_commit_msg:main',
        ],
    },
)
