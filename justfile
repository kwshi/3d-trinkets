set positional-arguments := true

build-solvespace path:
  python -m script.solvespace {{quote(invocation_directory())}}/"$1"
