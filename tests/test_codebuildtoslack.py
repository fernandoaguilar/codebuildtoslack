#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `codebuildtoslack` package."""


import unittest
from unittest.mock import patch
import os
from click.testing import CliRunner
from datetime import datetime, timedelta
from time import mktime
from codebuildtoslack import codebuildtoslack
from codebuildtoslack import cli


class TestCodebuildtoslack(unittest.TestCase):
    """Tests for `codebuildtoslack` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_calculate_build_time_text(self):
        """Test something."""
        start_time = datetime.utcnow() - timedelta(minutes=6, seconds=23)
        unix_secs = mktime(start_time.timetuple()) * 1000
        os.environ['CODEBUILD_START_TIME'] = str(unix_secs)
        result = codebuildtoslack.calculate_build_time_text()
        assert result == '6 minutes, 23 seconds'

    def test_command_line_interface_in_non_codebuild_environment(self):
        """Test the CLI."""
        os.environ.pop('CODEBUILD_CI', None)
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'Not in an AWS Codebuild Environment' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output

    @patch('codebuildtoslack.codebuildtoslack.send_slack_message')
    def test_command_line_interface_in_codebuild_environment(self, mock_slack_send):
        """Test the CLI."""

        os.environ['CODEBUILD_CI'] = 'true'
        os.environ['CODEBUILD_BUILD_SUCCEEDING'] = '1'
        os.environ['CODEBUILD_BUILD_NUMBER'] = '321'
        os.environ['CODEBUILD_BUILD_ID'] = 'my-codebuild-project:some-uuid-goes-here'
        os.environ['CODEBUILD_WEBHOOK_TRIGGER'] = 'branch/master'
        os.environ['CODEBUILD_SOURCE_REPO_URL'] = 'https://github.com/myusername/myreponame.git'
        os.environ['CODEBUILD_SOURCE_VERSION'] = '123456abcdefghijklmnop'
        os.environ['CODEBUILD_BUILD_URL'] = 'https://codebuild.com/somepath'

        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'Slack message sent' in result.output

    def test_command_line_interface_in_codebuild_environment_no_slack_url(self):
        """Test the CLI."""

        os.environ['CODEBUILD_CI'] = 'true'
        os.environ['CODEBUILD_BUILD_SUCCEEDING'] = '1'
        os.environ['CODEBUILD_BUILD_NUMBER'] = '321'
        os.environ['CODEBUILD_BUILD_ID'] = 'my-codebuild-project:some-uuid-goes-here'
        os.environ['CODEBUILD_WEBHOOK_TRIGGER'] = 'branch/master'
        os.environ['CODEBUILD_SOURCE_REPO_URL'] = 'https://github.com/myusername/myreponame.git'
        os.environ['CODEBUILD_SOURCE_VERSION'] = '123456abcdefghijklmnop'
        os.environ['CODEBUILD_BUILD_URL'] = 'https://codebuild.com/somepath'

        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'No Slack url provided' in result.output
