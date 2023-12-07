#  Copyright (c) 2015-2018 Cisco Systems, Inc.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

from subprocess import CompletedProcess

import pytest

from molecule import config
from molecule.provisioner import distronode_playbook


@pytest.fixture()
def _instance(config_instance: config.Config):
    _instance = distronode_playbook.DistronodePlaybook("playbook", config_instance)

    return _instance


@pytest.fixture()
def _provisioner_section_data():
    return {"provisioner": {"name": "distronode", "env": {"FOO": "bar"}}}


@pytest.fixture()
def _verifier_section_data():
    return {"verifier": {"name": "distronode", "env": {"FOO": "bar"}}}


@pytest.fixture()
def _provisioner_verifier_section_data():
    return {
        "provisioner": {"name": "distronode", "env": {"FOO": "bar"}},
        "verifier": {"name": "distronode", "env": {"FOO": "baz"}},
    }


@pytest.fixture()
def _instance_for_verifier_env(config_instance: config.Config):
    _instance = distronode_playbook.DistronodePlaybook("playbook", config_instance, True)
    return _instance


@pytest.mark.parametrize(
    "config_instance",
    ["_provisioner_section_data"],
    indirect=True,
)
def test_env_in_provision(_instance_for_verifier_env):
    assert _instance_for_verifier_env._env["FOO"] == "bar"


@pytest.mark.parametrize("config_instance", ["_verifier_section_data"], indirect=True)
def test_env_in_verifier(_instance_for_verifier_env):
    assert _instance_for_verifier_env._env["FOO"] == "bar"


@pytest.mark.parametrize(
    "config_instance",
    ["_provisioner_verifier_section_data"],
    indirect=True,
)
def test_env_in_verify_override_provision(_instance_for_verifier_env):
    assert _instance_for_verifier_env._env["FOO"] == "baz"


@pytest.fixture()
def _inventory_directory(_instance):
    return _instance._config.provisioner.inventory_directory


def test_distronode_command_private_member(_instance):
    assert _instance._distronode_command is None


def test_distronode_playbook_private_member(_instance):
    assert _instance._playbook == "playbook"


def test_config_private_member(_instance):
    assert isinstance(_instance._config, config.Config)


def test_bake(_inventory_directory, _instance):
    pb = _instance._config.provisioner.playbooks.converge
    _instance._playbook = pb
    _instance.bake()

    args = [
        "distronode-playbook",
        "--become",
        "--inventory",
        _inventory_directory,
        "--skip-tags",
        "molecule-notest,notest",
        pb,
    ]

    assert _instance._distronode_command == args


def test_bake_removes_non_interactive_options_from_non_converge_playbooks(
    _inventory_directory,
    _instance,
):
    _instance.bake()

    args = [
        "distronode-playbook",
        "--inventory",
        _inventory_directory,
        "--skip-tags",
        "molecule-notest,notest",
        "playbook",
    ]

    assert _instance._distronode_command == args


def test_bake_has_distronode_args(_inventory_directory, _instance):
    _instance._config.distronode_args = ("foo", "bar")
    _instance._config.config["provisioner"]["distronode_args"] = ("frob", "nitz")
    _instance.bake()

    args = [
        "distronode-playbook",
        "--inventory",
        _inventory_directory,
        "--skip-tags",
        "molecule-notest,notest",
        "frob",
        "nitz",
        "foo",
        "bar",
        "playbook",
    ]

    assert _instance._distronode_command == args


def test_bake_does_not_have_distronode_args(_inventory_directory, _instance):
    for action in ["create", "destroy"]:
        _instance._config.distronode_args = ("foo", "bar")
        _instance._config.action = action
        _instance.bake()

        args = [
            "distronode-playbook",
            "--inventory",
            _inventory_directory,
            "--skip-tags",
            "molecule-notest,notest",
            "playbook",
        ]

        assert _instance._distronode_command == args


def test_bake_idem_does_have_skip_tag(_inventory_directory, _instance):
    _instance._config.action = "idempotence"
    _instance.bake()

    args = [
        "distronode-playbook",
        "--inventory",
        _inventory_directory,
        "--skip-tags",
        "molecule-notest,notest,molecule-idempotence-notest",
        "playbook",
    ]

    assert _instance._distronode_command == args


def test_execute_playbook(patched_run_command, _instance):
    _instance._distronode_command = "patched-command"
    result = _instance.execute()
    assert result == "patched-run-command-stdout"


def test_distronode_execute_bakes(_inventory_directory, patched_run_command, _instance):
    _instance.execute()

    assert _instance._distronode_command is not None

    args = [
        "distronode-playbook",
        "--inventory",
        _inventory_directory,
        "--skip-tags",
        "molecule-notest,notest",
        "playbook",
    ]

    assert _instance._distronode_command == args


def test_execute_bakes_with_distronode_args(
    _inventory_directory,
    patched_run_command,
    _instance,
):
    _instance._config.distronode_args = ("-o", "--syntax-check")
    _instance.execute()

    assert _instance._distronode_command is not None

    args = [
        "distronode-playbook",
        "--inventory",
        _inventory_directory,
        "--skip-tags",
        "molecule-notest,notest",
        "-o",
        "--syntax-check",
        "playbook",
    ]

    assert _instance._distronode_command == args


def test_executes_catches_and_exits_return_code(
    patched_run_command,
    _instance,
):
    patched_run_command.side_effect = [
        CompletedProcess(
            args="distronode-playbook",
            returncode=1,
            stdout="out",
            stderr="err",
        ),
    ]
    with pytest.raises(SystemExit) as e:
        _instance.execute()

    assert e.value.code == 1


def test_add_cli_arg(_instance):
    assert {} == _instance._cli

    _instance.add_cli_arg("foo", "bar")
    assert {"foo": "bar"} == _instance._cli


def test_add_env_arg(_instance):
    assert "foo" not in _instance._env

    _instance.add_env_arg("foo", "bar")
    assert _instance._env["foo"] == "bar"
