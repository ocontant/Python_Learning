__author__ = 'ocontant'
"""
Description: Exercise 1: Create a battleship game that take a number of ship submitted by the user and hide it randomly on the gameboard. The user then has to find them to win the game.
"""

from random import randint, getrandbits

#randint(0, len(board) - 1)
#int(raw_input("Guess Row:"))
#.join
#.append
#


def create_board():
    """
    :param size: Size of the gameboard. Can be between 5 and 25 square large.
    :return: The Gameboard.
    """

    # Player define the size of the gameboard. gameboard can be between 5 and 25 square large
    size = None
    errormsg = ""
    while size < 10 or size > 30:
        size = int(raw_input('\n\n%sChoose the size of the gameboard.'
                           '(min:10, max:30) :' % errormsg))
        if size < 10 or size > 30:
            errormsg = "ERROR: Value answer is not valid! please retry\n"

    # Generate the Gameboard
    gameboard = []
    for row in range(size):
        gameboard.append(['O'] * size)

    return gameboard


def print_board(playboard):
    """
    :param playboard: Type: list; Take multi dimension list variable gameboard
    :Output: Print nicely the gameboard on the screen
    """
    for row in playboard:
        print " ".join(row)

def random_row(board):
    """
    :param board: Type: list; Take multi dimension list variable gameboard
    :return: A random row in the gameboard
    """
    return randint(0, len(board) - 1)

def random_col(board):
    """
    :param board: Type: list; Take multi dimension list variable gameboard
    :return: A random column in the gameboard
    """
    return randint(0, len(board[0]) - 1)

def create_boat():
    """
    :return: A list of choosen boat type.  The number of items in the list define the numbers of ship to find in the game.
    """

    qty = int(raw_input("How many ship do you want?"))
    boat_type = []
    errormsg = ""

    for i in range(qty):
        answer = None
        while answer > 5 or answer < 1 or answer == None:
            answer = int(raw_input('\n\n\n\n\n%s1: Aircraft Carrier (size 5)\n'
                                   '2: Battle Cruise (size: 4)\n'
                                   '3: Battle Ship (size 3)\n'
                                   '4: Support Ship (size 2)\n'
                                   '5: Submarine (size 1)\n\n'
                                   "Ship %s\n"
                                   'Choose one of the following options:' % (errormsg, (i + 1))))
            if answer > 5 or answer < 1:
                errormsg = "\n\nERROR: Invalid Option: value %s is not a valid ship!\n" % answer

        # Validate that raw_input answer is in valid range
        # while answer > 5 or answer < 1:
        #     print "\n\nERROR: Invalid Option: value %s is not a valid boat!\n" % answer
        #     answer = None
        #     answer = int(raw_input("\n\n\n\n\n1: Aircraft Carrier (size 5)\n"
        #                        "2: Battle Cruise (size: 4)\n"
        #                        "3: Battle Ship (size 3)\n"
        #                        "4: Support Ship (size 2)\n"
        #                        "5: Submarine (size 1)\n\n"
        #                        "Ship %s\n"
        #                        "Choose one of the following options:" % (i + 1)))

        # Add value to boat_type list
        boat_type.append(answer)
    return boat_type


def get_boat_type(type_boat):
    """
    :param type_boat: Type: int; Take integer variable value that define the type of ship
    :return: The name and description of the ship.
    """
    if type_boat == 1:
        return ['Aircraft Carrier (size 5)', 5]
    elif type_boat == 2:
        return ['Battle Cruise (size: 4)', 4]
    elif type_boat == 3:
        return ['Battle Ship (size 3)', 3]
    elif type_boat == 4:
        return ['Support Ship (size 2)', 2]
    elif type_boat == 5:
        return ['Submarine (size 1)', 1]


def hidden_ship_coordinate(hidden_ship):
    for ship in hidden_ship:

        return range(ship[1], ship[2][1])


def hide_ships(board, ships):
    """
    :param board: Type: list of list of string; Take in a multi dimension list defining the Gameboard
    :param ship: Type: list of integer; Take in a list defining the type and number of ship to find in the game.
    :return: hidden_ships [int orientation, int start, list boat_info[str desc, int type_boat]
    """

    hidden_ships = []
    start_pos = []

    for ship in ships:

        # Get boat informations *size and description*
        ship_infos = get_boat_type(ship)

        # Debug
        print "DEBUG: %s: %s" % (ship_infos[0], ship_infos[1])

        # Find a spot big enough to hide ship

        while True: # Exit the loop if start and end position are inside the limit of the board

            # Decide which orientation to use to hide the ship. 0=horizontal, 1=vertical
            orientation = getrandbits(1)
            start_pos.append(random_row(board)) # index 0 = row
            start_pos.append(random_col(board)) # index 1 = col

            #Debug
            print "DEBUG: Start Posiion row: %s" % start_pos[0]
            print "DEBUG: Start Posiion col: %s" % start_pos[1]
            print "DEBUG: Orientation: %s" % orientation

            if orientation == 0:
                if ((start_pos[0] + ship_infos[1]) < len(board)) and (start_pos[1] < len(board)):  # Exit the loop if start and end position are inside the limit of the board
                    break
            elif orientation == 1:
                if ((start_pos[1] + ship_infos[1]) < len(board)) and (start_pos[0] < len(board)):  # Exit the loop if start and end position are inside the limit of the board
                    break
            else:
                print "ERROR: Value of orientation is set to something else than 0 or 1. Value: %s" % orientation


        hidden_ships.append([orientation, start_pos, ship_infos])
        print "Ship %s of type %s has been hidden" % (ship, ship_infos[0])

    # Debug
    print "DEBUG:", hidden_ships

    return hidden_ships

def guess_position():
    print "Not coded yet"

def is_ship_there():
    print "Not coded yet"

def is_ship_sunk():
    print "Not coded yet"

def is_all_ship_sunk():
    print "Not coded yet"




board = create_board()
ships = create_boat()
hidden_ships = hide_ships(board, ships)


#Debug
print "DEBUG:\n\n\n"
print_board(board)
for i in range(len(ships)):
    print "%s: %s" % (i, ships[i])


for ship in ships:
    ship_infos = get_boat_type(ship)
    print "%s: %s" % (ship_infos[0], ship_infos[1])


for j in range(len(hidden_ships)):
    # print "hidden_ships[j][0]:", hidden_ships[j][0]
    # print "hidden_ships[j][1]", hidden_ships[j][1]
    # print 'hidden_ships[j][2][0]', hidden_ships[j][2][0]
    # print 'hidden_ships[j][2][1])', hidden_ships[j][2][1]
    # print 'hidden_ships[j][1] + hidden_ships[j][2][1]', hidden_ships[j][1] + hidden_ships[j][2][1]

    print "\n\n%s:\n " \
          "orientation: %s\n" \
          "start: %s\n" \
          "end: %s\n" \
          "Ship Type: %s\n" \
          "Ship Size: %s\n" % (j, hidden_ships[j][0], hidden_ships[j][1], hidden_ships[j][1] + hidden_ships[j][2][1], hidden_ships[j][2][0], hidden_ships[j][2][1])



