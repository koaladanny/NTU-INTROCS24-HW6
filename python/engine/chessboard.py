"""
    Reference: https://github.com/NakerTheFirst/Four-in-a-row/
    You should not modify this file. 
"""
import tkinter as tk
from engine.board import Board
import time
from copy import deepcopy

"""
    You should not modify this file. 
"""
class Chessboard():
    """
    GUI for a four-in-a-row game.
    """
    def __init__(self, config, player1, player2=None, human_play=False, human_symbol=None):
        """
        Initializes the game board based on the configuration provided.

        Args:
            config (dict): A dictionary containing the number of columns, rows, and winning condition.
            player1 (BasePlayer): The first player instance.
            player2 (BasePlayer): The first player instance, if `human_play`=True, you can neglect this argument.
            human_play (Bool): If you want to be play the game by yourself.
        """
        self.__board = Board(config)
        self.__window = tk.Tk()
        self.__window.resizable(False, False)
        self.__bottom_frame = tk.Frame(self.__window, width=640, height=115 + (20 if human_play else 0), bg="#4C4246")
        self.__columns = config['num_cols']
        self.__rows = config['num_rows']
        self._involve_human = human_play
        window_w, window_h = self.__get_chessboard_size(self.__columns, self.__rows, human_play)
        self.__window_w = window_w
        self.__window_h = window_h
        self.__orb_columns = []
        self.__orbs = []
        self.__text = tk.StringVar()
        self.__text.set(f"Start!")
        self.__textbox_frame = None
        self.__text_info = None
        self.current_player_id = 0
        self.player1 = player1
        self.players = [self.player1, player2]
        self.human_symbol = human_symbol
        self.__window.bind('<Return>', self.__on_enter_key)

    def __on_enter_key(self, event):
        self.__human_move_on_input()

    def start(self):
        self.__init_scene()

        # Setup bottom frame
        self.__bottom_frame.pack(side="bottom", fill="x")
        self.__draw_textbox()

        # Draw orb columns
        orb_frame = self.__draw_orb_frame()
        self.__draw_orbs_columns(orb_frame)

        if not self._involve_human:
            # If agent vs agent, activate each agent every 1 sec
            self.__window.after(1000, self.__agents_play)
        self.__window.mainloop()

    def __agents_play(self):
        # Agents make move
        agent_move = self.players[self.current_player_id].get_move(deepcopy(self.__board.board))
        agent_res = self.__board.update(agent_move, self.players[self.current_player_id].symbol)
        self.__update_textbox_move_text(agent_res, f"Player {self.current_player_id+1}")
        # If Agent make an invalid move, it loses
        if not agent_res:
            self.__update_textbox_custom_text(f"Invalid move from Player {self.current_player_id+1}! Player {(self.current_player_id + 1) % 2 + 1} wins!")
            self.__window.update()
            time.sleep(5)
            self.__window.destroy()
            return
        arow, acol = agent_res
        self.__make_move(acol, arow, self.current_player_id)
        # Check agent win or tied
        if self.__board.is_winner(self.players[self.current_player_id].symbol):
            self.__update_textbox_custom_text(f"Player {self.current_player_id+1} wins!")
            self.__window.update()
            time.sleep(5)
            self.__window.destroy()
        if self.__board.is_full():
            print('FULL')
            self.__update_textbox_custom_text("Game Tied!")
            self.__window.update()
            time.sleep(5)
            self.__window.destroy()
        self.__window.after(1000, self.__agents_play)
        self.current_player_id = (self.current_player_id + 1) % 2

    def __init_scene(self):
        self.__window.title("Four In A Row")
        self.__window.geometry(f"{self.__window_w}x{self.__window_h}")
        self.__window.configure(bg="#2E282A")

    def __draw_textbox(self):
        self.__textbox_frame = tk.Frame(self.__bottom_frame, width=310, height=43, bg="#237373")
        self.__textbox_frame.pack(pady=20)
        self.__textbox_frame.grid_propagate(False)

        self.__text_info = tk.Label(self.__textbox_frame, textvariable=self.__text,
                                    font=("Ubuntu", -12), bg="#237373", fg="#FFF")
        self.__text_info.grid(sticky="nsew", padx=10, pady=10)
        self.__textbox_frame.columnconfigure(0, weight=1)
        self.__textbox_frame.rowconfigure(0, weight=1)

        if self._involve_human:
            self.__input_frame = tk.Frame(self.__bottom_frame, width=300)
            self.__input = tk.Entry(self.__input_frame)
            self.__input.focus_set()
            self.__input.pack(side='left', padx=[20,0])
            self.__submit = tk.Button(self.__input_frame, text="Go", command=self.__human_move_on_input)
            self.__submit.pack(side="right", pady=10, padx=[0, 20])
            self.__input_frame.pack(pady=[0, 20])

    def __draw_orb_frame(self):
        orb_frame = tk.Frame(self.__window, width=10, height=(12 * (self.__rows-1) + 40 * self.__rows), bg="#2E282A")
        orb_frame.pack(padx=20, pady=20, fill="both")
        return orb_frame

    def __draw_orbs_columns(self, orb_frame):
        for i in range(self.__columns):
            column = tk.Canvas(orb_frame, width=40, height=(12 * (self.__rows-1) + 40 * self.__rows), bg="#2E282A", bd=0, highlightthickness=0)
            column.place(x=0 + 50*i + 10*i)
            # column.bind('<Button-1>', self.__make_move(i))
            self.__orb_columns.append(column)
            self.__orbs.append(self.__create_orb_column(column, self.__rows))

    @staticmethod
    def __create_orb_column(column, height):
        orb_column = []
        for j in range(height):
            orb = column.create_oval(0, j * 40 + j * 12, 40, 40 + j * 40 + j * 12, fill="#A09297", outline="")
            orb_column.append(orb)
        return orb_column

    def __change_orb_colour(self, column, row, colour):
        # Revert the row index to put it in thr correct position
        self.__orb_columns[column].itemconfig(self.__orbs[column][row], fill=colour)

    def __make_move(self, column, row, index):
        color = "#CD5334" if index else "#237373"
        self.__change_orb_colour(column, row, color)
        self.__window.update()

    def __human_move_on_input(self):
        # Human makes move
        human_move = int(self.__input.get())
        res = self.__board.update(human_move, self.human_symbol)
        while not res:
            # Get input column until get a valid input
            self.__update_textbox_custom_text("Invalid input!")
            self.__input.delete(0, tk.END)
            human_move = int(self.__input.get())
            res = self.__board.update(human_move, self.human_symbol)
        self.__update_textbox_move_text(res, "Human")
        row, col = res
        self.__change_orb_colour(col, row, "#237373")
        self.__input.delete(0, tk.END)
        self.__window.update()
        # Check human win
        if self.__board.is_winner(self.human_symbol):
            self.__update_textbox_custom_text("Human Wins!")
            self.__window.update()
            time.sleep(5)
            self.__window.destroy()
            return
        if self.__board.is_full():
            self.__update_textbox_custom_text("Game Tied!")
            self.__window.update()
            time.sleep(5)
            self.__window.destroy()
            return
        # Agent makes move
        agent_move = self.player1.get_move(deepcopy(self.__board.board))
        agent_res = self.__board.update(agent_move, self.player1.symbol)
        self.__update_textbox_move_text(agent_res, "Agent")
        arow, acol = agent_res
        self.__change_orb_colour(acol, arow, "#CD5334")
        self.__window.update()
        # Check agent win
        if self.__board.is_winner(self.player1.symbol):
            self.__update_textbox_custom_text("Agent Wins!")
            self.__window.update()
            time.sleep(5)
            self.__window.destroy()
            return
        if self.__board.is_full():
            print('FULL')
            self.__update_textbox_custom_text("Game Tied!")
            self.__window.update()
            time.sleep(5)
            self.__window.destroy()
            return

    def __update_textbox_move_text(self, move, player_name):
        if not move:
            self.__text.set(f"{player_name} make a invalid move 🫠")
        else:
            self.__text.set(f"{player_name} make a move on column {move[1]}")
    def __update_textbox_custom_text(self, text):
        self.__text.set(text)

    def __get_chessboard_size(self, width, height, human_play):
        window_width = 40 + 60 * width - 12
        window_height = (12 * (height - 1) + 41 * height) + 115 + 40 + (35 if human_play else 0)
        return window_width, window_height
        
