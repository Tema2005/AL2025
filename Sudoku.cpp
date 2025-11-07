#include <iostream>
#include <vector>
using namespace std;

bool isValid(vector<vector<int>>& board,  int row,  int col,  int num) {
    // Проверка строки
    for (int j = 0; j < 9; ++j)
        if (board[row][j] == num)
            return false;

    // Проверка столбца
    for (int i = 0; i < 9; ++i)
        if (board[i][col] == num)
            return false;

    // Проверка блока 3x3
    int startRow = 3 * (row / 3);
    int startCol = 3 * (col / 3);
    for (int i = startRow; i < startRow + 3; ++i)
        for (int j = startCol; j < startCol + 3; ++j)
            if (board[i][j] == num)
                return false;

    return true;
}

bool solveSudoku(vector<vector<int>>& board) {
    for (int row = 0; row < 9; ++row) {
        for (int col = 0; col < 9; ++col) {
            if (board[row][col] == 0) {  // Пустая ячейка
                for (int num = 1; num <= 9; ++num) {
                    if (isValid(board,  row,  col,  num)) {
                        board[row][col] = num;
                        if (solveSudoku(board))  // Рекурсия
                            return true;
                        board[row][col] = 0;  // Откат
                    }
                }
                return false;  // Ни одна цифра не подошла
            }
        }
    }
    return true;  // Всё заполнено
}

void printBoard(const vector<vector<int>>& board) {
    for (int i = 0; i < 9; ++i) {
        for (int j = 0; j < 9; ++j)
            cout << board[i][j] << " ";
        cout << endl;
    }
}

int main() {
    vector<vector<int>> board = {
        {5,  3,  0,  0,  7,  0,  0,  0,  0}, 
        {6,  0,  0,  1,  9,  5,  0,  0,  0}, 
        {0,  9,  8,  0,  0,  0,  0,  6,  0}, 
        {8,  0,  0,  0,  6,  0,  0,  0,  3}, 
        {4,  0,  0,  8,  0,  3,  0,  0,  1}, 
        {7,  0,  0,  0,  2,  0,  0,  0,  6}, 
        {0,  6,  0,  0,  0,  0,  2,  8,  0}, 
        {0,  0,  0,  4,  1,  9,  0,  0,  5}, 
        {0,  0,  0,  0,  8,  0,  0,  7,  9}
    };

    if (solveSudoku(board)) {
        cout << "Решение найдено: " << endl;
        printBoard(board);
    } else {
        cout << "Решения нет." << endl;
    }

    return 0;
}
