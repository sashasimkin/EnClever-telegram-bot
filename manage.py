#!/bin/env python
import os
from importlib import import_module


def discover_commands(path='management'):
    """
    Very simple function that auth discovers
    all commands form `management` directory/package

    :param path:
    :return:
    """
    files = os.listdir(path)
    py_files = filter(lambda filename: filename.endswith('.py'), files)

    for file in py_files:
        import_module('{}.{}'.format(path, file.replace('.py', '')))


if __name__ == '__main__':
    discover_commands()

    from management.cli import cli

    cli()
