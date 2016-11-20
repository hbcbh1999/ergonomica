"""
[parser.py]

Lexer module. Contains tokenize().
"""

# pylint doesn't know that `from lib.verbs...` is run from the above dir
# pylint: disable=import-error

import re
import subprocess
from lib.verbs import verbs

def tokenize(string):
    """Tokenize ergonomica commands."""

    tokens = [""]
    try:
        bash_escaped = re.search("`(.+?)`", string).groups()

        for item in bash_escaped:
            cmd = item.split(",")
            evaluated_cmd = subprocess.check_output(cmd, cwd=verbs.directory)
            string = string.replace("`" + item + "`", evaluated_cmd)
    except AttributeError:
        pass

    tokens = [""]
    _special = False
    special = ""
    kwargs = []
    args = []

    for char in string:
        if _special:
            if char in ["}", "]"]:
                if _special == "{":
                    for item in special.split(","):
                        kwargs.append(item)
                elif _special == "[":
                    for item in special.split(","):
                        args.append(item)
                _special = False
            else:
                special += char
        else:
            if char == " ":
                tokens.append("")
            elif char in ["{", "["]:
                _special = char
                special = ""
            else:
                tokens[-1] += char

           # filter out empty strings
    return [[x for x in tokens if x], args, kwargs]

def parse(string):
    """Parses input"""
    blocks = [tokenize(x) for x in string.split("->")]
    for i in range(0, len(blocks)):
        blocks[i] = "%s(%s, %s)" % (blocks[i][0][0], ", ".join(blocks[i][1]), ", ".join([s.replace(":", "=") for s in blocks[i][2]]))
    return blocks