# pyright: strict
import typing
import dataclasses as dc

from . import format as slvs_value
from . import subject as slvs_subject


@dc.dataclass(frozen=True)
class Record:
    id: int
    data: dict[bytes, slvs_value.Value]

    def replace(self, key: bytes, value: slvs_value.Value):
        original = self.data[key]
        if type(value) != type(original):
            raise TypeError(f'original {original}: {type(original)}; replacement {value}: {type(value)}')

        return Record(self.id, {**self.data, key: value})

    def serialize(self, subject: slvs_subject.Tag, out: typing.BinaryIO):
        for key, value in self.data.items():
            out.write(subject.value)
            out.write(b".")
            out.write(key)
            out.write(b"=")
            value.serialize(out)
            out.write(b"\n")


class Partial:
    data: dict[bytes, slvs_value.Value]

    def __init__(self):
        self.data = {}

    def finalize(self) -> Record:
        # https://github.com/solvespace/solvespace/blob/e7c0c1665f1684bb3195107147aaf254c852fa44/src/file.cpp#L123
        id = self.data.get(b"h.v", self.data.get(b"h.v."))
        assert isinstance(id, slvs_value.Hex), self.data
        return Record(id.value, self.data)
