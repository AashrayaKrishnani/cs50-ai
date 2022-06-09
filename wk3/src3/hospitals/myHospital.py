from cmath import log
from itertools import count
import random

class Space:

    def __init__(self, height, width, hospitals_count):
        self.height = height
        self.width = width
        self.hospitals_count = hospitals_count
        self.houses = set()
        self.hospitals = set()

    def add_house(self, row, col):
        self.houses.add((row, col))

    def get_cost(self, hospitals):
        cost = 0
        if len(hospitals)==0:
            return 0

        cost = sum( min(
            abs(house[0] - hospital[0]) + abs(house[1] - hospital[1])
            for hospital in hospitals 
        )  for house in self.houses)

        return cost

    def get_available_space(self):
        space = list(
            (i,j)
            for i in range(self.height)
            for j in range(self.width)
        )

        # Clear out houses and hospitals
        for house in self.houses:
            space.remove(house)
        for hospital in self.hospitals:
            space.remove(hospital)

        return space

    def get_neighbours(self, row, col):
        """
        Returns neighbouring cells that aren't houses or hospitals.
        """
        neighbours = []

        # Iterating over all cells in the 3x3 grid with (row, col) as center
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                # Validating
                if 0<=i<self.height and 0<=j<self.width:
                    neighbour = (i,j)
                    if neighbour != (row,col) and neighbour not in self.houses and neighbour not in self.hospitals:
                        neighbours.append(neighbour)

        return neighbours

    def hill_climb(self, log=True):
        """
        Executes the hill-climbing algorithm to find State with Min(local or global) Cost.
        """
        count=0

        # # Testing
        # self.hospitals.add((3,3))
        # self.hospitals.add((4,4))

        # Initializing Hospitals randomly
        self.hospitals = set()
        for i in range(self.hospitals_count):
            self.hospitals.add( random.choice(self.get_available_space()) )

        # Reporting Inital State
        if log:
            count+=1
            self.gen_img(f'hospital{count}.png')

        repeat = True

        # Looping till we find the Minimum
        while(repeat):
            min_cost = float('inf')
            min_hospitals = self.hospitals
            # Checking all neighbours 
            for hospital in self.hospitals:
                # Iterating over all neighbours and compare each to current min case.
                for neighbour in self.get_neighbours(hospital[0], hospital[1]):
                    # Getting cost for hospitals+neighbour-hospital
                    hospitals = set(self.hospitals)
                    hospitals.remove(hospital)
                    hospitals.add(neighbour)
                    cost = self.get_cost(hospitals)
                    
                    if cost < min_cost:
                        min_cost = cost
                        min_hospitals = hospitals

            if self.get_cost(self.hospitals) == min_cost:   # When no other neighbour has lesser cost.
                repeat=False
            else:
                self.hospitals = min_hospitals
                if log:
                    print(f'Found state with cost={min_cost}')
                    self.gen_img(f"hospital{count}.png")
                    count += 1
                

        return self.hospitals

    def random_restart(self, n):
        """
        Iterates the Hill_climb algorithm 'n' times
        """
        count = 0

        min_cost = float('inf')
        min_hospitals = self.hospitals

        while(n>0):
            hospitals = self.hill_climb(log=False)
            cost = self.get_cost(hospitals)

            if cost<min_cost:
                min_cost = cost
                min_hospitals = hospitals
                print('Found State with cost = ' + str(cost))
                self.gen_img(f'hospitals{count}.png', hospitals=hospitals)
                count+=1
            
            n-=1

        self.hospitals = min_hospitals
        return min_hospitals

    def gen_img(self, name, hospitals=None):
        from PIL import Image, ImageDraw, ImageFont

        if hospitals is None:
            hospitals = self.hospitals

        cell_size = 100
        border = 2
        cost_size = 40
        padding = 40

        h = self.height*cell_size + 2*padding + cost_size
        w = self.width*cell_size

        # Create blank Canvas
        img = Image.new("RGBA", (w, h), 'white')

        house = Image.open("assets/images/House.png").resize((cell_size, cell_size))
        hospital = Image.open('assets/images/Hospital.png').resize((cell_size, cell_size))

        font = ImageFont.truetype('assets/fonts/OpenSans-Regular.ttf', 40)
        draw = ImageDraw.Draw(img)

        # Adding the cells
        for i in range(self.height):
            for j in range(self.width):

                # Draw the cell
                rect = [
                    (j * cell_size + border,
                     i * cell_size + border),
                    ((j + 1) * cell_size - border,
                     (i + 1) * cell_size - border)
                ]
                draw.rectangle(rect, 'black')

                if (i,j) in hospitals:
                    img.paste(hospital, rect[0], hospital)
                elif (i,j) in self.houses:
                    img.paste(house, rect[0], house)

        # Adding Cost
        draw.rectangle( (0, (self.height*cell_size), self.width*cell_size, self.height*cell_size + cost_size + padding*2 ),
        'black')

        # Adding Text
        draw.text( (padding, self.height*cell_size + padding),
            text=f'Cost: {self.get_cost(self.hospitals)}', 
            fill='white', 
            font=font)

        # Saving
        img.save(name)


WIDTH = 20
HEIGHT = 20
HOSPITALS_COUNT = 4
HOUSE_COUNT = 10

# Creating a Space
space = Space(HEIGHT, WIDTH, HOSPITALS_COUNT)

# Randomly assigning houses
for i in range(HOUSE_COUNT):
    (a,b) = random.choice( space.get_available_space())
    space.add_house(a,b)

space.gen_img('initial.png')

# Starting hill Climbing XD
# hospitals = space.hill_climb()

# Multiple Hill Climbing
hospitals = space.random_restart(n=100)