import yaml #import pyyaml

with open(f"./paths.yaml", "r") as f:
    conf = yaml.safe_load(f)

i=0