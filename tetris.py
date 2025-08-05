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
    global score, game_board
    
    new_board = [row for row in game_board if 0 in row]
    lines_cleared = grid_height - len(new_board)

    if lines_cleared > 0:
        empty_lines = [[0 for _ in range(grid_width)] for _ in range(lines_cleared)]
        game_board = empty_lines + new_board
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

def draw_next_tetromino(tetromino):
    next_text = font.render("NEXT", True, (255, 255, 255))
    screen.blit(next_text, (screen_width + 10, 5))
    
    preview_x = screen_width + 10
    preview_y = 30
    
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell == 'X':
                pygame.draw.rect(screen, tetromino.color, (
                    preview_x + x * (block_size // 2),
                    preview_y + y * (block_size // 2),
                    block_size // 2, block_size // 2
                ))

def find_hard_drop_y(tetromino):
    temp_y = tetromino.y
    while is_valid_move(tetromino, dy=1, new_shape=tetromino.shape):
        temp_y += 1
    return temp_y

def main_loop():
    global game_over
    running = True
    clock = pygame.time.Clock()
    
    current_tetromino = Tetromino(random.randint(0, len(tetrominoes) - 1))
    next_tetromino = Tetromino(random.randint(0, len(tetrominoes) - 1))
    
    fall_time = 0
    move_time = 0
    
    fall_speed_normal = 0.5
    fall_speed_soft_drop = 0.05
    fall_speed = fall_speed_normal
    
    move_speed = 0.1  # 빠른 좌우 이동 속도

    while running:
        dt = clock.tick(60) / 1000.0
        fall_time += dt
        move_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    fall_speed = fall_speed_normal

        # 키를 누르고 있는 상태를 감지하여 빠른 이동 처리
        keys = pygame.key.get_pressed()
        
        # 소프트 드롭 속도 제어
        if keys[pygame.K_DOWN]:
            fall_speed = fall_speed_soft_drop
        else:
            fall_speed = fall_speed_normal

        # 빠른 좌우 이동 제어
        if move_time > move_speed:
            if keys[pygame.K_LEFT] and is_valid_move(current_tetromino, dx=-1):
                current_tetromino.move(-1, 0)
            if keys[pygame.K_RIGHT] and is_valid_move(current_tetromino, dx=1):
                current_tetromino.move(1, 0)
            move_time = 0

        # 단일 키 입력 처리 (회전, 하드 드롭)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                rotated_shape = list(zip(*current_tetromino.shape[::-1]))
                
                # 2x2 블록(인덱스 1)은 회전해도 모양이 같으므로 위치 보정 필요 없음
                if current_tetromino.shape_index == 1:
                     if is_valid_move(current_tetromino, new_shape=rotated_shape):
                         current_tetromino.rotate()
                else:
                    kick_offsets = [(0, 0), (-1, 0), (1, 0), (-2, 0), (2, 0)]
                    for dx, dy in kick_offsets:
                        if is_valid_move(current_tetromino, dx=dx, dy=dy, new_shape=rotated_shape):
                            current_tetromino.x += dx
                            current_tetromino.y += dy
                            current_tetromino.rotate()
                            break

            if event.key == pygame.K_SPACE:
                drop_y = find_hard_drop_y(current_tetromino)
                current_tetromino.y = drop_y

        if fall_time > fall_speed:
            if is_valid_move(current_tetromino, dy=1):
                current_tetromino.move(0, 1)
            else:
                lock_block(current_tetromino)
                check_and_clear_lines()
                
                current_tetromino = next_tetromino
                next_tetromino = Tetromino(random.randint(0, len(tetrominoes) - 1))
                
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
        draw_next_tetromino(next_tetromino)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_loop()