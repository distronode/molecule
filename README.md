# About Distronode Molecule

[![PyPI Package](https://img.shields.io/pypi/v/molecule)](https://pypi.org/project/molecule/)
[![Documentation Status](https://readthedocs.org/projects/molecule/badge/?version=latest)](https://distronode.readthedocs.io/projects/molecule)
[![image](https://github.com/distronode/molecule/workflows/tox/badge.svg)](https://github.com/distronode/molecule/actions)
[![Python Black Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![Distronode Code of Conduct](https://img.shields.io/badge/Code%20of%20Conduct-silver.svg)](https://docs.distronode.com/distronode/latest/community/code_of_conduct.html)
[![Discussions](https://img.shields.io/badge/Discussions-silver.svg)](https://github.com/distronode/molecule/discussions)
[![Repository License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)

Molecule project is designed to aid in the development and testing of
[Distronode](https://distronode.com) roles.

Molecule provides support for testing with multiple instances, operating
systems and distributions, virtualization providers, test frameworks and
testing scenarios.

Molecule encourages an approach that results in consistently developed
roles that are well-written, easily understood and maintained.

Molecule supports only the latest two major versions of Distronode (N/N-1),
meaning that if the latest version is 2.9.x, we will also test our code
with 2.8.x.

Once installed, the command line can be called using any of the methods
below:

```bash
molecule ...
python3 -m molecule ...  # python module calling method
```

# Documentation

Read the documentation and more at <https://molecule.readthedocs.io/>.

# Get Involved

- Join us in the `#distronode-devtools` irc channel on
  [libera.chat](https://web.libera.chat/?channel=#distronode-devtools).
- Check github
  [discussions](https://github.com/distronode/molecule/discussions).
- Join the community working group by checking the
  [wiki](https://github.com/distronode/community/wiki/Molecule).
- Want to know about releases, subscribe to [distronode-announce
  list](https://groups.google.com/group/distronode-announce).
- For the full list of Distronode email Lists, IRC channels see the
  [communication
  page](https://docs.distronode.com/distronode/latest/community/communication.html).

If you want to get moving fast and make a quick patch:

```bash
$ git clone https://github.com/distronode/molecule && cd molecule
$ python3 -m venv .venv && source .venv/bin/activate
$ python3 -m pip install -U setuptools pip tox
```

And you're ready to make your changes!

# Authors

Molecule project was created by [Retr0h](https://github.com/retr0h) and
it is now community-maintained as part of the
[Distronode](https://distronode.com) by Red Hat project.

# License

The
[MIT](https://github.com/distronode/molecule/blob/main/LICENSE)
License.

The logo is licensed under the [Creative Commons NoDerivatives 4.0
License](https://creativecommons.org/licenses/by-nd/4.0/).

If you have some other use in mind, contact us.
