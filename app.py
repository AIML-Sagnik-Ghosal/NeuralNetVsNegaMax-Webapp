import traceback
from flask import Flask, Response, request, render_template
import chess
import chess.engine as eng
import chess.svg
import numpy as np
from tensorflow.keras.models import model_from_json
import time as t
# Searching Ai's Move
def aimove():
    move = selectmove(2)
    return move
# Searching Stockfish's Move
def position_parser(position_string):
    piece_map = {'K': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 'Q': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 'R': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 'B': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                 'N': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                 'P': [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                 'k': [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                 'q': [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                 'r': [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                 'b': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                 'n': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 'p': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]}

    position_array = []

    ps = position_string.replace('/', '')

    for char in ps:
        position_array += 12 * int(char) * [0] if char.isdigit() else piece_map[char]

    # print("position_parser =>  position_array: {}".format(asizeof.asizeof(position_array)))

    return position_array


def fen_to_binary_vector(uci):
    # counter += 1
    # clear_output(wait=True)
    # print(str(counter)+"\n")
    board.push(uci)
    fen=board.fen()
    board.pop()
    fen_infos = fen.split()

    pieces_ = 0
    turn_ = 1
    castling_rights_ = 2
    en_passant_ = 3
    half_moves_ = 4
    moves_ = 5

    binary_vector = []

    binary_vector += ([1 if fen_infos[turn_] == 'w' else 0]
                      + [1 if 'K' in fen_infos[castling_rights_] else 0]
                      + [1 if 'Q' in fen_infos[castling_rights_] else 0]
                      + [1 if 'k' in fen_infos[castling_rights_] else 0]
                      + [1 if 'q' in fen_infos[castling_rights_] else 0]
                      + position_parser(fen_infos[pieces_])
                      )

    # print("fen_to_binary_vector =>  binary_vector: {}".format(asizeof.asizeof(binary_vector)))
    # clear_output(wait=True)

    return binary_vector
def moves():
    move_vec=list(map(fen_to_binary_vector,board.legal_moves))
    move_nvec=np.array(list(map(np.array,move_vec)))
    pred_eval=model.predict(move_nvec)
    return sorted(list(zip(pred_eval,board.legal_moves)),key=lambda x:x[0])[:1]
def eval():
    pawntable = [0, 0, 0, 0, 0, 0, 0, 0,5, 10, 10, -20, -20, 10, 10, 5,5, -5, -10, 0, 0, -10, -5, 5,0, 0, 0, 20, 20, 0, 0, 0,5, 5, 10, 25, 25, 10, 5, 5,10, 10, 20, 30, 30, 20, 10, 10,50, 50, 50, 50, 50, 50, 50, 50,0, 0, 0, 0, 0, 0, 0, 0]
    knightstable = [-50, -40, -30, -30, -30, -30, -40, -50,-40, -20, 0, 5, 5, 0, -20, -40,-30, 5, 10, 15, 15, 10, 5, -30,-30, 0, 15, 20, 20, 15, 0, -30,-30, 5, 15, 20, 20, 15, 5, -30,-30, 0, 10, 15, 15, 10, 0, -30,-40, -20, 0, 0, 0, 0, -20, -40,-50, -40, -30, -30, -30, -30, -40, -50]
    bishopstable = [-20, -10, -10, -10, -10, -10, -10, -20,-10, 5, 0, 0, 0, 0, 5, -10,-10, 10, 10, 10, 10, 10, 10, -10,-10, 0, 10, 10, 10, 10, 0, -10,-10, 5, 5, 10, 10, 5, 5, -10,-10, 0, 5, 10, 10, 5, 0, -10,-10, 0, 0, 0, 0, 0, 0, -10,-20, -10, -10, -10, -10, -10, -10, -20]
    rookstable = [0, 0, 0, 5, 5, 0, 0, 0,-5, 0, 0, 0, 0, 0, 0, -5,-5, 0, 0, 0, 0, 0, 0, -5,-5, 0, 0, 0, 0, 0, 0, -5,-5, 0, 0, 0, 0, 0, 0, -5,-5, 0, 0, 0, 0, 0, 0, -5,5, 10, 10, 10, 10, 10, 10, 5,0, 0, 0, 0, 0, 0, 0, 0]
    queenstable = [-20, -10, -10, -5, -5, -10, -10, -20,-10, 0, 0, 0, 0, 0, 0, -10,-10, 5, 5, 5, 5, 5, 0, -10,0, 0, 5, 5, 5, 5, 0, -5,-5, 0, 5, 5, 5, 5, 0, -5,-10, 0, 5, 5, 5, 5, 0, -10,-10, 0, 0, 0, 0, 0, 0, -10,-20, -10, -10, -5, -5, -10, -10, -20]
    kingstable = [20, 30, 10, 0, 0, 10, 30, 20,20, 20, 0, 0, 0, 0, 20, 20,-10, -20, -20, -20, -20, -20, -20, -10,-20, -30, -30, -40, -40, -30, -30, -20,-30, -40, -40, -50, -50, -40, -40, -30,-30, -40, -40, -50, -50, -40, -40, -30,-30, -40, -40, -50, -50, -40, -40, -30,-30, -40, -40, -50, -50, -40, -40, -30]
    if board.is_checkmate():
            if board.turn:
                return -9999
            else:
                return 9999
    if board.is_stalemate():
            return 0
    if board.is_insufficient_material():
            return 0
    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))
    material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)
    pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq = pawnsq + sum([-pawntable[chess.square_mirror(i)]
                           for i in board.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)]
                               for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq = sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq = bishopsq + sum([-bishopstable[chess.square_mirror(i)]
                               for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)]
                           for i in board.pieces(chess.ROOK, chess.BLACK)])
    queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum([-queenstable[chess.square_mirror(i)]
                             for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)])
    kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)]
                           for i in board.pieces(chess.KING, chess.BLACK)])
    eval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
    if board.turn:
        return eval
    else:
        return -eval
