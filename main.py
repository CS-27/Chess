import pygame as pg

pg.init()

cell_size = 100
board_length = 8

screen = pg.display.set_mode((800, 800))
pg.display.set_caption("Chess")

# Game State, takes FEN string
Game_State = 'rnbqkbnr/pppppppp/8/8/8/2N5/PPPPPPPP/R1BQKBNR w KQkq - 0 1' #"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
Game_State_Array = list(Game_State)

moves = []
coordinates = []
piece = 0
fen_index_num = 0
fen_index_row = 0
fen_index_col = 0
clicked = False
fen_index_when_clicked = 0
fen_index_when_released = 0
x = 0
y = 0

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
# White pieces are designated using upper-case letters ("PNBRQK") while black pieces use lowercase ("pnbrqk")
# Empty squares are noted using digits 1 through 8 (the number of empty squares), and "/" separates ranks.
# Active color. "w" means White moves next, "b" means Black moves next.
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
    x = int(pg.mouse.get_pos()[0] / 100) * 100  # round down to nearest hundreth
    y = int(pg.mouse.get_pos()[1] / 100) * 100
    # '8/pp6/8/8/8/8/8/8 w KQkq - 0 1'
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
    #'8/pp6/8/8/8/8/8/8 w KQkq - 0 1'
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
                    Game_State_Array.insert(end_index + 2, str(num - (int(x / 100) - count + 1)))
                    surrounding_index_numeric(start_index, end_index, 2)
    else:
        Game_State_Array[end_index] = temp1
        surrounding_index_numeric(start_index, end_index, 0)
    Game_State = ''.join(str(i) for i in Game_State_Array)
    print(Game_State)
    print(Game_State_Array)
    return

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


#need to determine if in check, maybe an overarching class for pieces so that can restrict movement if in check
class Pieces:
    def __init__(self, x, y, p):
        self.x = x
        self.y = y
        self.p = p
        self.coord = (x/100, y/100)
        #self.coord =
        if self.p.islower():
            self.colour = 'b'
        elif self.p.isupper():
            self.colour = 'w'

