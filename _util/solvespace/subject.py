# pyright: strict
import enum


class Tag(enum.Enum):
    GROUP = b"Group"
    PARAM = b"Param"
    REQUEST = b"Request"
    ENTITY = b"Entity"
    CONSTRAINT = b"Constraint"
    STYLE = b"Style"
