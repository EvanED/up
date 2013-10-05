__doc__ = """up: Search up the directory tree for a file and run a command

Usage:
  up  <key-file> <command> [<arg>...]
"""

import sys
import os
import os.path
import platform
import subprocess


def find_dir_with_key(starting_dir, keyfile):
    """Returns the deepest directory that's a parent of starting_dir that contains keyfile"""
    if os.path.exists(os.path.join(starting_dir, keyfile)):
        return starting_dir
    parent = os.path.dirname(starting_dir)
    if parent == starting_dir:
        return None
    return find_dir_with_key(parent, keyfile)


def exec_command(command):
    """Start the given command. This function does not return."""
    if platform.system() != "Windows":
        os.execvp(command[0], command)
    else:
        subprocess.call(command, shell=True)


def main():
    keyfile = sys.argv[1]
    command = sys.argv[2:]
    
    key_dir = find_dir_with_key(os.getcwd(), keyfile)
    if key_dir is None:
        sys.stderr.write("{}: Could not find the key file {} in a parent of the current directory"
                         .format(sys.argv[0], keyfile))
        sys.exit(1)
    os.chdir(key_dir)
    exec_command(command)


if __name__ == "__main__":
    main()
