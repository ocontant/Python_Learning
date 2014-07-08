__author__ = 'ocontant'

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


def update_board(gameboard, coordinate, value):
    """
    :param gameboard: List of List defining the gameboard
    :param coordinate: X,Y coordinate
    :param value: Value to assign to the Grid case in the gameboard. ('O' Ocean, 'S' Ship Hit, 'X' Missed)
    :return: Updated gameboard.
    :Call: gameboard_var = update_board(gameboard, [x,y], 'S')
    """
    newgameboard = gameboard
    newgameboard[coordinate[0]][coordinate[1]] = value

    return newgameboard


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
            if answer > 5 or answer < 1 or answer == None:
                errormsg = "\n\nERROR: Invalid Option: value %s is not a valid ship!\n" % answer

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


def get_ship_coordinate(orientation, start_pos, ship_infos):
    """
    :param orientation:
    :param start_pos:
    :param ship_infos:
    :return:
    """
    ship_coordinate = []
    for size in range(ship_infos[1]):
        if orientation:  # 1 = true, 0 = false
            ship_coordinate.append([start_pos[0], (start_pos[orientation] + size)])
        else:
            ship_coordinate.append([(start_pos[orientation] + size), start_pos[1]])
    return ship_coordinate


def hide_ships(board, ships):
    """
    :param board: Type: list of list of string; Take in a multi dimension list defining the Gameboard
    :param ship: Type: list of integer; Each integer is a type of a ship. it defines the type and number of ship to find in the game.
    :return: hidden_ships [Coordinate[int(x),int(y)], ship_infos[str(desc),int(type_boat)]]
    """

    hidden_ships = []
    start_pos = []

    for ship in ships:

        # Get boat informations *size and description*
        ship_infos = get_boat_type(ship)

        # Debug
        print "DEBUG: ship_infos[0]:%s, ship_infos[1]: %s" % (ship_infos[0], ship_infos[1])

        # Find a spot big enough to hide ship

        while True: # Exit the loop if start and end position are inside the limit of the board
            orientation = None
            start_pos = []

            # Decide which orientation to use to hide the ship. 0=horizontal, 1=vertical
            orientation = getrandbits(1)
            start_pos.append(random_row(board)) # index 0 = row
            start_pos.append(random_col(board)) # index 1 = col

            #Debug
            # print "DEBUG: Start Posiion row: %s" % start_pos[0]
            # print "DEBUG: Start Posiion col: %s" % start_pos[1]
            # print "DEBUG: Orientation: %s" % orientation

            if ((start_pos[orientation] + ship_infos[1]) < len(board)):  # Exit the loop if start and end position are inside the limit of the board

                coordinates_ship = get_ship_coordinate(orientation, start_pos, ship_infos) # Get each pair of coordinate (x,y) to compare with other coordinate of other ship to detect if we are superposing ship

                juxtaposing = 0
                if len(hidden_ships) > 0:
                    for boat in hidden_ships:                       # Loop all ship hidden so far
                        for boat_coord in boat[0]:                  # Loop all coordinate for the current hidden ship
                            for ship_coord in coordinates_ship:      # Loop all coordinate for the new ship to hide
                                if ship_coord == boat_coord:        # Compare coordinate of the new ship to hide with the coordinate of all already hidden ship
                                    juxtaposing = 1
                    if juxtaposing: # 1 = true, 0 = false
                        print "WARNING: Coordinate touch another ship! Retrying another set of coordinate ..."
                    else:
                        break
                else:
                    break



        hidden_ships.append([coordinates_ship, ship_infos])
        print "Ship %s of type %s has been hidden" % (ship, ship_infos[0])

        #Debug
        # for boardcoord in coordinate_ship:
        #     x = boardcoord[0]
        #     y = boardcoord[1]
        #     board[x][y] = 'S'

    # Debug
    print "DEBUG: hidden_ships", hidden_ships

    return hidden_ships


def guess_position():
    """
    :return: User guess coordinate
    """
    guess_pos = []
    guess_pos.append(int(raw_input("Guess Row:"))-1)
    guess_pos.append(int(raw_input("Guess Col:"))-1)

    return guess_pos


def is_coordinate_attacked(gameboard, coordinate):
    """
    :param gameboard: List of list defining the gameboard
    :param coordinate: [int(x),int(y)]
    :return: True or False
    """
    if not gameboard[coordinate[0]][coordinate[1]] == 'O':
        return 1
    else:
        return 0


