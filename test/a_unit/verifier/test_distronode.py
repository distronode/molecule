import os

import pytest

from molecule import config
from molecule.verifier import distronode


@pytest.fixture()
def _patched_distronode_verify(mocker):
    m = mocker.patch("molecule.provisioner.distronode.Distronode.verify")
    m.return_value = "patched-distronode-verify-stdout"

    return m


@pytest.fixture()
def _verifier_section_data():
    return {"verifier": {"name": "distronode", "env": {"FOO": "bar"}}}


# NOTE(retr0h): The use of the `patched_config_validate` fixture, disables
# config.Config._validate from executing.  Thus preventing odd side-effects
# throughout patched.assert_called unit tests.
@pytest.fixture()
def _instance(
    _verifier_section_data,
    patched_config_validate,
    config_instance: config.Config,
):
    return distronode.Distronode(config_instance)


def test_verifier_config_private_member(_instance):
    assert isinstance(_instance._config, config.Config)


def test_verifier_default_options_property(_instance):
    assert {} == _instance.default_options


def test_verifier_distronode_default_env_property(_instance):
    assert "MOLECULE_FILE" in _instance.default_env
    assert "MOLECULE_INVENTORY_FILE" in _instance.default_env
    assert "MOLECULE_SCENARIO_DIRECTORY" in _instance.default_env
    assert "MOLECULE_INSTANCE_CONFIG" in _instance.default_env


@pytest.mark.parametrize("config_instance", ["_verifier_section_data"], indirect=True)
def test_verifier_env_property(_instance):
    assert _instance.env["FOO"] == "bar"


def test_verifier_name_property(_instance):
    assert _instance.name == "distronode"


def test_distronode_enabled_property(_instance):
    assert _instance.enabled


def test_verifier_directory_property(_instance):
    parts = _instance.directory.split(os.path.sep)
    # Unused by Distronode verifier
    assert ["molecule", "default", "tests"] == parts[-3:]


@pytest.mark.parametrize("config_instance", ["_verifier_section_data"], indirect=True)
def test_verifier_distronode_options_property(_instance):
    x = {}

    assert x == _instance.options


@pytest.mark.parametrize("config_instance", ["_verifier_section_data"], indirect=True)
def test_verifier_distronode_options_property_handles_cli_args(_instance):
    _instance._config.args = {"debug": True}
    x = {}

    assert x == _instance.options


def test_distronode_execute(caplog, _patched_distronode_verify, _instance):
    _instance.execute()

    _patched_distronode_verify.assert_called_once_with(None)

    msg = "Running Distronode Verifier"
    assert msg in caplog.text

    msg = "Verifier completed successfully."
    assert msg in caplog.text


def test_execute_does_not_execute(
    patched_distronode_converge,
    caplog: pytest.LogCaptureFixture,
    _instance,
):
    _instance._config.config["verifier"]["enabled"] = False
    _instance.execute()

    assert not patched_distronode_converge.called

    msg = "Skipping, verifier is disabled."
    assert msg in caplog.text
