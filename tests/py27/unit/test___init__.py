"""Test py23client __init__.py"""
import py23client

def test___version__():
    # type: () -> None
    """Test the version"""
    assert py23client.__version__

def test_client():
    # type: () -> None
    """Test the client is from v27"""
    client = py23client.client
    assert client.__name__ == "py23client.v27._27client"