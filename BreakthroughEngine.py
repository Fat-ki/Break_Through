class GameState():
    def __init__(self):
        self.board = [
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"]
        ]
        self.whiteToMove = True
        self.moveLog = []
    # 勝利的方法
    def gg(self):
        white_left = 0
        black_left = 0
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and r == 0) or (turn == 'b' and r == 7):
                    return True
                if turn == 'w':
                    white_left += 1
                elif turn == 'b':
                    black_left += 1
        if black_left == 0 or white_left == 0:
            return True
        return False

    # 移動棋子
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    # 回到上一動
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    def getValidMove(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    self.getPawnMoves(r, c, moves)
        return moves


    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if r-1 >= 0:
                if self.board[r-1][c] == '--':
                    moves.append(Move((r, c), (r-1, c), self.board))
                if (c+1) < 8:
                    if self.board[r-1][c+1][0] != 'w':
                        moves.append(Move((r, c), (r-1, c+1), self.board))
                if (c-1) >= 0:
                    if self.board[r-1][c-1][0] != 'w':
                        moves.append(Move((r, c), (r-1, c-1), self.board))
        else:
            if r+1 < 8:
                if self.board[r+1][c] == '--':
                    moves.append(Move((r, c), (r+1, c), self.board))
                if (c+1) < 8:
                    if self.board[r+1][c+1][0] != 'b':
                        moves.append(Move((r, c), (r+1, c+1), self.board))
                if (c-1) >= 0:
                    if self.board[r+1][c-1][0] != 'b':
                        moves.append(Move((r, c), (r+1, c-1), self.board))




class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        #print(self.moveID)

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
