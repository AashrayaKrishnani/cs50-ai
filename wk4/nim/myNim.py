import random
from time import sleep

class Nim:
    def __init__(self, initial=[1,3,5,7]) -> None:
        self.piles = initial.copy()
        self.player = 0
        self.winner = None

    @classmethod
    def available_actions(cls, piles):
        actions = set()

        for i in range(len(piles)):
            for j in range(1, piles[i]+1):
                actions.add((i,j))

        return actions

    @classmethod
    def other_player(cls, player):
        return 0 if player==1 else 1

    def switch_player(self):
        self.player = Nim.other_player(self.player)
    
    def move(self, action):
        pile, count = action

        # Checks
        if self.winner:
            raise Exception('Game already won: Winner ' + str(self.winner))
        elif pile not in range(len(self.piles)):
            raise Exception('Invalid pile index: ' + str(pile))
        elif count not in range(1, self.piles[pile]+1):
            raise Exception('Invalid number of objects to remove: ' + str(count))

        # Else execute move
        self.piles[pile] -= count
        self.switch_player()

        # Winner Check
        if all(pile==0 for pile in self.piles):
            self.winner = self.player 

class NimAI:

    def __init__(self, alpha=0.5, beta=1, epsilon=0.1) -> None:
        self.q = dict()
        self.alpha = alpha
        self.beta = beta
        self.epsilon = epsilon

    def get_q(self, state, action):
        try:
            return self.q[tuple(state), action]
        except KeyError:
            self.q[tuple(state), action]=0
            return 0

    def best_future_reward(self, state):

        actions = Nim.available_actions(state)
        best_future_reward = max(self.get_q(state, action) for action in actions) if actions else 0

        return best_future_reward

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        self.q[tuple(state), action] = old_q + self.alpha*((reward + self.beta * future_rewards) - old_q)

    def update(self, old_state, action, new_state, reward):
        old_val = self.get_q(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old_val, reward, best_future)
    
    def choose_action(self, state, epsilon=True):
        
        if not Nim.available_actions(state):
            raise Exception('No available Actions to Take')

        if epsilon:
            # Evaluating probability to make random or best_possible move
            epsilon = random.choices([True, False], [self.epsilon, (1-self.epsilon)], k=1).pop()

        # Random Move
        if epsilon:
            return random.choice(list(Nim.available_actions(state)))
        else:
            # Best Possible Move
            actions = (list(Nim.available_actions(state)))
            actions.sort(key= lambda action: self.get_q(state, action), reverse=True)
            best_action = actions[0]
            return best_action


def train(n):

    player = NimAI()

    for i in range(n):
        print(f'Playing Training Game {i+1}')

        game = Nim()

        last = {
            0: {'state': None, 'action':None}, 
            1: {'state': None, 'action':None}, 
        }

        while True:
            # Current data
            state = game.piles.copy()
            action = player.choose_action(game.piles)

            # Saving this data for future reference
            last[game.player]['state'] = state
            last[game.player]['action'] = action

            # Making the move
            game.move(action)

            new_state = game.piles.copy()

            if game.winner != None:
                # Update how we lost.
                player.update(state, action, new_state, -1)
                # Update how other (Current also, as game.move() switched players) player won.
                player.update(last[game.player]['state'],last[game.player]['action'], new_state, 1)
                
                break
            elif last[game.player]['state']: 
                # Continue Playing
                # Updating for current player if not the first two moves
                player.update(last[game.player]['state'],last[game.player]['action'], new_state, 0)

    # Return the trained soldier
    return player


def play(ai, human_player=None):

    # If human player isn't valid
    if not human_player or not human_player in range(2):
        human_player = random.choice(range(2))

    game = Nim()

    # Game loop
    while True:

        # Showing piles
        print()
        print('Piles:')
        for i, pile in enumerate(game.piles):
            print(f'Index {i}: Piles {pile}')
        print()

        # If human's turn
        if game.player==human_player:
            print("Your Turn :)")
            
            pile = None
            count = None

            while pile==None or count==None:
                try:
                    pile = int(input('Pile Index: '))
                    count = int(input('Number of objects: '))

                    if pile not in range(len(game.piles)):
                        pile=None
                    elif count not in range(len(1, game.piles[pile]+1)):
                        count=None

                except Exception:
                    pass
                    
            move = (pile, count)
        
        # Else Ai's turn
        else: 
            print('AI\'s Turn')
            move = ai.choose_action(game.piles)
            sleep(1)
            print(f'AI chose to take {move[1]} from pile {move[0]}.')

        # Making the move
        game.move(move)

        # Checking for Winner
        if game.winner!=None:
            print()
            print('Game Over!')
            winner = 'You!' if game.winner==human_player else 'AI'
            print(f'Winner is {winner}')
            return