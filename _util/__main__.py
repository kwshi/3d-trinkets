import sys
import typing
import dataclasses as dc

from .solvespace import defs
from .solvespace import format

Record = dict[str, format.Value]


@dc.dataclass
class SlvsSketch:
    groups: list[Record]
    params: list[typing.Any]
    entities: list[typing.Any]
    constraints: list[Record]
    requests: list[Record]
    styles: list[Record]


def parse_slvs(lines: typing.BinaryIO) -> SlvsSketch:
    version_string = lines.readline().rstrip()
    assert version_string == b"\xb1\xb2\xb3SolveSpaceREVa"

    sketch = SlvsSketch([], [], [], [], [], [])
    buffer: dict[defs.Subject, Record] = {subject: {} for subject in defs.Subject}

    for line in lines:
        if not line.rstrip():
            continue

        # TODO use split and match
        pos = line.find(b"=")
        if pos != -1:
            # record entry
            key = line[:pos].decode()
            field = defs.fields[key]
            value = format.parse_value(field.format, line[pos + 1 :], lines)
            buffer[field.subject][key] = value
        else:
            match line.rstrip():
                case b"AddGroup":
                    sketch.groups.append(buffer[defs.Subject.GROUP])
                    buffer[defs.Subject.GROUP] = {}
                case b"AddParam":
                    sketch.params.append(buffer[defs.Subject.PARAM])
                    buffer[defs.Subject.PARAM] = {}
                case b"AddRequest":
                    sketch.requests.append(buffer[defs.Subject.REQUEST])
                    buffer[defs.Subject.REQUEST] = {}
                case b"AddEntity":
                    sketch.entities.append(buffer[defs.Subject.ENTITY])
                    buffer[defs.Subject.ENTITY] = {}
                case b"AddConstraint":
                    sketch.entities.append(buffer[defs.Subject.CONSTRAINT])
                    buffer[defs.Subject.CONSTRAINT] = {}
                case _:
                    if (
                        line.startswith(b"Surface ")
                        or line.startswith(b"SCtrl ")
                        or line.startswith(b"TrimBy ")
                        or line.startswith(b"AddSurface")
                        or line.startswith(b"Curve ")
                        or line.startswith(b"CCtrl ")
                        or line.startswith(b"CurvePt ")
                        or line.startswith(b"AddCurve")
                    ):
                        continue
                    print(line)
                    assert False

    return sketch


print(parse_slvs(sys.stdin.buffer))
