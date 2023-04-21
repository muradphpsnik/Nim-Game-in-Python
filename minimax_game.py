import time
import tkinter as tk
import time

class NimGame:
    def __init__(self, n):
        self.n = n

    def startState(self):
        return self.n

    def isEmpty(self, state):
        return state == 0

    def utility(self, state, player):
        if state == 0:
            return float('-inf') if player == 1 else float('+inf')

    def actions(self, state):
        return [i for i in range(1, min(state+1, 4))] # limit actions to 1-3

    def successor(self, state, withdrawn):
        return state - withdrawn

def max_value(game, state, alpha, beta):
    if game.isEmpty(state):
        return (game.utility(state, 1), None)
    v = float('-inf')
    for a in game.actions(state):
        v = max(v, min_value(game, game.successor(state, a), alpha, beta)[0])
        if v >= beta:
            return (v, a)
        alpha = max(alpha, v)
    return (v, a)

def min_value(game, state, alpha, beta):
    if game.isEmpty(state):
        return (game.utility(state, -1), None)
    v = float('+inf')
    for a in game.actions(state):
        v = min(v, max_value(game, game.successor(state, a), alpha, beta)[0])
        if v <= alpha:
            return (v, a)
        beta = min(beta, v)
    return (v, a)

def minmax(game, state, player):
    alpha = float('-inf')
    beta = float('+inf')
    if player == 1:
        return max_value(game, state, alpha, beta)
    else:
        return min_value(game, state, alpha, beta)

cache = {}
class NimGameGUI:
    def __init__(self, n):
        self.game = NimGame(n)
        self.state = self.game.startState()
        self.player = 1

        # create main window and title
        self.window = tk.Tk()
        self.window.title("Nim Game")

        # create label for game start
        self.start_label = tk.Label(self.window, text="Who should start the game?")
        self.start_label.pack()

        # create button for player start
        self.player_start_button = tk.Button(self.window, text="Player", command=self.start_game_player)
        self.player_start_button.pack()

        # create button for computer start
        self.computer_start_button = tk.Button(self.window, text="Computer", command=self.start_game_computer)
        self.computer_start_button.pack()

        # create label for current state
        self.state_label = tk.Label(self.window, text="There are " + str(self.state) + " coins in the bag currently")
        self.state_label.pack()

        # create canvas to draw game board
        self.canvas = tk.Canvas(self.window, width=300, height=200)
        self.canvas.pack()

        # draw initial game board
        self.draw_board()

        # create label for player turn
        self.turn_label = tk.Label(self.window, text="")
        self.turn_label.pack()

        # create entry for player move
        self.move_entry = tk.Entry(self.window)
        self.move_entry.pack()

        # create button to submit player move
        self.move_button = tk.Button(self.window, text="Submit move", command=self.player_move)
        self.move_button.pack()

        # create restart button
        self.restart_button = tk.Button(self.window, text="Restart", command=self.restart_game)
        self.restart_button.pack()

        # start GUI main loop
        self.window.mainloop()

    def start_game_player(self):
        self.player = 1
        self.start_label.destroy()
        self.player_start_button.destroy()
        self.computer_start_button.destroy()
        self.turn_label.config(text="Your turn")

    def start_game_computer(self):
        self.player = -1
        self.start_label.destroy()
        self.player_start_button.destroy()
        self.computer_start_button.destroy()
        self.turn_label.config(text="Computer's turn")
        val, act = minmax(self.game, self.state, self.player)
        self.state -= act
        self.update_state_label()
        self.draw_board()
    def restart_game(self):
        self.state = self.game.startState()
        self.player = 1
        self.update_state_label()
        self.update_turn_label()
        self.draw_board()
    def draw_board(self):
        self.canvas.delete("all")
        x = 20
        y = 100
        for i in range(self.state):
            self.canvas.create_oval(x, y, x+20, y+20, fill="yellow")
            x += 30
            if x > 280:
                x = 20
                y -= 30

    def update_state_label(self):
        self.state_label.config(text="There are " + str(self.state) + " coins in the bag currently")

    def update_turn_label(self):
        if self.player == 1:
            self.turn_label.config(text="Your turn")
        else:
            self.turn_label.config(text="Computer's turn")

    def player_move(self):
        withdrawn = int(self.move_entry.get())
        self.move_entry.delete(0, tk.END)
        if withdrawn in [1, 2, 3] and self.state - withdrawn >= 0:
            self.state -= withdrawn
            self.update_state_label()
            if self.state == 0:
                self.turn_label.config(text="Congratulations! You won!")
                return
            self.player = -1
            self.update_turn_label()
            val, act = minmax(self.game, self.state, self.player)
            self.state -= act
            self.update_state_label()
            time.sleep(1)
            if self.state == 0:
                self.turn_label.config(text="Sorry you lost!")
                return
            self.player = 1
            self.update_turn_label()
        else:
            self.turn_label.config(text="Invalid move. Please try again.")

        self.draw_board()
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Nim Game")
    n = 25
    gui = NimGameGUI(n)
    root.mainloop()