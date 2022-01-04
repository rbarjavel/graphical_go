from PyQt5.QtWidgets import QMainWindow, QApplication, QToolBar, QLabel, QAction
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QRectF, QPoint

import socket
import ast
import sys


class Board():
    boardHeight = 7
    boardWidth = 7

    def __init__(self):
        self.boardHeight = 7
        self.boardWidth = 7


class Piece():
    Black = 0
    White = 1
    NoPiece = 2


class Go_Game(QMainWindow):
    boardHeight = 7
    boardWidth = 7
    boardArray = [
        [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece],
        [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece],
        [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece],
        [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece],
        [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece],
        [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece],
        [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece]
    ]
    saveBoard = [
        [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece],
        [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece],
        [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece],
        [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece],
        [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece],
        [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece],
        [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece]
    ]

    def __init__(self):
        super().__init__()
        self.turn = Piece.Black
        self.Board = Board()
        self.Piece = Piece()
        self.setWindowTitle('Go')
        self.setGeometry(300, 300, 900, 900)

        self.toolBar = QToolBar("Game", self)
        self.addToolBar(Qt.RightToolBarArea, self.toolBar)

        self.WhiteScore = 0
        self.BlackScore = 0

        self.WhiteCaptured = 0
        self.BlackCaptured = 0

        self.undoStatus = 0

        self.WhiteScoreLabel = QLabel("White Score: " + str(self.WhiteScore))
        self.BlackScoreLabel = QLabel("Black Score: " + str(self.BlackScore))

        self.WhiteCapturedLabel = QLabel("White Captured: " + str(self.WhiteCaptured))
        self.BlackCapturedLabel = QLabel("Black Captured: " + str(self.BlackCaptured))

        self.gameOverLabel = QLabel("Game")

        self.toolBar.addWidget(self.WhiteScoreLabel)
        self.toolBar.addWidget(self.BlackScoreLabel)
        self.toolBar.addWidget(self.WhiteCapturedLabel)
        self.toolBar.addWidget(self.BlackCapturedLabel)
        self.toolBar.addWidget(self.gameOverLabel)

        self.resetAction = QAction("RESET", self)
        self.resetAction.triggered.connect(self.reset)
        self.toolBar.addAction(self.resetAction)

        self.undoAction = QAction("UNDO", self)
        self.undoAction.triggered.connect(self.undo)
        self.toolBar.addAction(self.undoAction)

        self.passAction = QAction("PASS", self)
        self.passAction.triggered.connect(self.passTurn)
        self.toolBar.addAction(self.passAction)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(('localhost', 5002))
        self.s.send("connected".encode())

        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.drawPieces(painter)

    def checkBoard(self):
        for y in range(self.boardHeight):
            for x in range(self.boardWidth):
                if self.boardArray[x][y] != Piece.NoPiece:
                    self.checkBlocked(x, y)

    def reset(self):
        self.boardArray = [
            [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece],
            [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece],
            [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece],
            [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece],
            [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece],
            [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece],
            [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece]
        ]
        self.saveBoard = [
            [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece],
            [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece],
            [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece],
            [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece],
            [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece],
            [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece],
            [Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece, Piece.NoPiece]
        ]
        self.WhiteScore = 0
        self.BlackScore = 0
        self.WhiteCaptured = 0
        self.BlackCaptured = 0
        self.updateToolBar()
        self.update()

    def undo(self):
        for y in range(self.boardHeight):
            for x in range(self.boardWidth):
                temp = self.boardArray[y][x]
                self.boardArray[y][x] = self.saveBoard[y][x]
                self.saveBoard[y][x] = temp

        if self.undoStatus == 0:
            self.undoAction.setText("REDO")
            self.undoStatus = 1
        else:
            self.undoAction.setText("UNDO")
            self.undoStatus = 0
        self.updateToolBar()
        self.update()

    def passTurn(self):
        if self.turn == Piece.Black:
            self.turn = Piece.White
        else:
            self.turn = Piece.Black
        self.updateToolBar()
        self.update()

    def checkBlocked(self, row, col):
        try:
            if self.boardArray[col][row] == Piece.Black and self.boardArray[col][row+1] == Piece.White and self.boardArray[col][row-1] == Piece.White and self.boardArray[col+1][row] == Piece.White and self.boardArray[col-1][row] == Piece.White:
                self.boardArray[col][row] = Piece.NoPiece
                self.BlackCaptured += 1
            if self.boardArray[col][row] == Piece.White and self.boardArray[col][row+1] == Piece.Black and self.boardArray[col][row-1] == Piece.Black and self.boardArray[col+1][row] == Piece.Black and self.boardArray[col-1][row] == Piece.Black:
                self.boardArray[col][row] = Piece.NoPiece
                self.WhiteCaptured += 1
        except IndexError:
            pass

    def calculateScore(self):
        black = 0
        white = 0
        for y in range(self.boardHeight):
            for x in range(self.boardWidth):
                if self.boardArray[x][y] == Piece.Black:
                    black += 1
                elif self.boardArray[x][y] == Piece.White:
                    white += 1
        self.WhiteScore = white
        self.BlackScore = black

    def updateToolBar(self):
        self.calculateScore()
        self.WhiteScoreLabel.setText("White Score: " + str(self.WhiteScore))
        self.BlackScoreLabel.setText("Black Score: " + str(self.BlackScore))
        self.WhiteCapturedLabel.setText("White Captured: " + str(self.WhiteCaptured))
        self.BlackCapturedLabel.setText("Black Captured: " + str(self.BlackCaptured))

    def checkWin(self):
        for y in range(self.boardHeight):
            for x in range(self.boardWidth):
                if self.boardArray[y][x] == Piece.NoPiece:
                    return False
        return True

    def gameOver(self):
        print("over")
        if self.BlackScore > self.WhiteScore:
            self.gameOverLabel.setText("Black Wins!")
        elif self.BlackScore < self.WhiteScore:
            self.gameOverLabel.setText("White Wins!")
        else:
            self.gameOverLabel.setText("Tie!")
        self.update()

    def mousePressEvent(self, QMouseEvent):
        point = QMouseEvent.pos()
        tileSize = {"x": self.size().width() / (self.boardWidth+1), "y": self.size().height() / (self.boardHeight+1)}
        col = int(point.x() / tileSize["x"])
        row = int(point.y() / tileSize["y"])

        self.s.send(f"place|{col}|{row}".encode())
        # receive data from socket
        data = self.s.recv(1024).decode()
        print(data + "\n")
        board = ast.literal_eval(data)

        for y in range(self.boardHeight):
            for x in range(self.boardWidth):
                self.boardArray[y][x] = board[y][x]

        data = ""
        # for y in range(self.boardHeight):
        #     for x in range(self.boardWidth):
        #         self.saveBoard[y][x] = self.boardArray[y][x]

        # if col > self.boardWidth:
        #     col = self.boardWidth
        # if row > self.boardHeight:
        #     row = self.boardHeight
        # if self.boardArray[col][row] == Piece.NoPiece:
        #     if self.turn == Piece.Black:
        #         self.boardArray[col][row] = self.turn
        #     elif self.turn == Piece.White:
        #         self.boardArray[col][row] = self.turn
        #     self.checkBoard()
        #     if self.turn == Piece.Black:
        #         self.turn = Piece.White
        #     elif self.turn == Piece.White:
        #         self.turn = Piece.Black
        #     if self.checkWin():
        #         self.gameOver()
        #     self.updateToolBar()

        self.update()

    def drawBoardSquares(self, painter):
        """
        Draw all the square on the board
        :param QPainter painter: The painter used for this frame
        """
        tileSize = {"x":self.size().width() / (self.boardWidth+1),"y":self.size().height() / (self.boardHeight+1)}
        painter.setPen(QPen(QBrush(Qt.black), 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                if row in range(1, Board.boardHeight) and col in range(1, Board.boardWidth):
                    painter.setPen(QPen(QBrush(Qt.black), 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    painter.drawRect(QRectF(
                        tileSize["x"]*col,
                        tileSize["y"]*row,
                        tileSize["x"],
                        tileSize["y"])
                    )
                if row == (self.boardHeight-1) / 2 and col == (self.boardWidth-1) / 2:
                    painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
                    painter.setPen(QPen(QBrush(Qt.black), 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                    center = QPoint(
                        tileSize["x"]*col + tileSize["x"],
                        tileSize["y"]*row + tileSize["y"]
                    )
                    painter.drawEllipse(center, tileSize["x"]*0.05, tileSize["y"]*0.05)
                    painter.setBrush(QBrush(Qt.transparent, Qt.SolidPattern))

    def drawPieces(self, painter: QPainter):
        """
        Draw the pieces on the board
        :param QPainter painter: The painter used for this frame
        """
        tileSize = {"x": self.size().width() / (self.boardWidth+1), "y": self.size().height() / (self.boardHeight+1)}
        radiusX = tileSize["x"] / 2.0
        radiusY = tileSize["y"] / 2.0
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                if self.boardArray[col][row] == Piece.Black:
                    painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
                    painter.setPen(QPen(QBrush(Qt.white), 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                if self.boardArray[col][row] == Piece.White:
                    painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))
                    painter.setPen(QPen(QBrush(Qt.black), 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                if self.boardArray[col][row] != Piece.NoPiece:
                    center = QPoint(
                        tileSize["x"]*col + radiusX + tileSize["x"]/2.0,
                        tileSize["y"]*row + radiusY + tileSize["y"]/2.0
                    )
                    painter.drawEllipse(center, radiusX*0.8, radiusY*0.8)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Go_Game()
    sys.exit(app.exec_())
