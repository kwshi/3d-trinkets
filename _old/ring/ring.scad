include <lib.scad>

PATTERN = "-... .- ---";
//PATTERN = "- - -";

UNIT_DOT = .75;
UNIT_DASH = 1.5;
UNIT_SPACE = .5;
UNIT_SEP = .75;
UNIT_END = 3; // 1.25

// radius of ring
RADIUS = 7;

THICKNESS = 1;
EPS = 1e-3;

// ratio of segment width to unit length
ASPECT = 2;

// ratio of supporting spine to segment width
//SPINE = 1/2;
SPINE = 2/3;

N_RING = 128;

BEVEL = .25;


sizes = [for (c = PATTERN) (c == "." ? UNIT_DOT : c == "-" ? UNIT_DASH : UNIT_SPACE) + UNIT_SEP];
acc_sizes = accumulate(sizes);
total = sum(sizes) + UNIT_END;
width = 2*PI*RADIUS/total * ASPECT;
spine = SPINE * width;

poly_seg = function(u) [
  //[0, 0],
  //[(RADIUS+THICKNESS) * tan(360/total * u), 0],
  //[(RADIUS+THICKNESS) * tan(360/total * u), width/2],
  ////[(1-SPINE)*width/2, width/2],
  ////[0, SPINE*width/2-BEVEL],
  //[BEVEL, width/2],
  //[0, width/2-BEVEL],

  [0, 0],
  [RADIUS * tan(360/total * u) + width/2, 0],
  [RADIUS * tan(360/total * u), width/2],
  [BEVEL, width/2],
  [0, width/2-BEVEL],
];

poly_prof = function(x) let(w = x*width) [
  [RADIUS, -w/2+BEVEL], [RADIUS+BEVEL, -w/2],
  [RADIUS+THICKNESS-BEVEL, -w/2], [RADIUS+THICKNESS, -w/2+BEVEL],
  [RADIUS+THICKNESS, +w/2-BEVEL], [RADIUS+THICKNESS-BEVEL, +w/2],
  [RADIUS+BEVEL, +w/2], [RADIUS, +w/2-BEVEL],
];

echo(sizes);
echo(acc_sizes);


module prof(x) {
  rotate_extrude($fn=N_RING) polygon(poly_prof(x));
}

module segments_slanted() {
  for (i = [0:len(sizes)-1])
    if (PATTERN[i] != " ")
      rotate([90, 0, acc_sizes[i] / total * 360])
        linear_extrude(RADIUS+THICKNESS+EPS) {
          unit = PATTERN[i] == "." ? UNIT_DOT : UNIT_DASH;
          polygon(poly_seg(unit));
        }
}

module segments_male() {
  for (i = [0:len(sizes)-1])
    if (PATTERN[i] != " ")
      hull() {
        cylinder(r=EPS, h=(1+SPINE)*width/4);
        rotate([90, 0, acc_sizes[i] / total * 360]) {
          unit = PATTERN[i] == "." ? UNIT_DOT : UNIT_DASH;
          translate([0, 0, RADIUS+THICKNESS+EPS])
            linear_extrude(EPS)
            polygon(poly_seg(unit));
        }
      }
}

module segments_female() {
  for (i = [0:len(sizes)-1])
    if (PATTERN[i] != " ")
      hull() {
        cylinder(r=EPS, h=(1+SPINE)*width/4);
        rotate([90, 0, acc_sizes[i] / total * 360]) {
          unit = PATTERN[i] == "." ? UNIT_DOT : UNIT_DASH;
          translate([0, 0, RADIUS+THICKNESS+EPS])
            linear_extrude(EPS)
            polygon(poly_seg(unit));
        }
      }
}

module ring_symmetric() {
  prof(SPINE);
  intersection() {
    prof(1);
    mirror_copy([0, 0, 1]) segments_slanted();
  }
}

module ring_male() {
  prof(SPINE);
  intersection() {
    prof(1);
    segments_male();
  }
}

module ring_female() {
  prof(SPINE);
  intersection() {
    prof(1);
    segments_female();
  }
}

ring_symmetric();
//ring_male();
//ring_female();

//translate([0, 0, width]) rotate([180, 0, 0]) ring_female();
