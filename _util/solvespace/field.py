# pyright: strict
import dataclasses as dc

from . import format as slvs_value
from . import subject as slvs_subject


@dc.dataclass
class Field:
    key: bytes
    subject: slvs_subject.Tag
    format: slvs_value.Tag


# https://github.com/solvespace/solvespace/blob/e7c0c1665f1684bb3195107147aaf254c852fa44/src/file.cpp#L87
def _generate_fields():
    fields: dict[bytes, Field] = {}
    raw = {
        b"Group.h.v": b"x",
        b"Group.type": b"d",
        b"Group.order": b"d",
        b"Group.name": b"S",
        b"Group.activeWorkplane.v": b"x",
        b"Group.opA.v": b"x",
        b"Group.opB.v": b"x",
        b"Group.valA": b"f",
        b"Group.valB": b"f",
        b"Group.valC": b"f",
        b"Group.color": b"c",
        b"Group.subtype": b"d",
        b"Group.skipFirst": b"b",
        b"Group.meshCombine": b"d",
        b"Group.forceToMesh": b"d",
        b"Group.predef.q.w": b"f",
        b"Group.predef.q.vx": b"f",
        b"Group.predef.q.vy": b"f",
        b"Group.predef.q.vz": b"f",
        b"Group.predef.origin.v": b"x",
        b"Group.predef.entityB.v": b"x",
        b"Group.predef.entityC.v": b"x",
        b"Group.predef.swapUV": b"b",
        b"Group.predef.negateU": b"b",
        b"Group.predef.negateV": b"b",
        b"Group.visible": b"b",
        b"Group.suppress": b"b",
        b"Group.relaxConstraints": b"b",
        b"Group.allowRedundant": b"b",
        b"Group.allDimsReference": b"b",
        b"Group.scale": b"f",
        b"Group.remap": b"M",
        b"Group.impFile": b"i",
        b"Group.impFileRel": b"P",
        b"Param.h.v.": b"x",  # wtf?
        b"Param.val": b"f",
        b"Request.h.v": b"x",
        b"Request.type": b"d",
        b"Request.extraPoints": b"d",
        b"Request.workplane.v": b"x",
        b"Request.group.v": b"x",
        b"Request.construction": b"b",
        b"Request.style": b"x",
        b"Request.str": b"S",
        b"Request.font": b"S",
        b"Request.file": b"P",
        b"Request.aspectRatio": b"f",
        b"Entity.h.v": b"x",
        b"Entity.type": b"d",
        b"Entity.construction": b"b",
        b"Entity.style": b"x",
        b"Entity.str": b"S",
        b"Entity.font": b"S",
        b"Entity.file": b"P",
        b"Entity.point[0].v": b"x",
        b"Entity.point[1].v": b"x",
        b"Entity.point[2].v": b"x",
        b"Entity.point[3].v": b"x",
        b"Entity.point[4].v": b"x",
        b"Entity.point[5].v": b"x",
        b"Entity.point[6].v": b"x",
        b"Entity.point[7].v": b"x",
        b"Entity.point[8].v": b"x",
        b"Entity.point[9].v": b"x",
        b"Entity.point[10].v": b"x",
        b"Entity.point[11].v": b"x",
        b"Entity.extraPoints": b"d",
        b"Entity.normal.v": b"x",
        b"Entity.distance.v": b"x",
        b"Entity.workplane.v": b"x",
        b"Entity.actPoint.x": b"f",
        b"Entity.actPoint.y": b"f",
        b"Entity.actPoint.z": b"f",
        b"Entity.actNormal.w": b"f",
        b"Entity.actNormal.vx": b"f",
        b"Entity.actNormal.vy": b"f",
        b"Entity.actNormal.vz": b"f",
        b"Entity.actDistance": b"f",
        b"Entity.actVisible": b"b",
        b"Constraint.h.v": b"x",
        b"Constraint.type": b"d",
        b"Constraint.group.v": b"x",
        b"Constraint.workplane.v": b"x",
        b"Constraint.valA": b"f",
        b"Constraint.valP.v": b"x",
        b"Constraint.ptA.v": b"x",
        b"Constraint.ptB.v": b"x",
        b"Constraint.entityA.v": b"x",
        b"Constraint.entityB.v": b"x",
        b"Constraint.entityC.v": b"x",
        b"Constraint.entityD.v": b"x",
        b"Constraint.other": b"b",
        b"Constraint.other2": b"b",
        b"Constraint.reference": b"b",
        b"Constraint.comment": b"S",
        b"Constraint.disp.offset.x": b"f",
        b"Constraint.disp.offset.y": b"f",
        b"Constraint.disp.offset.z": b"f",
        b"Constraint.disp.style": b"x",
        b"Style.h.v": b"x",
        b"Style.name": b"S",
        b"Style.width": b"f",
        b"Style.widthAs": b"d",
        b"Style.textHeight": b"f",
        b"Style.textHeightAs": b"d",
        b"Style.textAngle": b"f",
        b"Style.textOrigin": b"x",
        b"Style.color": b"c",
        b"Style.fillColor": b"c",
        b"Style.filled": b"b",
        b"Style.visible": b"b",
        b"Style.exportable": b"b",
        b"Style.stippleType": b"d",
        b"Style.stippleScale": b"f",
    }

    format_lookup = {fmt.value: fmt for fmt in slvs_value.Tag}
    subject_lookup = {subject.value: subject for subject in slvs_subject.Tag}

    for key, format_code in raw.items():
        subject_name, subject_key = key.split(b".", 1)
        fields[key] = Field(
            subject_key, subject_lookup[subject_name], format_lookup[format_code]
        )
    return fields


LOOKUP = _generate_fields()
