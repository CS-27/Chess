import pygame as pg

pg.init()

cell_size = 100
board_length = 8

screen = pg.display.set_mode((800, 800))
pg.display.set_caption("Chess")

# Game State, takes FEN string
Game_State = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
Game_State_Array = list(Game_State)

moves = []
coordinates = []
piece = 0
fen_index_num = 0
fen_index_row = 0
fen_index_col = 0
clicked = False
check = False
white_turn = True
fen_index_when_clicked = 0
fen_index_when_released = 0
x = 0
y = 0
check_x = 0
check_y = 0
check_piece = 0
check_colour = 0
check_piece_symbol = 0
coords_of_enemy_checking_pieces = []
coords_of_actual_enemy_checking_piece = []
coords_of_own_checking_pieces = []
discovered_attack_on_own_king = False
discovered_attack_on_own_king_after = False
discovered_attack_on_enemy_king = False
block_attack_on_king = False
global_colour = 0
global_piece_symbol = 0
temp_piece = 0
number_of_pieces_giving_check = 0
coords_of_two_checking_pieces = []
potential_for_double_check = False
double_attacked_squares = []
white_king_not_moved  = True
white_king_rook_not_moved = True
white_queen_rook_not_moved = True
black_king_not_moved = True
black_king_rook_not_moved = True
black_queen_rook_not_moved = True

# Board
board = pg.Surface((cell_size * 8, cell_size * 8))
board.fill((152, 103, 0))
for i in range(0, 8):
    for j in range(0, 8):
        if i % 2 == 0 and j % 2 == 0:
            pg.draw.rect(board, (242, 242, 242), (i * cell_size, j * cell_size, cell_size, cell_size))
        elif i % 2 != 0 and j % 2 != 0:
            pg.draw.rect(board, (242, 242, 242), (i * cell_size, j * cell_size, cell_size, cell_size))

# Pieces
# If neither side can castle, this is "-". Otherwise, this has one or more letters: "K" (White can castle kingside), "Q" (White can castle queenside), "k" (Black can castle kingside), and/or "q" (Black can castle queenside). A move that temporarily prevents castling does not negate this notation.
# En passant target square in algebraic notation. If there's no en passant target square, this is "-". If a pawn has just made a two-square move, this is the position "behind" the pawn. This is recorded regardless of whether there is a pawn in position to make an en passant capture.[6]
# etc refer to https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
Piece_images = {}

P_img = pg.image.load('wp.png')
Piece_images['P'] = pg.transform.scale(P_img, (100, 100))
N_img = pg.image.load('wn.png')
Piece_images['N'] = pg.transform.scale(N_img, (100, 100))
B_img = pg.image.load('wb.png')
Piece_images['B'] = pg.transform.scale(B_img, (100, 100))
R_img = pg.image.load('wr.png')
Piece_images['R'] = pg.transform.scale(R_img, (100, 100))
Q_img = pg.image.load('wq.png')
Piece_images['Q'] = pg.transform.scale(Q_img, (100, 100))
K_img = pg.image.load('wk.png')
Piece_images['K'] = pg.transform.scale(K_img, (100, 100))

p_img = pg.image.load('bp.png')
Piece_images['p'] = pg.transform.scale(p_img, (100, 100))
n_img = pg.image.load('bn.png')
Piece_images['n'] = pg.transform.scale(n_img, (100, 100))
b_img = pg.image.load('bb.png')
Piece_images['b'] = pg.transform.scale(b_img, (100, 100))
r_img = pg.image.load('br.png')
Piece_images['r'] = pg.transform.scale(r_img, (100, 100))
q_img = pg.image.load('bq.png')
Piece_images['q'] = pg.transform.scale(q_img, (100, 100))
k_img = pg.image.load('bk.png')
Piece_images['k'] = pg.transform.scale(k_img, (100, 100))

def gamestate():
    count = 0
    row = 0
    for i in Game_State:
        if i in "PNBRQKpnbrqk":
            img = Piece_images[i]
            screen.blit(img, (0 + count * 100, row * 100))
            count += 1
        elif i == '/':
            row += 1
            count = 0
        elif i.isnumeric():
            count += int(i)
        elif i == ' ':
            break
    return

def fen_index_of_click():
    global clicked
    global fen_index_num
    global fen_index_row
    global fen_index_col
    global x
    global y
    fen_index_row = 0
    fen_index_col = 0
    fen_index_num = 0
    clicked = pg.mouse.get_pressed()[0] # returns (bool, bool, bool). One for each mouse button. Indexing at 0
    x = int(pg.mouse.get_pos()[0] / 100) * 100
    y = int(pg.mouse.get_pos()[1] / 100) * 100
    for i in Game_State:
        if (x, y) == (fen_index_col, fen_index_row):
            break
        if i == '/':
            fen_index_num += 1
            fen_index_row += 100
            fen_index_col = 0
        elif i in "PNBRQKpnbrqk":
            fen_index_num += 1
            fen_index_col += 100
        elif i.isnumeric():
            count = 0
            for j in range(0, int(i)):
                if (x, y) != (fen_index_col, fen_index_row):
                    fen_index_col += 100
                    count += 1
            if count == int(i):
                fen_index_num += 1
    print(fen_index_num)
    return

def turn_rotater():
    global white_turn
    count = 0
    for i in Game_State:
        count += 1
        if i == ' ':
            turn = Game_State_Array[count]
            if turn == 'w':
                white_turn = False #rotate it
                Game_State_Array[count] = 'b'
            elif turn == 'b':
                white_turn = True
                Game_State_Array[count] = 'w'
    return white_turn

def surrounding_index_numeric(start_index, end_index, i):
    if end_index > start_index:
        i = 0
    if (start_index + i - 1) >= 0:
        if Game_State_Array[start_index + i - 1].isnumeric() and not Game_State_Array[start_index + i + 1].isnumeric():
            Game_State_Array[start_index + i - 1] = str(int(Game_State_Array[start_index + i - 1]) + 1)
            Game_State_Array.pop(start_index + i)
        elif Game_State_Array[start_index + i + 1].isnumeric() and not Game_State_Array[start_index + i - 1].isnumeric():
            Game_State_Array[start_index + i + 1] = str(int(Game_State_Array[start_index + i + 1]) + 1)
            Game_State_Array.pop(start_index + i)
        elif Game_State_Array[start_index + i - 1].isnumeric() and Game_State_Array[start_index + i + 1].isnumeric():
            Game_State_Array[start_index + i - 1] = str(int(Game_State_Array[start_index + i - 1]) + 1 + int(Game_State_Array[start_index + i + 1]))
            Game_State_Array.pop(start_index + i)
            Game_State_Array.pop(start_index + i)
        else:
            Game_State_Array[start_index + i] = '1'
    else:
        if Game_State_Array[start_index + i + 1].isnumeric():
            Game_State_Array[start_index + i + 1] = str(int(Game_State_Array[start_index + i + 1]) + 1)
            Game_State_Array.pop(start_index + i)
        else:
            Game_State_Array[start_index + i] = '1'
    return

