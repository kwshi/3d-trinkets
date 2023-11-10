import typing
from . import format


class Group(typing.TypedDict, total=False):
    h_v: format.Hex
    type: format.Int
    order: format.Int
    name: format.Str
    activeWorkplane_v: format.Hex
    opA_v: format.Hex
    opB_v: format.Hex
    valA: format.Float
    valB: format.Float
    valC: format.Float
    color: format.Color
    subtype: format.Int
    skipFirst: format.Bool
    meshCombine: format.Int
    forceToMesh: format.Int
    predef_q_w: format.Float
    predef_q_vx: format.Float
    predef_q_vy: format.Float
    predef_q_vz: format.Float
    predef_origin_v: format.Hex
    predef_entityB_v: format.Hex
    predef_entityC_v: format.Hex
    predef_swapUV: format.Bool
    predef_negateU: format.Bool
    predef_negateV: format.Bool
    visible: format.Bool
    suppress: format.Bool
    relaxConstraints: format.Bool
    allowRedundant: format.Bool
    allDimsReference: format.Bool
    scale: format.Float
    remap: format.EntityMap
    impFile: None
    impFileRel: str
