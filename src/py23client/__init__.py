"""Jira Client Models and APIs"""
import sys
import warnings

if sys.version_info.major < 3:
    warnings.warn(
        (
            "DEPRECATION: Python 2.7 reached the end of its life on January 1st, 2020. "
            "Please upgrade to Python 3."
        ),
        UserWarning,
        stacklevel=2,
    )
    from importlib_metadata import version
    from py23client.v27 import _27client as client

else:
    from importlib.metadata import version
    from py23client.v310 import _310client as client # type: ignore[no-redef]


__version__ = version("py23client")
__all__ = ("client",)
