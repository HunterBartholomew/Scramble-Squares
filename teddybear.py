"""
US Military Branches:
    Aa = Army
    Bb = Navy
    Cc = Air Force
    Dd = Coast Guard

    ABCD = +ve
    abcd = -ve

clockwise-order assumed for card image data
"""
import sys
SHOW_PROGRESS = True

CARDS = [
    'dbcA', 'DCba', 'Abad',     #Initial  Arrangement
    'bdAc','CdDb' , 'ccBA',
    'DBCa', 'dAcb', 'aCBd',
]

def main():
    empty_board = [None for _ in range(9)]
    solvable, solution = solve(CARDS, empty_board)
    if not solvable:
        print 'no solution found :('
        fo.write("no solution found :(");
    else:
        print_board(solution)
        print 'solved! :)'
        fo.write("solved! :)");


# clockwise winding
LEFT, TOP, RIGHT, BOTTOM = 0, 1, 2, 3


# squares/nodes and out-links
# squares are numbered like most 2d arrays:
# 0 1 2
# 3 4 5
# 6 7 8
# links are (src-dir, dest-node, dest-dir)
SQUARE_LINKS = (
    # top row
    ((RIGHT, 1, LEFT), (BOTTOM, 3, TOP)),
    ((LEFT, 0, RIGHT), (BOTTOM, 4, TOP), (RIGHT, 2, LEFT)),
    ((LEFT, 1, RIGHT), (BOTTOM, 5, TOP)),

    # middle row
    ((TOP, 0, BOTTOM), (RIGHT, 4, LEFT), (BOTTOM, 6, TOP)),
    ((LEFT, 3, RIGHT), (TOP, 1, BOTTOM), (RIGHT, 5, LEFT), (BOTTOM, 7, TOP)),
    ((LEFT, 4, RIGHT), (TOP, 2, BOTTOM), (BOTTOM, 8, TOP)),

    # bottom row
    ((TOP, 3, BOTTOM), (RIGHT, 7, LEFT)),
    ((LEFT, 6, RIGHT), (TOP, 4, BOTTOM), (RIGHT, 8, LEFT)),
    ((LEFT, 7, RIGHT), (TOP, 5, BOTTOM)),
)


def solve(cards, board):
    """try to solve [the remainder of] the board, assuming
    that all pieces already placed fit correctly.

    Args:
        cards: list of cards to choose from
        board: 9-element array indicating board state

    Returns:
        True if the remainder has been solved
    """    
    if SHOW_PROGRESS:
      print_board(board)

    if not cards:
        # base-case: no more cards
        return True, board

    # we will put a card in the first empty space
    mine = board.index(None)
    
    # try every available card, in each possible rotation
    for choice, remainder in choices(cards):
        for card in rotations(choice):

            # place a card on the board
            new_board = board[0:mine] + [card] + board[mine + 1:]
            # check that it fits with pieces
            # that are already on the board
            fits = True
            for my_dir, other, other_dir in SQUARE_LINKS[mine]:
                if board[other]:
                    fits &= edge_match(new_board[mine][my_dir],
                                       new_board[other][other_dir])

            if fits:
                # our card fits, recurse
                solved, solved_board = solve(remainder, new_board)
                if solved:
                    return True, solved_board

    return False, None  # nothing fit


def choices(items):
    """iterate over the possible single choices in a list,
    splitting the list into a choice and the remainder

    Args:
        items: items to choose from

    Yields:
        tuple of selected item, and the remainder of items
        in the list
    """
    for idx, choice in enumerate(items):
        remainder = items[0:idx] + items[idx + 1:]
        yield choice, remainder


def rotations(text):
    """iterate over all rotations of a string"""
    for idx, _ in enumerate(text):
        yield text[idx:] + text[0:idx]


def edge_match(a, b):
    """an edge matches if the letters match,
    and they are not both lower or upper case"""
    return (a.lower() == b.lower() and
            is_uppercase(a) == is_lowercase(b))


def is_uppercase(a):
    return a == a.upper()


def is_lowercase(a):
    return a == a.lower()


# cartesian to card-dir
CARDXY = {(0, 1): LEFT, (1, 0): TOP, (2, 1): RIGHT, (1, 2): BOTTOM}

def print_board(board):
    """render board using the shader"""
    if SHOW_PROGRESS:
        for y in range(50):
            fo.write("\n");
    for y in range(12):
        fo.write(''.join(board_shader(x, y, board) for x in range(15)));
        fo.write("\n");
def board_shader(sx, sy, board):
    """pixelshader style render function"""
    tx, ty = sx/5, sy/4   # screen to tile
    px, py = sx%5, sy%4   # screen to tile-pixel
    square = ty * 3 + tx
    card = board[square]
    if card is None:
        return '-'
    try:
        dir = CARDXY[(px, py)]
    except KeyError:
        return ' '
    return board[square][dir]


if __name__ == '__main__':
    fo=open("Arrangements_tried.txt","a+")
    main()
    fo.close()
