import pygame as pg

pg.init()

cell_size = 100
board_length = 8

screen = pg.display.set_mode((800, 800))
pg.display.set_caption("Chess")

# Game State, takes FEN string
Game_State = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
Game_State_Array = list(Game_State)

fen_index_num = -1
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

def fen_index_of_click(): #deduction should be true if it's the end index
    global clicked
    global fen_index_num
    global fen_index_row
    global fen_index_col
    global x
    global y
    fen_index_row = 0
    fen_index_col = 0
    fen_index_num = -1
    clicked = pg.mouse.get_pressed()[0] # returns (bool, bool, bool). One for each mouse button. Indexing at 0
    x = int(pg.mouse.get_pos()[0] / 100) * 100  # round down to nearest hundreth
    y = int(pg.mouse.get_pos()[1] / 100) * 100
    for i in Game_State:
        if (x, y) == (fen_index_col, fen_index_row) and i != '/':
            fen_index_num += 1
            break
        if (x, y) == (fen_index_col, fen_index_row) and i == '/':
            break
        if i == '/':
            fen_index_num += 1
            fen_index_row += 100
            fen_index_col = 0
        elif i in "PNBRQKpnbrqk":
            fen_index_num += 1
            fen_index_col += 100
        elif i.isnumeric():
            if (x, y) != (fen_index_col, fen_index_row):
                fen_index_num += 1
            for j in range(0, int(i)):
                if (x, y) != (fen_index_col, fen_index_row):
                    fen_index_col += 100

            #else:
            #    if int(i) == 1:
            #        fen_index_num += 1
    print(fen_index_num)
    return

def capture(start_index, end_index):
    global Game_State
    global Game_State_Array
    temp1 = Game_State_Array[start_index]
    temp2 = Game_State_Array[end_index]

    if Game_State_Array[end_index].isnumeric() and int(Game_State_Array[end_index]) > 1:
        count = 0
        for i in Game_State_Array[end_index-1:0:-1]: #for loop that moves back to the slash and checks if the len of that is equal to or greater than x
            if i != '/':
                if i.isnumeric():
                    count += int(i)
                else:
                    count += 1
            else:
                break
        if count == int(x/100) and count != 0:
            Game_State_Array[end_index] = temp1
            Game_State_Array[start_index] = '1'
        else: # if count != int(x/100), which suggests that theres number at end index and our x coord falls somewhere in the middle of that numbers blank squares
            Game_State_Array[end_index] = str(int(x/100) - count)#str(int(Game_State_Array[end_index])-1)
            Game_State_Array.insert(end_index + 1, temp1)
            if int(x/100) != 7:
                Game_State_Array.insert(end_index + 2, str(8 - int(x/100) - 1))
            if start_index > end_index and int(x/100) != 7:
                Game_State_Array[start_index + 2] = '1'
            elif start_index > end_index:
                Game_State_Array[start_index + 1] = '1'
            elif end_index > start_index:
                Game_State_Array[start_index] = '1'
    else:
        Game_State_Array[end_index] = temp1
        Game_State_Array[start_index] = '1'

    Game_State = ''.join(str(i) for i in Game_State_Array)
    print(Game_State)
    print(Game_State_Array)
    return

running = True
while running:
    screen.blit(board, board.get_rect())
    gamestate()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            fen_index_of_click()
            if clicked == True:
                fen_index_when_clicked = fen_index_num
        elif event.type == pg.MOUSEBUTTONUP:
            fen_index_of_click() #overcounts because i start at 0 and count every element
            # if released == True: (enter some code in the fen index fn
            fen_index_when_released = fen_index_num
            capture(fen_index_when_clicked, fen_index_when_released)

    pg.display.update()
