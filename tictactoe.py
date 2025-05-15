import tkinter as tk
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Tic Tac Toe")
        self.score = {'Player': 0, 'Computer': 0}
        self.theme = 'light'
        self.root.configure(bg="white")
        self.show_menu()

    def show_menu(self):
        self.clear_window()
        self.menu_frame = tk.Frame(self.root, bg=self.bg_color())
        self.menu_frame.pack(pady=100)

        tk.Label(self.menu_frame, text="Select Difficulty", font=("Helvetica", 20), bg=self.bg_color(), fg=self.fg_color()).pack(pady=10)

        self.difficulty = tk.StringVar(value="Easy")
        for level in ["Easy", "Medium", "Hard", "Impossible"]:
            tk.Radiobutton(self.menu_frame, text=level, variable=self.difficulty, value=level, font=("Helvetica", 16),
                           bg=self.bg_color(), fg=self.fg_color(), selectcolor=self.bg_color()).pack(anchor=tk.W, padx=20)

        tk.Button(self.menu_frame, text="Start Game", font=("Helvetica", 16), command=self.start_game).pack(pady=10)
        tk.Button(self.menu_frame, text="Toggle Light/Dark Mode", font=("Helvetica", 12), command=self.toggle_theme).pack(pady=5)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_game(self):
        self.clear_window()
        self.status = tk.Label(self.root, text="Your turn", font=("Helvetica", 14), bg=self.bg_color(), fg=self.fg_color())
        self.status.pack()
        self.score_label = tk.Label(self.root, text=self.get_score_text(), font=("Helvetica", 12), bg=self.bg_color(), fg=self.fg_color())
        self.score_label.pack()
        self.board_frame = tk.Frame(self.root, bg=self.bg_color())
        self.board_frame.pack()
        self.reset_board()

    def reset_board(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.board_frame, text="", font=("Helvetica", 24), width=5, height=2,
                                command=lambda x=i, y=j: self.user_move(x, y),
                                bg=self.bg_color(), fg=self.fg_color(), activebackground=self.bg_color())
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def user_move(self, x, y):
        if self.board[x][y] == "" and not self.check_winner():
            self.board[x][y] = "X"
            self.buttons[x][y].config(text="X")
            if self.check_winner():
                self.status.config(text="You win!")
                self.score['Player'] += 1
                self.update_score()
                self.root.after(1500, self.start_game)
                return
            self.status.config(text="Computer's turn")
            self.root.after(500, self.computer_move)

    def computer_move(self):
        if self.check_winner() or self.is_full():
            return
        level = self.difficulty.get().lower()
        if level == "easy":
            move = self.random_move()
        elif level == "medium":
            move = self.medium_ai()
        elif level == "hard":
            move = self.minimax_ai(depth_limit=3)
        else:
            move = self.minimax_ai()
        if move:
            x, y = move
            self.board[x][y] = "O"
            self.buttons[x][y].config(text="O")
            if self.check_winner():
                self.status.config(text="Computer wins!")
                self.score['Computer'] += 1
                self.update_score()
                self.root.after(1500, self.start_game)
            else:
                self.status.config(text="Your turn")

    def update_score(self):
        self.score_label.config(text=self.get_score_text())

    def get_score_text(self):
        return f"Player: {self.score['Player']} | Computer: {self.score['Computer']}"

    def is_full(self):
        return all(cell != "" for row in self.board for cell in row)

    def random_move(self):
        empty = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ""]
        return random.choice(empty) if empty else None

    def medium_ai(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "X"
                    if self.check_winner():
                        self.board[i][j] = ""
                        return (i, j)
                    self.board[i][j] = ""
        return self.random_move()

    def minimax_ai(self, depth_limit=None):
        best_score = float('-inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O"
                    score = self.minimax(False, 0, depth_limit)
                    self.board[i][j] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move

    def minimax(self, is_maximizing, depth, depth_limit):
        winner = self.get_winner()
        if winner == "X":
            return -10 + depth
        elif winner == "O":
            return 10 - depth
        elif self.is_full() or (depth_limit is not None and depth >= depth_limit):
            return 0
        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "O"
                        score = self.minimax(False, depth + 1, depth_limit)
                        self.board[i][j] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "X"
                        score = self.minimax(True, depth + 1, depth_limit)
                        self.board[i][j] = ""
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self):
        return self.get_winner() is not None

    def get_winner(self):
        for line in self.get_lines():
            if line[0] == line[1] == line[2] != "":
                return line[0]
        return None

    def get_lines(self):
        lines = []
        lines.extend(self.board)
        lines.extend([[self.board[r][c] for r in range(3)] for c in range(3)])
        lines.append([self.board[i][i] for i in range(3)])
        lines.append([self.board[i][2 - i] for i in range(3)])
        return lines

    def toggle_theme(self):
        self.theme = 'dark' if self.theme == 'light' else 'light'
        self.root.configure(bg=self.bg_color())
        self.show_menu()

    def bg_color(self):
        return "#222222" if self.theme == 'dark' else "#ffffff"

    def fg_color(self):
        return "#ffffff" if self.theme == 'dark' else "#000000"

root = tk.Tk()
TicTacToe(root)
root.mainloop()
