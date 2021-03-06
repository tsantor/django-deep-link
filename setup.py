#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from django_deep_link/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


version = get_version("django_deep_link", "__init__.py")

readme = open("README.md").read()
history = open("HISTORY.md").read()
requirements = open("requirements.txt").readlines()

setup(
    name="django-deep-link",
    version=version,
    description="""Your project description goes here""",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    author="Tim Santor",
    author_email="tsantor@xstudios.com",
    url="https://github.com/tsantor/django-deep-link",
    packages=[
        "django_deep_link",
    ],
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords="django-deep-link",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django :: 2.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
