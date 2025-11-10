# Visidata NG v1.02

<!-- //windsurf-scope: RENAME-REPO -->

## Project overview

**Visidata NG** is a community-maintained fork of the
[VisiData](https://github.com/saulpw/visidata) project created by
[Saul Pwanson](mailto:vd@saul.pw). This fork remains fully compliant with the
GNU GPLv3, retains upstream copyright notices, and incorporates local
modifications that are clearly documented throughout this repository.

![Frequency table](https://visidata.org/freq-move-row.gif)

## Release information

- Current release: **1.02** (2025-11-10)
- Release notes: see [CHANGELOG.md](CHANGELOG.md)

## Project scope

* Goal: provide an officially independent distribution that continues to
  develop the VisiData codebase while crediting upstream authors.
* License: GNU GPLv3 (see [LICENSE.gpl3](LICENSE.gpl3)).
* Attribution: all upstream notices are preserved. New contributions are
  © their respective authors and released under GPLv3.
* Upstream relationship: this project is not affiliated with the original
  maintainers. Compatibility with upstream releases is pursued on a
  best-effort basis.

## Platform requirements

* Linux, macOS, or Windows (via WSL)
* Python 3.8+
* Optional extras enabled via `requirements.txt`

## Installation

Until PyPI packages are published under the `visidata-ng` name, install
directly from source:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

To install a specific revision:

```bash
pip install git+https://github.com/denisotree/visidata-ng.git@<tag-or-branch>
```

## Usage

```bash
vd <input>
<command> | vd
```

Press `Ctrl+Q` to quit at any time. The CLI entry point remains `vd` for
backward compatibility with existing workflows.

## Documentation

The upstream documentation remains a comprehensive reference while local
changes are stabilised:

* [VisiData documentation](https://visidata.org/docs)
* [Plugin Author's Guide and API Reference](https://visidata.org/docs/api)
* [Quick reference](https://visidata.org/man) (also accessible within `vd`
  via `Ctrl+H`)
* [Intro to VisiData Tutorial](https://jsvine.github.io/intro-to-visidata/)

This repository will publish Visidata NG-specific documentation under the
`docs/` directory as changes diverge from upstream.

## Support and issue tracking

Please open GitHub issues at
<https://github.com/denisotree/visidata-ng/issues>. Feature requests aimed at
the upstream project should be filed with the original maintainers instead.

Community chat remains available through the public channels operated by the
upstream maintainers (Discord, IRC, Mastodon) unless alternative venues are
announced here.

## License and attribution

Code is provided under the [GNU General Public License v3.0](LICENSE.gpl3).
All files derived from VisiData retain the original copyright notices.
Modifications in this fork are attributed within commit history and changelog
entries. When redistributing binary builds, include the full text of the
license and acknowledge both upstream and Visidata NG contributors.

## Credits

Visidata NG is made possible thanks to the original VisiData authors,
contributors, and community. This fork extends their work; please support the
upstream project via [Patreon](https://www.patreon.com/saulpw) if you rely on
their ongoing maintenance.

