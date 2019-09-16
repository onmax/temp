import math
import sys
import time
import platform

import curses

from colorama import Fore, Back, Style


class UI:
    board_str = ""
    cursor_pos = (0, 0)

    def __init__(self):
        self.walls = {
            "v": "\u2502",  # │
            "h": "\u2500",  # ─
            "bl": "\u2514",  # └
            "br": "\u2518",  # ┘
            "tr": "\u2510",  # ┐
            "tl": "\u250c",   # ┌
            "t0": "\u252c",   # ┬
            "t90": "\u2524",  # ┤
            "t180": "\u2534",  # ┴
            "t240": "\u251c",  # ├,
            "cross": "\u253c"  # ┼
        }

        self.keys = []
        if platform.system() == "Windows":
            self.keys = {
                "up": 119,
                "down": 115,
                "left": 97,
                "right": 100,
                "space": 32
            }
        elif platform.system() == "Linux":
            self.keys = {
                "up": 65,
                "down": 66,
                "left": 68,
                "right": 67,
                "space": 32
            }

        self.win = curses.initscr()

    def print_bar(self, ncolumns, horizontal_wall, left_wall, middle_wall, right_wall):
        str_bar = left_wall

        horizontal_wall *= 3
        str_bar += f"{horizontal_wall}{middle_wall}" * (ncolumns - 1)
        str_bar += f"{horizontal_wall}"

        str_bar += right_wall

        self.board_str += str_bar + "\n"

    def print_row(self, row, i):

        vertical_wall = self.walls["v"]
        str_row = vertical_wall

        for j, c in enumerate(row):
            c = str(c)
            char_to_print = " " if c == "-" else c

            if (i, j) == self.cursor_pos:
                if char_to_print == " ":
                    str_row += f"█-█{vertical_wall}"
                else:
                    str_row += f"█{char_to_print}█{vertical_wall}"

            else:
                str_row += f" {char_to_print} {vertical_wall}"

        self.board_str += str_row + "\n"

    def listener(self):
        while True:
            ch = self.win.getch()

            if ch in self.keys.values():
                break
            time.sleep(0.05)
        dir = None
        if ch == self.keys["up"]:
            dir = "up"
        elif ch == self.keys["down"]:
            dir = "down"
        elif ch == self.keys["left"]:
            dir = "left"
        elif ch == self.keys["right"]:
            dir = "right"
        elif ch == self.keys["space"]:
            dir = "space"

        return dir

    def set_up_board(self, board):
        # Get the length of the first row.
        #
        #
        #  TODO: Check that all rows have the same length
        ncolumns = len(board[0])

        # Set the top bar
        self.print_bar(
            ncolumns, self.walls["h"], self.walls["tl"], self.walls["t0"], self.walls["tr"])

        for i, row in enumerate(board):
            self.print_row(row, i)
            if i != len(board) - 1:
                self.print_bar(
                    ncolumns, self.walls["h"], self.walls["t240"], self.walls["cross"], self.walls["t90"])
            else:
                self.print_bar(
                    ncolumns, self.walls["h"], self.walls["bl"], self.walls["t180"], self.walls["br"])

        self.win.scrollok(1)
        self.win.addstr(self.board_str)

        # self.listener()
