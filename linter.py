#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by roadhump
# Copyright (c) 2015 roadhump
#
# License: MIT
#

"""This module exports the Eslint_d plugin class."""

import re
from SublimeLinter.lint import NodeLinter


class Eslint_d(NodeLinter):

    """Provides an interface to eslint_d."""

    syntax = ('javascript', 'html', 'javascriptnext', 'javascript (babel)', 'javascript (jsx)', 'jsx-real')
    npm_name = 'eslint_d'
    cmd = ('eslint_d', '@')
    executable = None
    version_args = '--version'
    version_re = r'eslint_d v(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 2.1.0'
    regex = (
        r'^.+?: line (?P<line>\d+), col (?P<col>\d+), '
        r'(?:(?P<error>Error)|(?P<warning>Warning)) - '
        r'(?P<message>.+)'
    )
    config_fail_regex = re.compile(r'^Cannot read config file: .*\r?\n')
    crash_regex = re.compile(
        r'^(.*?)\r?\n\w*Error: \1',
        re.MULTILINE
    )
    line_col_base = (1, 1)
    selectors = {
        'html': 'source.js.embedded.html'
    }

    def find_errors(self, output):
        """
        Parse errors from linter's output.

        We override this method to handle parsing eslint crashes.
        """

        match = self.config_fail_regex.match(output)
        if match:
            return [(match, 0, None, "Error", "", match.group(0), None)]

        match = self.crash_regex.match(output)
        if match:
            msg = "ESLint crashed: %s" % match.group(1)
            return [(match, 0, None, "Error", "", msg, None)]

        return super().find_errors(output)
