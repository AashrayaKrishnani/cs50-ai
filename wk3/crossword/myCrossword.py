
class Variable:

    ACROSS = 'across'
    DOWN = 'down'

    def __init__(self, i, j, length, direction):
        self.i = i
        self.j = j 
        self.length = length
        self.direction = direction
        self.cells = set()
        # Populating apt cells
        for k in range(self.length):
            self.cells.add( 
                (self.i+k if self.direction==Variable.DOWN else self.i,
                self.j+k if self.direction==Variable.ACROSS else self.j)
            )

    def __eq__(self, other):
        return (isinstance(other, Variable) and self.i==other.i and self.j==other.j 
        and self.length == other.length and self.direction==other.direction)

    def __repr__(self):
        return f'Variable(({self.i}, {self.j}), {self.length}, {self.direction})'

    def __hash__(self) -> int:
        return hash((self.i, self.j, self.length, self.direction))

class Crossword:
    
    def __init__(self, structure_file, words_file) -> None:
        
        # Loading Words
        with open(words_file) as f:
            self.words = set(f.read().upper().splitlines())

        # Determining Structure of Crossword
        self.structure = []
        with open(structure_file) as f:
            contents = f.read().splitlines()
            self.height = len(contents)
            self.width = max(len(line) for line in contents)

            for r in range(self.height):
                row = []
                for c in range(self.width):
                    # If valid and blank, make it True, else false.
                    row.append(c<len(contents[r]) and contents[r][c]=='_')
                self.structure.append(row)

        # Determining Variables
        self.variables = set()
        for r in range(self.height):
            for c in range(self.width):
                # If blank
                if self.structure[r][c]:

                    # Checking for Vertical Words.
                    if r==0 or not self.structure[r-1][c]:
                        length = 1
                        for k in range(r+1, self.height):
                            if not self.structure[k][c]:
                                break
                            else:
                                length += 1

                        # If a valid vertical word
                        if length>1:
                            self.variables.add(
                                Variable(r, c, length, Variable.DOWN)
                            )
                           
                    # Checking for Horizontal Words.
                    if c==0 or not self.structure[r][c-1]:
                        length = 1
                        for k in range(c+1, self.width):
                            if not self.structure[r][k]:
                                break
                            else:
                                length += 1

                        # If a valid vertical word
                        if length>1:
                            self.variables.add(
                                Variable(r, c, length, Variable.ACROSS)
                            )

        # Setting up the set of Overlaps
        self.overlaps = dict()
        for v1 in self.variables:
            for v2 in self.variables:
                if v1==v2:
                    continue
                else:
                    intersection = v1.cells.intersection(v2.cells)
                    if intersection:
                        (i, j) = intersection.pop()
                        self.overlaps[v1, v2] = (
                            i-v1.i if v1.direction==Variable.DOWN else j-v1.j,
                            i-v2.i if v2.direction==Variable.DOWN else j-v2.j
                        )
                    else: 
                        self.overlaps[v1, v2] = None


    def neighbours(self, var):
        # Returns overlapping neighbours 
        return set(
            v for v in self.variables
            if v!=var and self.overlaps[v, var]
        )