def selectmove(depth):
    bestMove = chess.Move.null()
    bestValue = -99999
    alpha = -100000
    beta = 100000
    for move in board.legal_moves:
        board.push(move)
        boardValue = -alphabeta(-beta, -alpha, depth - 1)
        if boardValue > bestValue:
            bestValue = boardValue
            bestMove = move
        if (boardValue > alpha):
            alpha = boardValue
        board.pop()
    return bestMove
def alphabeta(alpha, beta, depthleft):
    bestscore = -9999
    if (depthleft == 0):
        return quiesce(alpha, beta)
    for move in board.legal_moves:
        board.push(move)
        score = -alphabeta(-beta, -alpha, depthleft - 1)
        board.pop()
        if (score >= beta):
            return score
        if (score > bestscore):
            bestscore = score
        if (score > alpha):
            alpha = score
    return bestscore
def quiesce(alpha, beta):
    stand_pat = eval()
    if (stand_pat >= beta):
        return beta
    if (alpha < stand_pat):
        alpha = stand_pat
    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiesce(-beta, -alpha)
            board.pop()
            if (score >= beta):
                return beta
            if (score > alpha):
                alpha = score
    return alpha
def acceval(move):
    engine = eng.SimpleEngine.popen_uci("C:\\Users\SAGNIK GHOSHAL\Downloads\stockfish-windows-x86-64-avx2\stockfish\\stockfish-windows-x86-64-avx2.exe")
    ma=x=0
    mi=10000
    for m in board.legal_moves:
        board.push(m)
        i=engine.analyse(board,limit=chess.engine.Limit(time=0.1))
        s=i['score'].white().score() if not board.turn else i['score'].black().score() 
        if s==None:
            s=-100
        if m==move:
            x=s
        if s<mi:
            mi=s
        if s>ma:
            ma=s
        board.pop()
    return round((x-mi)/(ma-mi)*100,2)
acc1=acc2=t1=t2=0
cur='ai'
vsstate="off"
app = Flask(__name__)
# Front Page of the Flask Web Page
@app.route("/")
def main():
    global acc1,acc2,t1,t2,vsstate
    if board.is_checkmate():
        vsstate="off"
    return render_template("index.html",nnacc=acc1,nnt=t1,aiacc=acc2,ait=t2)
# Display Board
@app.route("/board.svg/")
def board():
    return Response(chess.svg.board(board=board, size=700), mimetype='image/svg+xml')
# Human Move
@app.route("/move/")
def move():
    try:
        move = request.args.get('move', default="")
        board.push_san(move)
    except Exception:
        traceback.print_exc()
    return main()
# Make Ai’s Move
@app.route("/ai/", methods=['POST'])
def ai():
    s=t.time()
    global cur,t2,acc2
    try:
        move=aimove()
    except Exception:
        traceback.print_exc()
    t2=round((t.time()-s)*1000,2)
    acc2=acceval(move)
    cur="ai"
    board.push(move)
    return main()
# Make UCI Compatible engine's move
@app.route("/nn/", methods=['POST'])
def nn():
    s=t.time()
    global cur,t1,acc1
    try:
        m=moves()
    except Exception:
        traceback.print_exc()
    t1=round((t.time()-s)*1000,2)
    acc1=acceval(m[0][1])
    cur='nn'
    board.push(m[0][1])
    return main()
@app.route("/vs/", methods=['POST','GET'])
def vs():
    try:
        global cur,vsstate
        if board.is_checkmate():
            vsstate="off"
            return main()
        vsstate="on"
        if cur=='ai':
            return nn()
        else:
            return ai()
    except Exception:
        traceback.print_exc()
        main()
@app.route('/vsstate')
def get_vs():
    global vsstate
    return str(vsstate)
# New Game
@app.route("/game/", methods=['POST'])
def game():
    board.reset()
    global acc1,acc2,t1,t2,cur,vsstate
    acc1=acc2=t1=t2=0
    cur='ai'
    vsstate="off"
    return main()
# Undo
@app.route("/undo/", methods=['POST'])
def undo():
    try:
        board.pop()
    except Exception:
        traceback.print_exc()
    return main()
board = chess.Board()
model=model_from_json(open("C:\\Users\SAGNIK GHOSHAL\Documents\code\phython\Chess_bot\\model.json","r").read())
app.run(debug=True)