def move(start_index, end_index):
    global Game_State
    global Game_State_Array
    temp1 = Game_State_Array[start_index]
    temp2 = Game_State_Array[end_index]
    if Game_State_Array[end_index].isnumeric() and int(Game_State_Array[end_index]) > 1:
        count = 0
        for i in Game_State_Array[end_index - 1:0:-1]: #for loop that moves back to the slash and checks if the len of that is equal to or greater than x
            if i != '/' and end_index - 1 >= 0:
                if i.isnumeric():
                    count += int(i)
                else:
                    count += 1
            else:
                break
        if end_index == 1:
            count += 1
        if count == int(x/100):
            num = int(Game_State_Array[end_index])
            Game_State_Array[end_index] = temp1
            Game_State_Array.insert(end_index + 1, str(num - 1))
            surrounding_index_numeric(start_index, end_index, 1)
        else:
            if int(Game_State_Array[end_index]) > int(x/100):
                num = int(Game_State_Array[end_index])
                if int(x/100) >= 1:
                    Game_State_Array[end_index] = str(int(x/100) - count)
                    Game_State_Array.insert(end_index + 1, temp1)
                    if (num - (int(x/100) - count + 1)) > 0:
                        Game_State_Array.insert(end_index + 2, str(num - (int(x/100) - count + 1)))
                        surrounding_index_numeric(start_index, end_index, 2)
                    else:
                        surrounding_index_numeric(start_index, end_index, 1)
                elif int(x/100) == 0:
                    Game_State_Array[end_index] = temp1
                    Game_State_Array.insert(end_index + 1, str(num - 1))
                    surrounding_index_numeric(start_index, end_index, 1)
            elif int(x/100) > int(Game_State_Array[end_index]):
                num = int(Game_State_Array[end_index])
                Game_State_Array[end_index] = str(int(x / 100) - count)
                Game_State_Array.insert(end_index + 1, temp1)
                if num != (int(x / 100) - count + 1):
                    Game_State_Array.insert(end_index + 2, str(num - (int(x / 100) - count + 1)))
                    surrounding_index_numeric(start_index, end_index, 2)
                elif Game_State_Array[end_index] < temp2:
                    if end_index > start_index:
                        counter = 0
                        for i in Game_State_Array[start_index:end_index]:
                            if i.isnumeric():
                                counter += 1
                            elif i != '/':
                                counter += 1
                            elif i == '/':
                                break
                        if end_index - start_index <= counter:
                            Game_State_Array.insert(end_index + 2, str(int(temp2) - int(Game_State_Array[end_index])))
                            Game_State_Array.pop(start_index)
                        else:
                            surrounding_index_numeric(start_index, end_index, 1)
                    elif end_index < start_index:
                        counter = 0
                        for i in Game_State_Array[start_index:end_index:-1]:
                            if i.isnumeric():
                                counter += 1
                            elif i != '/':
                                counter += 1
                            elif i == '/':
                                break
                        if start_index - end_index <= counter:
                            Game_State_Array.insert(end_index + 2, str(int(temp2) - int(Game_State_Array[end_index])))
                            Game_State_Array.pop(start_index)
                        else:
                            surrounding_index_numeric(start_index, end_index, 1)
                else:
                    surrounding_index_numeric(start_index, end_index, 1)
            elif int(x/100) == int(Game_State_Array[end_index]):
                if int(x/100) == count:
                    num = int(Game_State_Array[end_index])
                    Game_State_Array[end_index] = temp1
                    if num != 1:
                        Game_State_Array.insert(end_index + 1, str(num - 1))
                        surrounding_index_numeric(start_index, end_index, 1)
                    else:
                        surrounding_index_numeric(start_index, end_index, 0)
                else:
                    num = int(Game_State_Array[end_index])
                    Game_State_Array[end_index] = str(int(x / 100) - count)
                    Game_State_Array.insert(end_index + 1, temp1)
                    if (num - (int(x / 100) - count + 1)) > 0:
                        Game_State_Array.insert(end_index + 2, str(num - (int(x / 100) - count + 1)))
                        surrounding_index_numeric(start_index, end_index, 2)
                    else:
                        surrounding_index_numeric(start_index, end_index, 1)
    else:
        Game_State_Array[end_index] = temp1
        surrounding_index_numeric(start_index, end_index, 0)
    Game_State = ''.join(str(i) for i in Game_State_Array)
    print(Game_State)
    print(Game_State_Array)
    return

def search_for_symbol(x, y, symbol):
    global temp_piece
    temp_piece = 0
    if symbol.upper() == 'R':
        temp_piece = Rook(x, y, symbol)
    elif symbol.upper() == 'N':
        temp_piece = Knight(x, y, symbol)
    elif symbol.upper() == 'B':
        temp_piece = Bishop(x, y, symbol)
    elif symbol.upper() == 'Q':
        temp_piece = Queen(x, y, symbol)
    elif symbol.upper() == 'K':
        temp_piece = King(x, y, symbol)
    elif symbol.upper() == 'P':
        temp_piece = Pawn(x, y, symbol)
    return temp_piece

def location():
    global coordinates
    coordinates = [[], [], [], [], [], [], [], []]
    count = 0
    for i in Game_State:
        if i in "PNBRQKpnbrqk":
            coordinates[count].append(i)
        elif i == '/':
            count += 1
        elif i.isnumeric():
            for j in range(0, int(i)):
                coordinates[count].append('-')
        elif i == ' ':
            break
    return

def change_global_check_coords(x, y):
    global check_x
    global check_y
    check_x = x
    check_y = y
    return

