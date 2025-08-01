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
    """이동하려는 위치가 유효한지 확인합니다."""
    shape_to_check = new_shape if new_shape else tetromino.shape
    for y, row in enumerate(shape_to_check):
        for x, cell in enumerate(row):
            if cell == 'X':
                # 이동하려는 위치 계산
                new_x = tetromino.x + x + dx
                new_y = tetromino.y + y + dy
                
                # 경계 검사
                if not (0 <= new_x < grid_width and 0 <= new_y < grid_height):
                    return False
    return True

# 7. 게임판 그리기
def draw_grid():
    for x in range(0, screen_width, block_size):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, screen_height))
    for y in range(0, screen_height, block_size):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (screen_width, y))

# 8. 게임 루프
def main_loop():
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
        
        if fall_time > fall_speed:
            if is_valid_move(current_tetromino, dy=1):
                current_tetromino.move(0, 1)
            fall_time = 0

        screen.fill((0, 0, 0))
        draw_grid()
        current_tetromino.draw()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_loop()