import subprocess


def run(command, shell=False):
    r = subprocess.run(command, shell=shell, capture_output=True, check=True, universal_newlines=True)
    return r.stdout