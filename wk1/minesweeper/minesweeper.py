import random  


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.count -= 1
            self.cells.remove(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1. Marking as Move Made
        self.moves_made.add(cell)
        self.safes.add(cell)

        # 2. Marking this 'cell' as a safe cell for all statements in knowledge.
        self.mark_safe(cell)
        
        # 3. Adding new Sentence based on 'cell' and 'count' to knowledge
        cells = set()

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i,j) in self.mines:
                        count -= 1
                    elif (i,j) not in self.safes:
                        cells.add((i,j))
        s = Sentence(cells, count)
        if s not in self.knowledge:
            self.knowledge.append(Sentence(cells, count))

        # 4. Updating safes and mines.
        self.check_and_update()

        # 5. Inferring sentences and from Knowledge and updating.
        # Repeating this till we make no further changes to the knowledgeBase :)

        self.infer_and_add()
        self.check_and_update()
        # Inferring using the Subset Method
        # while(self.infer_and_add()):
        #     self.check_and_update()

        

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # addKnowledge() is called manually so don't do it here :)

        self.check_and_update()

        for cell in self.safes:
            if cell not in self.moves_made:
                # Making this move :D
                self.moves_made.add(cell)
                return cell

        # If no safe move found
        return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # addKnowledge() is called manually so don't do it here :)

        possible_moves= []

        for i in range(self.height):
            for j in range(self.width):
                cell = (i,j)
                # Validating potential move
                if cell not in self.mines and cell not in self.moves_made:
                    possible_moves.append(cell)

        if len(possible_moves) == 0:
            return None
        else:
            return possible_moves.pop()


    def check_and_update(self):
        """
        Iterates the Knowledge base to check and update if new cells can be marked safe or as mines.
        """
        for sentence in self.knowledge:
            # Checking for New Safe Cells
            for cell in sentence.known_safes():
                if cell not in self.safes:
                    self.safes.add(cell)

            # Checking for New Mine Cells
            for cell in sentence.known_mines():
                if cell not in self.mines:
                    self.mines.add(cell)
            
        def optimize_knowledge(self):
            """
                Removes sentences that have given maximum information they could give.
                Such that knowledge only has useful sentences that can still be used to obtain new information.
            """
            for s in self.knowledge:
                if len(s.cells) == s.count or s.count==0 or len(s.cells)==0:
                    self.knowledge.remove(s)

        optimize_knowledge(self)

    def infer_and_add(self):
        """
            Checks all sentences in Knowledge to find Set-Subset pairs and create new sentences inferring from them.
        """
        modified = False

        for i in range(len(self.knowledge)):
            s1 = self.knowledge[i]
            for j in range(i+1, len(self.knowledge)):
                s2 = self.knowledge[j]
                # Checking for Subset condition
                if s1.cells.isdisjoint(s2.cells):
                    continue
                elif s1.cells.issubset(s2.cells) or s2.cells.issubset(s1.cells):
                    # Inferring Information for New Sentence
                    s = s2.cells.difference(s1.cells) if s1.cells.issubset(s2.cells) else s1.cells.difference(s2.cells) 
                    c = (s2.count - s1.count) if s1.cells.issubset(s2.cells) else (s1.count - s2.count)
                    # Adding new Sentence
                    sentence = Sentence(s,c)
                    if len(s) != 0 and sentence not in self.knowledge and len(s) >= c:
                        self.knowledge.append(sentence)
                        modified = True

        return modified
