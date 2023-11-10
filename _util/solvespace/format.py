# pyright: strict
import enum
import typing
import dataclasses as dc
import abc


# https://github.com/solvespace/solvespace/blob/e7c0c1665f1684bb3195107147aaf254c852fa44/src/file.cpp#L212
class Tag(enum.Enum):
    ENTITY_MAP = b"M"
    STR = b"S"
    PATH = b"P"
    BOOL = b"b"
    COLOR = b"c"
    INT = b"d"
    FLOAT = b"f"
    HEX = b"x"
    # https://github.com/solvespace/solvespace/blob/e7c0c1665f1684bb3195107147aaf254c852fa44/src/file.cpp#L456
    IGNORE = b"i"


class Value(abc.ABC):
    @abc.abstractmethod
    def serialize(self, out: typing.BinaryIO, /) -> None:
        ...

    @classmethod
    @abc.abstractmethod
    def parse(cls, first_line: bytes, lines: typing.Iterator[bytes], /) -> typing.Self:
        ...


@dc.dataclass
class Hex(Value):
    value: int

    def serialize(self, out: typing.BinaryIO):
        out.write(f"{self.value:08x}".encode())

    @classmethod
    def parse(cls, first_line: bytes, _: typing.Iterator[bytes]):
        return cls(int(first_line, 16))


@dc.dataclass
class Int(Value):
    value: int

    def serialize(self, out: typing.BinaryIO):
        out.write(f"{self.value}".encode())

    @classmethod
    def parse(cls, first_line: bytes, _: typing.Iterator[bytes]):
        return cls(int(first_line))


@dc.dataclass
class Str(Value):
    value: bytes

    def serialize(self, out: typing.BinaryIO):
        out.write(self.value)

    @classmethod
    def parse(cls, first_line: bytes, _: typing.Iterator[bytes]):
        return cls(first_line)


@dc.dataclass
class Float(Value):
    value: float

    def serialize(self, out: typing.BinaryIO):
        out.write(f"{self.value}".encode())

    @classmethod
    def parse(cls, first_line: bytes, _: typing.Iterator[bytes]):
        return cls(float(first_line))


@dc.dataclass
class Bool(Value):
    value: bool

    def serialize(self, out: typing.BinaryIO):
        out.write(f"{int(self.value)}".encode())

    @classmethod
    def parse(cls, first_line: bytes, _: typing.Iterator[bytes]):
        return cls(bool(int(first_line)))


@dc.dataclass
class Color(Value):
    value: int

    def serialize(self, out: typing.BinaryIO):
        out.write(f"{self.value:08x}".encode())

    @classmethod
    def parse(cls, first_line: bytes, _: typing.Iterator[bytes]):
        return cls(int(first_line, 16))


@dc.dataclass
class Path(Value):
    value: bytes

    def serialize(self, out: typing.BinaryIO):
        out.write(self.value)

    @classmethod
    def parse(cls, first_line: bytes, _: typing.Iterator[bytes]):
        return cls(first_line)


@dc.dataclass
class EntityMap(Value):
    # save file format:
    # `{` on first line,
    # then `%d %08x %d` for each item,
    # then `}` on single line
    data: list[tuple[int, int, int]]

    def serialize(self, out: typing.BinaryIO):
        out.write(b"{\n")
        for a, b, c in self.data:
            out.write(f"{a} {b:08x} {c}\n".encode())
        out.write(b"}")

    @classmethod
    def parse(cls, first_line: bytes, lines: typing.Iterator[bytes]):
        assert first_line.rstrip() == b"{"
        data: list[tuple[int, int, int]] = []
        for line in lines:
            if line.rstrip() == b"}":
                break
            a, b, c = line.split()
            data.append((int(a), int(b, 16), int(c)))
        return cls(data)


@dc.dataclass
class Ignore(Value):
    def serialize(self, _: typing.BinaryIO):
        pass

    @classmethod
    def parse(cls, _first_line: bytes, _: typing.Iterator[bytes]):
        return cls()


BY_TAG: dict[Tag, type[Value]] = {
    Tag.HEX: Hex,
    Tag.INT: Int,
    Tag.STR: Str,
    Tag.BOOL: Bool,
    Tag.FLOAT: Float,
    Tag.COLOR: Color,
    Tag.ENTITY_MAP: EntityMap,
    Tag.IGNORE: Ignore,
    Tag.PATH: Path,
}
