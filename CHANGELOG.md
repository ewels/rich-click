# Changelog: rich-click

## Version 0.4.0.dev0

Major change: New usage, so that we can avoid having to do monkey patching [#10](https://github.com/ewels/rich-click/pull/10).

- Add ability to create groups of options with separate panels
- Show positional arguments in their own panel by default
- Add config `GROUP_ARGUMENTS_OPTIONS` option to group with options
- Improve handing of metavars, give option to show appended instead of in column
- Add support for printing errors nicely

## Version 0.3.0 (2022-02-13)

- Add ability to create groups of commands with separate panels
- Add support for rich console markup or Markdown in help texts
- Set default for `MAX_WIDTH` to `None` instead of `100`
- Switch boolean option `SKIP_ARGUMENTS` to `SHOW_ARGUMENTS`
- Improve regular expression for flags like `-bg`
- Use click's string for default value, instead of the value directly
- Show some previously missed metavar types (eg. choice and range options)
- Stripped required-asterisk column from options table if none are required

## Version 0.2.0 (2022-02-10)

- Made most styling decisions configurable
- Added support for more click parameters
  - Showing default values, showing if required, showing if deprecated, epilog
  - Option now hidden if set in click

## Version 0.1.2 (2022-02-10)

- Seems to work fine on Python 3.6, so dropped the requirement down to this instead of Python 3.7

## Version 0.1.1 (2022-02-10)

- Fix a bug in `setup.cfg` that broke installation

## Version 0.1.0 (2022-02-09)

Initial development version of `rich-click`, mostly as a proof of concept.

Supports basic generic functionality for printing help from click commands and groups.

Code was initially written by [@willmcgugan](https://github.com/willmcgugan) for `rich-cli`
and then further developed by [@ewels](http://github.com/ewels/).
