# pieces with W or B at the beginning of the string determines what team they belong to
# N means none state
import copy

depthness = 2

def aphaBeta(boardState):
  return maxF(0, boardState, -10000000, 10000000)

def maxF(depth, boardState, apha, beta):
  if depth >= depthness:
    return boardState.boardEval()
  max = -100000000000
  for state in getSucceedStates(boardState, "W"):
    val = minF(depth, state, apha, beta)

    if val > beta:
      return val

    if apha < val:
      apha = val

    if max < val:
      max = val

  return max

def minF(depth, boardState, apha, beta):
  if depth >= depthness:
    return boardState.boardEval()

  min = 100000000000
  for state in getSucceedStates(boardState, "B"):
    val = 0
    val = maxF(depth + 1, state, apha, beta)
    if val < apha:
      return val

    if beta > val:
      beta = val

    if min > val:
      min = val

  return min

def getSucceedStates(cB, team):
  teamMove = None
  if team == cB.white:
    teamMove = cB.getWhitePieces()
  else:
    teamMove = cB.getBlackPieces()
  boardStates = []
  for fState in teamMove:
    for tState in cB.legalMoves(cB.getPiece(fState), fState):
      newBoard = chessBoard(board_state = copy.deepcopy(cB.getBoard()))
      newBoard.updateBoard(fState, tState)
      boardStates.append(newBoard)
  return boardStates

def replace(lis, elem1, elem2):
  for i in range(0, len(lis)):
    if elem1 == elem2:
      lis[i] = elem2

