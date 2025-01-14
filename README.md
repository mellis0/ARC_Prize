This is my solution to the ARC Prize Problem, which is a yet-to-be-solved problem about how to deduce patterns from a very small dataset (2 to 5 examples). Humans generally perform very well on the ARC problems compared to computers.

The ARC prize corpus is a collection of grids with colorful squares. To solve one, an agent must deduce the pattern from an example pair, then apply that pattern to the test grid.

To explore ARC problems you can visit https://arcprize.org or manually try to solve problems here: https://tail.cc.gatech.edu/kbai/arc-prize/

The foundation of my solution is the Breadth-First Search algorithm. My agent considers a set of basic actions that can be taken to augment the grid, like swapping colors or rotating the grid, then it searches over those actions to see if it can deduce a path from the input to the output. This path is essentially the pattern, so once a path is found, it can be applied to the test grid.

The Breadth-First Search in my agent is bolstered by some modifications that make it more efficient, like never repeating a state in the search and refusing to expand actions that add irrelevant colors to the grid.
