# -*- coding: utf-8 -*-

"""Console script for codebuildtoslack."""
import sys
import click
import codebuildtoslack


@click.command()
def main(args=None):
    """Console script for codebuildtoslack."""
    codebuildtoslack.main()


@click.command()
def test_slack(args=None):
    codebuildtoslack.test_slack_message()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
