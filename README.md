# Maze Solver
A Python program made to solve rectangular mazes, which are generated from https://keesiemeijer.github.io/maze-generator/.
## Example
<table>
   <tr>
      <th>Sample maze</th>
      <th>Solution</th>
   </tr>
   <tr>
      <td><img src="https://raw.githubusercontent.com/YokelMan/maze-solver/main/img/maze.png"></td>
      <td><img src="https://raw.githubusercontent.com/YokelMan/maze-solver/main/img/maze_solution.png"></td>
   </tr>
</table>

## Program methodology
The program works in the following way:
1. Loads image path and wall thickness (option used to change size of maze) using [command line arguments](https://docs.python.org/3/library/sys.html#sys.argv).
2. Loads image by using the [pillow library](https://python-pillow.org/), sets width and height of the maze and then encodes all/some pixels as 0 (white) or 1 (black) in a 2D list, mimicking the maze in two dimensions.
3. Defines some elementary variables like a direction [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)) to keep track of multiple directions, and functions related to moving in the maze and painting the solution.
4. The solution is made in the form of a direction list, which keeps track of the directions to take from the initial position in order to reach the final position (for an example of this see the code), which is then painted on the original maze image using the appropriate functions.
5. The final painted image is [shown](https://pillow.readthedocs.io/en/latest/reference/Image.html#PIL.Image.Image.show) to the user, the solution being painted in red color. The user then has the option to save the image permanently in their native image application.
## Features
* Solves mazes instantly
* Support for custom value of columns, rows and wall thickness
## Dependencies
[Pillow](https://python-pillow.org/) - a widely used fork of PIL (Python Imaging Library). Download it with `pip install pillow`.
## Get started
1. Download a maze image from the website https://keesiemeijer.github.io/maze-generator/. You can customize wall thickness, columns and rows options. (Support for other options will be added later.)
2. Run the program `maze.py` from command line along with arguments for image path as well as wall thickness (in that order).
   Example: `python maze.py maze.png 10` (Here it's assumed that path of both the program and the image is the same as your current working directory.)
3. See the magic unfold!
## Further improvements
There are several features that can be added - more customization, a more efficient algorithm, etc. Some of them are listed below:
* Custom colors for walls and passages
* Support for different types of maze entries, i.e. custom entry and exit points
* GUI-fying it
* Maze generator!
### Note:
I thought that trying to find the solution in the opposite manner (going from exit to entry point) would be much faster, but when I actually tested the time the program took to run in both cases (entry -> exit and exit -> entry), the former was often faster. In retrospect either my measurement of the time taken could have been erroneous (I used the [time.time()](https://docs.python.org/3/library/time.html#time.time) function) or I didn't write my program properly for the latter case. Please let me know if there can be a better solution either by issuing a PR or contacting me through Discord. Thanks!
