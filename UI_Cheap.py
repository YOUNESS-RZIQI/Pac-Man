from dataclasses import dataclass

@dataclass
class Cell:
    north: bool
    east: bool
    south: bool
    west: bool
    is_42: bool


gride = [
[Cell(north=True, east=False, south=False, west=True), Cell(north=True, east=False, south=False, west=False), Cell(north=True, east=True, south=True, west=False)], 
[Cell(north=False, east=True, south=False, west=True), Cell(north=False, east=False, south=True, west=True), Cell(north=True, east=True, south=False, west=False)], 
[Cell(north=False, east=False, south=True, west=True), Cell(north=True, east=False, south=True, west=False), Cell(north=False, east=True, south=True, west=False)]
]


#   All Screens:
# 
#       1) Game View Screen:
#
#                  * 
#
#
#       2) Main Menu Screen:
#
#
#
#
#
#       3)  Game-over Screen: 
#
#
#