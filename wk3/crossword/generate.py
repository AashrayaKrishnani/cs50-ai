import sys 

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k] 
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.crossword.variables:
            domain = self.domains[var]
            length = var.length

            toRemove = set()

            for value in domain:
                if len(value) != length:
                    toRemove.add(value)

            domain = domain.difference(toRemove)

            self.domains[var] = domain

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        revised = False

        if self.crossword.overlaps[x, y]:
            xi, yi = self.crossword.overlaps[x, y]
                
            toRemove = set()

            for xVal in self.domains[x]:
                needsRev = True

                for yVal in self.domains[y]:
                    if xVal[xi] == yVal[yi]:
                        needsRev = False

                if needsRev:
                    toRemove.add(xVal)
                    revised = True

        self.domains[x] = set(self.domains[x]).difference(toRemove)

        return revised
        
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        
        # Populating arcs with all arcs: No variable should be equal to any other variable.
        if not arcs:
            arcs = []

            for v1 in self.crossword.variables:
                for v2 in self.crossword.variables:
                    if not v1 == v2 and self.crossword.overlaps[v1, v2]:
                        arcs.append((v1, v2))

        # Beginning AC-3
        for (x, y) in arcs:
            revised = self.revise(x, y)

            if len(self.domains[x]) == 0:     # No solution possible
                return False 

            if revised:
                # Add Additional Arcs if We made changes
                neighbors = self.crossword.neighbors(x)
                neighbors.remove(y)
                for n in neighbors: 
                    if (x, n) not in arcs:
                        arcs.append((x, n))

        # If all went well
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(assignment.keys()) == len(self.crossword.variables) 

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        isConsistent = True

        # Making sure that all values are unique.
        if len(set(assignment.values())) != len(set(assignment.keys())):
            isConsistent = False

        assigned = assignment.keys()

        for var in assigned:
            # Variable's length must be equal to length of the value
            if not var.length == len(assignment[var]):
                isConsistent = False
            
            # Checking to see if any neighbouring conflicts exist
            for n in self.crossword.neighbors(var):
                if n in assigned:
                    (vi, ni) = self.crossword.overlaps[var, n]
                    if assignment[var][vi] != assignment[n][ni]:
                        isConsistent = False

        return isConsistent

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        def choices_eliminated(val):
            eliminations = 0
            for n in self.crossword.neighbors(var):
                (vi, ni) = self.crossword.overlaps[var, n]

                for n_val in self.domains[n]:
                    if val[vi] != n_val[ni]:
                        eliminations += 1

            return eliminations

        return list(self.domains[var]).sort(key=choices_eliminated)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned = set(self.crossword.variables).difference(set(assignment.keys()))

        var = unassigned.pop()
        degree = len(self.crossword.neighbors(var))
        remn_values = len(self.domains[var])

        for v in unassigned:
            if (len(self.domains[v]) < remn_values                  # Has lesser values in domain than var
                or                                                      # Has equal values, but greater degree than var
                    (len(self.domains[v]) == remn_values and len(self.crossword.neighbors(var)) > degree)):
                var = v
                degree = len(self.crossword.neighbors(var))
                remn_values = len(self.domains[var])
        
        return var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if(self.assignment_complete(assignment)):
            return assignment

        # Else choose random variable and dig deeper
        var = self.select_unassigned_variable(assignment)

        for value in self.domains[var]:
            assignment[var] = value

            # If Consistent and gives result, gift back goodness ;p
            if self.consistent(assignment):
                result = self.backtrack(assignment)

                if result:
                    return result

            # If it didn't work out down the path, time to clean up!
            del assignment[var]

        # If there's no solution forward
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
