import argparse
import contextlib
import os
import shutil
import sys

import parse

import fileinput

from run import run


@contextlib.contextmanager
def makedirs(name):
    try:
        os.makedirs(name)
    except:
        pass
    yield None

def chdir(name):
    ret = os.getcwd()
    os.chdir(name)
    return ret


@contextlib.contextmanager
def directory(name):
    ret = chdir(name)
    yield ret

    os.chdir(ret)


class Reader():
    def __init__(self):
        self.fileinput = fileinput.input()

    def parseline(self, parser):
        line = sys.stdin.readline()#self.fileinput.readline()   #if you don't need "addfile-like" behaviour, can be refactored into a generator with yield
        actions_this_turn = line.replace("\n", "").split(" ")
        if actions_this_turn[0] == "exit":
            exit(0)

        args = parser.parse_args(actions_this_turn)
        return actions_this_turn[0], args

class Main():
    def __init__(self):
        self.dirstack = []
        self.reader = Reader()

    def _execute(self):
        while True:
            command, args = self.reader.parseline(parse.get_parser())
            getattr(self, command)(args)
            pass

    def chdir(self, args):
        old_dir = chdir(args.folder)
        self.dirstack.append(old_dir)

    def back(self, args):
        os.chdir(self.dirstack.pop())

    def add(self, args):
        with makedirs("./"+args.folder):
            with directory("./"+args.folder):
                self.dirstack.append(os.getcwd())

    def remove(self, args):
        # todo if not a full path, add a "./"
        shutil.rmtree("./"+args.folder)
        i = self.dirstack.index(os.getcwd()+"/"+args.folder)
        self.dirstack = self.dirstack[:i]

    def dosomethingcomplicated(self, args):
        out = run("cat main.py", shell=True)
        print(out)

    def addfiles(self, args):
        print("Enter files to add:")
        parser = argparse.ArgumentParser(prog='PROG')
        parser.add_argument("filename", type=str)  # todo make a "filename" type or something
        while True:
            print("\t", end="")
            command, args = self.reader.parseline(parser)
            if command == "stop":
                break

            run(f"touch ./{command}", shell=True)

if __name__ == "__main__":
    with makedirs("./workdir"):
        with directory("./workdir"):
            Main()._execute()