# Developer Contributing Guide <!-- omit from toc -->

## Contents <!-- omit from toc -->

- [Warning](#warning)
- [Install `python`](#install-python)
  - [Installing `python` on Windows](#installing-python-on-windows)
  - [Installing `python` on Debian (Ubuntu)](#installing-python-on-debian-ubuntu)
    - [1. Install `pyenv`](#1-install-pyenv)
    - [2. Install `python` with `pyenv`](#2-install-python-with-pyenv)
- [Development Setup](#development-setup)
  - [`python` 2.7 for Windows](#python-27-for-windows)
  - [`python` 3.10 for Windows](#python-310-for-windows)
  - [`python` 2.7 for Debian (Ubuntu)](#python-27-for-debian-ubuntu)
  - [`python` 3.10 for Debian (Ubuntu)](#python-310-for-debian-ubuntu)
- [Build](#build)
  - [Windows Package Build and Validation for `python` 3.10](#windows-package-build-and-validation-for-python-310)
  - [Windows Package Build and Validation for `python` 2.7](#windows-package-build-and-validation-for-python-27)
  - [Linux Package Build and Validation for `python` 3.10](#linux-package-build-and-validation-for-python-310)
  - [Linux Package Build and Validation for `python` 2.7](#linux-package-build-and-validation-for-python-27)
  - [Build across Linux and Windows for `python` 2.7 and 3.10](#build-across-linux-and-windows-for-python-27-and-310)
    - [Windows Build and Stash](#windows-build-and-stash)
    - [Debian Build and Stash](#debian-build-and-stash)
    - [Verify Windows](#verify-windows)
    - [Verify Debian](#verify-debian)


## Warning

This experimental repo is intended to show you how to contribute to both python3.10 and python2.7.

It is only for educational purposes. You should never do this. It's bad and silly.

If your company, or organization, still is supporting python2.7,
I am willing to bet you have an ROI in 48 months, or less,
by investing in migration to 3.10+

The tooling and support in 3.10+ is _amazing_. And 2.7 has been 100% EOLd since 2020.

Further, you should use the latest python. This example is for being stuck on 3.10.

## Install `python`

### Installing `python` on Windows

I recommend using `choco` for python installs.
For this repo, I recommend:

```powershell
# As admin
choco install python2 --version 2.7.18 -y
choco install python --version 3.10.11 -y
``` 

### Installing `python` on Debian (Ubuntu)

#### 1. Install `pyenv`

Follow this guide: https://medium.com/@aashari/easy-to-follow-guide-of-how-to-install-pyenv-on-ubuntu-a3730af8d7f0

#### 2. Install `python` with `pyenv`

```bash
pyenv install 2.7
pyenv install 3.10
```

## Development Setup

> We assume you're using `vscode` for this.
>
> If not, I recommend it.
>
> We assume you installed `python` using the methods above.
>
> You don't have to follow these naming conventions, but it is a good visual to understand what kind
> of environment you're in


### `python` 2.7 for Windows


```powershell
C:\python27\python -m virtualenv wvenv27
wvenv\Scripts\activate
python setup.py develop
# I noticed running the above step was failing, but it appears it successfully installs the client:
# error: Couldn't find a setup script in c:\users\zhaberma\appdata\local\temp\easy_install-m3rrqp\importlib_metadata-8.5.0.tar.gz
# And after running the below commands, then rerunning the above command, the error does not reappear

pip install pytest pytest-cov
pytest tests/py27
```

### `python` 3.10 for Windows

```powershell
C:\python310\python -m venv wvenv310
wvenv310/Scripts/activate
pip install poetry
poetry install
poetry run pytest
```

### `python` 2.7 for Debian (Ubuntu)

```bash
pyenv global 2.7.18
pyenv virtualenv nvenv27_py2py3-example
pyenv activate nvenv27_py2py3-example
pip install pytest pytest-cov
python setup.py develop
pytest tests/py27
```

### `python` 3.10 for Debian (Ubuntu)

```bash
pyenv global 3.10.16
pyenv virtualenv nvenv310_py2py3-example
pyenv activate nvenv310_py2py3-example
pip install poetry
poetry install
poetry run pytest
```

## Build

> Assumes you have gone through Development Setup

The build process is order-dependent.

That is, it does not pass the transitive property vibe check, yo.

Also, if you're here, a reminder: **Do not do this unless you like to throw away your time and money.**

### Windows Package Build and Validation for `python` 3.10

```powershell
wvenv310/Scripts/activate
pip uninstall py23client -y
poetry build
pip install py23client --find-links dist/
python -c "import py23client; print(py23client.__version__)"
# should output 0.1.0
```

### Windows Package Build and Validation for `python` 2.7

```powershell
wvenv27/Scripts/activate
pip uninstall py23client -y
python setup.py build bdist_wheel -d dist sdist -d dist
pip install py23client --find-links dist/
python -c "import py23client; print(py23client.__version__)"
# should output 0.1.0
```

### Linux Package Build and Validation for `python` 3.10

```bash
pyenv activate nvenv310_py2py3-example
pip uninstall py23client -y
poetry build
pip install py23client --find-links dist/
python -c "import py23client; print(py23client.__version__)"
# should output 0.1.0
```

### Linux Package Build and Validation for `python` 2.7

```powershell
pyenv activate nvenv27_py2py3-example
pip uninstall py23client -y
python setup.py build bdist_wheel -d dist sdist -d dist
pip install py23client --find-links dist/
python -c "import py23client; print(py23client.__version__)"
# should output 0.1.0
```

### Build across Linux and Windows for `python` 2.7 and 3.10

> This assumes you have two completely different workspaces

#### Windows Build and Stash

```powershell
wvenv310/Scripts/activate
poetry build
wvenv27/Scripts/activate
python setup.py build bdist_wheel -d dist sdist -d dist
copy dist\* C:\temp\py23client\
```

#### Debian Build and Stash

> We only build the python 2.7 wheel.
> Everything else should be the same between the two (hopefully)

```bash
pyenv activate nvenv27_py2py3-example
python setup.py build bdist_wheel -d dist
cp dist/* /mnt/c/Temp/py23client/
```

#### Verify Windows

```powershell
C:\Python27\python.exe -m virtualenv py27new
.\py27new\Scripts\activate
pip install py23client --find-links C:\Temp\py23client
# Should see 'Processing c:\temp\py23client\py23client-0.1.0-cp27-cp27m-win_amd64.whl' in the output
python -c "from py23client import client; print(client.__file__)"
# Should see something like:
#   -c:1: UserWarning: DEPRECATION: Python 2.7 reached the end of its life on January 1st, 2020. Please upgrade to Python 3.
#   C:\code\py2py3-example\py27new\lib\site-packages\py23client\v27\_27client.pyc
deactivate
C:\Python310\python.exe -m venv py310new
.\py310new\Scripts\activate
pip install py23client --find-links C:\Temp\py23client
# Should see 'Processing c:\temp\py23client\py23client-0.1.0-py3-none-any.whl' in the output
python -c "from py23client import client; print(client.__file__)"
# Should see seomthing like 'C:\code\py2py3-example\py310new\lib\site-packages\py23client\v310\_310client.py'
```

#### Verify Debian

```bash
pyenv global 2.7.18
pyenv virtualenv nvenv27_py2py3-new
pyenv activate nvenv27_py2py3-new
pip install py23client --find-links /mnt/c/Temp/py23client/
# Should see 'Processing /mnt/c/Temp/py23client/py23client-0.1.0-cp27-cp27mu-linux_x86_64.whl' in the output
python -c "from py23client import client; print(client.__file__)"
# Should see something like:
#   -c:1: UserWarning: DEPRECATION: Python 2.7 reached the end of its life on January 1st, 2020. Please upgrade to Python 3.
#   /home/zachary/.pyenv/versions/nvenv27_py2py3-new/lib/python2.7/site-packages/py23client/v27/_27client.pyc
pyenv deactivate
pyenv global 3.10.16
pyenv virtualenv nvenv310_py2py3-new
pyenv activate nvenv310_py2py3-new
pip install py23client --find-links /mnt/c/Temp/py23client/
# Should see 'Processing /mnt/c/Temp/py23client/py23client-0.1.0-py3-none-any.whl' in the output
python -c "from py23client import client; print(client.__file__)"
# Should see something like '/home/zachary/.pyenv/versions/nvenv310_py2py3-new/lib/python3.10/site-packages/py23client/v310/_310client.py'
```
