# Minimal Example on Multi-Versioned Python Package Management

This is a minimal (and currently incomplete) example on how to develop, build, package, and test a project that _requires_ python 2.7 support.

This specifically attempts to adopt modern tools from python 3.10, and bolt on 2.7 support.

If you are in this situation, I do not envy you.

## Type Checking Python 2.7

https://github.com/python/mypy/blob/4687cec37a2a28e477e0fcf7eb95d2701bea55eb/docs/source/python2.rst

## Building

### Python2.7 Windows

```powershell
python2 -m virtualenv wvenv27
wvenv27/Scripts/activate
python setup.py develop
# I noticed running the above step was failing, but it appears it successfully installs the client:
# error: Couldn't find a setup script in c:\users\zhaberma\appdata\local\temp\easy_install-m3rrqp\importlib_metadata-8.5.0.tar.gz
# And after running the below commands, the error does not reappear

pip install pytest pytest-cov
pytest tests/py27
```

### Python2.7 Ubuntu (Debian)

> !!!! :caution: This is currently broken
>
> Likely a problem with setup.py and packages/find_packages()

Follow this first: https://medium.com/@aashari/easy-to-follow-guide-of-how-to-install-pyenv-on-ubuntu-a3730af8d7f0

```bash
pyenv install 2.7
pyenv global 2.7.18
python -m virtualenv nvenv27
source ~/.pyenv/versions/nvenv27/bin/activate
python setup.py develop
pip install pytest pytest-cov
pytest tests/py27
```

### Python 3.10 (Windows or Linux)

```bash
python -m venv venv
venv/Scripts/activate # windows
source venv/bin/activate # linux
pip install poetry
poetry install
pytest tests/py310
```
