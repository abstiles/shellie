# Shellie

Using subprocess to invoke and process the output of command-line tools in
Python is incredibly painful, especially when compared with using an ordinary
unixy shell. It's incredibly verbose, and you need to wrap everything in
layer after layer of delimiter and/or function calls. Here's an example of
invoking the `gpg` command-line tool to decrypt the file located at `path`
with a key that requires a password to unlock:

    result = subprocess.run([
        'gpg', '--batch', '--yes', '--pinentry-mode', 'loopback',
        '--passphrase-fd', '0', '--decrypt', path],
        input=password,
        capture_output=True)
    result.check_returncode()
    decrypted = result.stdout

Can we do better than this? This is certainly a straightforward,
Pythonic-looking function. It's very sensible.

But I don't want sensible, I want _easy_. And I don't care if I have to violate
the laws of Man and God to get it. How close can we get to what we can do with
a unixy shell?

    decrypted = (sh % f'''
        gpg --batch --yes --pinentry-mode loopback --passphrase-fd 0
            --decrypt '{path}'
        ''' << password).raise_for_status().stdout

# Features

* Easy, fluent chaining for raising exceptions on nonzero exit codes.
* Automatically capture `stdout`, `stderr`, and exit codes for completed
  commands.
* `stdin` redirect with `< file_path` and `<< literal_string`.
* Automatic shell-like argument lexing.
* Simplify the simplest cases.

# TODOs

Things I'd like to get working:

## Simpler pipelines without Popen nastiness

    sh % 'ls -thral' | 'grep ignore' | 'tail -1'

## Write output directy to a file

    sh.ls > 'dir_contents.out'

## Append output directy to a file

    sh.ls >> 'dir_contents.out'

## Redirect stderr to a file or file descriptor

    sh % 'ls nonexistant_file' @ 2 > 'ls.err'
    sh % 'ls nonexistant_file' @ 2 > 1
