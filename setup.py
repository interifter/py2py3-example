"""Proceed with caution in this file.

IMPORTANT NOTE: NONE OF THIS IS REQUIRED FOR PYTHON 3.10+

IF YOU ARE LOOKING AT THIS, CONSIDER UPGRADING TO 3.10.

This file is written to support python2.7.
This means we don't get wonderful things like type hints, mypy, and pylint.

All of the ignores/disables in this file are due to the
VSCode python tooling targeting modern python versions.

If you make modifications to this file, you need to minimally run

```
(win-venv27) python setup.py develop
(win-venv27) pip uninstall py23client -y
(win-venv27) python setup.py build bdist_wheel -d dist sdist -d dist
(win-venv27) pip install py23client --find-links dist/
(win-venv310) poetry install
(nix-venv27) python setup.py develop
(nix-venv27) pip uninstall py23client -y
(nix-venv27) python setup.py build bdist_wheel -d dist sdist -d dist
(nix-venv27) pip install py23client --find-links dist/
(nix-venv310) poetry install
```

When you are planning to generate the dist/ files, order matters.

1. Run `poetry build` in py3.10+ first
2. Run `python setup.py build bdist_wheel -d dist sdist -d dist` for py2.7 after

This is because the generated tar.gz will target py3.10 unless we build for 2.7
We have some ugly Shim code to delete any existing tar.gz and replace it with 
    one generated in this file
"""

import os
import warnings
import sys
from setuptools import setup # type: ignore[import-untyped]
#pylint: disable=import-error, no-name-in-module
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel # type: ignore[import-not-found]


if sys.version_info.major > 2:
    # pylint: disable=raising-format-tuple, line-too-long
    raise SystemError("You are using sys.version_info=%s. This file is for python 2.7. Use 'poetry install' instead", sys.version_info)

warnings.warn(
    (
        "DEPRECATION: Python 2.7 reached the end of its life on January 1st, 2020. "
        "Please upgrade your Python as Python 2.7 is no longer maintained."
    ),
    UserWarning,
    stacklevel=2,
)

class Shim:
    """Shim class to ensure we're reading from the pyproject.toml"""

    def __init__(self, name, version, old_name, new_name):
        self.name = name
        self.version = version
        self.old_name = old_name
        self.new_name = new_name

    @classmethod
    def load_from_pyproject(cls, old_name, new_name):
        """Load from pyproject.toml"""
        
        # pylint: disable=unspecified-encoding
        with open(old_name, "r") as handle:
            lines = handle.readlines()
        name = ""
        version = ""

        for line in lines:
            if line.startswith("name"):
                name = line.split(" = ")[1].replace("\"", "").strip()
            elif line.startswith("version"):
                version = line.split(" = ")[1].replace("\"", "").strip()
        os.rename(old_name, new_name)
        return cls(name, version, old_name, new_name)

    @classmethod
    def load(cls):
        """Load metadata"""
        old_name = "pyproject.toml"
        new_name = "_pyproject.toml"
        print("Searching for " + old_name)
        if os.path.isfile(old_name):
            return cls.load_from_pyproject(old_name, new_name)

        name = ""
        version = ""
        # pylint: disable=unspecified-encoding
        with open("PKG-INFO", "r") as handle:
            lines = handle.readlines()
        for line in lines:
            if line.startswith("Name"):
                name = line.split(": ")[1].replace("\"", "").strip()
            elif line.startswith("Version"):
                version = line.split(": ")[1].replace("\"", "").strip()
        return cls(name, version, old_name, new_name)

    def clean(self):
        """Remove tar.gz"""
        name = "dist/" + self.name + "-" + self.version + ".tar.gz"
        print("Searching for " + name)
        if os.path.isfile(name):
            print("source archive exists. Deleting")
            os.unlink(name)
            self.clean()

    def restore(self):
        """Restore the pyproject.toml"""
        if os.path.isfile(self.new_name):
            os.rename(self.new_name, self.old_name)

class bdist_wheel(_bdist_wheel):
    """OS-specific magic"""
    def finalize_options(self):
        """Override"""
        _bdist_wheel.finalize_options(self)
        self.root_is_pure = False # pylint: disable=attribute-defined-outside-init

shim = Shim.load()
try:

    setup(
        python_requires="<3",
        name=shim.name,
        version=shim.version,
        install_requires=[
            'importlib-metadata',
        ],
        package_dir={"": "src"},
        classifiers = [
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.7",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
        keywords = ["python2"],
        options={
            "bdist_wheel": {
                "universal": False
            }
        },
        cmdclass={"bdist_wheel": bdist_wheel},
        extras_require={}
    )
finally:
    shim.restore()
