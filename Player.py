import Board
import Ship
import random


class Player:
    def __init__(self, board_size, bot, diff, ships):
        self.ships = []
        self.board_size = board_size
        self.my_board = Board.Board(board_size)
        self.opp_board = Board.Board(board_size)
        self.remaining_attacks = []
        self.attack_stack = []
        self.opp_ships = []
        self.turns = 0

        for i in ships:
            self.opp_ships.append(i)

        if bot == 'P':
            self.bot = False
        elif bot == 'C':
            self.bot = True
            for i in range(board_size):
                for j in range(board_size):
                    self.remaining_attacks.append([i, j])
            self.diff = diff

    def add_ship(self, ship_number, length):
        # Add a ship to the player
        if not self.bot:
            # This section is for human players
            # Print the current board and state ships length
            self.my_board.print_board()
            print("Ship: " + str(ship_number) + ", Length: " + str(length))

            valid_position = False

            # Ask for position and check if it is valid
            while not valid_position:
                x = input("Ship " + str(ship_number) + " x coordinate = ")
                y = input("Ship " + str(ship_number) + " y coordinate = ")
                d = input("Ship " + str(ship_number) + " direction = ").lower()

                if d == 'h':
                    if not x.isnumeric() or int(x) + length > self.board_size:
                        print("Invalid ship position, please choose again (ship goes off the board)")
                        continue
                    for i in range(length):
                        if self.my_board.board[int(y), int(x) + i] == 'S':
                            print("Invalid ship position, please choose again (ship overlaps another ship")
                            valid_position = False
                            break
                        else:
                            x = int(x)
                            y = int(y)
                            valid_position = True
                elif d == 'v':
                    if not y.isnumeric() or int(y) + length > self.board_size:
                        print("Invalid ship position, please choose again (ship goes off the board)")
                        continue
                    for i in range(length):
                        if self.my_board.board[int(y) + i, int(x)] == 'S':
                            print("Invalid ship position, please choose again (ship overlaps another ship)")
                            valid_position = False
                            break
                        else:
                            x = int(x)
                            y = int(y)
                            valid_position = True
                else:
                    print("Invalid direction, please choose again (must be 'h' or 'v')")
        else:
            # This section is for if the computer has to generate ship positions
            d = random.choice(['h', 'v'])

            valid_position = False
            while not valid_position:
                if d == 'h':
                    x = random.randrange(self.board_size - length)
                    y = random.randrange(self.board_size)
                else:
                    x = random.randrange(self.board_size)
                    y = random.randrange(self.board_size - length)

                if d == 'h':
                    for i in range(length):
                        if self.my_board.board[y, x + i] == 'S':
                            valid_position = False
                            break
                        else:
                            valid_position = True
                elif d == 'v':
                    for i in range(length):
                        if self.my_board.board[y + i, x] == 'S':
                            valid_position = False
                            break
                        else:
                            valid_position = True

        # Once the valid coordinates are chosen, add a new ship and update the boards
        self.ships.append(Ship.Ship(x, y, length, d))
        for coord in self.ships[ship_number].coords:
            self.my_board.coord_update(coord[0], coord[1], 'S')

    def opp_attack(self, x, y):
        # Check the input coordinates against the coordinates of each ship, if hit then update ship
        for ship in self.ships:
            for i in range(len(ship.coords)):
                if [x, y] == ship.coords[i]:
                    action = ship.update_ship(i)
                    if action == "Hit":
                        return action, []
                    elif action == "Sank!":
                        return action, ship.coords
        return "Miss", []

    def still_alive(self):
        # If a player has at least one ship which is not dead then the are still alive
        for ship in self.ships:
            if not ship.dead:
                return True
        return False





