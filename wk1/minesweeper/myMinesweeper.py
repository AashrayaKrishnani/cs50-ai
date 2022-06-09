import random

class Minesweeper:
    def __init__(self, height, width, mines):

        # Initializing basic values
        self.height = height
        self.width = width
        self.mine_count = mines
        self.mines = set()
        self.mines_found = set()
        self.board = []

        # Generating blank board with tiles.
        for i in range(height):
            row = []
            for j in range(width):
                row.append(False)
            self.board.append(row)

        # Randomly Seeding Mines
        while(len(self.mines)<mines):
            cell = (random.randrange(height), random.randrange(width))
            if cell not in self.mines:
                self.mines.add(cell)
                self.board[cell[0]][cell[1]] = True

    def isMine(self, cell):
        return self.board[cell[0]][cell[1]]

    def nearbyMines(self, cell):
        """
        Finds mines in a 3x3 box with 'cell' as centre. The 'cell' in itself is excluded.
        """
        count =0

        for i in range(cell[0]-1, cell[0] +2):               # End index is exclusive
            for j in range(cell[1]-1, cell[1]+2):

                # If cell
                if (i,j) == cell:
                    pass

                # If in bounds, and mine.    
                if i in range(self.height) and j in range(self.width) and self.board[i][j]:
                    count += 1

        return count       

    def won(self):
        # Won if found all mines :)
        return self.mines_found == self.mines

    def print(self):
        # Textual Representation of the board along with mines

        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j]:        # If mine
                    print("X", endl='')
                else:
                    print("-", endl='')
            print()

class Sentence:

    def __init__(self, cells, count):
        self.cells = cells
        self.count = count

    def __eq__(self, other):
        return  self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        If count of mines == number of cells -> All Cells Are Mines!
        """
        if self.count == len(self.cells):
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        If count==0, all cells are Safe :D
        """
        if self.count == 0:
            return self.cells
        else:
            return set()
    def mark_mine(self, cell):
        """
        If mine in self.cells, remove it, and reduce count by 1 :D
        """
        if cell in self.cells:
            self.count -= 1
            self.cells.remove(cell)

    def mark_safe(self, cell):
        """
        If safe cell in self.cells, remove it and keep count the same. :D
        """
        if cell in self.cells:
            self.cells.remove(cell)

class MinesweeperAI():
    """
    My Sweet little AI ;p
    """

    def __inti__(self, height=8, width=8):

        # Initialization Stuff ;p

        self.height=height
        self.width=width

        self.moves_made = set()
        self.mines = set()
        self.safes = set()

        self.knowledge = []

    def mark_mine(self, cell):
        """Mark the Cell as a Mine in all Sentences in Knowledge"""

        self.mines.add(cell)

        for s in self.knowledge:
            s.mark_mine(cell)

    def mark_safe(self, cell):
        """Mark the Cell Safe in all Sentences in Knowledge"""

        self.safes.add(cell)

        for s in self.knowledge:
            s.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when a Made Move is SAFE, to update knowledge on newly obtained data.
        Count indicates the number of nearby mines! :) 
        """
        # 1. Marking as Move Made
        self.moves_made.add(cell)

        # 2. Marking this 'cell' as a safe cell for all statements in knowledge.
        self.mark_safe(cell)
        
        # 3. Adding new Sentence based on 'cell' and 'count' to knowledge
        cells = set()

        # Looping over all cells within one row and column to fill 'cells' with nearby unmarked cells.
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

        # Updating Knowledge if Necessary
        s = Sentence(cells, count)
        if s not in self.knowledge:
            self.knowledge.append(Sentence(cells, count))

        # 4. Updating safes and mines.
        self.check_and_update()

        # 5. Inferring sentences and from Knowledge and updating.
        # Repeating this till we make no further changes to the knowledgeBase :)

        self.infer_and_add()
        self.check_and_update()
        
    def make_safe_move(self):
        """
        Tries to return a Safe Move,
        Return None if it's not possible.
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
        Assesses the possible new moves that aren't mines,
        Randomly chooses from them :D

        Return None if no Random Moves Possible
        (Indicating we won ;p)
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
