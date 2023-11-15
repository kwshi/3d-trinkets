# pyright: strict
import typing
import dataclasses as dc

from ..slvs.sketch import Sketch
from ..slvs import format as slvs_value

_DEFAULT_KEY = b"valA"


@dc.dataclass(frozen=True)
class Parameter:
    constraint: int
    key: bytes
    default: float | None

    def validate(self, sketch: Sketch):
        constraint = sketch.constraints[self.constraint]
        assert isinstance(constraint.data[_DEFAULT_KEY], slvs_value.Float)

    @classmethod
    def parse(cls, data: typing.Any):
        assert isinstance(data, dict), data
        data = typing.cast(dict[typing.Any, typing.Any], data)
        assert data.keys() <= {"constraint", "key", "default"}, data.keys()

        assert "constraint" in data
        constraint = data["constraint"]
        assert isinstance(constraint, int)

        key = data.get("key", "valA")
        assert isinstance(key, str), key

        default = data.get("default", None)
        assert isinstance(default, float | int | None)

        return cls(
            constraint, key.encode(), None if default is None else float(default)
        )

    @classmethod
    def parse_parameters(cls, parameters: typing.Any) -> dict[str, typing.Self]:
        assert isinstance(parameters, dict), parameters

        result: dict[str, typing.Self] = {}
        for name, parameter in typing.cast(
            dict[typing.Any, typing.Any], parameters
        ).items():
            assert isinstance(name, str), name
            parameter = cls.parse(parameter)
            result[name] = parameter

        return result
