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
python -m virtualenv nvenv27
source ~/.pyenv/versions/nvenv27/bin/activate
python setup.py develop
pip install pytest pytest-cov
pytest tests/py27
```

### `python` 3.10 for Debian (Ubuntu)

```bash
pyenv global 3.10.16
python -m venv nvenv310
source ~/.pyenv/versions/nvenv310/bin/activate
pip install poetry
poetry install
poetry run pytest
```