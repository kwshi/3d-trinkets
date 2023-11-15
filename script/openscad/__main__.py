# pyright: strict

import typing
import argparse
import os.path
import tomllib
import json
import subprocess as sp
import sys

from .config import Config


parser = argparse.ArgumentParser()
parser.add_argument("config_dir", type=str)
args = parser.parse_args()

config_dir = typing.cast(str, args.config_dir)
assert os.path.isdir(config_dir)

with open(os.path.join(config_dir, "openscad.toml"), "rb") as config_file:
    config = Config.parse(tomllib.load(config_file))

json_path = os.path.join(config_dir, ".openscad.json")
with open(json_path, "w") as f:
    json.dump(config.generate_openscad_parameters(), f)

source_path = os.path.join(config_dir, config.source)
assert source_path.endswith(".scad")
source_name = source_path.removesuffix(".scad")

for key in config.profiles.keys():
    sp.call(
        [
            "openscad",
            "-p",
            json_path,
            "-P",
            key,
            "-o",
            f"{source_name}.{key}.stl",
            source_path,
        ]
    )
