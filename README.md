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

## credentials

```shell
export SMTP_HOST=qwer.ty
export SMTP_PORT=1234
export SMTP_USER=qwer@qwer.ty
read -s -p "SMTP_PASS: " SMTP_PASS
export SMTP_PASS
```

## development

```shell
uv sync
uv build
python -m unittest -v
```
