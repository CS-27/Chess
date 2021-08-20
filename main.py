import pygame as pg

pg.init()

cell_size = 100
board_length = 8

screen = pg.display.set_mode((800, 800))
pg.display.set_caption("Chess")

# Game State, takes FEN string
Game_State = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

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
Piece_images['scaled_P_img'] = pg.transform.scale(P_img, (100, 100))
N_img = pg.image.load('wn.png')
Piece_images['scaled_N_img'] = pg.transform.scale(N_img, (100, 100))
B_img = pg.image.load('wb.png')
Piece_images['scaled_B_img'] = pg.transform.scale(B_img, (100, 100))
R_img = pg.image.load('wr.png')
Piece_images['scaled_R_img'] = pg.transform.scale(R_img, (100, 100))
Q_img = pg.image.load('wq.png')
Piece_images['scaled_Q_img'] = pg.transform.scale(Q_img, (100, 100))
K_img = pg.image.load('wk.png')
Piece_images['scaled_K_img'] = pg.transform.scale(K_img, (100, 100))

p_img = pg.image.load('bp.png')
Piece_images['scaled_p_img'] = pg.transform.scale(p_img, (100, 100))
n_img = pg.image.load('bn.png')
Piece_images['scaled_n_img'] = pg.transform.scale(n_img, (100, 100))
b_img = pg.image.load('bb.png')
Piece_images['scaled_b_img'] = pg.transform.scale(b_img, (100, 100))
r_img = pg.image.load('br.png')
Piece_images['scaled_r_img'] = pg.transform.scale(r_img, (100, 100))
q_img = pg.image.load('bq.png')
Piece_images['scaled_q_img'] = pg.transform.scale(q_img, (100, 100))
k_img = pg.image.load('bk.png')
Piece_images['scaled_k_img'] = pg.transform.scale(k_img, (100, 100))

def gamestate():
    count = 0
    row = 0
    for i in Game_State:
        if i in "PNBRQKpnbrqk":
            string = 'scaled_' + i + '_img'
            img = Piece_images[string]
            screen.blit(img, (0 + count * 100, row * 100))
            count += 1
        elif i == '/':
            row += 1
            count = 0
        elif isinstance(i, (int)):
            count += int(i)

running = True
while running:
    screen.blit(board, board.get_rect())
    gamestate()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    pg.display.update()
