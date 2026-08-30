A-Maze-ing
==========
_This project has been created as part of the 42 curriculum by amelhach, yrziqi._


Description
-----------

A-Maze-ing is a Python project that generates and solves mazes.The goal of the project is to build a reliable maze generator capable of producing valid maze structures, optionally including multiple paths, and computing a short  solution path between an entry and an exit.

The maze is internally represented as a grid of cells where each cell contains four walls (north, east, south, west).The generator builds the maze using a graph traversal algorithm and guarantees connectivity between cells.

The project also includes a reusable Python module that allows the maze generator to be imported and used in future projects.

Main features:

*   Maze generation
    
*   Entry and exit management
    
*   Optional perfect maze generation
    
*   Pathfinding solution
    
*   Export of maze structure
    
*   Reusable Python package
    

Instructions
============

Requirements
------------

*   Python **3.10+**
    
*   pip
    
*   virtualenv (recommended)
    

Installation
------------

Create a virtual environment and activate:

`   python3 -m venv MAZE        `

`   source MAZE/bin/activate    `

Install the package:

`   pip install mazegen-1.0.0-py3-none-any.whl   `

or

`   pip install mazegen-1.0.0.tar.gz   `

Basic Usage
-----------

Example of generating a maze:

`   from mazegen.maze import MazeGenerator   `

`   maze = MazeGenerator(    width=20,    height=20,    entry=(0, 0),    exit=(19, 19),    perfect=True,    seed=42)    `

`   maze.generate()   `

Accessing the Maze Structure
----------------------------

The generated maze structure is accessible through the grid attribute.

Example:

`   for row in maze.grid:   `

`    print(row)   `

Each cell contains:

*   north
    
*   east
    
*   south
    
*   west
    
*   is\_42
    

Example:

`   cell = maze.grid[0][0]`

`print(cell.north)`

`print(cell.east) `

`print(cell.south)`

`print(cell.west)   `

Accessing the Solution
----------------------

The generator also allows access to a valid solution path.

Example:

`    path = maze.bfs_shortest_path() `

`    print(path)   `

Example output:

`   [(0,0), (1,0), (1,1), (2,1), ...]   `

Custom Parameters
-----------------

The generator supports multiple parameters:

 Parameter | Description

\--------- | -----------

   width   | Maze width
 
   height  | Maze height
 
   entry   | Entry coordinates
 
   exit    | Exit coordinates
 
  perfect  | Generate a perfect maze
 
   seed    | Random seed

Example:

`   maze = MazeGenerator(width=30,    height=30,    entry=(0,0),    exit=(29,29),    perfect=False,    seed=123)   `

Configuration File Structure
============================

The configuration file allows customization of maze generation.

Example format:

`   width = 20  height = 20  entry=(0,0)  exit=(19,19)  perfect=true  seed=42   `

Parameters:

*   width
    
*   height
    
*   entry
    
*   exit
    
*   perfect
    
*   seed
    

Maze Generation Algorithm
=========================

The maze generation algorithm used in this project is **Depth-First Search (DFS)** with backtracking.

Steps:

1.  Start from the entry cell.
    
2.  Mark the cell as visited.
    
3.  Randomly choose an unvisited neighbor.
    
4.  Remove the wall between cells.
    
5.  Continue until all cells are visited.
    

Why This Algorithm
==================

The DFS algorithm was chosen because:

*   It is simple and efficient.
    
*   It guarantees a connected maze.
    
*   It produces natural maze structures.
    
*   It is widely used in procedural generation.
    

Its time complexity is linear with respect to the number of cells.

Reusable Code
=============

The reusable part of the project is the **MazeGenerator module**.

It is implemented as a standalone class that can be imported in other projects:

`   from mazegen.maze import MazeGenerator   `

The module provides:

*   Maze generation
    
*   Access to maze structure
    
*   Solution path computation
    

The package can be installed with pip and reused in any Python project.

Team and Project Management
===========================

Team Roles
----------

\-The work on this project was divided between the team members.

*   _**amelhach**_ implemented the core maze logic, including the maze generation using the DFS algorithm, the pathfinding using BFS, the maze generation process, and the functionality to save the maze and the solution path into a file.
    
*   _**yrziqi**_ worked on the visualization part of the project, including printing the maze, creating the MaKefile , and handling the packaging and documentation of the project.
    

Project Planning
----------------

Initial plan:

1.  Maze data structure
    
2.  Maze generation algorithm
    
3.  Pathfinding solution
    
4.  File export
    
5.  Python packaging
    
6.  Documentation
    

The project evolved with improvements to:

*   code structure
    
*   type hints
    
*   error handling
    
*   packaging
    

What Worked Well
----------------

*   Clear separation between generator and solver
    
*   Modular architecture
    
*   Reusable code design
    

What Could Be Improved
----------------------

*   Additional generation algorithms
    
*   Visualization tools
    
*   Performance optimization for large mazes
    

Tools Used
----------

*   Python
    
*   Git
    
*   Virtual environments
    
*   flake8
    
*   mypy
    

Resources
=========

Documentation and references used:

- Python documentation  
- DFS algorithm references  
- Maze generation tutorials  
- Graph traversal algorithms  

Useful resources:

- [Python Documentation](https://docs.python.org/3/)
- [Algorithm for BFS](https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/)
- [Algorithm for DFS](https://www.geeksforgeeks.org/dsa/depth-first-search-or-dfs-for-a-graph/)
- [Difference Between BFS and DFS](https://medium.com/@sohel.indianreveler/difference-between-bfs-and-dfs-unraveling-the-maze-of-graph-traversal-b96c58103743)

Use of AI
=========

AI tools were used to assist with:

*   concept explanations
    
*   debugging explanations
    
*   documentation structuring
    

All algorithms and architecture decisions were implemented and validated manually.