def in_check(x, y, piece, colour, piece_symbol):
    global check
    global check_piece
    global check_colour
    global check_piece_symbol
    check = False
    check_piece_symbol = piece_symbol
    check_piece = search_for_symbol(check_x, check_y, check_piece_symbol)
    check_colour = colour
    moves = check_piece.moves(check_x, check_y, colour)
    for (i, j) in moves:
        if colour == 'w':
            if coordinates[j//100][i//100] == 'k':
                check = True
        elif colour == 'b':
            if coordinates[j//100][i//100] == 'K':
                check = True

def block_check(x, y, piece, colour, piece_symbol):
    moves1 = []
    if not isinstance(check_piece_symbol, int):
        c = check_piece_symbol
        d = check_x
        e = check_y
    else:
        for (a, b) in coords_of_actual_enemy_checking_piece:
            c = coordinates[b//100][a//100]
            d = a
            e = b
    if colour == 'w':
        temp_piece2 = search_for_symbol(x, y, c.lower())
        temp_piece4 = search_for_symbol(x, y, c.upper())
        moves2 = temp_piece2.moves(x, y, 'b')
        moves4 = temp_piece4.moves(x, y, 'w')
    else:
        temp_piece2 = search_for_symbol(x, y, c.upper())
        temp_piece4 = search_for_symbol(x, y, c.lower())
        moves2 = temp_piece2.moves(x, y, 'w')
        moves4 = temp_piece4.moves(x, y, 'b')
    if piece_symbol.upper() != 'K':
        for (i, j) in moves2:
            if coordinates[y // 100][x // 100] != coordinates[e//100][d//100]: #not capturing checking piece directly
                if coordinates[j//100][i//100].upper() == 'K' or coordinates[j//100][i//100] == piece_symbol:
                    if i < x and j < y and x < d and y < e:
                        moves1.append((x, y))
                    elif i > x and j > y and x > d and y > e:
                        moves1.append((x, y))
                    elif i < x and j > y and x < d and y > e:
                        moves1.append((x, y))
                    elif i > x and j < y and x > d and y < e:
                        moves1.append((x, y))
                    elif i > x and j == y and x > d and y == e:
                        moves1.append((x, y))
                    elif i < x and j == y and x < d and y == e:
                        moves1.append((x, y))
                    elif i == x and j > y and x == d and y > e:
                        moves1.append((x, y))
                    elif i == x and j < y and x == d and y < e:
                        moves1.append((x, y))
        if coordinates[y // 100][x // 100] == coordinates[e//100][d//100]:
            moves1.append((x, y))
    elif piece_symbol.upper() == 'K':
        if (d, e) not in moves4:
                moves1.append((x, y))
    return moves1

def path_from_piece_to_own_king(x, y, piece, colour, piece_symbol):
    global discovered_attack_on_own_king
    discovered_attack_on_own_king = False
    if colour == 'w':
        temp_piece = search_for_symbol(x, y, 'q')
        temp_moves = temp_piece.moves(x, y, 'b')
        for (a, b) in temp_moves:
            if coordinates[b // 100][a // 100] == 'K':
                return True
    elif colour == 'b':
        temp_piece = search_for_symbol(x, y, 'Q')
        temp_moves = temp_piece.moves(x, y, 'w')
        for (a, b) in temp_moves:
            if coordinates[b // 100][a // 100] == 'k':
                return True
    else:
        return False

def path_from_piece_to_enemy_king(x, y, piece, colour, piece_symbol):
    global discovered_attack_on_enemy_king
    discovered_attack_on_enemy_king = False
    if colour == 'w':
        temp_piece = search_for_symbol(x, y, 'Q')
        temp_moves = temp_piece.moves(x, y, 'w')
        for (a, b) in temp_moves:
            if coordinates[b // 100][a // 100] == 'k':
                return True
    elif colour == 'b':
        temp_piece = search_for_symbol(x, y, 'q')
        temp_moves = temp_piece.moves(x, y, 'b')
        for (a, b) in temp_moves:
            if coordinates[b // 100][a // 100] == 'K':
                return True
    else:
        return False

def own_pieces_attacking_blocker_piece(x, y, piece, colour, piece_symbol):
    global coords_of_own_checking_pieces
    coords_of_own_checking_pieces = []
    for i in ['R', 'B', 'Q']:
        if colour == 'w':
            temp_piece = search_for_symbol(x, y, i.lower())
            temp_moves = temp_piece.moves(x, y, colour)
            for (a, b) in temp_moves:
                if coordinates[b // 100][a // 100] == i.upper():
                    coords_of_own_checking_pieces.append((a, b))
        elif colour == 'b':
            temp_piece = search_for_symbol(x, y, i.upper())
            temp_moves = temp_piece.moves(x, y, colour)
            for (a, b) in temp_moves:
                if coordinates[b // 100][a // 100] == i.lower():
                    coords_of_own_checking_pieces.append((a, b))
    return


def enemy_pieces_attacking_blocker_piece(x, y, piece, colour, piece_symbol):
    global coords_of_enemy_checking_pieces
    coords_of_enemy_checking_pieces = []
    for i in ['R', 'B', 'Q']:
        if colour == 'w':
            temp_piece = search_for_symbol(x, y, i.upper())
            temp_moves = temp_piece.moves(x, y, colour)
            for (a, b) in temp_moves:
                if coordinates[b//100][a//100] == i.lower():
                    coords_of_enemy_checking_pieces.append((a, b))
        elif colour == 'b':
            temp_piece = search_for_symbol(x, y, i.lower())
            temp_moves = temp_piece.moves(x, y, colour)
            for (a, b) in temp_moves:
                if coordinates[b//100][a//100] == i.upper():
                    coords_of_enemy_checking_pieces.append((a, b))
    return

def new_attack_on_enemy_king(x, y, piece, colour, piece_symbol):
    #maybe have a global list for pins if a,b leads to discovered_attack_on_king true
    global coords_of_two_checking_pieces
    global discovered_attack_on_enemy_king
    discovered_attack_on_enemy_king = False
    count = 0
    for e in coords_of_own_checking_pieces:
        count += 1
    if count > 0:
        for (a, b) in coords_of_own_checking_pieces:
            temp_piece1 = search_for_symbol(x, y, coordinates[b // 100][a // 100])
            if colour == 'w':
                k = 'k'
            elif colour == 'b':
                k = 'K'
            if not isinstance(temp_piece1, int):
                temp_moves = temp_piece1.moves(x, y, colour)
                for (c, d) in temp_moves:
                    if coordinates[d // 100][c // 100] == k:
                        if coordinates[b // 100][a // 100].upper() == 'B' or coordinates[b // 100][a // 100].upper() == 'Q':
                            if x < a and y < b:  # bishop moving up and left
                                if c < x and d < y:
                                    discovered_attack_on_enemy_king = True
                                    coords_of_two_checking_pieces.clear()
                                    coords_of_two_checking_pieces.append((a, b))
                            elif x > a and y < b:  # bishop moving up and right
                                if c > x and d < y:
                                    discovered_attack_on_enemy_king = True
                                    coords_of_two_checking_pieces.clear()
                                    coords_of_two_checking_pieces.append((a, b))
                            elif x < a and y > b:  # bishop moving down and left
                                if c < x and d > y:
                                    discovered_attack_on_enemy_king = True
                                    coords_of_two_checking_pieces.clear()
                                    coords_of_two_checking_pieces.append((a, b))
                            elif x > a and y > b:  # bishop moving down and right
                                if c > x and d > y:
                                    discovered_attack_on_enemy_king = True
                                    coords_of_two_checking_pieces.clear()
                                    coords_of_two_checking_pieces.append((a, b))
                        if coordinates[b // 100][a // 100].upper() == 'R' or coordinates[b // 100][a // 100].upper() == 'Q':
                            if x < a and y == b:  # rook moving left
                                if c < x and d == y:
                                    discovered_attack_on_enemy_king = True
                                    coords_of_two_checking_pieces.clear()
                                    coords_of_two_checking_pieces.append((a, b))
                            elif x > a and y == b:  # rook moving right
                                if c > x and d == y:
                                    discovered_attack_on_enemy_king = True
                                    coords_of_two_checking_pieces.clear()
                                    coords_of_two_checking_pieces.append((a, b))
                            elif y < b and x == a:  # rook moving up
                                if d < y and c == x:
                                    discovered_attack_on_enemy_king = True
                                    coords_of_two_checking_pieces.clear()
                                    coords_of_two_checking_pieces.append((a, b))
                            elif y > b and x == a:  # rook moving down
                                if d > y and c == x:
                                    discovered_attack_on_enemy_king = True
                                    coords_of_two_checking_pieces.clear()
                                    coords_of_two_checking_pieces.append((a, b))
        return

def new_attack_on_own_king(x, y, piece, colour, piece_symbol, i: range(1, 3), temp_symbol):
    #maybe have a global list for pins if a,b leads to discovered_attack_on_king true
    global discovered_attack_on_own_king
    global block_attack_on_king
    global coords_of_actual_enemy_checking_piece
    coords_of_actual_enemy_checking_piece = []
    if i == 1:
        discovered_attack_on_own_king = False
    if i == 2:
        block_attack_on_king = False
    count = 0
    for e in coords_of_enemy_checking_pieces:
        count += 1
    if count > 0:
        for (a, b) in coords_of_enemy_checking_pieces:
            print(coords_of_enemy_checking_pieces)
            temp_piece1 = search_for_symbol(x, y, coordinates[b // 100][a // 100])
            if colour == 'w':
                col, k, k2 = 'b', temp_symbol.upper(), 'K'
            elif colour == 'b':
                col, k, k2 = 'w', temp_symbol.lower(), 'k'
            if not isinstance(temp_piece1, int):
                temp_moves = temp_piece1.moves(x, y, col)
                for (c, d) in temp_moves:
                    if coordinates[d // 100][c // 100] == k or coordinates[d // 100][c // 100] == k2:
                        if coordinates[b // 100][a // 100].upper() == 'B' or coordinates[b // 100][a // 100].upper() == 'Q':
                            if x < a and y < b:  # bishop moving up and left
                                if c < x and d < y:
                                    if i == 1:
                                        discovered_attack_on_own_king = True
                                    if i == 2:
                                        block_attack_on_king = True
                                    coords_of_actual_enemy_checking_piece.append((a, b))
                            elif x > a and y < b:  # bishop moving up and right
                                if c > x and d < y:
                                    if i == 1:
                                        discovered_attack_on_own_king = True
                                    if i == 2:
                                        block_attack_on_king = True
                                    coords_of_actual_enemy_checking_piece.append((a, b))
                            elif x < a and y > b:  # bishop moving down and left
                                if c < x and d > y:
                                    if i == 1:
                                        discovered_attack_on_own_king = True
                                    if i == 2:
                                        block_attack_on_king = True
                                    coords_of_actual_enemy_checking_piece.append((a, b))
                            elif x > a and y > b:  # bishop moving down and right
                                if c > x and d > y:
                                    if i == 1:
                                        discovered_attack_on_own_king = True
                                    if i == 2:
                                        block_attack_on_king = True
                                    coords_of_actual_enemy_checking_piece.append((a, b))
                        if coordinates[b // 100][a // 100].upper() == 'R' or coordinates[b // 100][a // 100].upper() == 'Q':
                            if x < a and y == b:  # rook moving left
                                if c < x and d == y:
                                    if i == 1:
                                        discovered_attack_on_own_king = True
                                    if i == 2:
                                        block_attack_on_king = True
                                    coords_of_actual_enemy_checking_piece.append((a, b))
                            elif x > a and y == b:  # rook moving right
                                if c > x and d == y:
                                    if i == 1:
                                        discovered_attack_on_own_king = True
                                    if i == 2:
                                        block_attack_on_king = True
                                    coords_of_actual_enemy_checking_piece.append((a, b))
                            elif y < b and x == a:  # rook moving up
                                if d < y and c == x:
                                    if i == 1:
                                        discovered_attack_on_own_king = True
                                    if i == 2:
                                        block_attack_on_king = True
                                    coords_of_actual_enemy_checking_piece.append((a, b))
                            elif y > b and x == a:  # rook moving down
                                if d > y and c == x:
                                    if i == 1:
                                        discovered_attack_on_own_king = True
                                    if i == 2:
                                        block_attack_on_king = True
                                    coords_of_actual_enemy_checking_piece.append((a, b))
        return

def safe_square_for_king(x, y, piece, colour, piece_symbol):
    if piece_symbol.upper() != 'K':
        return True
    for i in ['R', 'N', 'B', 'Q', 'K', 'P']:
        if colour == 'w':
            i = i.upper()
            j = i.lower()
        else:
            i = i.lower()
            j = i.upper()
        temp_piece2 = search_for_symbol(x, y, i)
        temp_moves2 = temp_piece2.moves(x, y, colour)
        for (a, b) in temp_moves2:
            if coordinates[b//100][a//100] == j:
                return False
    return True

def king_moves_if_double_check(x, y, piece, colour, piece_symbol):
    global coords_of_two_checking_pieces
    global double_attacked_squares
    double_attacked_squares = []
    (a, b) = coords_of_two_checking_pieces[0]
    (c, d) = coords_of_two_checking_pieces[1]
    attacking_piece1 = search_for_symbol(a, b, coordinates[b//100][a//100])
    attacking_piece2 = search_for_symbol(c, d, coordinates[d // 100][c // 100])
    if coordinates[b//100][a//100].islower():
        double_attacked_squares.append(attacking_piece1.moves(a, b, 'b'))
        double_attacked_squares.append(attacking_piece2.moves(c, d, 'b'))
    else:
        double_attacked_squares.append(attacking_piece1.moves(a, b, 'w'))
        double_attacked_squares.append(attacking_piece2.moves(c, d, 'w'))
    return double_attacked_squares

class Pieces:
    def __init__(self, x, y, p):
        self.x = x
        self.y = y
        self.p = p
        #self.coord = (x/100, y/100)
        if self.p.islower():
            self.colour = 'b'
        elif self.p.isupper():
            self.colour = 'w'

class Rook(Pieces):
    def moves(self, x, y, colour):
        moves = []
        x = x//100
        y = y//100
        p = self.p
        colour = self.colour
        max_up = 0
        max_down = 0
        max_right = 0
        max_left = 0
        while (x + max_left - 1) >= 0:
            if coordinates[y][x + max_left - 1] == '-':
                max_left -= 1
            elif (colour == 'b' and coordinates[y][x + max_left - 1].isupper()) or (colour == 'w' and coordinates[y][x + max_left - 1].islower()):
                max_left -= 1
                break
            elif (coordinates[y][x + max_left - 1] == p):
                max_left -= 1
            else:
                break
        while (x + max_right + 1) <= 7:
            if coordinates[y][x + max_right + 1] == '-':
                max_right += 1
            elif (colour == 'b' and coordinates[y][x + max_right + 1].isupper()) or (colour == 'w' and coordinates[y][x + max_right + 1].islower()):
                max_right += 1
                break
            elif coordinates[y][x + max_right + 1] == p:
                max_right += 1
            else:
                break
        while (y + max_down + 1) <= 7:
            if coordinates[y + max_down + 1][x] == '-':
                max_down += 1
            elif (colour == 'b' and coordinates[y + max_down + 1][x].isupper()) or (colour == 'w' and coordinates[y + max_down + 1][x].islower()):
                max_down += 1
                break
            elif coordinates[y + max_down + 1][x] == p:
                max_down += 1
            else:
                break
        while (y + max_up - 1) >= 0:
            if coordinates[y + max_up - 1][x] == '-':
                max_up -= 1
            elif (colour == 'b' and coordinates[y + max_up - 1][x].isupper()) or (colour == 'w' and coordinates[y + max_up - 1][x].islower()):
                max_up -= 1
                break
            elif coordinates[y + max_up - 1][x] == p:
                max_up -= 1
            else:
                break
        for i in range(1, 8):
            if x-i >= x+max_left:
                moves.append(((x-i)*100, y*100))
            if x+i <= x+max_right:
                moves.append(((x+i)*100, y*100))
            if y-i >= y+max_up: #up the board is (-) in y direction
                moves.append((x*100, (y-i)*100))
            if y+i <= y+max_down:
                moves.append((x*100, (y+i)*100))
        return moves

class Knight(Pieces):
    def moves(self, x, y, colour):
        x = x//100
        y = y//100
        moves = []
        p = self.p
        colour = self.colour
        for v in [-2, -1, 1, 2]:
            if abs(v) % 2 == 0:
                for i in [1, -1]:
                    if x+i in range (0,8) and y+v in range (0,8):
                        if (colour == 'w' and (coordinates[y + v][x + i].islower() or coordinates[y + v][x + i] == '-')) or (colour == 'b' and (coordinates[y + v][x + i].isupper() or coordinates[y + v][x + i] == '-')):
                            moves.append(((x+i)*100, (y+v)*100))
            else:
                for j in [2, -2]:
                    if x + j in range(0, 8) and y + v in range(0, 8):
                        if (colour == 'w' and (coordinates[y + v][x + j].islower() or coordinates[y + v][x + j] == '-')) or (colour == 'b' and (coordinates[y + v][x + j].isupper() or coordinates[y + v][x + j] == '-')):
                            moves.append(((x+j)*100, (y+v)*100))
        return moves

class Bishop(Pieces):
    def moves(self, x, y, colour):
        moves = []
        x = x // 100
        y = y // 100
        p = self.p
        colour = self.colour
        max_up_left = 0 #all positive values
        max_up_right = 0
        max_down_left = 0
        max_down_right = 0
        while (x - max_up_left - 1) >= 0 and (y - max_up_left - 1) >= 0:
            if coordinates[y - max_up_left - 1][x - max_up_left - 1] == '-':
                max_up_left += 1
            elif (colour == 'b' and coordinates[y - max_up_left - 1][x - max_up_left - 1].isupper()) or (colour == 'w' and coordinates[y - max_up_left - 1][x - max_up_left - 1].islower()):
                max_up_left += 1
                break
            elif coordinates[y - max_up_left - 1][x - max_up_left - 1] == p:
                max_up_left += 1
            else:
                break
        while (x + max_up_right + 1) <= 7 and (y - max_up_right - 1) >= 0:
            if coordinates[y - max_up_right - 1][x + max_up_right + 1] == '-':
                max_up_right += 1
            elif (colour == 'b' and coordinates[y - max_up_right - 1][x + max_up_right + 1].isupper()) or (colour == 'w' and coordinates[y - max_up_right - 1][x + max_up_right + 1].islower()):
                max_up_right += 1
                break
            elif coordinates[y - max_up_right - 1][x + max_up_right + 1] == p:
                max_up_right += 1
            else:
                break
        while (x - max_down_left - 1) >= 0 and (y + max_down_left + 1) <= 7:
            if coordinates[y + max_down_left + 1][x - max_down_left - 1] == '-':
                max_down_left += 1
            elif (colour == 'b' and coordinates[y + max_down_left + 1][x - max_down_left - 1].isupper()) or (colour == 'w' and coordinates[y + max_down_left + 1][x - max_down_left - 1].islower()):
                max_down_left += 1
                break
            elif coordinates[y + max_down_left + 1][x - max_down_left - 1] == p:
                max_down_left += 1
            else:
                break
        while (x + max_down_right + 1) <= 7 and (y + max_down_right + 1) <= 7:
            if coordinates[y + max_down_right + 1][x + max_down_right + 1] == '-':
                max_down_right += 1
            elif (colour == 'b' and coordinates[y + max_down_right + 1][x + max_down_right + 1].isupper()) or (colour == 'w' and coordinates[y + max_down_right + 1][x + max_down_right + 1].islower()):
                max_down_right += 1
                break
            elif coordinates[y + max_down_right + 1][x + max_down_right + 1] == p:
                max_down_right += 1
            else:
                break
        for i in range(1, 8):
            if (x-i) >= x-max_up_left and (y-i) >= y-max_up_left:
                moves.append(((x-i)*100, (y-i)*100))
            if (x+i) <= x+max_down_right and (y+i) <= y+max_down_right:
                moves.append(((x+i)*100, (y+i)*100))
            if (x+i) <= x+max_up_right and (y-i) >= y-max_up_right:
                moves.append(((x+i)*100, (y-i)*100))
            if (x-i) >= x-max_down_left and (y+i) <= y+max_down_left:
                moves.append(((x-i)*100, (y+i)*100))
        return moves

class Queen(Pieces):
    def moves(self, x, y, colour):
        x = x
        y = y
        moves = []
        p = self.p
        rook = Rook(x, y, p)
        bishop = Bishop(x, y, p)
        rook_moves = rook.moves(x, y, colour)
        bishop_moves = bishop.moves(x, y, colour)
        queen_list = rook_moves + bishop_moves
        return queen_list

class King(Pieces): # need to add castling
    def moves(self, x, y, colour):
        moves = []
        x = x // 100
        y = y // 100
        p = self.p
        colour = self.colour
        if x - 1 >= 0 :
            if (colour == 'w' and coordinates[y][(x - 1)].islower()) or (colour == 'b' and coordinates[y][(x - 1)].isupper()) or (coordinates[y][(x - 1)] == '-'):
                moves.append(((x*100) - 100, (y*100)))
        if x + 1 <= 7:
            if (colour == 'w' and coordinates[y][(x + 1)].islower()) or (colour == 'b' and coordinates[y][(x + 1)].isupper()) or (coordinates[y][(x + 1)] == '-'):
                moves.append(((x*100) + 100, (y*100)))
        if y - 1 >= 0:
            if (colour == 'w' and coordinates[(y - 1)][x].islower()) or (colour == 'b' and coordinates[(y - 1)][x].isupper()) or (coordinates[(y - 1)][x] == '-'):
                moves.append(((x*100) , (y*100) - 100))
        if y + 1 <= 7:
            if (colour == 'w' and coordinates[(y + 1)][x].islower()) or (colour == 'b' and coordinates[(y + 1)][x].isupper()) or (coordinates[(y + 1)][x] == '-'):
                moves.append(((x*100) , (y*100) + 100))
        if x - 1 >= 0 and y - 1 >= 0:
            if (colour == 'w' and coordinates[y - 1][(x - 1)].islower()) or (colour == 'b' and coordinates[y - 1][(x - 1)].isupper()) or (coordinates[y - 1][(x - 1)] == '-'):
                moves.append(((x*100) - 100, (y*100) - 100))
        if x + 1 <= 7 and y + 1 <= 7:
            if (colour == 'w' and coordinates[y + 1][(x + 1)].islower()) or (colour == 'b' and coordinates[y + 1][(x + 1)].isupper()) or (coordinates[y + 1][(x + 1)] == '-'):
                moves.append(((x*100) + 100, (y*100) + 100))
        if x + 1 <= 7 and y - 1 >= 0:
            if (colour == 'w' and coordinates[y - 1][(x + 1)].islower()) or (colour == 'b' and coordinates[y - 1][(x + 1)].isupper()) or (coordinates[y - 1][(x + 1)] == '-'):
                moves.append(((x*100) + 100, (y*100) - 100))
        if x - 1 >= 0 and y + 1 <= 7:
            if (colour == 'w' and coordinates[y + 1][(x - 1)].islower()) or (colour == 'b' and coordinates[y + 1][(x - 1)].isupper()) or (coordinates[y + 1][(x - 1)] == '-'):
                moves.append(((x*100) - 100, (y*100) + 100))
        if colour == 'w':
            if white_king_not_moved == True:
                    if white_king_rook_not_moved == True:
                        if coordinates[y][x+1] == '-' and coordinates[y][x+2] == '-':
                            moves.append(((x*100)+200, (y*100)))
                    if white_queen_rook_not_moved == True:
                        if coordinates[y][x - 1] == '-' and coordinates[y][x - 2] == '-':
                            moves.append(((x * 100) - 200, (y * 100)))
        elif colour == 'b':
            if black_king_not_moved == True:
                    if black_king_rook_not_moved == True:
                        if coordinates[y][x + 1] == '-' and coordinates[y][x + 2] == '-':
                            moves.append(((x * 100) + 200, (y * 100)))
                    if black_queen_rook_not_moved == True:
                        if coordinates[y][x - 1] == '-' and coordinates[y][x - 2] == '-':
                            moves.append(((x * 100) - 200, (y * 100)))
        return moves

class Pawn(Pieces):
    def moves(self, x, y, colour):
        moves = []
        x = x // 100
        y = y // 100
        p = self.p
        colour = self.colour
        if colour == 'w':
            if y == 6 and coordinates[4][x] == '-':
                moves.append(((x * 100), (y * 100) - 200))
            if y - 1 >= 0 and coordinates[y-1][x] == '-': #implement queening
                moves.append(((x * 100), (y * 100) - 100))
            if y - 1 >= 0 and x + 1 <= 7:
                if coordinates[y - 1][(x + 1)].islower():
                    moves.append(((x * 100) + 100, (y * 100) - 100))
            if y - 1 >= 0 and x - 1 >= 0:
                if coordinates[y - 1][(x - 1)].islower():
                    moves.append(((x * 100) - 100, (y * 100) - 100))
            #need to implement en passant
        elif colour == 'b':
            if y == 1 and coordinates[3][x] == '-':
                moves.append(((x * 100), (y * 100) + 200))
            if y + 1 <= 7 and coordinates[y+1][x] == '-': #implement queening
                moves.append(((x * 100), (y * 100) + 100))
            if y + 1 <= 7 and x + 1 <= 7:
                if coordinates[y + 1][(x + 1)].isupper():
                    moves.append(((x * 100) + 100, (y * 100) + 100))
            if y + 1 <= 7 and x - 1 >= 0:
                if coordinates[y + 1][(x - 1)].isupper():
                    moves.append(((x * 100) - 100, (y * 100) + 100))
        return moves

running = True
while running:
    screen.blit(board, board.get_rect())
    gamestate()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            fen_index_of_click()
            if clicked == True:
                fen_index_when_clicked = fen_index_num
                global_piece_symbol = Game_State_Array[fen_index_when_clicked]
                if global_piece_symbol.isupper():
                    global_colour = 'w'
                elif global_piece_symbol.islower():
                    global_colour = 'b'
                start_x = x
                start_y = y
                location()
                print(coordinates)
                piece = search_for_symbol(x, y, global_piece_symbol)
                print(x, y)
                if not isinstance(piece, int):
                    moves = piece.moves(x, y, global_colour)
                print(moves)
                discovered_attack_on_own_king_after = False
            if path_from_piece_to_own_king(x, y, piece, global_colour, global_piece_symbol):
                enemy_pieces_attacking_blocker_piece(x, y, piece, global_colour, global_piece_symbol)
                new_attack_on_own_king(x, y, piece, global_colour, global_piece_symbol, 1, 'k')
            if path_from_piece_to_enemy_king(x, y, piece, global_colour, global_piece_symbol):
                own_pieces_attacking_blocker_piece(x, y, piece, global_colour, global_piece_symbol)
                new_attack_on_enemy_king(x, y, piece, global_colour, global_piece_symbol)
                if discovered_attack_on_enemy_king:
                    potential_for_double_check = True
        if event.type == pg.MOUSEBUTTONUP:
            fen_index_of_click()
            fen_index_when_released = fen_index_num
            if discovered_attack_on_own_king:
                blocking_moves = block_check(x, y, piece, global_colour, global_piece_symbol)
                if (x, y) in blocking_moves:
                    discovered_attack_on_own_king_after = False
                else:
                    discovered_attack_on_own_king_after = True
            if not isinstance(check_piece_symbol, int):
                new_attack_on_own_king(x, y, piece, global_colour, global_piece_symbol, 2, check_piece_symbol)
            if (x, y) in moves and global_piece_symbol.isalpha() and (not discovered_attack_on_own_king_after or (discovered_attack_on_own_king and (block_attack_on_king or global_piece_symbol.upper() == 'K'))) and safe_square_for_king(x, y, piece, global_colour, global_piece_symbol):
                if white_turn:
                    if global_piece_symbol == 'K' and start_x + 200 == x and start_y == y:
                        incremental_move1 = safe_square_for_king(x-100, y, piece, global_colour, global_piece_symbol)
                        incremental_move2 = safe_square_for_king(x, y, piece, global_colour, global_piece_symbol)
                        if incremental_move1 and incremental_move2:
                            counter = -1
                            for j in Game_State_Array:
                                counter += 1
                                if j == 'K':
                                    break
                            if not Game_State_Array[counter-1].isalpha():
                                Game_State_Array[counter-1] = str(int(Game_State_Array[counter-1]) + 1)
                                Game_State_Array[counter] = 'R'
                                Game_State_Array[counter + 1] = 'K'
                                Game_State_Array[counter + 2] = '1'
                                Game_State = ''.join(str(i) for i in Game_State_Array)
                                white_king_not_moved = False
                                white_king_rook_not_moved = False
                                turn_rotater()
                            else:
                                Game_State_Array[counter] = '1'
                                Game_State_Array[counter+1] = 'R'
                                Game_State_Array[counter + 2] = 'K'
                                Game_State_Array.insert(counter + 3, '1')
                                Game_State = ''.join(str(i) for i in Game_State_Array)
                                white_king_not_moved = False
                                white_king_rook_not_moved = False
                                turn_rotater()
                    elif global_piece_symbol == 'K' and start_x - 200 == x and start_y == y:
                        incremental_move1 = safe_square_for_king(x+100, y, piece, global_colour, global_piece_symbol)
                        incremental_move2 = safe_square_for_king(x, y, piece, global_colour, global_piece_symbol)
                        if incremental_move1 and incremental_move2:
                            counter = -1
                            for j in Game_State_Array:
                                counter += 1
                                if j == 'K':
                                    break
                            if not Game_State_Array[counter+1].isalpha():
                                Game_State_Array[counter+1] = str(int(Game_State_Array[counter+1]) + 1)
                                Game_State_Array[counter] = 'R'
                                Game_State_Array[counter - 1] = 'K'
                                Game_State_Array[counter - 2] = '2'
                                Game_State = ''.join(str(i) for i in Game_State_Array)
                                white_king_not_moved = False
                                white_queen_rook_not_moved = False
                                turn_rotater()
                            else:
                                Game_State_Array.insert(counter+1, '1')
                                Game_State_Array[counter] = 'R'
                                Game_State_Array[counter - 1] = 'K'
                                Game_State_Array[counter - 2] = '2'
                                Game_State = ''.join(str(i) for i in Game_State_Array)
                                white_king_not_moved = False
                                white_queen_rook_not_moved = False
                                turn_rotater()
                    elif check:
                        if potential_for_double_check:
                            if len(coords_of_two_checking_pieces) == 2:
                                if global_piece_symbol == 'K':
                                    king_moves_if_double_check(x, y, piece, global_colour, global_piece_symbol)
                                    if (x, y) not in double_attacked_squares:
                                        move(fen_index_when_clicked, fen_index_when_released)
                                        turn_rotater()
                                        change_global_check_coords(x, y)
                                        potential_for_double_check = False
                                        white_king_not_moved = False
                        else:
                            check_moves = block_check(x, y, piece, 'w', global_piece_symbol)
                            if (x, y) in check_moves:
                                move(fen_index_when_clicked, fen_index_when_released)
                                turn_rotater()
                                change_global_check_coords(x, y)
                                in_check(x, y, piece, 'w', global_piece_symbol)
                                if discovered_attack_on_enemy_king:
                                    new_attack_on_enemy_king(x, y, piece, global_colour, global_piece_symbol)
                                    if not discovered_attack_on_enemy_king:
                                        check = True
                                if global_piece_symbol == 'R' and start_x == 700 and start_y == 700:
                                    white_king_rook_not_moved = False
                                elif global_piece_symbol == 'R' and start_x == 0 and start_y == 700:
                                    white_queen_rook_not_moved = False
                                elif global_piece_symbol == 'K' and start_x == 400 and start_y == 700:
                                    white_king_not_moved = False
                                print(check)
                    elif global_piece_symbol.isupper():
                        move(fen_index_when_clicked, fen_index_when_released)
                        turn_rotater()
                        change_global_check_coords(x, y)
                        in_check(x, y, piece, 'w', global_piece_symbol)
                        if discovered_attack_on_enemy_king:
                            new_attack_on_enemy_king(x, y, piece, global_colour, global_piece_symbol)
                            if not discovered_attack_on_enemy_king:
                                if check:
                                    number_of_pieces_giving_check = 2
                                    coords_of_two_checking_pieces.append((x, y))
                                check = True
                        if global_piece_symbol == 'R' and start_x == 700 and start_y == 700:
                            white_king_rook_not_moved = False
                        elif global_piece_symbol == 'R' and start_x == 0 and start_y == 700:
                            white_queen_rook_not_moved = False
                        elif global_piece_symbol == 'K' and start_x == 400 and start_y == 700:
                            white_king_not_moved = False
                        print(check)

                else:
                    if global_piece_symbol == 'k' and start_x + 200 == x and start_y == y:
                        incremental_move1 = safe_square_for_king(x - 100, y, piece, global_colour, global_piece_symbol)
                        incremental_move2 = safe_square_for_king(x, y, piece, global_colour, global_piece_symbol)
                        if incremental_move1 and incremental_move2:
                            counter = -1
                            for j in Game_State_Array:
                                counter += 1
                                if j == 'k':
                                    break
                            if not Game_State_Array[counter - 1].isalpha():
                                Game_State_Array[counter - 1] = str(int(Game_State_Array[counter - 1]) + 1)
                                Game_State_Array[counter] = 'r'
                                Game_State_Array[counter + 1] = 'k'
                                Game_State_Array[counter + 2] = '1'
                                Game_State = ''.join(str(i) for i in Game_State_Array)
                                black_king_not_moved = False
                                black_king_rook_not_moved = False
                                turn_rotater()
                            else:
                                Game_State_Array[counter] = '1'
                                Game_State_Array[counter + 1] = 'r'
                                Game_State_Array[counter + 2] = 'k'
                                Game_State_Array.insert(counter + 3, '1')
                                Game_State = ''.join(str(i) for i in Game_State_Array)
                                black_king_not_moved = False
                                black_king_rook_not_moved = False
                                turn_rotater()
                    elif global_piece_symbol == 'k' and start_x - 200 == x and start_y == y:
                        incremental_move1 = safe_square_for_king(x + 100, y, piece, global_colour, global_piece_symbol)
                        incremental_move2 = safe_square_for_king(x, y, piece, global_colour, global_piece_symbol)
                        if incremental_move1 and incremental_move2:
                            counter = -1
                            for j in Game_State_Array:
                                counter += 1
                                if j == 'k':
                                    break
                            if not Game_State_Array[counter + 1].isalpha():
                                Game_State_Array[counter + 1] = str(int(Game_State_Array[counter + 1]) + 1)
                                Game_State_Array[counter] = 'r'
                                Game_State_Array[counter - 1] = 'k'
                                Game_State_Array[counter - 2] = '2'
                                Game_State = ''.join(str(i) for i in Game_State_Array)
                                black_king_not_moved = False
                                black_queen_rook_not_moved = False
                                turn_rotater()
                            else:
                                Game_State_Array.insert(counter + 1, '1')
                                Game_State_Array[counter] = 'r'
                                Game_State_Array[counter - 1] = 'k'
                                Game_State_Array[counter - 2] = '2'
                                Game_State = ''.join(str(i) for i in Game_State_Array)
                                black_king_not_moved = False
                                black_queen_rook_not_moved = False
                                turn_rotater()
                    elif check:
                        if potential_for_double_check:
                            if len(coords_of_two_checking_pieces) == 2:
                                if global_piece_symbol == 'k':
                                    king_moves_if_double_check(x, y, piece, global_colour, global_piece_symbol)
                                    if (x, y) not in double_attacked_squares:
                                        move(fen_index_when_clicked, fen_index_when_released)
                                        turn_rotater()
                                        change_global_check_coords(x, y)
                                        potential_for_double_check = False
                                        black_king_not_moved = False
                        else:
                            check_moves = block_check(x, y, piece, 'b', global_piece_symbol)
                            if (x, y) in check_moves and (x, y) in moves:
                                move(fen_index_when_clicked, fen_index_when_released)
                                turn_rotater()
                                change_global_check_coords(x, y)
                                in_check(x, y, piece, 'b', global_piece_symbol)
                                if discovered_attack_on_enemy_king:
                                    new_attack_on_enemy_king(x, y, piece, global_colour, global_piece_symbol)
                                    if not discovered_attack_on_enemy_king:
                                        check = True
                                if global_piece_symbol == 'r' and start_x == 700 and start_y == 0:
                                    black_king_rook_not_moved = False
                                elif global_piece_symbol == 'r' and start_x == 0 and start_y == 0:
                                    black_queen_rook_not_moved = False
                                elif global_piece_symbol == 'k' and start_x == 400 and start_y == 0:
                                    black_king_not_moved = False
                                print(check)
                    elif global_piece_symbol.islower():
                        move(fen_index_when_clicked, fen_index_when_released)
                        turn_rotater()
                        change_global_check_coords(x, y)
                        in_check(x, y, piece, 'b', global_piece_symbol)
                        if discovered_attack_on_enemy_king:
                            new_attack_on_enemy_king(x, y, piece, global_colour, global_piece_symbol)
                            if not discovered_attack_on_enemy_king:
                                if check:
                                    number_of_pieces_giving_check = 2
                                    coords_of_two_checking_pieces.append((x, y))
                                check = True
                        if global_piece_symbol == 'r' and start_x == 700 and start_y == 0:
                            black_king_rook_not_moved = False
                        elif global_piece_symbol == 'r' and start_x == 0 and start_y == 0:
                            black_queen_rook_not_moved = False
                        elif global_piece_symbol == 'k' and start_x == 400 and start_y == 0:
                            black_king_not_moved = False
                        print(check)

    pg.display.update()
