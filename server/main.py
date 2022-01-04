from multiprocessing import Process
import socket
import select


class Piece():
    Black = 0
    White = 1
    NoPiece = 2


class Game:
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
        self.turn = Piece.Black

        self.WhiteScore = 0
        self.BlackScore = 0

        self.WhiteCaptured = 0
        self.BlackCaptured = 0

        self.undoStatus = 0

    def undo(self):
        for y in range(self.boardHeight):
            for x in range(self.boardWidth):
                temp = self.boardArray[y][x]
                self.boardArray[y][x] = self.saveBoard[y][x]
                self.saveBoard[y][x] = temp

    def checkBoard(self):
        for y in range(self.boardHeight):
            for x in range(self.boardWidth):
                if self.boardArray[x][y] != Piece.NoPiece:
                    self.checkBlocked(x, y)

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

    def checkWin(self):
        for y in range(self.boardHeight):
            for x in range(self.boardWidth):
                if self.boardArray[y][x] == Piece.NoPiece:
                    return False
        return True

    def placePiece(self, row, col, players, client):
        for y in range(self.boardHeight):
            for x in range(self.boardWidth):
                self.saveBoard[y][x] = self.boardArray[y][x]

        if self.boardArray[col][row] == Piece.NoPiece:
            if self.turn == Piece.Black and players[Piece.Black] == client:
                self.boardArray[col][row] = Piece.Black
                self.turn = Piece.White
            elif self.turn == Piece.White and players[Piece.White] == client:
                self.boardArray[col][row] = Piece.White
                self.turn = Piece.Black
            self.checkBoard()
            self.calculateScore()
            # if self.checkWin():
            #     return True
            # else:
            #     return False
            return self.boardArray
        else:
            return False


class Server():
    def run(self):
        self.CONNECTION_LIST = []
        self.RECV_BUFFER = 4096
        self.PORT = 5002

        self.game = Game()

        self.Players = [None, None]

        self.Players[Piece.Black] = None
        self.Players[Piece.White] = None

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("0.0.0.0", self.PORT))
        self.server_socket.listen(10)

        self.CONNECTION_LIST.append(self.server_socket)
        while 1:
            read_sockets, write_sockets, error_sockets = select.select(self.CONNECTION_LIST,[],[])
            for i, sock in enumerate(read_sockets):
                if sock == self.server_socket:
                    sockfd, addr = self.server_socket.accept()
                    self.CONNECTION_LIST.append(sockfd)

                else:
                    data = sock.recv(self.RECV_BUFFER).decode("utf-8")
                    if data:
                        self.parse_msg(data, sock.getpeername(), sock)
        self.server_socket.close()

    def parse_msg(self, data, addr, sock):
        command = data.replace('\n', '').split('|')
        if command[0] == 'connected':
            if self.Players[Piece.Black] is None:
                self.Players[Piece.Black] = addr[0]
            else:
                self.Players[Piece.White] = addr[0]
        if command[0] == 'place':
            board = self.game.placePiece(int(command[1]), int(command[2]), self.Players, addr[0])
            print(board)
            self.broadcast_data(sock, str(board).encode())

    def broadcast_data(self, sock, message):
        for socket in self.CONNECTION_LIST:
            if socket != self.server_socket:
                socket.send(message)


if __name__ == "__main__":
    host = 'localhost'
    port = 1234

    s = Server()
    s.run()
