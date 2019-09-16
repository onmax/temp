from ui import UI


class Cell():
    def __init__(self, team, role, possible_target=False):
        self.team = team
        self.role = role
        self.possible_target = possible_target

    def __str__(self):
        if self.role == "king":
            char = "K"
        elif self.team == "white":
            char = "W"
        elif self.team == "black":
            char = "B"
        elif self.possible_target:
            char = "·"
        else:
            char = " "
        return char

    def is_piece(self):
        return self.role in ["marker", "king"]

    def set_possible_target(self, status):
        self.possible_target = status


class GameEngine():
    board = []
    ui = None
    board_size = {"width": -1, "height": -1}
    possible_targets_coords = []
    piece_to_move = None

    def __init__(self):
        self.set_up_board()
        self.ui = UI()
        self.ui.set_up_board(self.board)
        self.polling()

    def set_up_board(self):
        # Initial set up. It can be changed
        str_board = """ - - - B B B - - -
                        - - - - B - - - -
                        - - - - W - - - -
                        B - - - W - - - B
                        B B W W K W W B B
                        B - - - W - - - B
                        - - - - W - - - -
                        - - - - B - - - -
                        - - - B B B - - -"""

        for str_row in str_board.split("\n"):
            row = []

            for piece in str_row.strip().split(" "):
                team = None
                role = None

                if piece == "B":
                    team = "black"
                elif piece == "W" or piece == "K":
                    team = "white"

                if piece == "K":
                    role = "king"
                elif piece == "B" or piece == "W":
                    role = "marker"

                p = Cell(team, role)
                row.append(p)

            self.board.append(row)

        self.board_size["width"] = max(len(r) for r in self.board)
        self.board_size["height"] = len(self.board)

    def evaluate_possible_target(self, x, y):
        self.possible_targets_coords = []
        # It checks from the piece to the left
        for x2 in range(x-1, -1, -1):
            if not self.board[x2][y].is_piece():
                self.board[x2][y].set_possible_target(True)
                self.possible_targets_coords.append((x2, y))
            else:
                break

        # It checks from the piece to the right
        for x2 in range(x+1, self.board_size["width"]):
            if not self.board[x2][y].is_piece():
                self.board[x2][y].set_possible_target(True)
                self.possible_targets_coords.append((x2, y))
            else:
                break

        # It checks from the piece to the top
        for y2 in range(y-1, -1, -1):
            if not self.board[x][y2].is_piece():
                self.board[x][y2].set_possible_target(True)
                self.possible_targets_coords.append((x, y2))
            else:
                break

        # It checks from the piece to the bottom
        for y2 in range(y+1, self.board_size["height"]):
            if not self.board[x][y2].is_piece():
                self.board[x][y2].set_possible_target(True)
                self.possible_targets_coords.append((x, y2))

            else:
                break

        if len(self.possible_targets_coords) != 0:
            self.piece_to_move = (x, y)

    def move_piece(self, dest_x, dest_y):
        destination = self.board[dest_x][dest_y]
        self.board[dest_x][dest_y] = self.board[self.piece_to_move[0]
                                                ][self.piece_to_move[1]]
        self.board[self.piece_to_move[0]][self.piece_to_move[1]] = destination
        self.clear_targets()

    def clear_targets(self):
        self.piece_to_move = None
        self.possible_targets_coords = []
        for r in self.board:
            for c in r:
                c.set_possible_target(False)

    def polling(self):
        action = None
        while True:
            # Wait to read an arrow key
            action = self.ui.listener()

            x = self.ui.cursor_pos[0]
            y = self.ui.cursor_pos[1]

            if action == "up":
                x -= 1
                self.ui.cursor_pos = (max(0, x), y)

            if action == "down":
                x += 1
                self.ui.cursor_pos = (min(x, self.board_size["height"]-1), y)

            if action == "left":
                y -= 1
                self.ui.cursor_pos = (x, max(0, y))

            if action == "right":
                y += 1
                self.ui.cursor_pos = (x, min(y, self.board_size["width"]-1))

            if action == "space":
                if self.board[x][y].is_piece() and len(self.possible_targets_coords) == 0:
                    self.evaluate_possible_target(x, y)
                elif len(self.possible_targets_coords) > 0 and self.piece_to_move != None:
                    if (x, y) in self.possible_targets_coords:
                        self.move_piece(x, y)
                    elif self.piece_to_move == (x, y):
                        self.clear_targets()

            self.ui.set_up_board(self.board)
