# watch-diff

[![PyPI](https://img.shields.io/pypi/v/watch-diff.svg)](https://pypi.org/project/watch-diff)

Periodically run a command and receive nice diff styled emails on output changes.

## Features

- Supports Python >= 3.10
- Uses only Python Standard Library
- Sends email diff in both text and html form
- Output changes to CLI and optionally to SMTP
- Uses `Message-ID` and `In-Reply-To` to group email threads

## Setup

```shell
pip install watch-diff
```

## Usage

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

## SMTP Setup

```shell
export SMTP_HOST=qwer.ty
export SMTP_PORT=1234
export SMTP_USER=qwer@qwer.ty
read -s -p "SMTP_PASS: " SMTP_PASS
export SMTP_PASS
```

## Development

```shell
uv sync
uv build
python -m unittest -v
```
