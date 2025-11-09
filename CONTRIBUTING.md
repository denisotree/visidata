# Contributing to Visidata NG

<!-- //windsurf-scope: RENAME-REPO -->

Visidata NG is a GPLv3 fork of [VisiData](https://github.com/saulpw/visidata)
maintained independently from the upstream project. We honour all upstream
copyright notices and ask contributors to do the same. By proposing changes
here you grant permission to redistribute your work under GPLv3.

If you intend for your contribution to land upstream as well, please discuss
with the original maintainers separately and follow their processes.

## Spread the Word

The single best way you can contribute is to share your enthusiasm about
Visidata NG (and VisiData) with other people.
A vibrant community is essential to its sustainable development.

However, direct and forceful promotion is probably not the most effective approach for a tool like VisiData.
People generally need to be exposed several times and from several sources before they will try some terminal utility they've never heard of before.

Some people are interested, but are daunted by the installation process or the interface; you can [help them get it installed](/install), and provide a few pointers to get started.
Don't make it too complicated or overload them with too many features.
Stick to the basics: arrow keys, quit, help, search, sort, freq table.

We also need people to mention VisiData in their forums and communities that relate to data and terminal programs.
Don't spam or do a drive-by promotion; these are largely ineffective and will often be received negatively.
Endorsements have more weight from people who actively post about other relevant topics; we don't want to become the "VisiData Brigade".

Finally, if you are on "Web 2.social", you can post a [tweet](https://twitter.com/visidata) or a [tutorial]() or a [demo](https://www.youtube.com/watch?v=N1CBDTgGtOU) or [host a workshop](https://www.meetup.com/pt-BR/Journocoders/events/258035880/), or anything else you think might make people interested in exploring the wonderful world of VisiData.

## Support on Patreon

If this fork or the upstream project saves you time on a regular basis, please
consider supporting [Saul Pwanson on Patreon](https://www.patreon.com/saulpw)
and other contributors who make the ecosystem sustainable.

## Start a Project Using VisiData

If you know Python and want to augment it to suit your own workflow, you can
create a loader or a plugin. The upstream team maintains
[a detailed API guide](https://www.visidata.org/docs/api/) that still applies.

Here are some great examples:

  - [jsvine's custom visidata plugins](https://github.com/jsvine/visidata-plugins)
  - [layertwo's pcap loader](https://github.com/saulpw/visidata/blob/develop/visidata/loaders/pcap.py)

Without fail, these projects lead to discovering bugs and help flesh out the API, which result in design improvements in VisiData.
Importantly, each issue found this way comes with real world motivations, so it is easy to explain your reasoning behind proposals and core feature requests.

## Feature Requests

VisiData is designed to be extensible, and most feature requests can be implemented as a one line command, or a tiny snippet of code to include in a `.visidatarc`.

If a change requires updates to shared core functionality, please open an issue
in this repository so we can align on how Visidata NG should diverge from or
track the upstream project.
Otherwise, in the spirit of Marie Kondo, the issue will be closed without prejudice.

Feature requests with some amount of working Python code are more likely to get attention.
Design proposals with concrete use cases are very welcome.

## Writing a well constructed bug report

If you encounter any bugs or have any problems specific to this fork, please
[create an issue on GitHub](https://github.com/denisotree/visidata-ng/issues).
For upstream-only issues, continue to use their trackers.

A great bug report will include:

  - a stacktrace, if there is an unexpected error; the most recent full stack traces can be viewed with `Ctrl+E` (then saved with `Ctrl+S`)
  - a [.vd](http://visidata.org/docs/save-restore/) and sample dataset that reproduces the issue
  - a .png/.gif (esp. for user interface changes)

Some examples of great bug reports from the VisiData project (still excellent
references):

  - [#350 by @chocolateboy](https://github.com/saulpw/visidata/issues/350)
  - [#340 by @Mikee-3000](https://github.com/saulpw/visidata/issues/340)


## Submitting Source Code

Check out the [Plugin Authors Guide](https://visidata.org/docs/api) for an
overview of the API. Code in `visidata/features/` or `visidata/loaders/` is
generally welcome, as long as it is useful to someone and safe for everyone.

Visidata NG accepts pull requests against the `develop-ng` branch unless a
maintainer specifies otherwise. No Contributor License Agreement is required;
the GPLv3 covers contributions.

# Open Source License and Copyright

Visidata NG is an open-source utility that can be installed and used for free
under the terms of the [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html).

The core Visidata NG utility will remain free and libre. Contributors retain
their own copyrights; commits are merged under GPLv3 without additional
assignment requirements. Respect existing notices when editing upstream files
and add co-authored-by trailers where appropriate.
