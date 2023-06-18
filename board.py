import pygame
pygame.init()

font = pygame.font.SysFont(None, 60)

class Board:
    def __init__(self, playersigns):
        '''
        playersigns: Sign for respective players
        e.g. {1: 'X', 0: 'O'}
        '''
        self.size = 6
        self.playersigns = playersigns
        self.board = [[' ' for _ in range(self.size)] for _ in range(self.size)]
    
    def draw(self, screen, checked_winners, colors):
        '''
        Draws cell seperators and player moves on pygame screen
        '''
        s_h = screen.get_height()-150
        s_w = screen.get_width()
        dx = s_w // self.size 
        dy = s_h // self.size 

        screen.fill((51, 51, 51))
        
        # Draw cell seperators
        for i in range(self.size+1):
            pygame.draw.line(screen, (255, 255, 255), (dx*i, 0), (dx*i, s_h), 3)
            pygame.draw.line(screen, (255, 255, 255), (0, dy*i), (s_w, dy*i), 3)
        #score
        # score_font = pygame.font.SysFont('arial', 24)
        # player1_score_text = score_font.render(f"Player:", True, (255, 255, 255))
        # player2_score_text = score_font.render(f"AI:", True, (255, 255, 255))
        # screen.blit(player1_score_text)
        # screen.blit(player2_score_text)

        # Draw player moves
        for i in range(self.size):
            for j in range(self.size):
                if checked_winners[i][j]:     # Checked if a winner
                    screen.blit(font.render(self.board[i][j], 1, colors[1]), (j*dx+18, i*dy+18))
                else:
                    screen.blit(font.render(self.board[i][j], 1, colors[0]), (j*dx+18, i*dy+18))

    def update(self, i, j, player):
        '''
        Updates board[i][j] for player 1 or 2
        Returns True if successful
        '''
        # Already played in this cell
        if self.board[i][j] != ' ':
            return False

        self.board[i][j] = self.playersigns[player]
        return True
    
    @staticmethod
    def check_winner(board, checked_winners, playersigns):
        '''
        checked_winners: Already checked winners, no need to check again
        Returns winner player number, [Array of cells that made up wins]
        If no winner, retruns None, None
        '''
        for player, sign in playersigns.items():
            for i in range(len(board)):
                for j in range(len(board)):
                    if checked_winners[i][j]:
                        continue
                    if board[i][j] == sign:
                        # 2x2
                        if board[i][j] == board[(i - 1) % len(board)][j] == board[i-1][(j + 1) % len(board)] == board[(i ) % len(board)][(j + 1) % len(board)] == sign:
                            if (not(checked_winners[(i - 1) % len(board)][j]==True and checked_winners[i-1][(j + 1) % len(board)]==True and checked_winners[(i ) % len(board)][(j + 1) % len(board)]==True)):
                                return player, [((i-1)% len(board), (j+1) % len(board)),((i) % len(board), (j+1) % len(board)),((i-1) % len(board), j),(i, j)]
                        if board[i][j] == board[(i + 1) % len(board)][j] == board[i][(j - 1) % len(board)] == board[(i + 1) % len(board)][(j - 1) % len(board)] == sign:
                            if (not(checked_winners[(i + 1) % len(board)][j]==True and checked_winners[i][(j - 1) % len(board)]==True and checked_winners[(i + 1) % len(board)][(j - 1) % len(board)]==True)):
                                return player, [(i, j), ((i+1) % len(board), j), (i, (j-1) % len(board)), ((i+1) % len(board), (j-1) % len(board))]
                        elif checked_winners[i][(j+1)% len(board)]==True and checked_winners[(i+1)%len(board)][j]==True and checked_winners[(i+1)%len(board)][(j+1)% len(board)]==False:
                            if board[i][j] == board[i][(j+1)%len(board)] == board[(i+1)% len(board)][j] == board[(i+1) % len(board)][(j + 1) % len(board)] == sign:
                                return player, [(i, j), ((i) % len(board), (j+1)%len(board)), ((i+1) % len(board),j), ((i+1) % len(board), (j+1) % len(board))]                            
                        # 4 
                        elif board[i][j] == board[(i-1) % len(board)][(j - 1) % len(board)] == board[(i - 1) % len(board)][(j+1)% len(board)] == board[(i - 2) % len(board)][j] == sign:
                            return player, [(i, j), ((i-1) % len(board), (j-1) % len(board)), ((i-1) % len(board), (j+1) % len(board)), ((i-2) % len(board), (j))]
                        elif board[i][j] == board[(i-1) % len(board)][(j - 1) % len(board)] == board[(i ) % len(board)][(j-2)% len(board)] == board[(i +1) % len(board)][j-1] == sign:
                            return player, [((i+1) % len(board), (j-1)),((i) % len(board), (j-2) % len(board)),(i, j), ((i-1) % len(board), (j-1) % len(board))]
                        elif board[i][j] == board[(i+1) % len(board)][(j - 1) % len(board)] == board[(i+1 ) % len(board)][(j+1)% len(board)] == board[(i +2) % len(board)][j] == sign:
                            return player, [((i+2) % len(board), (j)),((i+1) % len(board), (j-1) % len(board)),((i+1) % len(board), (j+1) % len(board)),(i, j)]
        return None, None

    @staticmethod
    def all_filled(board):
        '''
        Checks if all spots are filled
        '''
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == ' ':
                    return False
        return True

    def clear(self):
        '''
        Initializes a clear new board
        '''
        self.board = [[' ' for _ in range(self.size)] for _ in range(self.size)]

    @staticmethod
    def _adjacent_cells(cell1, cell2):
        '''
        Returns True if adjacent in row, colomn, right-diagonal or left-diagonal
        '''
        if cell1[0] == cell2[0] and abs(cell1[1] - cell2[1]) == 1:  # row
            return True
        
        elif abs(cell1[0] - cell2[0]) == 1 and cell1[1] == cell2[1]:    # column
            return True
        
        elif abs(cell1[0] - cell2[0]) == 1 and abs(cell1[1] - cell2[1]) == 1:   # right-diagonal
            return True
        
        if cell1[0] == cell2[0] and cell1[1] == cell2[1]:   # left-diagonal
            return True
        
        return False

    def draw_line(self, screen, cell1, cell2, color=(255, 255, 255)):
        '''
        Draws a line from cell1 to cell2 on pygame screen
        '''
        s_h = screen.get_height()-150
        s_w = screen.get_width()
        dx = s_w // self.size
        dy = s_h // self.size

        if Board._adjacent_cells(cell1, cell2):
            point1 = dx * cell1[1] + dx//2, dy * cell1[0] + dy//2 
            point2 = dx * cell2[1] + dx//2, dy * cell2[0] + dy//2
            pygame.draw.line(screen, color, point1, point2, 5)
        else:
            if (cell1 == (0, 0) and cell2 == (self.size-1, self.size-1)) or (cell2 == (0, 0) and cell1 == (self.size-1, self.size-1)):     # corner right-diagonal edges
                pygame.draw.line(screen, color, (s_w - dx//2, s_h - dy//2), (s_w, s_h), 5)
                pygame.draw.line(screen, color, (0, 0), (dx//2, dy//2), 5)
            
            elif (cell1 == (self.size-1, 0) and cell2 == (0, self.size-1)) or (cell2 == (self.size-1, 0) and cell1 == (0, self.size-1)):   # corner left-diagonal edges
                pygame.draw.line(screen, color, (dx//2, s_h - dy//2), (0, s_h), 5)
                pygame.draw.line(screen, color, (s_w, 0), (s_w - dx//2, dy//2), 5)
            elif cell1[0] == cell2[0] and (cell1[1], cell2[1]) == (0, self.size-1):   # row edges
                point1 = dx * cell1[1] + dx//2, dy * cell1[0] + dy//2 
                pygame.draw.line(screen, color, (0, point1[1]), point1, 5)
                
                point2 = dx * cell2[1] + dx//2, dy * cell2[0] + dy//2
                pygame.draw.line(screen, color, point2, (s_w, point2[1]), 5)

            elif cell1[0] == cell2[0] and (cell2[1], cell1[1]) == (0, self.size-1):   # row edges
                point1 = dx * cell2[1] + dx//2, dy * cell2[0] + dy//2 
                pygame.draw.line(screen, color, (0, point1[1]), point1, 5)
                
                point2 = dx * cell1[1] + dx//2, dy * cell1[0] + dy//2
                pygame.draw.line(screen, color, point2, (s_w, point2[1]), 5)

            elif cell1[1] == cell2[1] and (cell1[0], cell2[0]) == (0, self.size-1):   # column edges
                point1 = dx * cell1[1] + dx//2, dy * cell1[0] + dy//2 
                pygame.draw.line(screen, color, (point1[0], 0), point1, 5)
                
                point2 = dx * cell2[1] + dx//2, dy * cell2[0] + dy//2
                pygame.draw.line(screen, color, point2, (point2[0], s_h), 5)

            elif cell1[1] == cell2[1] and (cell2[0], cell1[0]) == (0, self.size-1):   # column edges
                point1 = dx * cell2[1] + dx//2, dy * cell2[0] + dy//2 
                pygame.draw.line(screen, color, (point1[0], 0), point1, 5)
                
                point2 = dx * cell1[1] + dx//2, dy * cell1[0] + dy//2 
                pygame.draw.line(screen, color, point2, (point2[0], s_h), 5)