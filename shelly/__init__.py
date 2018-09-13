#!/usr/bin/env python3

'''A helper library for running shell commands.'''

import subprocess
import shlex
import shutil

from typing import Any, Optional, Dict, Union, List
from pathlib import Path
from dataclasses import dataclass


@dataclass
class ShellCommandResult:
    '''Hold data corresponding to a command's output.'''

    exit_code: int = 0
    stdout: bytes = b''
    stderr: bytes = b''

    def __init__(self, exit_code: int = 0,
                 stdout: Union[str, bytes] = b'',
                 stderr: Union[str, bytes] = b'') -> None:
        self.exit_code = exit_code
        self.stdout = stdout if isinstance(stdout, bytes) else stdout.encode()
        self.stderr = stderr if isinstance(stderr, bytes) else stderr.encode()


class ShellCommand:
    '''Model a shell command for execution.'''

    def __init__(self, command: List[str],
                 stdin: Union[bytes, Path, None] = None) -> None:
        self.command = command
        self.stdin = stdin
        if shutil.which(self.command[0]) is None:
            raise FileNotFoundError(
                f'No such file or directory: "{self.command[0]}"')

    def run(self) -> ShellCommandResult:
        '''Execute this command, returning its result.'''

        if isinstance(self.stdin, bytes) or self.stdin is None:
            result = subprocess.run(self.command, input=self.stdin,
                                    capture_output=True)
        else:
            with open(self.stdin, 'rb') as infile:
                result = subprocess.run(
                    self.command, stdin=infile, capture_output=True)
        return ShellCommandResult(result.returncode,
                                  result.stdout,
                                  result.stderr)

    def __lshift__(self, input: Union[str, bytes]) -> 'ShellCommand':
        input = input if isinstance(input, bytes) else input.encode()
        return ShellCommand(self.command, input)

    def __lt__(self, input_file: str) -> 'ShellCommand':
        return ShellCommand(self.command, Path(input_file))


def sh(command: Union[str, List[str]]) -> ShellCommand:
    '''Convenience method for creating shell commands.'''

    if isinstance(command, str):
        command = shlex.split(command)
    else:
        command = list(command)

    return ShellCommand(command)
