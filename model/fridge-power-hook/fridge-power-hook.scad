include <../lib/list.scad>

thickness = 3;
anchor = 50;
depth = 25;
width = 42.5;
chamfer = 5;
length = 30;

linear_extrude(height=length) {
  difference() {
    polygon(sums([
      [0, 0],
      [anchor, 0],
      thickness/2 * [1, 1],
      thickness/2 * [-1, 1],
      [-anchor-thickness/2, 0],
      thickness/2 * [-1, -1],
      [0, thickness/2-depth+chamfer],
      chamfer * [-1, -1],
      [-width+2*chamfer, 0],
      chamfer * [-1, 1],
      [0, depth-chamfer-thickness/2],
      thickness/2 * [-1, 1],
      [-thickness/4, 0],
      thickness/4 * [-1, -1],
      [0, -3*thickness/4-depth+chamfer],
      (thickness + width) * [1, -1],
      [thickness/2, 0],
      thickness/2 * [1, 1],
    ]));
    polygon(sums([
      [-2*thickness, -depth],
      [-width+chamfer+3*thickness, 0],
      thickness/2 * [-1, -1],
      (width-chamfer-2*thickness) * [1, -1],
      thickness/2 * [1, 1],
      [0, width-chamfer-3*thickness],
    ]));
  }
}
