base_spacing = 4;
base_thickness = 8;
base_chamfer_top = 2;
base_chamfer_bottom = 1;
pillar_radius = 4;
pillar_gap = .5;
pillar_chamfer = 1;
layout_spacing = 3;

disk_radii = [9, 12, 15, 18, 21, 24];
disk_thickness = 4;
disk_gap = .5;
disk_chamfer = 1;

function accumulate(l, i=0, acc=[0])
  = i == len(l) ? acc : accumulate(l, i+1, concat(acc, [acc[len(acc)-1] + l[i]]));


pillar_height = len(disk_radii) * (disk_thickness+disk_gap) + disk_chamfer;
_max_radius = max(disk_radii);
_disk_inner_radius = pillar_radius + pillar_gap;
_disk_radii_accumulate = accumulate(disk_radii);


assert(base_spacing > base_chamfer_top);
assert(_disk_inner_radius + 2 * disk_chamfer < min(disk_radii));

$fn = 24;

module mirror_copy(v) {
  children();
  mirror(v) children();
}

module per_pillar() {
  children();
  mirror_copy([1, 0])
  translate([disk_radii[len(disk_radii)-2]+disk_radii[len(disk_radii)-1]+base_spacing, 0])
    children();
}

module base() {
  hull()
    per_pillar() 
      rotate_extrude()
      polygon([
       [0,0],
       [_max_radius+base_spacing-base_chamfer_bottom, 0],
       [_max_radius+base_spacing, base_chamfer_bottom],
       [_max_radius+base_spacing, base_thickness-base_chamfer_top],
       [_max_radius+base_spacing-base_chamfer_top, base_thickness],
       [0, base_thickness],
      ]);
  
  per_pillar()
  rotate_extrude()
  polygon([
    [0, 0],
    [pillar_radius+pillar_chamfer,base_thickness],
    [pillar_radius,base_thickness+pillar_chamfer],
    [pillar_radius,base_thickness+pillar_height-pillar_chamfer],
    [pillar_radius-pillar_chamfer,base_thickness+pillar_height],
    [0, base_thickness+pillar_height],
  ]);
}


module disk(radius) {
  rotate_extrude()
  polygon([
    [_disk_inner_radius, disk_chamfer],
    [_disk_inner_radius+disk_chamfer, 0],
    [radius-disk_chamfer, 0],
    [radius, disk_chamfer],
    [radius, disk_thickness-disk_chamfer],
    [radius-disk_chamfer, disk_thickness],
    [_disk_inner_radius+disk_chamfer, disk_thickness],
    [_disk_inner_radius, disk_thickness-disk_chamfer],
  ]);
}


translate([0, _max_radius+base_spacing+layout_spacing])
base();

//translate([0, -disk_radii[0]]) disk(disk_radii[0]);
//translate([disk_radii[0]+disk_radii[2], -disk_radii[2]]) disk(disk_radii[2]);
//translate([disk_radii[0]+2*disk_radii[2]+disk_radii[4], -disk_radii[4]]) disk(disk_radii[4]);
//
//translate([-disk_radii[0], -2*disk_radii[0]-disk_radii[5]]) disk(disk_radii[5]);
//translate([-disk_radii[0]+disk_radii[5]+disk_radii[3], -2*disk_radii[2]-disk_radii[3]]) disk(disk_radii[3]);

//disk(disk_radii[0]);
//translate([disk_radii[0]+disk_radii[2], 0]) disk(disk_radii[2]);
//translate([disk_radii[0]+2*disk_radii[2]+disk_radii[4], 0]) disk(disk_radii[4]);

echo(_disk_radii_accumulate);
translate(-[_disk_radii_accumulate[len(disk_radii)]+layout_spacing*(len(disk_radii)-1)/2, 0])
for (i = [0:len(disk_radii)-1])
translate([_disk_radii_accumulate[i]+_disk_radii_accumulate[i+1]+i*layout_spacing, -disk_radii[i]])
  disk(disk_radii[i]);
