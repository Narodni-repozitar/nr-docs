#!/usr/bin/env python

import os
import re
import sys


class TargetHelp:

    def __init__(self, name):
        self._name = name
        self._help_lines = []

    def add_line(self, line):
        self._help_lines.append(line)

    def get_result(self, max_target_width, output):
        template = '  %-{}s  %s\n'.format(max_target_width)

        if self._help_lines:
            output.write(template % (self._name, self._help_lines[0]))

            for line in self._help_lines[1:]:
                output.write(template % ('', line))

            output.write('\n')


class HelpBuilder:

    def __init__(self):
        self._help = []
        self._max_target_width = 0

    def found_target(self, name):
        self._max_target_width = max(len(name), self._max_target_width)
        self._help.append(TargetHelp(name))

    def found_help(self, line):
        self._help[-1].add_line(line)

    def get_result(self, output):
        for target_help in self._help:
            target_help.get_result(self._max_target_width, output)


class HelpLineDirector:

    def __init__(self, _help):
        self._help = _help

    def add_line(self, line):
        match = re.match(r'^\t+@## *(.+) *', line)

        if match:
            self._help.found_help(match.group(1))
            return self

        return TargetLineDirector(self._help)


class TargetLineDirector:

    def __init__(self, _help):
        self._help = _help

    def add_line(self, line):
        match = re.match(r'^([a-zA-Z_-]+):', line)

        if match:
            self._help.found_target(match.group(1))
            return HelpLineDirector(self._help)

        return self


class HelpDirector:

    def __init__(self, builder):
        self._director = TargetLineDirector(builder)

    def build(self, lines):
        for line in lines:
            self._director = self._director.add_line(line)


def main():
    makefile = os.path.join(os.path.dirname(__file__), 'Makefile')
    builder = HelpBuilder()
    director = HelpDirector(builder)
    director = director.build(open(makefile, 'r'))
    builder.get_result(sys.stdout)


if __name__ == "__main__":
    main()
