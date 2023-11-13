# pyright: strict

import typing
import dataclasses as dc

import os.path
from ..slvs import sketch as slvs_sketch
from ..slvs import format as slvs_value

from .parameter import Parameter


_DictAny = dict[typing.Any, typing.Any]


@dc.dataclass
class Config:
    source: str
    parameters: dict[str, Parameter]
    profiles: dict[str, dict[str, float]]

    @classmethod
    def parse(cls, config: dict[str, typing.Any]):
        assert config.keys() <= {"source", "parameter", "profile"}
        assert "source" in config

        source, parameters, profiles = (
            config["source"],
            config.get("parameter", {}),
            config.get("profile", {}),
        )
        assert isinstance(source, str), source
        assert isinstance(profiles, dict), profiles

        for name, profile in profiles.items():
            assert isinstance(name, str), name
            assert isinstance(profile, dict), profile

            for parameter, value in typing.cast(_DictAny, profile).items():
                assert isinstance(parameter, str), parameter
                assert isinstance(value, float), value

        return cls(
            source,
            Parameter.parse_parameters(parameters),
            typing.cast(dict[str, dict[str, float]], profiles),
        )

    def load_sketch(self, base: str):
        with open(os.path.join(base, self.source), "rb") as f:
            return slvs_sketch.Sketch.parse(f)

    def _validate_profile(self, profile: dict[str, float]):
        assert profile.keys() <= self.parameters.keys()
        for name, parameter in self.parameters.items():
            assert name in profile or parameter.default is not None

    def validate(self, sketch: slvs_sketch.Sketch):
        for profile in self.profiles.values():
            self._validate_profile(profile)
        for parameter in self.parameters.values():
            parameter.validate(sketch)

    def _apply_profile(
        self,
        profile: dict[str, float],
        sketch: slvs_sketch.Sketch,
    ) -> slvs_sketch.Sketch:
        constraints = {**sketch.constraints}
        for name, parameter in self.parameters.items():
            value = profile.get(name, parameter.default)
            assert value is not None
            constraints[parameter.constraint] = constraints[
                parameter.constraint
            ].replace_float(parameter.key, value)
        return dc.replace(sketch, constraints=constraints)

    def apply(self, sketch: slvs_sketch.Sketch):
        return {
            name: self._apply_profile(profile, sketch)
            for name, profile in self.profiles.items()
        }
