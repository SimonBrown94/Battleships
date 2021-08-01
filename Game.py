import Player
import random
import numpy as np


def battleships(test=None):
    if test:
        print("Playing in test mode, there is no data validation on inputs")
        size = int(input("board size?"))
        p1diff = input("p1 diff?")
        p2diff = input("p2 diff?")
        num_ship = int(input("number of ships?"))
        tships = []
        for i in range(num_ship):
            tships.append(int(input("ship " + str(i) + " length?")))

        n_game = int(input("number of games?"))

        result = []

        for i in range(n_game):
            result.append(game(size, "C", p1diff, "C", p2diff, tships))
        print(result)
    else:
        game()


def game(size=None, tp1=None, tp1d=None, tp2=None, tp2d=None, stest=None):

    # Ask for board size and verify
    if size:
        board_size = size
    else:
        while True:
            board_size = input("How big do you want the board?")

            if not board_size.isnumeric() or int(board_size) < 5:
                print("Board must be an integer 5 or larger")
            else:
                board_size = int(board_size)
                break

    # Ask if players are people of computers
    if tp1:
        p1bot = tp1
        p1diff = tp1d
        p2bot = tp2
        p2diff = tp2d
    else:
        while True:
            p1bot = input("P1: 'P'erson or 'C'omputer").upper()
            if p1bot not in ("P", "C"):
                print("The player must be P or C")
            else:
                if p1bot == "C":
                    while True:
                        p1diff = input("P1 Difficulty? E, M or H").upper()
                        if p1diff not in ("E", "M", "H"):
                            print("Difficulty choice not valid, choose again")
                        else:
                            break
                else:
                    p1diff = "P"
                break

        while True:
            p2bot = input("P2: 'P'erson or 'C'omputer").upper()
            if p2bot not in ("P", "C"):
                print("The player must be P or C")
            else:
                if p2bot == 'C':
                    while True:
                        p2diff = input("P2 Difficulty? E, M or H").upper()
                        if p2diff not in ("E", "M", "H"):
                            print("Difficulty choice not valid, choose again")
                        else:
                            break
                else:
                    p2diff = "P"
                break

    ships = []

    # Get number of ships
    if stest:
        number_of_ships = len(stest)
        for i in stest:
            ships.append(i)
    else:
        while True:
            number_of_ships = input("How many ships would you like?")
            if not number_of_ships.isnumeric() or not 1 <= int(number_of_ships) <= board_size//2:
                print("You must have between 1 and " + str(board_size//2) + " ships")
            else:
                number_of_ships = int(number_of_ships)
                break

        # Get size of each ship
        for i in range(number_of_ships):
            ships.append(0)
            while True:
                ship_len = input("How big do you want ship " + str(i) + " ?")
                if not ship_len.isnumeric() or not 2 <= int(ship_len) <= board_size//2:
                    print("Ship must be between 2 and " + str(board_size//2) + " long")
                else:
                    ships[i] = int(ship_len)
                    break

    # Create the players
    players = [Player.Player(board_size, p1bot, p1diff, ships),
               Player.Player(board_size, p2bot, p2diff, ships)]

    # Get ship locations for each player
    for player in range(2):
        print("Player " + str(player) + " setup")
        for i in range(number_of_ships):
            players[player].add_ship(i, ships[i])

        print("Final player " + str(player) + " board")
        players[player].my_board.print_board()

    player_number = 0
    opponent_number = 1

    # Gameplay
    while True:
        players[player_number].turns += 1
        # Print current boards
        print("------------------------------------------------------")
        print("Player " + str(player_number) + "'s turn")
        print("My board")
        players[player_number].my_board.print_board()
        print("Opponent board")
        players[player_number].opp_board.print_board()

        # Get coordinates of the players guess
        x, y = turn(players[player_number], players[opponent_number])

        # Return if the move was a miss, hit or sink
        action, sank_ship = players[opponent_number].opp_attack(x, y)

        print(action)

        # Update boards
        if action == "Hit":
            players[player_number].opp_board.board[y, x] = 'h'
            players[opponent_number].my_board.board[y, x] = 'h'
        elif action == "Sank!":
            for coord in sank_ship:
                players[player_number].opp_board.board[coord[1], coord[0]] = 'd'
                players[opponent_number].my_board.board[coord[1], coord[0]] = 'd'
        else:
            players[player_number].opp_board.board[y, x] = 'm'
            players[opponent_number].my_board.board[y, x] = 'm'

        if len(sank_ship) in players[player_number].opp_ships:
            players[player_number].opp_ships.remove(len(sank_ship))

        # Check if the opponent is still alive, if dead end game
        if not players[opponent_number].still_alive():
            break

        # Switch over the player and the opponent
        player_number, opponent_number = opponent_number, player_number

    print("Player " + str(player_number) + " wins!")
    print("Player " + str(player_number) + " final board")
    players[player_number].my_board.print_board()

    print("Player " + str(opponent_number) + " final board")
    players[opponent_number].my_board.print_board()
    print(players[player_number].diff, players[player_number].turns)

    if size is not None:
        return players[player_number].diff, players[player_number].turns


def turn(player, opponent):
    # Return the coordinates of the players move
    if not player.bot:
        while True:
            x = input("x coordinate")
            y = input("y coordinate")

            if not x.isnumeric() or \
                    not y.isnumeric() or \
                    int(x) >= player.board_size or \
                    int(y) >= player.board_size:
                print("Coordinate off the board, choose again")
                continue
            elif player.opp_board.board[int(y)][int(x)] != '-':
                print("Position already chosen, choose again")
                continue
            else:
                x = int(x)
                y = int(y)
                break

    else:
        x, y = bot_turn(player, opponent)

    return x, y


def bot_turn(player, opponent):

    if player.diff == "E":
        return bot_easy(player)
    elif player.diff == "M":
        return bot_medium(player, opponent)
    elif player.diff == "H":
        return bot_hard(player)


def bot_easy(player):
    i = random.randrange(len(player.remaining_attacks))
    return player.remaining_attacks.pop(i)


def bot_medium(player, opponent):
    if player.attack_stack:
        x, y = player.attack_stack.pop()
    else:
        x, y = bot_easy(player)

    if opponent.opp_attack(x, y)[0] in ("Hit", "Sank!"):
        check_attacks(player, x + 1, y)
        check_attacks(player, x - 1, y)
        check_attacks(player, x, y + 1)
        check_attacks(player, x, y - 1)

    return x, y


def bot_hard(player):
    heat_map = np.array([[0 for i in range(player.board_size)]
                            for j in range(player.board_size)])

    for attack_ship in player.opp_ships:
        for x in range(player.board_size - attack_ship + 1):
            for y in range(player.board_size):
                attack_value = 1
                for i in range(attack_ship):
                    if player.opp_board.board[y, x+i] in ("m", "d"):
                        attack_value = 0
                        break
                    elif player.opp_board.board[y, x+i] == "h":
                        attack_value = attack_value + 5

                for i in range(attack_ship):
                    if player.opp_board.board[y, x + i] == "-":
                        heat_map[y, x+i] += attack_value

        for x in range(player.board_size):
            for y in range(player.board_size - attack_ship + 1):
                attack_value = 1
                for i in range(attack_ship):
                    if player.opp_board.board[y+i, x] in ("m", "d"):
                        attack_value = 0
                        break
                    elif player.opp_board.board[y+i, x] == "h":
                        attack_value = attack_value + 5

                for i in range(attack_ship):
                    if player.opp_board.board[y+i, x] == "-":
                        heat_map[y+i, x] += attack_value

    # print(heat_map)
    # print(heat_map.max())
    max_attack = np.where(heat_map == heat_map.max())
    # print(max_attack[1][0], max_attack[0][0])

    return max_attack[1][0], max_attack[0][0]


def check_attacks(player, x, y):
    if [x, y] in player.remaining_attacks:
        player.attack_stack.append([x, y])
        player.remaining_attacks.remove([x, y])

#testcomment