#Helps manage the states of the board
#
class ChessBoard():

  def __init__(self, board_state = [["" for i in range(0, 8)] for j in range(0, 8)]):
    self.board_state = board_state
    self.white_pieces = []
    self.black_pieces = []

    self.white = "W"
    self.black = "B"

    self.queen = "QE"
    self.queenVal = 10

    self.pawn = "PA"
    self.pawnVal = 1

    self.knight = "KN"
    self.knightVal = 4

    self.king = "KI"
    self.kingVal = 1000000

    self.bishop = "BI"
    self.bishopVal = 5

    self.rook = "RO"
    self.rookVal = 7

    for i in range(0, 8):
      for j in range(0, 8):
        team = self.getTeam((i, j))
        if team == self.white:
          self.white_pieces.append([i, j])
        elif team == self.black:
          self.black_pieces.append([i, j])

  def boardEval(self):
    whiteScore = 0
    blackScore = 0
    for state in self.white_pieces:
      whiteScore += self.scorePiece(state)

    for state in self.black_pieces:
      blackScore += self.scorePiece(state)

    return whiteScore - blackScore

  def scorePiece(self, state):
    piece = self.getPiece(state)
    if piece == self.queen:
      return self.queenVal
    elif piece == self.bishop:
      return self.bishopVal
    elif piece == self.rook:
      return self.rookVal
    elif piece == self.pawn:
      return self.pawnVal
    elif piece == self.knight:
      return self.knightVal
    elif piece == self.king:
      return self.kingVal
    return 0

  def getBoard(self):
    return self.board_state

  def getWhitePieces(self):
    return self.white_pieces

  def getBlackPieces(self):
    return self.black_pieces

  def legalMoves(self, piece, state):
    moves = []
    team = self.getTeam(state)

    if piece == self.queen:
      moves += self.straightMoves(state)
      moves += self.diagnolMoves(state)
    elif piece == self.bishop:
      moves += self.diagnolMoves(state)
    elif piece == self.rook:
      moves += self.straightMoves(state)
    elif piece == self.pawn:
      moves += self.pawnMoves(state)
    elif piece == self.knight:
      moves += self.knightMoves(state)
    elif piece == self.king:
      moves += self.kingMoves(state)
    return moves

  def pawnMoves(self, state):
    moves = []
    currState = copy.deepcopy(state)

    if self.getTeam(currState) == self.white:
      dir = -1
    else:
      dir = 1

    foward = [currState[0], currState[1] + dir]
    if self.isEmpty(foward):
        moves.append(foward)

    leftCapture = [currState[0] - 1, currState[1] + dir]
    if not self.isEmpty(leftCapture) and not self.isSameTeam(leftCapture, currState):
        moves.append(leftCapture)

    rightCapture = [currState[0] + 1, currState[1] + dir]
    if not self.isEmpty(rightCapture) and not self.isSameTeam(rightCapture, currState):
        moves.append(rightCapture)

    return moves

  def knightMoves(self, state):
    moves = []
    currState = copy.deepcopy(state)

    potential = []
    potential.append([currState[0] + 1, currState[1] + 2])
    potential.append([currState[0] - 1, currState[1] + 2])
    potential.append([currState[0] + 1, currState[1] - 2])
    potential.append([currState[0] - 1, currState[1] - 2])

    for p in potential:
      if self.isLegal(potential, state):
        moves.append(p)
    return moves

  def kingMoves(self, state):
    moves = []
    currState = copy.deepcopy(state)

    potential = []
    potential.append([currState[0] + 1, currState[1] + 1])
    potential.append([currState[0] - 1, currState[1] + 1])
    potential.append([currState[0] + 1, currState[1] - 1])
    potential.append([currState[0] - 1, currState[1] - 1])
    potential.append([currState[0], currState[1] - 1])
    potential.append([currState[0], currState[1] + 1])
    potential.append([currState[0] + 1, currState[1]])
    potential.append([currState[0] - 1, currState[1]])

    for p in potential:
      if self.isLegal(potential, state):
        moves.append(p)
    return moves

  def straightMoves(self, state):
    moves = []
    currState = [state[0] + 1, state[1]]
    while self.isLegal(currState, state):
      moves.append(currState)
      if not self.isEmpty(currState):
        break
      currState = [currState[0] + 1, currState[1]]

    currState = [state[0] - 1, state[1]]
    while self.isLegal(currState, state):
      moves.append(currState)
      if not self.isEmpty(currState):
        break
      currState = [currState[0] - 1, currState[1]]

    currState = [state[0], state[1] + 1]
    while self.isLegal(currState, state):
      moves.append(currState)
      if not self.isEmpty(currState):
        break
      currState = [currState[0], currState[1] + 1]

    currState = [state[0], state[1] - 1]
    while self.isLegal(currState, state):
      moves.append(currState)
      if not self.isEmpty(currState):
        break
      currState = [currState[0], currState[1] - 1]
    return moves

  def diagnolMoves(self, state):
    moves = []
    currState = [state[0] + 1, state[1] + 1]
    while self.isLegal(currState, state):
      moves.append(currState)
      if not self.isEmpty(currState):
        break
      currState = [state[0] + 1, state[1] + 1]

    currState = [state[0] + 1, state[1] - 1]
    while self.isLegal(currState, state):
      moves.append(currState)
      if not self.isEmpty(currState):
        break
      currState = [state[0] + 1, state[1] - 1]

    currState = [state[0] - 1, state[1] + 1]
    while self.isLegal(currState, state):
      moves.append(currState)
      if not self.isEmpty(currState):
        break
      currState = [state[0] - 1, state[1] + 1]

    currState = [state[0] - 1, state[1] - 1]
    while self.isLegal(currState, state):
      moves.append(currState)
      if not self.isEmpty(currState):
        break
      currState = [state[0] - 1, state[1] - 1]
    return moves

  def inBounds(self, state):
    return 0 <= state[0] and state[0] < 8 and 0 <= state[1] and state[1] < 8

  def updateBoard(self, fState, tState):
    i, j = fState
    i2, j2 = tState
    team = self.getTeam(fState)

    #Promotion piece detected
    if self.getPiece(fState) == self.pawn and (j2 == 7 or j2 == 0):
      self.board_state[i][j] = team + self.queen

    #Capture piece
    if not self.isEmpty(tState):
      if team == self.white:
        self.black_pieces.remove(tState)
      else:
        self.white_pieces.remove(tState)

    #Move piece
    if team == self.white:
      replace(self.white_pieces, fState, tState)
    else:
      replace(self.black_pieces, fState, tState)

    self.board_state[i2][j2] = self.board_state[i][j]
    self.board_state[i][j] = ""

  def getTeam(self, state):
    i, j = state
    return self.board_state[i][j][:1]

  def getPiece(self, state):
    i, j = state
    return self.board_state[i][j][1:]

  def isSameTeam(self, currentState, otherState):
    if self.isEmpty(currentState) or self.isEmpty(otherState):
      return False

    return self.getTeam(currentState) == self.getTeam(otherState)

  def isEmpty(self, state):
    i, j = state
    return self.board_state[i][j] == ""

  def isLegal(self, currState, otherState):
    if not self.inBounds(currState):
      return False

    return not self.isSameTeam(currState, otherState)

  def __str__(self):
    boardStr = ""
    for row in self.board_state:
      boardStr += str(row) + "\n"
    return boardStr
