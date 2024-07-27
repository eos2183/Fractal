import pygame
import numpy as np
from numba import jit, prange
import colorsys

# 초기 설정
WIDTH, HEIGHT = 800, 600
MAX_ITER = 2000  # 반복 횟수 증가

# 초기 뷰 설정
x_min, x_max = -2.0, 1.0
y_min, y_max = -1.5, 1.5

# Pygame 초기화
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mandelbrot Set")

@jit(nopython=True, parallel=True)
def mandelbrot(h, w, max_iter, x_min, x_max, y_min, y_max):
    result = np.zeros((h, w), dtype=np.float64)  # float64로 변경
    for i in prange(h):
        for j in prange(w):
            x = x_min + (x_max - x_min) * j / (w - 1)
            y = y_min + (y_max - y_min) * i / (h - 1)
            c = complex(x, y)
            z = 0
            for k in range(max_iter):
                if abs(z) > 2:
                    break
                z = z*z + c
            if k < max_iter - 1:
                result[i, j] = k + 1 - np.log(np.log2(abs(z)))  # 부드러운 색상 전환
            else:
                result[i, j] = k
    return result

def create_color_palette(n):
    palette = []
    for i in range(n):
        hue = (i / n) % 1.0  # 색상 순환
        saturation = 1.0 if i < n - 1 else 0.0  # 마지막 색상은 검은색
        value = 1.0 if i < n - 1 else 0.0
        r, g, b = [int(x * 255) for x in colorsys.hsv_to_rgb(hue, saturation, value)]
        palette.append((r, g, b))
    return palette

color_palette = create_color_palette(MAX_ITER)

@jit(nopython=True)
def apply_palette(fractal, palette):
    h, w = fractal.shape
    result = np.zeros((h, w, 3), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            index = int(fractal[i, j]) % len(palette)
            result[i, j] = palette[index]
    return result

def update_screen(x_min, x_max, y_min, y_max):
    fractal = mandelbrot(HEIGHT, WIDTH, MAX_ITER, x_min, x_max, y_min, y_max)
    colored_fractal = apply_palette(fractal, color_palette)
    surf = pygame.surfarray.make_surface(colored_fractal.transpose(1, 0, 2))
    screen.blit(surf, (0, 0))
    pygame.display.flip()

def zoom(x_min, x_max, y_min, y_max, zoom_factor, mouse_x, mouse_y):
    x_range = x_max - x_min
    y_range = y_max - y_min
    mouse_x_frac = mouse_x / WIDTH
    mouse_y_frac = mouse_y / HEIGHT
    
    new_x_range = x_range * zoom_factor
    new_y_range = y_range * zoom_factor
    
    new_x_min = x_min + mouse_x_frac * (x_range - new_x_range)
    new_x_max = new_x_min + new_x_range
    new_y_min = y_min + mouse_y_frac * (y_range - new_y_range)
    new_y_max = new_y_min + new_y_range
    
    return new_x_min, new_x_max, new_y_min, new_y_max

# 메인 루프
running = True
dragging = False
drag_start = None
needs_update = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 좌클릭
                dragging = True
                drag_start = event.pos
            elif event.button == 4:  # 스크롤 업 (줌 인)
                x_min, x_max, y_min, y_max = zoom(x_min, x_max, y_min, y_max, 0.8, event.pos[0], event.pos[1])
                needs_update = True
            elif event.button == 5:  # 스크롤 다운 (줌 아웃)
                x_min, x_max, y_min, y_max = zoom(x_min, x_max, y_min, y_max, 1.2, event.pos[0], event.pos[1])
                needs_update = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # 좌클릭 해제
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                dx = event.pos[0] - drag_start[0]
                dy = event.pos[1] - drag_start[1]
                drag_start = event.pos
                
                move_x = (x_max - x_min) * dx / WIDTH
                move_y = (y_max - y_min) * dy / HEIGHT
                x_min -= move_x
                x_max -= move_x
                y_min += move_y
                y_max += move_y
                
                needs_update = True

    if needs_update:
        update_screen(x_min, x_max, y_min, y_max)
        needs_update = False

pygame.quit()