def is_ship_hit(coordinate, hidden_ships):
    """
    # Must check all hidden_ships coordinate and check if HIT.  If HIT, must update gameboard and check if ship is sunk and if all ship are sunk
    :param coordinate: X,Y coordinate to check
    :param hidden_ships: [Coordinate[int(x),int(y)], ship_infos[str(desc),int(type_boat)]]
    :return:
    """
    hit = 0

    for ship in hidden_ships:                       # Loop all ship hidden so far
        print "DEBUG is_ship_hit: ship", ship
        print "DEBUG is_ship_hit: ship[0]", ship[0]
        for ship_coords in ship[0]:                  # Loop all coordinate for the current hidden ship
            print "DEBUG is_ship_hit: ship_coords", ship_coords
            if ship_coords == coordinate:        # Compare coordinate of the new ship to hide with the coordinate of all already hidden ship
                hit = 1
                break
            print "DEBUG is_ship_hit: coordinate", coordinate

    if not hit: # 1 = true, 0 = false
        return 0
    else:
        return ship


def is_ship_sunk(gameboard, ship):
    """
    :param gameboard: List of list defining the gameboard
    :param ship: [[coordinates: [x,y]], [ship_infos: str(desc), int(type)]
    :return:
    """
    counter = 0
    for ship_coords in ship[0]:                  # Loop all coordinate for the current hidden ship
        if gameboard[ship_coords[0]][ship_coords[1]] == 'S':
            counter += 1

    if counter == len(ship[0]):
        return 1
    else:
        return 0


def is_all_ship_sunk(gameboard, hidden_ships):
    """
    :param gameboard: List of list defining the gameboard
    :param hidden_ships: [Coordinate[int(x),int(y)], ship_infos[str(desc),int(type_boat)]]
    :return:
    """
    for ship in hidden_ships:                       # Loop all ship hidden so far
        for ship_coords in ship[0]:                  # Loop all coordinate for the current hidden ship
                if gameboard[ship_coords[0]][ship_coords[1]] == 'O':
                    return 0                         # Will exit at the moment a coordinate == 'O' for ocean where a ship coordiante is.
    return 1                                         # Will execute only if no ship coordinate == 'O'


#### MAIN SECTION ####

# Initialization of the game
gameboard = create_board()
ships = create_boat()
hidden_ships = hide_ships(gameboard, ships)

# Start Playing
i = 0
while i < 10:
    print "Attempt:", i

    guess_pos = []
    guess_pos = guess_position()

    if is_coordinate_attacked(gameboard, guess_pos):
        print "Target already attacked previously!  Find another coordinate to attack!"
    else:
        shiphit = is_ship_hit(guess_pos, hidden_ships)

        if not shiphit:                                             # If guess_pos doesn't hit a ship, display X at coordinate on board, Else ship is hit and display S on board and validate if ship is sunk.
            gameboard = update_board(gameboard, guess_pos, 'X')
            print_board(gameboard)
            print "You missed!"
            i += 1
        else:                                                       # Ship has been hit, update gameboard
            gameboard = update_board(gameboard, guess_pos,'S')
            print_board(gameboard)

            if is_ship_sunk(gameboard, shiphit):                    # Ship might have been sunk by last hit.
                if is_all_ship_sunk(gameboard, hidden_ships):       # Ship has been sunk, maybe all ship are sunk by now.
                    print "Congratulation! You sunk all ship!!!"
                    break
                print "You hit a ship and sunk it!"
            else:
                print "You hit a ship!!!\n"




#### DEBUG SECTION ####

#Debug
# print "DEBUG:\n\n\n"
# print_board(gameboard)
# for i in range(len(ships)):
#     print "%s: %s" % (i, ships[i])
#
#
# for ship in ships:
#     ship_infos = get_boat_type(ship)
#     print "%s: %s" % (ship_infos[0], ship_infos[1])
#
#
# for j in range(len(hidden_ships)):
#     print "j", j
#     print 'hidden_ships[j][0]', hidden_ships[j][0]
#     print 'hidden_ships[j][2][0]', hidden_ships[j][1][0]
#     print 'hidden_ships[j][2][1])', hidden_ships[j][1][1]
#
#     print "\n\n%s:\n" \
#           "Set of coordinates: %s\n"\
#           "Ship Type: %s\n" \
#           "Ship Size: %s\n" % (j, hidden_ships[j][0], hidden_ships[j][1][0], hidden_ships[j][1][1])



