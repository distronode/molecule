"""Testinfra tests."""


def test_distronode_hostname(host):
    """Validate hostname."""
    f = host.file("/tmp/molecule/instance-1")
    assert not f.exists
