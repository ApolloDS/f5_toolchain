#!/usr/bin/env python
import os
from setuptools import setup, find_packages
from f5_toolchain.main import __version__

with open('README.md') as readme_file:
    readme = readme_file.read()

def _get_requirements(requirements_file):
  """Returns a list of dependencies for setup() from requirements.txt.
  Currently a requirements.txt is being used to specify dependencies. In order
  to avoid specifying it in two places, we're going to use that file as the
  source of truth.
  """
  with open(requirements_file) as f:
    return [_parse_line(line) for line in f if line]


def _parse_line(s):
  """Parses a line of a requirements.txt file."""
  requirement, *_ = s.split("#")
  return requirement.strip()

# Get the requirements from file.
req_file = ""
if os.path.exists("requirements.txt"):
  req_file = "requirements.txt"

setup(
    name='f5-toolchain',
    version=__version__,
    description="F5 automation toolchain CLI tool",
    long_description=readme,
    author="Peter Baumann",
    author_email='petbau@linuxnet.ch',
    url='',
    packages=find_packages(include=['f5_toolchain']),
    entry_points={
        'console_scripts': [
            'f5-toolchain=f5_toolchain.main:main'
        ]
    },
    include_package_data=True,
    install_requires=_get_requirements(req_file),
    setup_requires=['wheel'],
    zip_safe=False,
    keywords='f5-toolchain',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.9',
    ]
)
