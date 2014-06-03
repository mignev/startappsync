StartAppSync
=======

# Installation

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

- Add tests
- Add to travis
- Add rsync to dependencies and add toturial how to install it?
- Make the documentation better
- Upload the tool to pypi
- Add README in Bulgarian

# CHANGELOG

### 0.0.1:


#Copyright
Copyright (c) 2014 Marian Ignev. See LICENSE for further details.
