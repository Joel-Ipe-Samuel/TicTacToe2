import tkinter as tk
from tkinter import messagebox

class UltimateTicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("(Tic-Tac-Toe)\u00b2")
        self.root.configure(bg='#f0f0f0')
        
        # Game state
        self.sub_boards = [[[[None for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.main_board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.next_board = None
        self.winner = None
        
        # Colors
        self.colors = {
            'X': '#3b82f6',
            'O': '#ef4444',
            'bg': '#ffffff',
            'highlight': '#fef08a',
            'border': '#d1d5db',
            'won': "#ffffff"
        }
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="(Tic Tac Toe)\u00b2", 
                        font=('Arial', 24, 'bold'), bg='#f0f0f0', fg='#1f2937')
        title.pack(pady=10)
        
        # Status frame
        self.status_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.status_frame.pack(pady=5)
        
        self.player_label = tk.Label(self.status_frame, text=f"Current Player: {self.current_player}",
                                     font=('Arial', 16, 'bold'), bg='#f0f0f0', 
                                     fg=self.colors[self.current_player])
        self.player_label.pack()
        
        self.message_label = tk.Label(self.status_frame, text="Click any cell to start!",
                                     font=('Arial', 12), bg='#f0f0f0', fg='#4b5563')
        self.message_label.pack()
        
        # Game board frame
        self.board_frame = tk.Frame(self.root, bg='#1f2937', padx=5, pady=5)
        self.board_frame.pack(padx=20, pady=10)
        
        # Create 3x3 grid of sub-boards
        self.buttons = [[[[None for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.sub_frames = [[None for _ in range(3)] for _ in range(3)]
        self.won_labels = [[None for _ in range(3)] for _ in range(3)]
        
        for main_row in range(3):
            for main_col in range(3):
                # Frame for each sub-board
                sub_frame = tk.Frame(self.board_frame, bg=self.colors['bg'], 
                                    padx=3, pady=3, relief=tk.RAISED, borderwidth=2)
                sub_frame.grid(row=main_row, column=main_col, padx=3, pady=3)
                self.sub_frames[main_row][main_col] = sub_frame
                
                # Create 3x3 grid of buttons in each sub-board
                for sub_row in range(3):
                    for sub_col in range(3):
                        btn = tk.Button(sub_frame, text='', font=('Arial', 16, 'bold'),
                                       width=3, height=1, bg=self.colors['bg'],
                                       command=lambda mr=main_row, mc=main_col, 
                                       sr=sub_row, sc=sub_col: 
                                       self.handle_click(mr, mc, sr, sc))
                        btn.grid(row=sub_row, column=sub_col, padx=1, pady=1)
                        self.buttons[main_row][main_col][sub_row][sub_col] = btn
                
                # Label to show winner of sub-board (hidden initially)
                won_label = tk.Label(sub_frame, text='', font=('Arial', 48, 'bold'),
                                    bg=self.colors['won'])
                self.won_labels[main_row][main_col] = won_label
        
        # Control buttons
        control_frame = tk.Frame(self.root, bg='#f0f0f0')
        control_frame.pack(pady=10)
        
        new_game_btn = tk.Button(control_frame, text="New Game", font=('Arial', 14, 'bold'),
                                bg='#8b5cf6', fg='white', padx=20, pady=8,
                                command=self.reset_game, cursor='hand2')
        new_game_btn.pack(side=tk.LEFT, padx=5)
        
        rules_btn = tk.Button(control_frame, text="Rules", font=('Arial', 14, 'bold'),
                             bg='#6366f1', fg='white', padx=20, pady=8,
                             command=self.show_rules, cursor='hand2')
        rules_btn.pack(side=tk.LEFT, padx=5)
        
    def handle_click(self, main_row, main_col, sub_row, sub_col):
        if self.winner:
            return
        
        # Check if move is in the required board
        if self.next_board and (main_row, main_col) != self.next_board:
            self.message_label.config(text="Must play in the highlighted board!")
            return
        
        # Check if the sub-board is already won
        if self.main_board[main_row][main_col]:
            self.message_label.config(text="This sub-board is already won!")
            return
        
        # Check if the cell is empty
        if self.sub_boards[main_row][main_col][sub_row][sub_col]:
            self.message_label.config(text="Cell is already occupied!")
            return
        
        # Make the move
        self.sub_boards[main_row][main_col][sub_row][sub_col] = self.current_player
        btn = self.buttons[main_row][main_col][sub_row][sub_col]
        btn.config(text=self.current_player, fg=self.colors[self.current_player], 
                  state='disabled', disabledforeground=self.colors[self.current_player])
        
        # Check if this wins the sub-board
        sub_winner = self.check_win(self.sub_boards[main_row][main_col])
        if sub_winner:
            self.main_board[main_row][main_col] = sub_winner
            self.mark_sub_board_won(main_row, main_col, sub_winner)
            
            # Check if this wins the main board
            main_winner = self.check_win(self.main_board)
            if main_winner:
                self.winner = main_winner
                self.message_label.config(text=f"Player {main_winner} wins the game! (o゜▽゜)o☆",
                                        fg='#059669', font=('Arial', 14, 'bold'))
                messagebox.showinfo("Game Over!", f"Player {main_winner} wins the game!")
                return
        elif self.is_board_full(self.sub_boards[main_row][main_col]):
            self.main_board[main_row][main_col] = 'T'
            self.mark_sub_board_won(main_row, main_col, 'T')
        
        # Determine next board
        if not self.main_board[sub_row][sub_col]:
            self.next_board = (sub_row, sub_col)
            self.message_label.config(text="Next player must play in highlighted board")
        else:
            self.next_board = None
            self.message_label.config(text="Next player can play anywhere!")
        
        # Check for draw
        if self.is_board_full(self.main_board):
            self.winner = 'Draw'
            self.message_label.config(text="Game is a draw!", 
                                    fg='#dc2626', font=('Arial', 14, 'bold'))
            messagebox.showinfo("Game Over", "Game is a draw!")
            return
        
        # Switch player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.player_label.config(text=f"Current Player: {self.current_player}",
                                fg=self.colors[self.current_player])
        
        # Update highlighting
        self.update_highlighting()
    
    def mark_sub_board_won(self, main_row, main_col, winner):
        # Hide all buttons
        for sub_row in range(3):
            for sub_col in range(3):
                self.buttons[main_row][main_col][sub_row][sub_col].grid_remove()
        
        # Show winner label
        if winner == 'T':
            self.won_labels[main_row][main_col].config(text='TIE', fg='#6b7280')
        else:
            self.won_labels[main_row][main_col].config(text=winner, fg=self.colors[winner])
        self.won_labels[main_row][main_col].place(relx=0.5, rely=0.5, anchor='center')
    
    def update_highlighting(self):
        for main_row in range(3):
            for main_col in range(3):
                frame = self.sub_frames[main_row][main_col]
                if self.next_board and (main_row, main_col) == self.next_board:
                    frame.config(bg=self.colors['highlight'], relief=tk.SUNKEN, borderwidth=3)
                else:
                    frame.config(bg=self.colors['bg'], relief=tk.RAISED, borderwidth=2)
    
    def check_win(self, board):
        # Check rows
        for row in board:
            if row[0] and row[0] == row[1] == row[2]:
                return row[0]
        
        # Check columns
        for col in range(3):
            if board[0][col] and board[0][col] == board[1][col] == board[2][col]:
                return board[0][col]
        
        # Check diagonals
        if board[0][0] and board[0][0] == board[1][1] == board[2][2]:
            return board[0][0]
        if board[0][2] and board[0][2] == board[1][1] == board[2][0]:
            return board[0][2]
        
        return None
    
    def is_board_full(self, board): #Check if a board is completely filled
        for row in board:
            if None in row:
                return False
        return True
    
    def reset_game(self): #Reset the game to initial state
        self.sub_boards = [[[[None for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.main_board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.next_board = None
        self.winner = None
        
        # Reset all buttons and labels
        for main_row in range(3):
            for main_col in range(3):
                self.won_labels[main_row][main_col].place_forget()
                for sub_row in range(3):
                    for sub_col in range(3):
                        btn = self.buttons[main_row][main_col][sub_row][sub_col]
                        btn.grid(row=sub_row, column=sub_col, padx=1, pady=1)
                        btn.config(text='', state='normal', bg=self.colors['bg'])
        
        # Reset labels
        self.player_label.config(text=f"Current Player: {self.current_player}",
                                fg=self.colors[self.current_player])
        self.message_label.config(text="Click any cell to start!", 
                                 fg='#4b5563', font=('Arial', 12))
        
        # Reset highlighting
        self.update_highlighting()
    
    def show_rules(self):
        rules = """Ultimate Tic-Tac-Toe Rules:

        1. Click any cell in the highlighted board (or any board 
        if no highlight). 

        2. Win a sub-board by getting 3 in a row (horizontal, 
        vertical, or diagonal).

        3. Your move determines which board your opponent 
        must play in next. 

        4. If sent to an already-won board, you can play 
        anywhere.

        5. Win the game by getting 3 sub-boards in a row on 
        the main board!"""
        
        messagebox.showinfo("How to Play", rules)

if __name__ == "__main__":
    root = tk.Tk()
    game = UltimateTicTacToe(root)
    root.mainloop()