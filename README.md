**Tile Puzzle Solver using A* Algorithm**
* This project aims to find the least number of moves required to change a given board from its initial state to the goal state. The provided skeleton code is solved using the A* algorithm approach, where a heuristic function is employed to minimize time and increase program efficiency. The allowed moves include left shift (L), right shift (R), upward shift (U), downward shift (D), clockwise rotation (Ic), and counterclockwise rotation (Icc).

**Design and Approach**
* The basic flow of the solution involves determining all possible states from every state, associating each state with a cost, and deciding the next move based on this cost. Key functions include:

**Successor():** This function returns a list of all possible states and calls other functions like:

* A: move_right
* B: move_left
* C: move_clockwise
* D: move_cclockwise

Each of these functions performs operations that alter the elements of the array. Additionally, new functions such as extract_inner_mat, rotate_inner_clock, rotate_inner_cclock, and replace_inner_mat are utilized for rotating the inner matrix within the 5x5 matrix.


The fringe list stores all the successors possible for every state of the board, with each element consisting of the cost of the state, the board, and the associated move. This list is heapified to ensure the board with the minimum cost is easily accessible.

**Problem Specifications**
* **Initial State:** The input boards with replaced tiles represent the initial state.
* **Goal State:** The final board with all tiles placed in sequential order is the goal state.
* **Successor States:** The board formed after performing the allowed moves constitutes the successor states (R, L, U, D, Ic, Icc, Oc, Occ).
* **State Space:** It comprises all transformations the board undergoes each time a shift is performed before reaching the goal state.

**Heuristic Function**

The heuristic function calculates the number of steps each element must take from its current position to its goal position. It stores the actual index of the elements (x1, y1) and their original index (x2, y2), then computes the Euclidean distance between the two positions. The heuristic returns the sum of all Euclidean distances calculated from the current board. While providing an optimal solution for board0, it yields a suboptimal solution for board1.
