# pyright: strict

import typing
import argparse
import os.path
import tomllib
import subprocess as sp

from . import config
from .slvs import sketch as slvs_sketch

parser = argparse.ArgumentParser()
parser.add_argument('config_dir', type=str)
args = parser.parse_args()

config_dir = typing.cast(str, args.config_dir)
assert os.path.isdir(config_dir)

with open(os.path.join(config_dir, 'solvespace.toml'), 'rb') as config_file:
    config = config.Config.parse(tomllib.load(config_file))
    
source_path = os.path.join(config_dir, config.source)
assert source_path.endswith('.slvs')
source_name = source_path.removesuffix('.slvs')
with open(source_path, 'rb') as f:
    sketch_base = slvs_sketch.Sketch.parse(f)

config.validate(sketch_base)
out_paths: list[str] = []
for name, sketch in config.apply(sketch_base).items():
    out_path = f'{source_name}.{name}.slvs'
    out_paths.append(out_path)
    with open(out_path, 'wb') as out:
        sketch.serialize(out)

sp.call(['solvespace-cli', 'export-mesh', '--output', '%.stl', *out_paths])
