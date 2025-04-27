import random
DEPTH = 4
WIN = 10000

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]


def findBestMove(gs,validMove):
    global nextMove, cnt
    nextMove = None
    random.shuffle(validMove)
    cnt = 0
    #findMoveMinMax(gs, validMove, DEPTH, gs.whiteToMove)
    findMoveMinMaxAlphaBeta(gs, validMove, DEPTH, -WIN, WIN, gs.whiteToMove)
    #findMoveNegaMaxAlphaBeta(gs, validMove, DEPTH, -WIN, WIN, 1 if gs.whiteToMove else -1)
    #print(cnt)
    return nextMove


def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove,cnt
    cnt+=1
    if depth == 0:
        return scoreBoard(gs)

    if whiteToMove:
        maxScore = -WIN
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMove()
            score = findMoveMinMax(gs, nextMoves, depth-1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = WIN
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMove()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore


def findMoveMinMaxAlphaBeta(gs, validMoves, depth, alpha, beta, whiteToMove):
    global nextMove, cnt
    #cnt += 1
    if gs.gg():
        if gs.whiteToMove:
            return -WIN
        else:
            return WIN
    if depth == 0:   # 若到最底層或是此盤面已經贏了就回傳分數
        return scoreBoard(gs)

    # 設定白子的分數為正，黑子分數為負
    if whiteToMove:
        maxScore = -WIN  # 尋找最高分數的走法
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMove()
            score = findMoveMinMaxAlphaBeta(gs, nextMoves, depth-1, alpha, beta, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
            alpha = max(maxScore, alpha)
            if beta <= alpha:
                break
        return maxScore
    else:
        minScore = WIN  # 尋找最低分數的走法
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMove()
            score = findMoveMinMaxAlphaBeta(gs, nextMoves, depth - 1, alpha, beta, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
            beta = min(minScore, beta)
            if beta <= alpha:
                break
        return minScore

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove,cnt
    cnt+=1
    if depth == 0 or gs.gg():   # 若到最底層或是此盤面已經贏了就回傳分數
        return scoreBoard(gs) * turnMultiplier

    maxScore = -WIN
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMove()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

def scoreBoard(gs):
    score = 0
    for row in range(8):
        for col in range(8):
            if gs.board[row][col][0] == 'w':
                score += (7-row)
                score += 5
            elif gs.board[row][col][0] == 'b':
                score -= row
                score -= 5
    return score


