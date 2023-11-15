# pyright: strict
import typing
import dataclasses as dc


@dc.dataclass
class Parameter:
    Value = int | float | bool | str | list["Value"]
    default: Value | None

    @classmethod
    def parse(cls, data: typing.Any):
        assert isinstance(data, dict)
        data = typing.cast(dict[typing.Any, typing.Any], data)
        assert data.keys() <= {"default"}

        default = data.get("default", None)
        if default is not None:
            assert cls.check_value(default)
        return cls(default)

    @classmethod
    def parse_parameters(cls, data: typing.Any):
        assert isinstance(data, dict)
        data = typing.cast(dict[typing.Any, typing.Any], data)

        result: dict[str, cls] = {}
        for key, parameter_data in data.items():
            assert isinstance(key, str)
            parameter = cls.parse(parameter_data)
            result[key] = parameter

        return result

    @classmethod
    def check_value(cls, data: typing.Any) -> typing.TypeGuard[Value]:
        match data:
            case int() | float() | bool() | str():
                return True
            case list():
                return all(map(cls.check_value, typing.cast(list[typing.Any], data)))
            case _:
                return False

    @classmethod
    def serialize_value(cls, value: Value):
        match value:
            case True:
                return "true"
            case False:
                return "false"
            case int() | float():
                return f"{value}"
            case str():
                return value
            case list():
                return f'[{",".join(map(cls.serialize_value, value))}]'


class OpenSCADParameters(typing.TypedDict):
    parameterSets: dict[str, dict[str, str]]
    fileFormatVersion: str


@dc.dataclass
class Config:
    source: str
    parameters: dict[str, Parameter]
    profiles: dict[str, dict[str, Parameter.Value]]

    @classmethod
    def parse(cls, data: typing.Any):
        assert isinstance(data, dict)
        data = typing.cast(dict[typing.Any, typing.Any], data)
        assert data.keys() <= {"source", "parameter", "profile"}
        assert {"source"} <= data.keys()

        source = data["source"]
        assert isinstance(source, str)

        parameters = Parameter.parse_parameters(data.get("parameter", {}))

        profiles = data.get("profile", {})
        assert cls.check_profiles(profiles, parameters)
        return cls(source, parameters, profiles)

    @staticmethod
    def check_profile(
        data: typing.Any,
        parameters: dict[str, Parameter],
    ) -> typing.TypeGuard[dict[str, Parameter.Value]]:
        return (
            isinstance(data, dict)
            and all(
                isinstance(key, str) and Parameter.check_value(value)
                for key, value in typing.cast(
                    dict[typing.Any, typing.Any], data
                ).items()
            )
            and all(
                parameter.default is not None or name in data
                for name, parameter in parameters.items()
            )
        )

    @classmethod
    def check_profiles(
        cls,
        data: typing.Any,
        parameters: dict[str, Parameter],
    ) -> typing.TypeGuard[dict[str, dict[str, Parameter.Value]]]:
        return isinstance(data, dict) and all(
            isinstance(key, str) and cls.check_profile(value, parameters)
            for key, value in typing.cast(dict[typing.Any, typing.Any], data).items()
        )

    def generate_openscad_parameters(self) -> OpenSCADParameters:
        return {
            "parameterSets": {
                name: {
                    key: Parameter.serialize_value(
                        typing.cast(
                            Parameter.Value, profile.get(key, parameter.default)
                        )
                    )
                    for key, parameter in self.parameters.items()
                }
                for name, profile in self.profiles.items()
            },
            "fileFormatVersion": "1",
        }
