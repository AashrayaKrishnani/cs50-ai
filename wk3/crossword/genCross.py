import sys

from myCrossword import *

class CrosswordGenerator:

    def __init__(self, crossword) -> None:
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words 
            for var in self.crossword.variables
        }

    def get_grid(self, assignment):
        """
        Generates 2-D grid representation 
        of the crossword's current assignment

        """
        grid = [
            ['█' for j in range(self.crossword.width)]
            for i in range(self.crossword.height)
        ]

        # Putting respective values
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    grid[i][j] = ' '

        for var, word in assignment.items():
            (i,j) = (var.i, var.j)
            for k in range(var.length):
                r = i + (k if var.direction==Variable.DOWN else 0)
                c = j + (k if var.direction==Variable.ACROSS else 0)
                grid[r][c] = word[k]

        return grid

    def print(self, assignment):
        grid = self.get_grid(assignment)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                print(grid[i][j], end='')
            print()
 
    def save(self, assignment, out):
        from PIL import ImageDraw, Image, ImageFont
        
        grid = self.get_grid(assignment)
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2*cell_border
        
        # Blank Blank Canvas
        img = Image.new(
            'RGBA',
            ( self.crossword.width*cell_size, self.crossword.height*cell_size),
            'black'
        )
        
        font = ImageFont.truetype('assets/OpenSans-Regular.ttf', 55)
        draw = ImageDraw.Draw(img)
        
        # Drawing now
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                rect = [
                (
                    j*cell_size + cell_border,
                    i*cell_size + cell_border
                ),
                (
                    (j+1)*cell_size-cell_border,
                    (i+1)*cell_size-cell_border
                )
                ]
                
                if self.crossword.structure[i][j]:
                    # Empty white Box
                    color = "white"
                    draw.rectangle(rect, color)

                    if not grid[i][j] == ' ':
                        color = 'black'

                        (w, h) = draw.textsize(grid[i][j], font)
                        draw.text(
                            (rect[0][0] + ((interior_size-w)/2),
                            rect[0][1] + (interior_size-h)/2),
                            grid[i][j],
                            fill=color,
                            font=font
                        )

        # Highlighting starting letters
        for var in self.crossword.variables:
            (i,j) = (var.i, var.j)
            (w,h) = draw.textsize(grid[i][j], font)
            draw.text(
                            (j*cell_size + cell_border + ((interior_size-w)/2),
                            i*cell_size + cell_border + (interior_size-h)/2),
                            grid[i][j],
                            fill='red',
                            font=font
                        )

            

        img.save(out)


    def generate(self):
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Removes Domain values from each variable that don't satisfy 
        the variable's unary constraint: var.length == value.length
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
        Makes variable 'x' Consistent with variable 'y' by
        limiting it's domain such that for Each Value,
        there is Atleast 1 valid value in y's domain
        satisfying all dependent constraints if any.
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
        Makes all Nodes Arc Consistent, by removing 
        domain values that violate any binary constraint.
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
                neighbours = self.crossword.neighbours(x)
                neighbours.remove(y)
                for n in neighbours: 
                    if (x, n) not in arcs:
                        arcs.append((x, n))

        # If all went well
        return True

    def assignment_complete(self, assignment):
        """
        Checks if all variables have a value.
        """
        return len(assignment.keys()) == len(self.crossword.variables) 

    def consistent(self, assignment):
        """
        Makes sure:
        1. All variables have Unique values
        2. Values are Valid in length
        3. Values do not produce any conflicts.
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
            for n in self.crossword.neighbours(var):
                if n in assigned:
                    (vi, ni) = self.crossword.overlaps[var, n]
                    if assignment[var][vi] != assignment[n][ni]:
                        isConsistent = False

        return isConsistent

    def order_domain_values(self, var, assignment):
        """
        Returns domain values for variable,
        with the first value being the one that 
        Eliminates Least number of Values for other variables.
        """

        def choices_eliminated(val):
            eliminations = 0
            for n in self.crossword.neighbours(var):
                (vi, ni) = self.crossword.overlaps[var, n]

                for n_val in self.domains[n]:
                    if val[vi] != n_val[ni]:
                        eliminations += 1

            return eliminations

        return list(self.domains[var]).sort(key=choices_eliminated)

    def select_unassigned_variable(self, assignment):
        """
        Returns an Unassigned Variable with:
        first preference to those which have less values remaining,
        second preference to those connected with more neighbours.
        """
        unassigned = set(self.crossword.variables).difference(set(assignment.keys()))

        var = unassigned.pop()
        degree = len(self.crossword.neighbours(var))
        remn_values = len(self.domains[var])

        for v in unassigned:
            if (len(self.domains[v]) < remn_values                  # Has lesser values in domain than var
                or                                                      # Has equal values, but greater degree than var
                    (len(self.domains[v]) == remn_values and len(self.crossword.neighbours(var)) > degree)):
                var = v
                degree = len(self.crossword.neighbours(var))
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

    # sys.argv = 'genCross.py data/structure0.txt data/words0.txt'.split(' ')

    if len(sys.argv) not in [3, 4]:
        print('Usage: python genCross.py structure_file words_file [output_img]')
        sys.exit(1)
    
    # Parsing input
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv)==4 else None

    # Creating Crossword
    cw = Crossword(structure, words)
    cw_gen = CrosswordGenerator(cw)
    solution = cw_gen.generate()

    # Outputting solution
    if solution:
        cw_gen.print(solution)
        if output:
            cw_gen.save(solution, output)
    else:
        print('No Solution Found, Sorry!')

if __name__ =='__main__':
    main()
