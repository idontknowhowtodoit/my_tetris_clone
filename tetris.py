# tetris.py
import pygame
import sys

# 1. 초기화
pygame.init()

# 2. 화면 설정
screen_width = 300
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Tetris Clone")

# 3. 게임 루프
def main_loop():
    running = True
    while running:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # 화면을 검은색으로 채우기
        screen.fill((0, 0, 0))
        
        # 화면 업데이트
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_loop()