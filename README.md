# CellularAutomata
 
Cellular Automata: a discrete model of computation studied in automata theory. Cellular automata are also called cellular spaces, tessellation automata, homogeneous structures, cellular structures, tessellation structures, and iterative arrays. Cellular automata have found application in various areas, including physics, theoretical biology and microstructure modeling. (*via. [wikipedia](https://en.wikipedia.org/wiki/Cellular_automaton)*)


![alt text](misc/ezgif-6-ecfc0914c8.gif)

Features:
-
The app is built off the idea of [Conways Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life), but with 2 twists.

### 1) Moore Neighborhood Reproduction
If a cell has exactly 1 partner next to it, there is a 10% chance that it will reproduce (replace the cell being checked)
### 2) Von Neumann Neighborhood Explosion (Work in Progress)
If a cell reaches 10 turns old, it will have a 50% chance of exploding. When the cell explodes it has a 50% chance for its adjacent cells to come alive/reset their age.

#### The base of the game is built using Pygame. Install Via.
```
pip install pygame
```
This program is still a work in progress, and if you have any recommendations let me know :)


