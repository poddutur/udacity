# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: According to the logic of the sudoku problem, if a situation arises where there are two squares/boxes in the same unit containing "same" and "only" two possible digits, then we can infer that other boxes cannot have these digits as the these two digits will be shared among these two squares/boxes. Hence we can eliminate these two digits from possibility set of other squares/boxes.  
Similarly this can be extended to 3 squares in the same unit containing same 3 elements or more generally 'x' squares containing same 'x' elements, thereby we can eliminate these elements from the possibility set of other squares in the same unit.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We added an additional constraint that the two diagonals cannot have a digit repeated (1-9 in the 9 boxes). As before we expressed this by considering each diagonal as a unit in diagonal units which we appended to the other units. So when we are checking for unit constraints, thus diagonal is also considered. 

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
