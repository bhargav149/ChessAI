from functools import lru_cache
import chess
import chess.polyglot

depthness = 10

#Hash the board for fast access and cache
chess.Board.__hash__ = chess.polyglot.zobrist_hash
@lru_cache(maxsize=None)

#Gets all legal moves and sort them for the best possible moves
def getMoves(board):
  moves = list(board.legal_moves)

  #sort for best result
  moves.sort(key=lambda move: board.is_capture(move), reverse=True)
  return moves

#Optimized minmax pruning trick for fast analysis
def aphaBeta(boardState):
  return maxF(0, boardState, float('inf'), float('-inf'))

def maxF(depth, boardState, alpha, beta):
  if depth >= depthness or boardState.is_game_over():
    return (evalBoard(boardState), None)

  max_value = float('-inf')
  best_move = None

  #Generate all moves for current turn
  for move in getMoves(boardState):

    #Change the board state to current move
    boardState.push(move)
    val, _ = minF(depth + 1, boardState, alpha, beta)
    boardState.pop()

    if val >= beta:
      return (val, move)

    if val > max_value:
      max_value = val
      best_move = move

    if alpha < val:
      alpha = val

  return (max_value, best_move)

def minF(depth, boardState, alpha, beta):

  #Stop at certain depth
  if depth >= depthness or boardState.is_game_over():
    return (evalBoard(boardState), None)

  minVal = float('inf')

  #Generate all moves for current turn
  for move in getMoves(boardState):

    #Change the board state to current move
    boardState.push(move)
    val, _ = maxF(depth + 1, boardState, alpha, beta)
    boardState.pop()

    if val <= alpha:
      return (val, move)

    if val < minVal:
        minVal = val

    if beta > val:
      beta = val

  return (minVal, None)

def evalBoard(board):

  #Game end with checkmate
  if board.is_checkmate():
    #Who lost?
    if board.turn:
      return float('-inf')
    else:
        return float('inf')

  #Stalemate
  if board.is_stalemate():
    return 0

  pieceVal = {chess.PAWN: 1, chess.KNIGHT: 4, chess.BISHOP: 5, chess.ROOK: 7, chess.QUEEN: 11}
  #Check all material on the board
  whiteVal = 0
  blackVal = 0
  for piece in board.piece_map().values():
    if piece.color == chess.WHITE and piece.piece_type != chess.KING:
      whiteVal += pieceVal[piece.piece_type]
    if piece.color == chess.BLACK and piece.piece_type != chess.KING:
      blackVal += pieceVal[piece.piece_type]

  score = whiteVal - blackVal
  return score


def convertTeam(team):
  if team == "W":
    return chess.WHITE
  else:
    return chess.BLACK

def convertPiece(piece):
  if piece == "QE":
    return chess.QUEEN
  elif piece == "PA":
    return chess.PAWN
  elif piece == "BI":
    return chess.BISHOP
  elif piece == "RO":
    return chess.ROOK
  elif piece == "KI":
    return chess.KING
  elif piece == "KN":
    return chess.KNIGHT
    
def arrayToChessPiece(p, pos, newBoard):
  team = p[:1]
  piece = p[1:]
  newPiece = chess.Piece(convertPiece(piece), convertTeam(team))
  newBoard.set_piece_at((7 - pos[0]) * 8 + pos[1], newPiece)


def chessBoardToPyChess(oldBoard):
  newBoard = chess.Board(None)
  for i in range(0, len(oldBoard)):
    for j in range(0, len(oldBoard)):
      arrayToChessPiece(oldBoard[i][j], (i, j), newBoard)
  return newBoard