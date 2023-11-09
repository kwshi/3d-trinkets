import enum
import typing
import dataclasses as dc


# https://github.com/solvespace/solvespace/blob/e7c0c1665f1684bb3195107147aaf254c852fa44/src/file.cpp#L212
class Tag(enum.Enum):
    ENTITY_MAP = "M"
    STR = "S"
    PATH = "P"
    BOOL = "b"
    COLOR = "c"
    INT = "d"
    FLOAT = "f"
    HEX = "x"
    # https://github.com/solvespace/solvespace/blob/e7c0c1665f1684bb3195107147aaf254c852fa44/src/file.cpp#L456
    IGNORE = "i"


@dc.dataclass
class Hex:
    value: int

    def serialize(self):
        return f"{self.value:08x}"


@dc.dataclass
class Int:
    value: int

    def serialize(self):
        return f"{self.value}"


@dc.dataclass
class Str:
    value: str

    def serialize(self):
        return self.value


@dc.dataclass
class Float:
    value: float

    def serialize(self):
        return f"{self.value}"


@dc.dataclass
class Bool:
    value: bool

    def serialize(self):
        return f"{int(self.value)}"


@dc.dataclass
class Color:
    value: int

    def serialize(self):
        return f"{self.value:08x}"


@dc.dataclass
class Path:
    value: str

    def serialize(self):
        return self.value


@dc.dataclass
class EntityMap:
    # save file format:
    # `{` on first line,
    # then `%d %08x %d` for each item,
    # then `}` on single line
    data: list[tuple[int, int, int]]

    def serialize(self):
        return "{{\n{}\n}}".format(
            "\n".join(f"{a} {b:08x} {c}" for a, b, c in self.data)
        )


@dc.dataclass
class Ignore:
    pass


Value = typing.Union[EntityMap, Str, Path, Bool, Color, Int, Float, Hex, Ignore]


def parse_value(tag: Tag, first_line: bytes, lines: typing.BinaryIO) -> Value:
    match tag:
        case Tag.HEX:
            return Hex(int(first_line, 16))
        case Tag.INT:
            return Int(int(first_line))
        case Tag.STR:
            return Str(first_line.decode())
        case Tag.BOOL:
            return Bool(bool(int(first_line)))
        case Tag.FLOAT:
            return Float(float(first_line))
        case Tag.COLOR:
            return Color(int(first_line, 16))
        case Tag.ENTITY_MAP:
            data: list[tuple[int, int, int]] = []
            for line in lines:
                if line.rstrip() == b"}":
                    break
                a, b, c = line.split()
                data.append((int(a), int(b, 16), int(c)))
            return EntityMap(data)
        case _:
            return Ignore()
