#!/usr/bin/env python3

from subprocess import CalledProcessError

import pytest

from shelly import sh, ShellCommandResult

def test_simple_string_command():
    sh('ls -lrt')


def test_list_command():
    sh(['ls', '-lrt'])


def test_operator_syntax():
    sh % 'ls -lrt'


def test_bad_type_command():
    with pytest.raises(TypeError):
        sh(1)


def test_missing_command():
    with pytest.raises(FileNotFoundError):
        sh % 'werkasjfdxicvouewrmmcvxciuver'


def test_cli_tool_helper():
    sh % 'tests/cli.tool'


def test_attribute_access_helper():
    sh.ls('-lrt') == sh('ls -lrt')


def test_item_access_helper():
    sh['tests/cli.tool']('-o', 'hi') == sh('tests/cli.tool -o hi')


def test_can_run():
    result = (sh % 'tests/cli.tool').run()
    assert result == ShellCommandResult()


def test_exit_code():
    result = (sh % 'tests/cli.tool -x 42').run()
    assert result == ShellCommandResult(exit_code=42)


def test_stdout_capture():
    result = (sh % 'tests/cli.tool -o "hi there"').run()
    assert result == ShellCommandResult(stdout='STDOUT: hi there\n')


def test_stderr_capture():
    result = (sh % 'tests/cli.tool -e "hi there"').run()
    assert result == ShellCommandResult(stderr='STDERR: hi there\n')


def test_stdin_writing():
    result = (sh % 'tests/cli.tool -i' << 'hi stdin').run()
    assert result == ShellCommandResult(stdout='STDIN: hi stdin\n')


def test_simplified_stdout():
    assert sh('tests/cli.tool -o "output"').stdout == b'STDOUT: output\n'


def test_simplified_stderr():
    assert sh('tests/cli.tool -e "errput"').stderr == b'STDERR: errput\n'


def test_simplified_exit_code():
    assert sh('tests/cli.tool -x 42').exit_code == 42


def test_raise_for_status_success():
    assert sh('tests/cli.tool').raise_for_status() == ShellCommandResult()


def test_raise_for_status_failure():
    with pytest.raises(CalledProcessError):
        sh('tests/cli.tool -x 42').raise_for_status()


def test_stdin_file():
    result = (sh % 'tests/cli.tool -i' < 'tests/test_input.txt').run()
    # One newline belongs to the test file, the other is a standard part of
    # cli.tool's output.
    assert result == ShellCommandResult(stdout='STDIN: Test input file.\n\n')
