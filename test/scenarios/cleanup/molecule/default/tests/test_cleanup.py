"""Testinfra tests."""

import os

import testinfra.utils.distronode_runner

testinfra_hosts = testinfra.utils.distronode_runner.DistronodeRunner(
    os.environ["MOLECULE_INVENTORY_FILE"],
).get_hosts("all")


def test_hosts_file(host):
    """Validate host file."""
    f = host.file("/etc/hosts")

    assert f.exists
    assert f.user == "root"
    assert f.group == "root"
