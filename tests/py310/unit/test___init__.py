"""Test py23client __init__.py"""
import py23client

def test___version__() -> None:
    """Test the version"""
    assert py23client.__version__

def test_client() -> None:
    """Test the client is from v310"""
    client = py23client.client
    assert client.__name__ == "py23client.v310._310client"