class Rook(Pieces):
    def moves(self):
        moves = []
        x = int(self.x)
        y = int(self.y)
        colour = self.colour
        max_up = 0
        max_down = 0
        max_right = 0
        max_left = 0
        #i can know the type of piece on a square that's landed on because of mouse release
        #gap upwards is 700-x then 600-x etc...
        #gap downwards is
        #coord = self.coord
        while (x//100 + max_left - 1) >= 0:
            if coordinates[y//100][x//100 + max_left - 1] == '-':
                max_left -= 1
            elif colour == 'b' and coordinates[y // 100][x // 100 + max_left - 1].isupper():
                max_left -= 1
                break
            elif colour == 'w' and coordinates[y // 100][x // 100 + max_left - 1].islower():
                max_left -= 1
                break
            else:
                break

        while ((x/100) + max_right + 1) <= 7:
            if coordinates[(y//100)][(x//100 + max_right + 1)] == '-':
                max_right += 1
            elif colour == 'b' and coordinates[y // 100][x // 100 + max_right + 1].isupper():
                max_right += 1
                break
            elif colour == 'w' and coordinates[y // 100][x // 100 + max_right + 1].islower():
                max_right += 1
                break
            else:
                break

        while (y//100 + max_down + 1) <= 7:
            if coordinates[y//100 + max_down + 1][x//100] == '-':
                max_down += 1
            elif colour == 'b' and coordinates[y // 100 + max_down + 1][x // 100].isupper():
                max_down += 1
                break
            elif colour == 'w' and coordinates[y // 100 + max_down + 1][x // 100].islower():
                max_down += 1
                break
            else:
                break

        while (y//100 + max_up + 1) >= 0:
            if coordinates[y//100 + max_up - 1][x//100] == '-':
                max_up -= 1
            elif colour == 'b' and coordinates[y // 100 + max_up - 1][x // 100].isupper():
                max_up -= 1
                break
            elif colour == 'w' and coordinates[y // 100 + max_up - 1][x // 100].islower():
                max_up -= 1
                break
            else:
                break

        for i in range(100,800,100):
            if (x-i)//100 >= x//100 + max_left:
                moves.append((x-i, y))
            if (x + i) // 100 <= x //100 + max_right:
                moves.append((x+i, y))
            if (y - i) // 100 >= y // 100 + max_up: #up the board is (-) in y direction
                moves.append((x, y-i))
            if (y + i) // 100 <= y // 100 + max_down:
                moves.append((x, y+i))
        return moves

class Knight(Pieces):
    def moves(self):
        moves = []
        x = self.x
        y = self.y
        for v in [-200, -100, 100, 200]:
            if abs(v) % 200 == 0:
                if x-100 in range (0,800,100) and y+v in range (0,800,100):
                    moves.append((x-100, y+v))
                if x+100 in range(0, 800, 100) and y+v in range(0, 800, 100):
                    moves.append((x+100, y+v))
            else:
                if x-200 in range(0, 800, 100) and y + v in range(0, 800, 100):
                    moves.append((x-200, y+v))
                if x + 200 in range(0, 800, 100) and y + v in range(0, 800, 100):
                    moves.append((x+200, y+v))
        return moves

class Bishop(Pieces):
    def moves(self):
        moves = []
        x = self.x
        y = self.y
        for i in range(100, 800, 100):
            if (x-i) >= 0 and (y-i) >= 0:
                moves.append((x-i, y-i))
            if (x+i) <= 700 and (y+i) <= 700:
                moves.append((x+i, y+i))
            if (x+i) <= 700 and (y-i) >= 0:
                moves.append((x+i, y-i))
            if (x-i) >= 0 and (y+i) <= 700:
                moves.append((x-i, y+i))
        return moves

class Queen(Pieces):
    def moves(self):
        moves = []
        x = self.x
        y = self.y
        for i in range(100, 800, 100):
            if x - (i) >= 0:
                moves.append((x - i, y))
            if x + (i) <= 700:
                moves.append((x + i, y))
            if y - (i) >= 0:
                moves.append((x, y - i))
            if y + (i) <= 700:
                moves.append((x, y + i))
            if (x-i) >= 0 and (y-i) >= 0:
                moves.append((x-i, y-i))
            if (x+i) <= 700 and (y+i) <= 700:
                moves.append((x+i, y+i))
            if (x+i) <= 700 and (y-i) >= 0:
                moves.append((x+i, y-i))
            if (x-i) >= 0 and (y+i) <= 700:
                moves.append((x-i, y+i))
        return moves

class King(Pieces): # need to add castling
    def moves(self):
        moves = []
        x = self.x
        y = self.y
        if x - (100) >= 0:
            moves.append((x - 100, y))
        if x + (100) <= 700:
            moves.append((x + 100, y))
        if y - (100) >= 0:
            moves.append((x, y - 100))
        if y + (100) <= 700:
            moves.append((x, y + 100))
        if (x - 100) >= 0 and (y - 100) >= 0:
            moves.append((x - 100, y - 100))
        if (x + 100) <= 700 and (y + 100) <= 700:
            moves.append((x + 100, y + 100))
        if (x + 100) <= 700 and (y - 100) >= 0:
            moves.append((x + 100, y - 100))
        if (x - 100) >= 0 and (y + 100) <= 700:
            moves.append((x - 100, y + 100))
        return moves

class Pawn(Pieces):
    def moves(self):
        moves = []
        x = self.x
        y = self.y
        colour = self.colour
        if colour == 'b':
            if y == 100:
                moves.append(())

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
                location()
                print(coordinates)
                if Game_State_Array[fen_index_when_clicked].upper() == 'R':
                    piece = Rook(x, y, Game_State_Array[fen_index_when_clicked])
                elif Game_State_Array[fen_index_when_clicked].upper() == 'N':
                    piece = Knight(x, y, Game_State_Array[fen_index_when_clicked])
                elif Game_State_Array[fen_index_when_clicked].upper() == 'B':
                    piece = Bishop(x, y, Game_State_Array[fen_index_when_clicked])
                elif Game_State_Array[fen_index_when_clicked].upper() == 'Q':
                    piece = Queen(x, y, Game_State_Array[fen_index_when_clicked])
                elif Game_State_Array[fen_index_when_clicked].upper() == 'K':
                    piece = King(x, y, Game_State_Array[fen_index_when_clicked])
                elif Game_State_Array[fen_index_when_clicked].upper() == 'P':
                    piece = Pawn(x, y, Game_State_Array[fen_index_when_clicked])
                print(x, y)
                moves = piece.moves()
                print(moves)
        if event.type == pg.MOUSEBUTTONUP:
            fen_index_of_click()
            fen_index_when_released = fen_index_num
            if (x, y) in moves:
                move(fen_index_when_clicked, fen_index_when_released)
            moves = 0
    pg.display.update()
