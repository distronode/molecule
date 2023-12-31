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

from molecule.model import schema_v3
from molecule.util import run_command


def test_base_config(_config):
    assert not schema_v3.validate(_config)


def test_molecule_schema():
    cmd = [
        "check-jsonschema",
        "-v",
        "--schemafile",
        "src/molecule/data/molecule.json",
        "test/resources/schema_instance_files/valid/molecule.yml",
    ]
    assert run_command(cmd).returncode == 0

    cmd = [
        "check-jsonschema",
        "-v",
        "--schemafile",
        "src/molecule/data/driver.json",
        "test/resources/schema_instance_files/invalid/molecule_delegated.yml",
    ]
    assert run_command(cmd).returncode != 0
