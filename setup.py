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
from setuptools import setup, find_packages # type: ignore[import-untyped]
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

    def __init__(self, name, version, url, author, author_email, old_name, new_name):
        self.name = name
        self.version = version
        self.old_name = old_name
        self.new_name = new_name
        self.url = url
        self.author = author
        self.author_email = author_email

    @classmethod
    def load_from_pyproject(cls, old_name, new_name):
        """Load from pyproject.toml"""
        
        # pylint: disable=unspecified-encoding
        with open(old_name, "r") as handle:
            lines = handle.readlines()
        name = ""
        version = ""
        url = ""
        author = ""
        author_email = ""

        for line in lines:
            if line.startswith("name"):
                name = line.split(" = ")[1].replace("\"", "").strip()
            elif line.startswith("version"):
                version = line.split(" = ")[1].replace("\"", "").strip()
            elif line.startswith("authors"):
                author = "hardcoded"
                author_email = "hardcoded@email.com"
        os.rename(old_name, new_name)
        return cls(name, version, url, author, author_email, old_name, new_name)

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
        url = ""
        author = "hardcoded"
        author_email = "hardcoded@email.com"

        # pylint: disable=unspecified-encoding
        with open("PKG-INFO", "r") as handle:
            lines = handle.readlines()
        for line in lines:
            if line.startswith("Name"):
                name = line.split(": ")[1].replace("\"", "").strip()
            elif line.startswith("Version"):
                version = line.split(": ")[1].replace("\"", "").strip()
        return cls(name, version, url, author, author_email, old_name, new_name)

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

root_dir = os.path.abspath(os.path.join(__file__, os.pardir))
root_src_dir = os.path.join(root_dir, "src", "py23client")

# Because we are customizing so many things, we are having a hard time
#   using the built-in functions provided with setuptools
# So, we created our own bespoke find_packages
# If you have a better way to do this (like deleting this), please create a PR
def find_my_packages(base_pkg_name = "", root = ""):
    """Finds the packages we care about"""
    packages = []
    for file_name in os.listdir(root):
        
        path = os.path.join(root, file_name)
        print("Searching " + path)
        if os.path.isfile(path) and path.endswith("__init__.py"):
            print("Found file: " + path)
            parent = os.path.dirname(path)
            package_name = os.path.basename(parent)
            full_package_name = ""
            if not base_pkg_name:
                full_package_name = package_name
            else:
                full_package_name = base_pkg_name + "." + package_name
            packages.append(full_package_name)
            base_pkg_name = full_package_name
            break

    for file_name in os.listdir(root):
        path = os.path.join(root, file_name)
        print("Searching " + path)
        if os.path.isdir(path):
            
            packages.extend(find_my_packages(base_pkg_name=base_pkg_name, root=path))
    return packages
    # TODO: properly build out package names
# print(find_my_packages(root=root_src_dir))
# sys.exit()

shim = Shim.load()
try:

    setup(
        python_requires="<3",
        name=shim.name,
        version=shim.version,
        author=shim.author,
        author_email=shim.author_email,
        url=shim.url,
        install_requires=[
            'importlib-metadata',
        ],
        package_dir={"": "src"},
        packages=find_my_packages(root=root_src_dir),
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
