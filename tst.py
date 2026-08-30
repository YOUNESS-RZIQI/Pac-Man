class Cell:
    def __init__(self, north, east, south, west, is_42):
        self.north, self.east, self.south, self.west, self.is_42 = north, east, south, west, is_42

gride = [
[Cell(north=True, east=False, south=False, west=True, is_42=False), Cell(north=True, east=False, south=False, west=False, is_42=False), Cell(north=True, east=True, south=True, west=False, is_42=False)], 
[Cell(north=False, east=True, south=False, west=True, is_42=False), Cell(north=False, east=False, south=True, west=True, is_42=False), Cell(north=True, east=True, south=False, west=False, is_42=False)], 
[Cell(north=False, east=False, south=True, west=True, is_42=False), Cell(north=True, east=False, south=True, west=False, is_42=False), Cell(north=False, east=True, south=True, west=False, is_42=False)]
]


#   All Screens:
# 
#       1) Main Screan:
#
#                  * 
#
#
#
#
#
#
#
#
#
#
#
#