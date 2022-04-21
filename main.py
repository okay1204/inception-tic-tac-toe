# pylint: disable=no-member, unused-wildcard-import
from typing import List, Literal, Optional, Tuple
import pygame

# Window size
WIDTH = 800
HEIGHT = 900

# Typing shortcuts
Mark = Literal['X', 'O', None]

# Initialize pygame
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Inception Tic Tac Toe")

# Colors
class Color:
    WHITE = (255, 255, 255)
    DARK_GRAY = (50, 50, 50)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    HIGHLIGHT = (255, 252, 179)

# Fonts
class Font:
    CURRENT_TURN = pygame.font.SysFont('Arial', 60)


class TicTacToeBoard:
    """
    Tic Tac Toe Board
    """

    BOARD_SIZE = 200
    BOARD_LINE_WIDTH = 10

    def __init__(self) -> None:
        # None = empty, X = X, O = O
        self.board: List[List[TickBox]] = []
        for _ in range(3):
            self.board.append([])
            for _ in range(3):
                self.board[-1].append(TickBox())

        # This is set to the winner if there is one
        self.winning_mark: Mark = None

    def draw(self, x: int, y: int) -> None:
        """
        Draws the board
        """

        # Draws a large black square to fill in with white squares
        pygame.draw.rect(screen, Color.DARK_GRAY, (x, y, self.BOARD_SIZE - self.BOARD_LINE_WIDTH, self.BOARD_SIZE - self.BOARD_LINE_WIDTH))

        # Loop through all 9 squares
        for boxX in range(3):
            for boxY in range(3):
                # Draw a TickBox
                self.board[boxY][boxX].draw(x + ((self.BOARD_SIZE / 3) * boxX), y + ((self.BOARD_SIZE / 3) * boxY))

    def set_mark(self, x: int, y: int, mark: Mark) -> None:
        """
        Sets a box to a mark
        """
        self.board[y][x].mark = mark

    def get_box(self, x: int, y: int) -> 'TickBox':
        """
        Gets the TickBox at a specific coordinate
        """
        return self.board[y][x]

    def check_winner(self) -> Mark:
        """
        Checks if there is a winner. Returns the winner if there is one and set winning_mark to the corresponding mark.
        """
        # Check rows
        for row in self.board:
            if row[0].mark == row[1].mark == row[2].mark and row[0].mark is not None:
                self.winning_mark = row[0]
                return self.winning_mark

        # Check columns
        for col in range(3):
            if self.get_box(0, col).mark and self.get_box(0, col).mark == self.get_box(1, col).mark == self.get_box(2, col).mark:
                self.winning_mark = self.board[0][col]
                return self.winning_mark

        # Check diagonals
        if self.get_box(0, 0).mark and self.get_box(0, 0).mark == self.get_box(1, 1).mark == self.get_box(2, 2).mark:
            self.winning_mark = self.board[0][0]
            return self.winning_mark
        if self.get_box(0, 2).mark and self.get_box(0, 2).mark == self.get_box(1, 1).mark == self.get_box(2, 0).mark:
            self.winning_mark = self.board[0][2]
            return self.winning_mark

        # No winner
        return None

    def is_full(self) -> bool:
        """
        Checks if the board is full
        """
        for row in self.board:
            for box in row:
                if box.mark is None:
                    return False
        return True

class TickBox:
    SIZE = (TicTacToeBoard.BOARD_SIZE - (TicTacToeBoard.BOARD_LINE_WIDTH * 2)) // 3

    XO_WIDTH = 7
    XO_MARGIN = 10

    def __init__(self):
        self.rect: Optional[pygame.Rect] = None
        self.mark: Mark = None

    def draw(self, x: int, y: int) -> None:
        self.rect = pygame.Rect(x, y, self.SIZE, self.SIZE)
        pygame.draw.rect(screen, Color.WHITE, self.rect)
        self.draw_mark(x, y)

    def draw_mark(self, x: int, y: int) -> None:
        # Draw the X or O
        if self.mark == 'X':
            # Draw the blue line from the top left to the bottom right 
            pygame.draw.line(
                screen,
                Color.BLUE,
                (
                    x + self.XO_MARGIN,
                    y + self.XO_MARGIN
                ),
                (
                    x + (self.SIZE - self.XO_MARGIN),
                    y + (self.SIZE - self.XO_MARGIN)
                ),
                self.XO_WIDTH
            )

            # Draw the blue line from the top right to the bottom left
            pygame.draw.line(
                screen,
                Color.BLUE,
                (
                    x + self.XO_MARGIN,
                    y + (TickBox.SIZE - self.XO_MARGIN)
                ),
                (
                    x + (TickBox.SIZE - self.XO_MARGIN),
                    y + self.XO_MARGIN
                ),
                self.XO_WIDTH
            )

        elif self.mark == 'O':
            # Get the center of the box
            circle_center = (
                x + TickBox.SIZE // 2,
                y + TickBox.SIZE // 2
            )

            # Draw outer red circle
            pygame.draw.circle(
                screen,
                Color.RED,
                circle_center,
                self.SIZE // 2 - (self.XO_MARGIN / 2)
            )
            # Draw inner white circle
            pygame.draw.circle(
                screen,
                Color.WHITE,
                circle_center,
                self.SIZE // 2 - (self.XO_MARGIN / 2) - self.XO_WIDTH
            )

    def is_hovered_over(self, mouse_pos: Tuple[int, int]) -> bool:
        if not self.rect:
            return False

        if self.rect.collidepoint(mouse_pos):
            return True
        return False

    def highlight(self) -> None:
        if not self.rect:
            return

        pygame.draw.rect(screen, Color.HIGHLIGHT, self.rect)
        self.draw_mark(self.rect.x, self.rect.y)

