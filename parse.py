import argparse

class ArgParseException(Exception):
    def __init__(self, string, type):
        super(ArgParseException, self).__init__(f"Argument {string} could not be cast to {type}")

def str2bool(string):
    string = string.lower()
    if string in ["true", "1", "yes"]:
        return True

    if string in ["false", "0", "no"]:
        return False

    raise ArgParseException(string, "boolean")

def get_parser(input=None):
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('--foo', action='store_true', help='foo help')
    subparsers = parser.add_subparsers(help='sub-command help')

    # create the parser for the "a" command
    parser_a = subparsers.add_parser('add', help='a help')
    parser_a.add_argument('folder', type=str, help='bar help')

    # create the parser for the "b" command
    parser_b = subparsers.add_parser('remove', help='b help')
    parser_b.add_argument("folder", type=str)

    parser_chdir = subparsers.add_parser('chdir', help='b help')
    parser_chdir.add_argument("folder", type=str)

    parser_back = subparsers.add_parser('back', help='b help')

    parser_complicated = subparsers.add_parser("dosomethingcomplicated")

    parser_addfiles = subparsers.add_parser('addfiles', help='b help')
    return parser