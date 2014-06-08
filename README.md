StartAppSync
=======

[![Build Status](https://travis-ci.org/mignev/startappsync.svg?branch=master)](https://travis-ci.org/mignev/startappsync)

# Installation

## Important: Now installing of startappsync is available only from the source! I will make it avaiable on PyPI soon.

Installing from PyPI using `pip`:

```bash
$ pip install setuptools
$ pip install startappsync
```

Installing from PyPI using `easy_install`:

```bash
$ easy_install setuptools
$ easy_install startappsync
```

Installing from source:

```bash
$ python setup.py install
```

## Installation Dependencies

The ``startappsync`` script depends on [PyYAML](http://www.pyyaml.org/) which links with [LibYAML](http://pyyaml.org/wiki/LibYAML),
which brings a performance boost to the PyYAML parser. However, installing
[LibYAML](http://pyyaml.org/wiki/LibYAML) is optional but recommended. On Mac OS X, you can use [homebrew](http://brew.sh/)
to install LibYAML:

```bash
$ brew install libyaml
```

On Linux, use your favorite package manager to install LibYAML. Here's how you
do it on Ubuntu:

```bash
$ sudo aptitude install libyaml-dev
```

On Windows, please install [PyYAML](http://www.pyyaml.org/) using the binaries they provide.



# Contributing
Fork the [Configo repo on GitHub](https://github.com/mignev/startappsync), make your super duper awesome changes :) and send me a Pull Request. :)



# TODO

- Add rsync to dependencies and add toturial how to install it?
- Make the documentation better
- Upload the tool to pypi
- Add README in Bulgarian

# CHANGELOG

## 0.0.1:

This is the first alpha release. So a lot of thinks may will be crappy. Please if you find some bugs, open issue and report them. 10x

### Features

- Use `startappsync` without arguments in startapp repo
- Use `startappsync` with `--repo` argument if you use it outside of startapp repo
- Use `startappsync` with `--from` and `--to` arguments if you want to use it with no startapp repos
- Add `--set-remote` argument to set what is your app, namespace in git config.

### Other

- Add tests
- Make it green on Travis


#Copyright
Copyright (c) 2014 Marian Ignev. See LICENSE for further details.
