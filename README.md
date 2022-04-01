# Solving sudoku puzzles with python


## What is sudoku?
---

### Core Concepts

* It's a logic puzzle based on a grid of X length and X width, with X being any natural number where the square root of itself is also a natural number, though the standard variant of the puzzle uses a 9 by 9 grid.
* The symbols used to fill the spaces within the grid can be any unique character set as long as it has enough characters to fill X number of spaces.
* The default symbol set nearly universally used are the numbers 1, 2, 3, 4... all the way up to X.
* The goal is to use logic and reasoning skills to place the symbols into a given grid where no house (i.e a row, column or subdivided box) contains the same character twice. These starting grids generally have spaces already filled in as clues for you to follow
* A way people have learned to make solving the puzzles easier is to list "pencil marks" for each space 

___
  
Over the years sudoku enthusiasts have managed to come up with a generally accepted difficulty ranking for each and every starting set based upon what methods and techniques you would need to use to solve the puzzle. All necessary methods follow below:

| Rating    | Techniques Used   |
| --------- | ----------------- |
| Simple    | Naked Single, Hidden Single |
| Easy      | Naked Pair, Hidden Pair, Pointing Pairs|
| Medium    | Naked Triple, Naked Quad, Pointing Triples, Hidden Triple, Hidden Quad|
| Hard      | XWing, Swordfish, Jellyfish, XYWing, XYZWing |

### __Naked__ ___Single / Pair / Triple / Quad___ __:__
    The naked phrase refers to a house where an X number spaces contain the same elements along with containing the same number of elements as the number of spaces which contain said elements. Meaning those spaces are the only ones in that house that can contain those elements, ergo you can remove all of those possible elements from all the other spaces in that house.

### __Hidden__ ___Single / Pair / Triple/ Quad___  __:__
    Insert Context

### __XWing, XYWing, XYZWing :__
    Insert Context

### __Swordfish :__
    Insert Context

### __Jellyfish :__
    Insert Context