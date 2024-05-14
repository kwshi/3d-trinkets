module Main where

import Graphics.Implicit
import Lib

ball :: SymbolicObj3
ball = rect3R 0 (0, 0, 0) (3, 4, 5)

main :: IO ()
main = writeSTL 0.1 "test.stl" ball
