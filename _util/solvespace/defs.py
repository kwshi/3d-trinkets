import enum
import dataclasses as dc

from . import format


class Subject(enum.Enum):
    GROUP = "g"
    PARAM = "p"
    REQUEST = "r"
    ENTITY = "e"
    CONSTRAINT = "c"
    STYLE = "s"


@dc.dataclass
class Field:
    key: str
    subject: Subject
    format: format.Tag


# https://github.com/solvespace/solvespace/blob/e7c0c1665f1684bb3195107147aaf254c852fa44/src/file.cpp#L87
def _generate_fields():
    fields: dict[str, Field] = {}
    raw = {
        "Group.h.v": "x",
        "Group.type": "d",
        "Group.order": "d",
        "Group.name": "S",
        "Group.activeWorkplane.v": "x",
        "Group.opA.v": "x",
        "Group.opB.v": "x",
        "Group.valA": "f",
        "Group.valB": "f",
        "Group.valC": "f",
        "Group.color": "c",
        "Group.subtype": "d",
        "Group.skipFirst": "b",
        "Group.meshCombine": "d",
        "Group.forceToMesh": "d",
        "Group.predef.q.w": "f",
        "Group.predef.q.vx": "f",
        "Group.predef.q.vy": "f",
        "Group.predef.q.vz": "f",
        "Group.predef.origin.v": "x",
        "Group.predef.entityB.v": "x",
        "Group.predef.entityC.v": "x",
        "Group.predef.swapUV": "b",
        "Group.predef.negateU": "b",
        "Group.predef.negateV": "b",
        "Group.visible": "b",
        "Group.suppress": "b",
        "Group.relaxConstraints": "b",
        "Group.allowRedundant": "b",
        "Group.allDimsReference": "b",
        "Group.scale": "f",
        "Group.remap": "M",
        "Group.impFile": "i",
        "Group.impFileRel": "P",
        "Param.h.v.": "x",
        "Param.val": "f",
        "Request.h.v": "x",
        "Request.type": "d",
        "Request.extraPoints": "d",
        "Request.workplane.v": "x",
        "Request.group.v": "x",
        "Request.construction": "b",
        "Request.style": "x",
        "Request.str": "S",
        "Request.font": "S",
        "Request.file": "P",
        "Request.aspectRatio": "f",
        "Entity.h.v": "x",
        "Entity.type": "d",
        "Entity.construction": "b",
        "Entity.style": "x",
        "Entity.str": "S",
        "Entity.font": "S",
        "Entity.file": "P",
        "Entity.point[0].v": "x",
        "Entity.point[1].v": "x",
        "Entity.point[2].v": "x",
        "Entity.point[3].v": "x",
        "Entity.point[4].v": "x",
        "Entity.point[5].v": "x",
        "Entity.point[6].v": "x",
        "Entity.point[7].v": "x",
        "Entity.point[8].v": "x",
        "Entity.point[9].v": "x",
        "Entity.point[10].v": "x",
        "Entity.point[11].v": "x",
        "Entity.extraPoints": "d",
        "Entity.normal.v": "x",
        "Entity.distance.v": "x",
        "Entity.workplane.v": "x",
        "Entity.actPoint.x": "f",
        "Entity.actPoint.y": "f",
        "Entity.actPoint.z": "f",
        "Entity.actNormal.w": "f",
        "Entity.actNormal.vx": "f",
        "Entity.actNormal.vy": "f",
        "Entity.actNormal.vz": "f",
        "Entity.actDistance": "f",
        "Entity.actVisible": "b",
        "Constraint.h.v": "x",
        "Constraint.type": "d",
        "Constraint.group.v": "x",
        "Constraint.workplane.v": "x",
        "Constraint.valA": "f",
        "Constraint.valP.v": "x",
        "Constraint.ptA.v": "x",
        "Constraint.ptB.v": "x",
        "Constraint.entityA.v": "x",
        "Constraint.entityB.v": "x",
        "Constraint.entityC.v": "x",
        "Constraint.entityD.v": "x",
        "Constraint.other": "b",
        "Constraint.other2": "b",
        "Constraint.reference": "b",
        "Constraint.comment": "S",
        "Constraint.disp.offset.x": "f",
        "Constraint.disp.offset.y": "f",
        "Constraint.disp.offset.z": "f",
        "Constraint.disp.style": "x",
        "Style.h.v": "x",
        "Style.name": "S",
        "Style.width": "f",
        "Style.widthAs": "d",
        "Style.textHeight": "f",
        "Style.textHeightAs": "d",
        "Style.textAngle": "f",
        "Style.textOrigin": "x",
        "Style.color": "c",
        "Style.fillColor": "c",
        "Style.filled": "b",
        "Style.visible": "b",
        "Style.exportable": "b",
        "Style.stippleType": "d",
        "Style.stippleScale": "f",
    }

    format_lookup = {fmt.value: fmt for fmt in format.Tag}
    subject_lookup = {subject.value: subject for subject in Subject}

    for key, format_code in raw.items():
        fields[key] = Field(
            key, subject_lookup[key[0].lower()], format_lookup[format_code]
        )
    return fields


fields = _generate_fields()
