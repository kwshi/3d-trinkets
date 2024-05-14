const = function(a) function(_) a;

map = function(f) function(list) [for (a = list) f(a)];

foldl = function(f, init, start=0) function(list)
  let (go = function(i, acc) i < len(list) ? go(i+1, f(acc, list[i])) : acc)
  go(start, init);

foldl1 = function(f, default=undef) function(list)
  len(list) == 0 ? default : foldl(f, list[0], start=1)(list);

scanl = function(f, init, start=0) function(list)
  let (go = function(i, acc, accs)
    i < len(list)
    ? let (next = f(acc, list[i])) go(i+1, next, concat(accs, [next]))
    : accs
  )
  go(start, init, []);

scanl1 = function(f) function(list)
  len(list) == 0 ? [] : concat([list[0]], scanl(f, list[0], start=1)(list));

sum = foldl1(function(a, b) a+b);
sums = scanl1(function(a, b) a+b);
