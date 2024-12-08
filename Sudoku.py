import pygame, sys
from sudoku_generator import *


#recommended classes:

class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value = 0
        self.selected = False



    def draw(self):
        cell_size = 50
        x = self.col * cell_size
        y = self.row * cell_size

        if self.selected == True:
            color = (28, 47, 255)
        else:
            color = (0, 0, 0)

        pygame.draw.rect(self.screen, color, (x, y, cell_size, cell_size), 2)

        font = pygame.font.Font(None, 40)
        if self.value != 0:
            text = font.render(str(self.value), 0, (0, 0, 0))
            self.screen.blit(text, (x + cell_size // 2 - 10, y + cell_size // 2 - 15))


class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty

        # determine number of cells to remove based on difficulty
        difficulty_dict = {"easy": 30, "medium": 40, "hard": 50}
        removed_cells = difficulty_dict[difficulty] if difficulty in difficulty_dict else 50

        # gen puzzle and solution
        gen = SudokuGenerator(9, removed_cells)
        gen.fill_values()
        self.solution = [row.copy() for row in gen.get_board()]
        gen.remove_cells()
        self.board_values = gen.get_board()
        self.original_board = [row.copy() for row in self.board_values]

        self.cells = [[Cell(self.board_values[row][col], row, col, screen) for col in range(9)] for row in range(9)]
        self.selected_cell = None

    def draw(self):
        for row in self.cells:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        current_selected_cell = self.selected_cell
        if self.selected_cell is not None:
            current_selected_cell.selected = False
        self.selected_cell = self.cells[row][col]
        self.selected_cell.selected = True

    def clear(self):
        current_selected_cell = self.selected_cell
        if current_selected_cell is not None:
            if self.original_board[current_selected_cell.row][current_selected_cell.col] == 0:
                current_selected_cell.set_cell_value(0)
                current_selected_cell.set_sketched_value(0)


    def reset_to_original(self):
        for row in range(9):
            for col in range(9):
                original_value = self.original_board[row][col]
                cell = self.cells[row][col]
                cell.set_cell_value(original_value)
                cell.set_sketched_value(0)

    def update_board(self):
        self.board_values = [[cell.value for cell in row] for row in self.cells]



def main():
    pygame.init()


    pygame.display.set_caption("Sudoku")
    screen = pygame.display.set_mode((500, 500))

    while True:
        difficulty = None

        def start_screen_buttons():
            gamemode_font = pygame.font.Font(None, 30)
            easy_button = pygame.Rect(225, 265, 100, 30)
            medium_button = pygame.Rect(225, 305, 100, 30)
            hard_button = pygame.Rect(225, 345, 100, 30)
            welcome_font = pygame.font.Font(None, 50)
            select_font = pygame.font.Font(None, 40)
            info_font = pygame.font.Font(None, 30)

            welcome_text = welcome_font.render("Welcome to Sudoku!", 0, (35, 44, 173))
            welcome_rect = welcome_text.get_rect(center = (225, 100))
            screen.blit(welcome_text, welcome_rect) # place text

            select_text = select_font.render("Select a Game Mode:", 0, (35, 44, 173))
            select_rect = select_text.get_rect(center = (225, 225))
            screen.blit(select_text, select_rect) # place text

            info_text = info_font.render("Click on Option to Begin!", 0, (35, 44, 173))
            info_rect = info_text.get_rect(center = (225, 450))
            screen.blit(info_text, info_rect) # place text

            pygame.draw.rect(screen, (255, 255, 255), easy_button)
            pygame.draw.rect(screen, (255, 255, 255), medium_button)
            pygame.draw.rect(screen, (255, 255, 255), hard_button)

            screen.blit(gamemode_font.render("Easy", 0, (8, 14, 92)), (253, 270))
            screen.blit(gamemode_font.render("Medium", 0, (8, 14, 92)), (242, 310))
            screen.blit(gamemode_font.render("Hard", 0, (8, 14, 92)), (253, 350))

            return easy_button, medium_button, hard_button

        # when difficulty not chosen yet
        while difficulty not in ["easy", "medium", "hard"]:
            screen.fill((212, 234, 255))
            easy_button, medium_button, hard_button = start_screen_buttons()
            pygame.display.flip()     # displays screen


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    if easy_button.collidepoint(position):
                        difficulty = "easy"
                    if medium_button.collidepoint(position):
                        difficulty = "medium"
                    if hard_button.collidepoint(position):
                        difficulty = "hard"



        board = Board(450, 450, screen, difficulty)
        running = True

        def game_buttons():
            reset_button = pygame.Rect(50, 460, 120, 50)
            restart_button = pygame.Rect(175, 460, 120, 50)
            exit_button = pygame.Rect(300, 460, 120, 50)
            button_font = pygame.font.Font(None, 36)
            buttons = [("Reset", pygame.Rect(50, 460, 120, 50)), ("Restart", pygame.Rect(175, 460, 120, 50)), ("Exit", pygame.Rect(300, 460, 120, 50))]

            for label, rect in buttons:
                pygame.draw.rect(screen, (255, 255, 255), rect) #draw button
                text_surface = button_font.render(label, 0, (0, 0, 0))
                text_position = (rect.x + 15, rect.y + 3)
                screen.blit(text_surface, text_position)


            return reset_button, restart_button, exit_button

        while running:
            screen.fill((212, 234, 255))
            board.draw()
            reset_button, restart_button, exit_button = game_buttons()
            pygame.display.flip()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if reset_button.collidepoint(pos):
                        return board.reset_to_original()
                    if restart_button.collidepoint(pos):
                        return reset_button, restart_button, exit_button
                    if exit_button.collidepoint(pos):
                        running = False
                        sys.exit()
                        break









if __name__ == "__main__":
    while True:
        main()
