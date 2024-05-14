accumulate = function(a) [
  for (
      i = 0, acc = 0;
      i < len(a);
      acc = acc + a[i], i = i + 1
      ) acc
];

sum = function(v) [for (_ = v) 1] * v;

module mirror_copy(v) {
  children();
  mirror(v) children();
}
