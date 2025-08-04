import pygame
import sys
import random

# 1. 초기화
pygame.init()

# 2. 화면 설정
screen_width = 300
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Tetris Clone")

# 3. 게임 변수
grid_width = 10
grid_height = 20
block_size = screen_width // grid_width
game_board = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
game_over = False
score = 0
font = pygame.font.Font(None, 24)

# 4. 블록 모양 정의
tetrominoes = [
    [['.', 'X', '.', '.'],
     ['.', 'X', '.', '.'],
     ['.', 'X', '.', '.'],
     ['.', 'X', '.', '.']],
    [['.', 'X', 'X'],
     ['.', 'X', 'X']],
    [['.', 'X', '.'],
     ['X', 'X', 'X']],
    [['.', 'X', '.'],
     ['.', 'X', '.'],
     ['.', 'X', 'X']],
    [['.', 'X', '.'],
     ['.', 'X', '.'],
     ['X', 'X', '.']],
    [['.', 'X', 'X'],
     ['X', 'X', '.']],
    [['X', 'X', '.'],
     ['.', 'X', 'X']]
]

# 5. 색상 정의
colors = [
    (0, 0, 0),      # 검은색 (배경)
    (0, 255, 255),  # 하늘색 (I)
    (255, 255, 0),  # 노란색 (O)
    (128, 0, 128),  # 보라색 (T)
    (255, 165, 0),  # 주황색 (L)
    (0, 0, 255),    # 파란색 (J)
    (0, 255, 0),    # 초록색 (S)
    (255, 0, 0)     # 빨간색 (Z)
]

# 6. 블록 클래스 정의
class Tetromino:
    def __init__(self, shape_index):
        self.shape_index = shape_index
        self.shape = tetrominoes[shape_index]
        self.color = colors[shape_index + 1]
        self.x = grid_width // 2 - len(self.shape[0]) // 2
        self.y = 0

    def draw(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell == 'X':
                    pygame.draw.rect(screen, self.color, (
                        (self.x + x) * block_size,
                        (self.y + y) * block_size,
                        block_size, block_size
                    ))
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

def is_valid_move(tetromino, dx=0, dy=0, new_shape=None):
    shape_to_check = new_shape if new_shape else tetromino.shape
    for y, row in enumerate(shape_to_check):
        for x, cell in enumerate(row):
            if cell == 'X':
                new_x = tetromino.x + x + dx
                new_y = tetromino.y + y + dy
                
                if not (0 <= new_x < grid_width and 0 <= new_y < grid_height and game_board[new_y][new_x] == 0):
                    return False
    return True

def lock_block(tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell == 'X':
                game_board[tetromino.y + y][tetromino.x + x] = tetromino.color

def check_and_clear_lines():
    """
    게임판에 가득 찬 줄이 있는지 확인하고 지우는 기능입니다.
    """
    global score
    lines_cleared = 0
    
    # 맨 밑 줄부터 위로 올라가며 확인
    for y in range(grid_height - 1, -1, -1):
        if 0 not in game_board[y]:
            lines_cleared += 1
            # 한 줄이 가득 찼으면 해당 줄을 삭제
            del game_board[y]
            # 맨 위에 빈 줄을 새로 추가
            game_board.insert(0, [0 for _ in range(grid_width)])
    
    if lines_cleared > 0:
        # 줄 개수에 따라 점수 부여
        score += lines_cleared * 100

def draw_grid():
    for x in range(0, screen_width, block_size):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, screen_height))
    for y in range(0, screen_height, block_size):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (screen_width, y))

def draw_game_board():
    for y, row in enumerate(game_board):
        for x, cell_color in enumerate(row):
            if cell_color != 0:
                pygame.draw.rect(screen, cell_color, (
                    x * block_size, y * block_size, block_size, block_size
                ))

def draw_score():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (5, 5))

def main_loop():
    global game_over
    running = True
    clock = pygame.time.Clock()
    
    current_tetromino = Tetromino(random.randint(0, len(tetrominoes) - 1))
    
    fall_time = 0
    fall_speed = 0.5

    while running:
        dt = clock.tick(60) / 1000.0
        fall_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and is_valid_move(current_tetromino, dx=-1):
                    current_tetromino.move(-1, 0)
                if event.key == pygame.K_RIGHT and is_valid_move(current_tetromino, dx=1):
                    current_tetromino.move(1, 0)
                if event.key == pygame.K_UP:
                    rotated_shape = list(zip(*current_tetromino.shape[::-1]))
                    if is_valid_move(current_tetromino, new_shape=rotated_shape):
                        current_tetromino.rotate()
                if event.key == pygame.K_DOWN:
                    if is_valid_move(current_tetromino, dy=1):
                        current_tetromino.move(0, 1)

        if fall_time > fall_speed:
            if is_valid_move(current_tetromino, dy=1):
                current_tetromino.move(0, 1)
            else:
                lock_block(current_tetromino)
                check_and_clear_lines()
                
                current_tetromino = Tetromino(random.randint(0, len(tetrominoes) - 1))
                
                # 게임 오버 확인
                if not is_valid_move(current_tetromino):
                    game_over = True
            fall_time = 0
        
        if game_over:
            running = False
            print(f"게임 오버! 최종 점수: {score}")

        screen.fill((0, 0, 0))
        draw_grid()
        draw_game_board()
        current_tetromino.draw()
        draw_score()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_loop()