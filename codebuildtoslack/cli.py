# -*- coding: utf-8 -*-

"""Console script for codebuildtoslack."""
import sys
import click
from codebuildtoslack import codebuildtoslack


@click.command()
def main(args=None):
    """Console script for codebuildtoslack."""
    codebuildtoslack.main()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
