# Solving sudoku puzzles with python


## What is sudoku?
---

### Core Concepts

* It's a logic puzzle based on a grid of X length and X width, with X being any natural number where the square root of itself is also a natural number, though the standard variant of the puzzle uses a 9 by 9 grid.
* The symbols used to fill the spaces within the grid can be any unique character set as long as it has enough characters to fill X number of spaces.
* The default symbol set nearly universally used are the numbers 1, 2, 3, 4... all the way up to X.
* The goal is to use logic skills to place the symbols into a given grid where no house (i.e a row, column or subdivided box) contains the same character twice. These starting grids generally have spaces already filled in as clues for you to follow
* A way people have learned to make solving the puzzles easier is to list "pencil marks" for each space 

___
  
Over the years sudoku enthusiasts have managed to come up with a generally accepted difficulty ranking for each and every starting set based upon what methods and techniques you would need to use to solve the puzzle. All necessary methods follow below:

| Rating    | Techniques Used   |
| --------- | ----------------- |
| Simple    | Naked Single, Hidden Single |
| Easy      | Naked Pair, Hidden Pair, Pointing Pairs|
| Medium    | Naked Triple, Naked Quad, Pointing Triples, Hidden Triple, Hidden Quad|
| Hard      | XWing, Swordfish, Jellyfish, XYWing, XYZWing |

### __Naked__ ___Single___ __:__
A naked single refers to a __single__ space where, if you had enough time to mark out every single correct pencil mark, there would only be one possible choice for that space. In code that's a fairly simple exercise where you loop over the 2D array of pencil marks and search for a space that only contains a single item, the corresponding space in the grid has to be that remaining item. This method, along with the hidden single method, are the only ways to be 100% sure that a grid space has been correctly assigned and are therefore the only methods that can interact with both the grid and markings.

### __Hidden__ ___Single___  __:__
A hidden single refers to a __single__ space where its pencil marks contain the only instance of a mark within its entire house, meaning for that row/column/box it is the only possible space for that mark to appear. What differs this from the naked single method is the mark is not going to be the only mark assigned to that space. The right mark will be "hidden" beneath other marks that can't be eliminated as a candidate by other means.

### __Pointing__ ___Pair / Triple___ __:__
A pointing set is a grouping of a single mark spread over two or three spaces in a box that belong to the same row or column. This means that the mark has to be in one of those spaces and can be removed from the rest of the row/column. However it's also true where a grouping of a single mark spread over two or three spaces in a column that are the only occurances of said mark in said column, along with being contained in the same subgrid. Where the mark can be removed from the rest of the subgrid as that mark can only occur in those spaces within the subgrid.

### __Naked__ ___Pair / Triple / Quad___ __:__
A naked pair/triple/quad refers to a __group__ of spaces within a house, where they're are all a part of a set of marks that can only appear in those spaces. Meaning you can eliminate that set of marks from appearing in the rest of the house. The marks are assured to appear in those specific spaces if they're all a subset of a set containing all numbers within the marks of the spaces and that the set is no greater in size than the number of spaces being included.

### __Hidden__ ___Pair / Triple/ Quad___ __:__
A hidden pair/triple/quad is very similar to the naked variants of the same name, however like the hidden single the pair/triple/quad the wanted marks are buried and "hidden" beneath other marks that can't be eliminated by using any other means. These marks that are hiding the pair/triple/quad underneath can be discarded. This method often works in conjunction with the naked pair/triple/quad method eliminate a great number of pencil marks from the harder difficulty puzzles.

### __XWing, XYWing, XYZWing :__
    Insert Context

### __Swordfish :__
    Insert Context

### __Jellyfish :__
    Insert Context