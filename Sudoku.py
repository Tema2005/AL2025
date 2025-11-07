class SudokuSolver: 
    def solve(self, board): 
        # Validate board structure
        if not self._validate_board_structure(board):
            return False
        
        # Validate initial board state
        if not self._validate_initial_board(board):
            return False
            
        for row in range(9): 
            for col in range(9): 
                if board[row][col] == 0:  # Empty cell
                    for num in range(1, 10): 
                        if self.is_valid(board, row, col, num): 
                            board[row][col] = num
                            if self.solve(board): 
                                return True
                            board[row][col] = 0  # Backtrack
                    return False  # No number worked
        return True  # Board is complete

    def is_valid(self, board, row, col, num): 
        # Check row
        for j in range(9): 
            if board[row][j] == num: 
                return False
        
        # Check column
        for i in range(9): 
            if board[i][col] == num: 
                return False
        
        # Check 3x3 block
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3): 
            for j in range(start_col, start_col + 3): 
                if board[i][j] == num: 
                    return False
        
        return True

    def _validate_board_structure(self, board):
        """Check if board is a 9x9 grid with valid values (0-9)"""
        if not isinstance(board, list) or len(board) != 9:
            return False
        for row in board:
            if not isinstance(row, list) or len(row) != 9:
                return False
            for cell in row:
                if not isinstance(cell, int) or cell < 0 or cell > 9:
                    return False
        return True

    def _validate_initial_board(self, board):
        """Check if initial board configuration is valid"""
        for row in range(9):
            for col in range(9):
                num = board[row][col]
                if num != 0:
                    # Temporarily remove the number to check if the position is valid
                    board[row][col] = 0
                    if not self.is_valid(board, row, col, num):
                        board[row][col] = num  # Restore before returning
                        return False
                    board[row][col] = num  # Restore
        return True


# Example usage
board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0], 
    [6, 0, 0, 1, 9, 5, 0, 0, 0], 
    [0, 9, 8, 0, 0, 0, 0, 6, 0], 
    [8, 0, 0, 0, 6, 0, 0, 0, 3], 
    [4, 0, 0, 8, 0, 3, 0, 0, 1], 
    [7, 0, 0, 0, 2, 0, 0, 0, 6], 
    [0, 6, 0, 0, 0, 0, 2, 8, 0], 
    [0, 0, 0, 4, 1, 9, 0, 0, 5], 
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

solver = SudokuSolver()
if solver.solve(board): 
    for row in board: 
        print(" ".join(map(str, row)))
else: 
    print("No solution exists!")
