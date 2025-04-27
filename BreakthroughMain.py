#主程式
import pygame as p  # 使用pygame套件完成介面設置
import BreakthroughEngine, SmartMoveFinder   # 載入自己寫的套件

# 基本視窗設定
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15
IMAGES = {}



# 主程式
def main():
    # 初始化
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = BreakthroughEngine.GameState()
    validMoves = gs.getValidMove()
    moveMade = False
    loadImages()
    running = True
    sqSelected = ()     # 點選的格子
    playerClicks = []   # keep track of player click
    gameOver = False

    playerOne = True    # 是人還是機器人
    playerTwo = False

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)    # 機器人是黑子還是白子
        # 遊戲是否進行中
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()    # 找出玩家所點選的格子
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col):    # 若重複點選就清空行動
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:  # 若點選兩次為不同地點
                        move = BreakthroughEngine.Move(playerClicks[0], playerClicks[1], gs.board)  # 移動棋子
                        print(move.getChessNotation())
                        if move in validMoves:  # 若移動到的位子是合法的
                            gs.makeMove(move)   # 移動到此格
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                        else:
                            playerClicks = [sqSelected]
            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # 按z可回復上一動
                    if not(playerOne and playerTwo):
                        gs.undoMove()
                        gs.undoMove()
                    else:
                        gs.undoMove()
                    moveMade = True
                    gameOver = False
                if e.key == p.K_r:  # 按r將盤面設回原形
                    gs = BreakthroughEngine.GameState()
                    validMoves = gs.getValidMove()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    gameOver = False

        #AI move
        if not gameOver and not humanTurn:
            AIMove = SmartMoveFinder.findBestMove(gs, validMoves)     # 回傳minmax的結果
            if AIMove is None:
                AIMove = SmartMoveFinder.findRandomMove(validMoves)     # 若沒回傳結果就隨便下一步
            gs.makeMove(AIMove)
            moveMade = True

        if moveMade:
            validMoves = gs.getValidMove()
            moveMade = False

        drawGameState(screen, gs, validMoves, sqSelected)
        if gs.gg():
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black wins!")
            else:
                drawText(screen, "White wins!")

        clock.tick(MAX_FPS)
        p.display.flip()

# 載入棋子的圖片
def loadImages():
    IMAGES['wp'] = p.transform.scale(p.image.load("images/wp.png"), (SQ_SIZE, SQ_SIZE))
    IMAGES['bp'] = p.transform.scale(p.image.load("images/bp.png"), (SQ_SIZE, SQ_SIZE))

# 提示下一步能走的位置
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

# 畫出整盤的情形
def drawGameState(screen, gs, validMoves, sqSelected):
    drawGameBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

# 畫出盤
def drawGameBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

# 畫出棋子
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

"""
def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framePerSquare = 10
    frameCount = (abs(dR) + abs(dC))
    for frame in range(frameCount+1):
        r, c =((move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount))
        drawGameBoard(screen)
        drawPieces(screen, board)

        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)

        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)

        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)
"""
# 寫出最後贏家
def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2,HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)

# 主程式執行
if __name__ == "__main__":
    main()