class InceptionBoard:
    """
    Inception Board
    """

    BOARD_SIZE = 750
    BOARD_LINE_WIDTH = 10
    BOARD_BOX_SIZE = (BOARD_SIZE - (BOARD_LINE_WIDTH * 2)) // 3


    def __init__(self) -> None:
        # None = empty, X = X, O = O
        self.board: List[List[TicTacToeBoard]] = []
        for _ in range(3):
            self.board.append([])
            for _ in range(3):
                self.board[-1].append(TicTacToeBoard())

    def get_board(self, x: int, y: int) -> TicTacToeBoard:
        """
        Gets the TicTacToeBoard at a specific coordinate
        """
        return self.board[y][x]

    def draw(self, x: int, y: int) -> None:
        """
        Draws the board
        """

        # Draws a large black square to fill in with tic tac toe boards
        pygame.draw.rect(screen, Color.DARK_GRAY, (x, y, self.BOARD_SIZE - self.BOARD_LINE_WIDTH, self.BOARD_SIZE - self.BOARD_LINE_WIDTH))

        # Loop through all 9 squares
        for boxX in range(3):
            for boxY in range(3):

                # Draw a smaller white square in the correct position for the background
                pygame.draw.rect(
                    screen,
                    Color.WHITE,
                    (
                        x + ((self.BOARD_SIZE / 3) * boxX),
                        y + ((self.BOARD_SIZE / 3) * boxY),
                        self.BOARD_BOX_SIZE,
                        self.BOARD_BOX_SIZE
                    )
                )

                # Draw a tic tac toe board in the center of the box
                self.board[boxY][boxX].draw(
                    x + ((self.BOARD_SIZE / 3) * boxX) + self.BOARD_BOX_SIZE // 2 - TicTacToeBoard.BOARD_SIZE // 2,
                    y + ((self.BOARD_SIZE / 3) * boxY) + self.BOARD_BOX_SIZE // 2 - TicTacToeBoard.BOARD_SIZE // 2
                )

    def get_hovering_tickbox(self) -> Optional[TickBox]:
        """
        Gets the TickBox that the mouse is hovering over
        """
        mouse_pos = pygame.mouse.get_pos()

        for miniboardX in range(3):
            for miniBoardY in range(3):
                miniboard = self.get_board(miniboardX, miniBoardY)

                for tickboxX in range(3):
                    for tickboxY in range(3):
                        tickbox = miniboard.get_box(tickboxX, tickboxY)

                        if tickbox.is_hovered_over(mouse_pos):
                            return tickbox

running: bool = True
board: InceptionBoard = InceptionBoard()
turn: Literal['X', 'O'] = 'X'
clicked_tickbox: Optional[TickBox] = None

while running:
    hovering_tickbox = board.get_hovering_tickbox()

    for event in pygame.event.get(): # Gets all the events which have occured till now and keeps tab of them.
        # Listens for the the X button at the top
        if event.type == pygame.QUIT:
            running = False
        # Listens for mouse left-click down
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if hovering_tickbox:
                clicked_tickbox = hovering_tickbox
        # Listens for mouse left-click release
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if clicked_tickbox and clicked_tickbox is hovering_tickbox:

                # If the box is empty, fill it with the current player's mark
                if not clicked_tickbox.mark:
                    clicked_tickbox.mark = turn
                    turn = 'X' if turn == 'O' else 'O'
                
                clicked_tickbox = None

    # Clear the screen
    screen.fill(Color.WHITE)
    
    text_surface: pygame.Surface = Font.CURRENT_TURN.render('Turn:', True, Color.BLACK)
    screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width(), 20))

    # Draw the board in the horizontal center and bottom of the screen
    board.draw((WIDTH // 2) - (board.BOARD_SIZE // 2), HEIGHT - board.BOARD_SIZE)
    
    if hovering_tickbox:
        hovering_tickbox.highlight()
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        # Set cursor to default
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)


    pygame.display.flip()

pygame.quit()