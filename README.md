# Pacman-Berkeley
This project aim is to improve the Pacman game, from Berkeley’s. Firstly, I implemented the
code for Depth-First Traversal (or Search), Breadth-First Traversal (or Search), the Uniform
Cost Search and the A* Search. The goal I wanted to implement was to improve this search
and for this I chose the Bidirectional Search. Bidirectional search algorithms interleave two
separate searches, a normal search forward from the start state, and a search backward from
the goal. It is well known that adding a heuristic to unidirectional search dramatically reduces
the search effort.
I chose to implement a certain heuristic, that unlike previous bidirectional heuristic search algorithms,
MM’s forward and backward searches are guaranteed to “meet in the middle”, never
expand a node beyond the solution midpoint. 
I chose two methods to implement this heuristic:
## Bidirectional with Breadth-First Search
Bidirectional MM implemented with two BFS algorithms, in the function biDirectionalSearchMM0():
here I used 2 queues, which I transverse both, one from one start to goal,
the other from the goal to the start, using both starting and ending point as pivots.
## Bidirectional with A* Search
Bidirectional MM implemented with two A* algorithms: here I used two A* algorithms, in the
same manner as the implementation with BFS. I noticed that this algorithm is more efficient
as the one with the BSF.
