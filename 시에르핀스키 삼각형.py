import pygame
import math

# 초기화
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("유한하면서 무한한 시에르핀스키 삼각형")

# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 초기 변수
zoom = 1 
offset_x, offset_y = 0, 0
dragging = False
last_pos = (0, 0) 


def draw_triangle(x1, y1, x2, y2, x3, y3, depth, max_depth):
    if depth == max_depth or (x2 - x1)**2 + (y2 - y1)**2 < 1:  # 픽셀 크기보다 작아지면 중단
        pygame.draw.polygon(screen, WHITE, [(x1, y1), (x2, y2), (x3, y3)], 1)
    else:
        #중점계산
        x12 = (x1 + x2) / 2
        y12 = (y1 + y2) / 2
        x23 = (x2 + x3) / 2
        y23 = (y2 + y3) / 2
        x31 = (x3 + x1) / 2
        y31 = (y3 + y1) / 2
        
        draw_triangle(x1, y1, x12, y12, x31, y31, depth + 1, max_depth)
        draw_triangle(x2, y2, x23, y23, x12, y12, depth + 1, max_depth)
        draw_triangle(x3, y3, x31, y31, x23, y23, depth + 1, max_depth)

running = True
clock = pygame.time.Clock()
1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:   # 확대
                zoom *= 1.1
            elif event.button == 5:   # 키로 축소
                zoom /= 1.1
            if event.button == 1:  # 좌클릭
                dragging = True
                last_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # 좌클릭 해제
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                dx, dy = event.pos[0] - last_pos[0], event.pos[1] - last_pos[1]
                offset_x += dx
                offset_y += dy
                last_pos = event.pos

    screen.fill(BLACK)
    
    # 삼각형 그리기
    size = min(width, height) * 0.8 * zoom
    x1 = width / 2 + math.cos(math.pi / 2) * size / 2 + offset_x
    y1 = height / 2 - math.sin(math.pi / 2) * size / 2 + offset_y
    x2 = width / 2 + math.cos(math.pi * 7 / 6) * size / 2 + offset_x
    y2 = height / 2 - math.sin(math.pi * 7 / 6) * size / 2 + offset_y
    x3 = width / 2 + math.cos(math.pi * 11 / 6) * size / 2 + offset_x
    y3 = height / 2 - math.sin(math.pi * 11 / 6) * size / 2 + offset_y
    
    max_depth = int(math.log(size, 2)) + 5  # zoom에 따라 동적으로 깊이 조절
    draw_triangle(x1, y1, x2, y2, x3, y3, 0, max_depth)
    
    pygame.display.flip()
    clock.tick(60)  # 60 FPS로 제한

pygame.quit()