# watch-diff

[![PyPI](https://img.shields.io/pypi/v/watch-diff.svg)](https://pypi.org/project/watch-diff)

## setup

```shell
pip install watch-diff
```

## usage

```console
$ watch-diff --help
usage: watch-diff [-h] [-v | -d] [-i SECONDS] [-r RECIPIENT] command

Watch command output and get notified on changes

positional arguments:
  command               the command to watch

optional arguments:
  -h, --help            show this help message and exit
  -i SECONDS, --interval SECONDS
                        number of seconds between executions
  -r RECIPIENT, --recipient RECIPIENT
                        send email to recipient

logging level:
  -v, --verbose         enable verbose output
  -d, --debug           show debugging statements
```

## development

```shell
# setup
python3 -m venv venv && . venv/bin/activate

# editable install
pip install -e .[dev]

# running tests
python -m unittest -v

# running tests for all supported python versions
tox
```
