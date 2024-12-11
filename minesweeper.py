import tkinter as tk
import random

class Minesweeper:
    def __init__(self, root, rows=10, cols=10, mines=20):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.buttons = []
        self.mine_positions = set()
        self.colors = {
            1: "blue",
            2: "green",
            3: "red",
            4: "purple",
            5: "maroon",
            6: "turquoise",
            7: "black",
            8: "gray"
        }
        self.create_widgets()

    def create_widgets(self):
        # Create the smiley face button
        self.smiley_button = tk.Button(self.root, text="☺", font=("Arial", 14), command=self.restart_game)
        self.smiley_button.grid(row=0, column=0, columnspan=self.cols, sticky="nsew")

        # Create the game board
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                button = tk.Button(
                    self.root, text="", width=3, height=1, font=("Arial", 14),
                    command=lambda r=r, c=c: self.on_click(r, c)
                )
                button.bind("<Button-3>", lambda e, r=r, c=c: self.on_right_click(r, c))
                button.grid(row=r + 1, column=c)  # Shift down by one row
                row.append(button)
            self.buttons.append(row)

        self.place_mines()

    def place_mines(self):
        self.mine_positions.clear()
        while len(self.mine_positions) < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            self.mine_positions.add((r, c))

    def on_click(self, r, c):
        if (r, c) in self.mine_positions:
            self.reveal_mines()
            self.end_game("Game Over!")
        else:
            self.reveal_cell(r, c)

    def on_right_click(self, r, c):
        button = self.buttons[r][c]
        if button["text"] == "":
            button["text"] = "⚑"  # Flag emoji
        elif button["text"] == "⚑":
            button["text"] = ""

    def reveal_cell(self, r, c):
        if self.buttons[r][c]["state"] == "disabled":
            return

        mines_around = self.count_adjacent_mines(r, c)
        if mines_around > 0:
            self.buttons[r][c]["text"] = str(mines_around)
            self.buttons[r][c]["fg"] = self.colors[mines_around]
        else:
            self.buttons[r][c]["text"] = ""

        self.buttons[r][c]["state"] = "disabled"

        if mines_around == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        self.reveal_cell(nr, nc)

    def count_adjacent_mines(self, r, c):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if (nr, nc) in self.mine_positions:
                    count += 1
        return count

    def reveal_mines(self):
        for r, c in self.mine_positions:
            self.buttons[r][c]["text"] = "*"
            self.buttons[r][c]["fg"] = "black"

    def end_game(self, message):
        for r in range(self.rows):
            for c in range(self.cols):
                self.buttons[r][c]["state"] = "disabled"
        tk.messagebox.showinfo("Minesweeper", message)

    def restart_game(self):
        # Reset the board
        for r in range(self.rows):
            for c in range(self.cols):
                button = self.buttons[r][c]
                button["text"] = ""
                button["state"] = "normal"
                button["fg"] = "black"
        self.place_mines()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper")
    game = Minesweeper(root)
    root.mainloop()
