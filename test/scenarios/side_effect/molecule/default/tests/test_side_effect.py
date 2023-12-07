"""Testinfra tests."""

import os

import testinfra.utils.distronode_runner

testinfra_hosts = testinfra.utils.distronode_runner.DistronodeRunner(
    os.environ["MOLECULE_INVENTORY_FILE"],
).get_hosts("all")


def test_side_effect_removed_file(host):
    """Validate that file was removed."""
    assert not host.file("/tmp/testfile").exists
