set positional-arguments := true

build-solvespace path:
  python -m script.solvespace {{quote(invocation_directory())}}/"$1"

build-openscad path:
  python -m script.openscad {{quote(invocation_directory())}}/"$1"
