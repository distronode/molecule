"""Testinfra tests."""

import os

import testinfra.utils.distronode_runner

testinfra_hosts = testinfra.utils.distronode_runner.DistronodeRunner(
    os.environ["MOLECULE_INVENTORY_FILE"],
).get_hosts("all")


def test_distronode_hostname(host):
    """Validate hostname."""
    f = host.file("/tmp/molecule/instance-1")

    assert not f.exists
