![octosuite](https://raw.githubusercontent.com/bellingcat/octosuite/refs/heads/master/img/octosuite.png)

TUI-based toolkit for GitHub data analysis.

![PyPI - Version](https://img.shields.io/pypi/v/octosuite)
![PyPI - Downloads](https://img.shields.io/pepy/dt/octosuite)
![Code Size](https://img.shields.io/github/languages/code-size/bellingcat/octosuite)
![Release Date](https://img.shields.io/github/release-date/bellingcat/octosuite)
![Build Status](https://img.shields.io/github/actions/workflow/status/bellingcat/octosuite/python-publish.yml)
![License](https://img.shields.io/github/license/bellingcat/octosuite)

## Overview

OctoSuite provides a terminal interface for exploring and exporting GitHub data. Access information about users,
repositories, organizations, and search across GitHub's platform.

## Features

- **User Data** - View profiles, repositories, followers, organizations, and activity, e.t.c.
- **Repository Data** - Access repository details, commits, issues, releases, and contributors
- **Organisation Data** - Explore organisation profiles, members, and repositories
- **Search** - Search across repositories, users, commits, issues, and topics
- **Export** - Save data in JSON, CSV, or HTML formats

## Installation

### PyPI

```bash
pip install octosuite
```

### Build from source

```bash
# Clone repository
git clone https://github.com/bellingcat/octosuite.git

# Move to octosuite directory
cd octosuite

# Build and install (uses uv)
make install

# If you dont have uv installed, you can install directly with pip:
pip install .

# Run
octosuite
```

> [!Note]
> You can run octosuite with commands `octosuite`, or `ocs`

## Usage

Navigate using <kbd>UP</kbd><kbd>DOWN</kbd> and <kbd>ENTER</kbd> to select options. The interface guides you through
selecting a
data source
and
choosing what information to retrieve. Preview the results and optionally export them in your preferred format.

![home](https://raw.githubusercontent.com/bellingcat/octosuite/refs/heads/master/img/menu.png)

## License

### MIT License

See the LICENSE file for details. License information is also available through the application's main menu.

## Contributing

Contributions are welcome. Please submit pull requests or open issues for bugs and feature requests. Good luck!