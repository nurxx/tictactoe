from math import inf as infinity

X = 'x'
O = 'o'
EMPTY = '_'

class Board:
    def __init__(self, board:list):
        self.board = board
        self.size = len(self.board)
        
    def visualize(self):
        print()
        print('-'*20)
        for index, value in enumerate(self.board):
            print(f'{index+1}', self.board[index])
        print('    1    2    3')
        print('-'*20)
    
    def can_move(self, row:int, column:int):
        return row in range(self.size) and column in range(self.size) and self.board[row][column] == EMPTY
        
    def move(self, row:int, column:int, player:str):
        self.board[row][column] = player
        
    def check_winner(self, player:str):
        winning_state = [player, player, player]
        left_diagonal = [self.board[i][i] for i in range(self.size)]
        right_diagonal = [self.board[self.size - i - 1][i] for i in range(self.size)]
        vertical_states = [[self.board[i][j] for i in range(self.size)] for j in range(self.size)]

        return winning_state in self.board or winning_state in vertical_states or winning_state == left_diagonal or winning_state == right_diagonal
               
    def evaluate(self):
        global winner
        
        if self.check_winner(X):
            winner = X
            return -10
        elif self.check_winner(O):
            winner = O
            return 10
        elif EMPTY not in self.board[0] and EMPTY not in self.board[1] and EMPTY not in self.board[2]:
            winner = 'No one'
            return 0
        else:
            return 1
        
    # Minimax with Alpha Beta Pruning
    def minimax(self, depth:int, alpha:int, beta:int, is_maximizing_player:bool):        
        if self.evaluate() != 1:
            return self.evaluate()
        
        if is_maximizing_player:
            max_eval = -infinity
            for row in range(self.size):
                for col in range(self.size):
                    if self.board[row][col] == EMPTY:
                        self.move(row, col, O)
                        max_eval = max(max_eval, self.minimax(depth + 1, alpha, beta, False))
                        alpha = max(alpha, max_eval)
                        self.board[row][col] = EMPTY
                        if alpha >= beta:
                            break
            return max_eval
        else:
            min_eval = +infinity
            for row in range(self.size):
                for col in range(self.size):
                    if self.board[row][col] == EMPTY:
                        self.move(row, col, X)
                        min_eval = min(min_eval, self.minimax(depth + 1, alpha, beta, True))
                        beta = min(beta, min_eval)
                        self.board[row][col] = EMPTY
                        if alpha >= beta:
                            break
            return min_eval
        
    def ai_play(self):
        best_value = -infinity
        best_row = best_col = -1
        
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == EMPTY:
                    self.move(row, col, O)
                    
                    value = self.minimax(0, -infinity, +infinity, False)

                    self.board[row][col] = EMPTY
                    if value > best_value:
                        best_row = row
                        best_col = col
                        best_value = value
        if self.can_move(best_row, best_col):
            self.move(best_row, best_col, O)
       
        
        
if __name__ == '__main__':
    initial_state=[[EMPTY,EMPTY,EMPTY],[EMPTY,EMPTY,EMPTY],[EMPTY,EMPTY,EMPTY]]

    board = Board(initial_state)
    
    human = 'x'
    ai = 'o'
    
    human_turn = False
    ai_turn = False
    
    first_player = input('Would you like to start first? (y/n): ')
    if first_player == 'n':
        ai_turn = True
        board.visualize()
    else:
        human_turn = True
    
    while (board.evaluate() == 1):
        if human_turn:
            board.visualize()
            x=int(input("Position row: "))
            y=int(input("Position column: "))
            if board.can_move(x-1, y-1):
                board.move(x-1, y-1, human)
            ai_turn = True
        if ai_turn:
            board.ai_play()
            print("Computer played")
            human_turn = True
            
    
    board.visualize()
    if winner == human:
        winner = "Human"
    
    if winner == ai:
        winner = "Computer"
    
    print(f"*** {winner} wins ***")