
# RLWay CPAgent

Regulation agent using constraint programming

**Author**: Charles Pombet (charles.pombet@eurodecision.com)

**Release**: October, 2023

## Features

RLWay CPAgent offers following functionalities :

+ 1

+ 2

Installation
------------

To install rlway_cpagent :

1. Make sure your `~/config/pip/pip.conf` file contais a reference to `packages.fr.eurodecision.com/nexus/...`. If not, type :

```bash
pip config set global.trusted-host "pypi.org packages.fr.eurodecision.com"
pip config set global.extra-index-url https://packages.fr.eurodecision.com/nexus/repository/pypi-ed/simple
```

2. type
```bash
pip install rlway-cpagent 
```
Usage
-----

Import the package

```python3
>>> import rlway_cpagent
```

Run from command line

```python3
rlway_cpagent
```


Documentation
-------------

```python3
cd rlway-cpagent
pip install -r requirements.txt
pip install -e .
make docs
```

will build and open the html documentation.


Contributing to RLWay CPAgent
---------------------------------------------

All bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome at [](https://github.com/chpombet/rlway-cpagent/issues)

