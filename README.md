# watch-diff

[![PyPI](https://img.shields.io/pypi/v/watch-diff.svg)](https://pypi.org/project/watch-diff)

## setup

```shell
pip install watch-diff
```

## usage

```console
$ watch-diff --help
usage: watch-diff [-h] [-v] [-i SECONDS] [-n] [-e RECIPIENT] command

Watch command output and get notified on changes

positional arguments:
  command               the command to watch

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         enable program verbosity
  -i SECONDS, --interval SECONDS
                        number of seconds between executions
  -n, --notify          send notification using notify-send
  -e RECIPIENT, --email RECIPIENT
                        send email to recipient
```

## development

```shell
# setup
python3.6 -m venv venv && . venv/bin/activate

# editable install
pip install -e .[dev]
```
