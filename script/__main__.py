# pyright: strict

import sys
from .solvespace import sketch as slvs_sketch

sketch = slvs_sketch.Sketch.parse(sys.stdin.buffer)
sketch.serialize(sys.stdout.buffer)
