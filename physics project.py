import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MagnetoElastic Particle Dynamics")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
GREEN = (0, 200, 0)

font = pygame.font.SysFont("arial", 20, bold=True)

particle_RADIUS = 6              
MAGNETIC_RANGE = 4 * particle_RADIUS
CONNECTION_RANGE = 150
SPRING_K = 0.00005
REPULSION_STRENGTH = 100
FRICTION = 1.0
MIN_DIST = 5                  


particles = []

button_width, button_height = 80, 40
button_rect = pygame.Rect(WIDTH - button_width - 10, 10, button_width, button_height)

is_dragging = False
drag_start_pos = (0, 0)
current_mouse_pos = (0, 0)
SPEED_FACTOR = 0.1

running = True

def apply_physics():

    for p in particles:
        p['acc'] = [0, 0]

    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            p1 = particles[i]
            p2 = particles[j]

            dx = p1['pos'][0] - p2['pos'][0]
            dy = p1['pos'][1] - p2['pos'][1]
            distance = math.hypot(dx, dy)
            
            if distance < MIN_DIST: 
                distance = MIN_DIST

            repulsion_force = 0
            if distance < MAGNETIC_RANGE:
                repulsion_force = REPULSION_STRENGTH / (distance * distance)

            spring_force = 0
            if distance < CONNECTION_RANGE:
                spring_force = SPRING_K * distance

            total_force = spring_force - repulsion_force

            fx = (dx / distance) * total_force
            fy = (dy / distance) * total_force

            p1['acc'][0] -= fx
            p1['acc'][1] -= fy
            p2['acc'][0] += fx
            p2['acc'][1] += fy

    for p in particles:
        p['vel'][0] += p['acc'][0]
        p['vel'][1] += p['acc'][1]
        
        p['vel'][0] *= FRICTION
        p['vel'][1] *= FRICTION

        p['pos'][0] += p['vel'][0]
        p['pos'][1] += p['vel'][1]

        if p['pos'][0] <= particle_RADIUS:
            p['pos'][0] = particle_RADIUS
            p['vel'][0] *= -1
        elif p['pos'][0] >= WIDTH - particle_RADIUS:
            p['pos'][0] = WIDTH - particle_RADIUS
            p['vel'][0] *= -1

        if p['pos'][1] <= particle_RADIUS:
            p['pos'][1] = particle_RADIUS
            p['vel'][1] *= -1
        elif p['pos'][1] >= HEIGHT - particle_RADIUS:
            p['pos'][1] = HEIGHT - particle_RADIUS
            p['vel'][1] *= -1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if button_rect.collidepoint(mouse_pos):
                particles = []
            else:
                is_dragging = True
                drag_start_pos = mouse_pos
                current_mouse_pos = mouse_pos
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if is_dragging:
                is_dragging = False
                
                dx = drag_start_pos[0] - current_mouse_pos[0]
                dy = drag_start_pos[1] - current_mouse_pos[1]
                
                new_particle = {
                    'pos': list(drag_start_pos),
                    'vel': [dx * SPEED_FACTOR, dy * SPEED_FACTOR],
                    'acc': [0, 0] 
                }
                particles.append(new_particle)
        
        elif event.type == pygame.MOUSEMOTION:
            if is_dragging:
                current_mouse_pos = pygame.mouse.get_pos()

    apply_physics()

    screen.fill(WHITE)

    for i in range(len(particles)):
        
        for j in range(i + 1, len(particles)):

            p1 = particles[i]
            p2 = particles[j]
            dist = math.hypot(p1['pos'][0] - p2['pos'][0], p1['pos'][1] - p2['pos'][1])
            
            if dist < CONNECTION_RANGE:

                pygame.draw.line(screen, BLACK, p1['pos'], p2['pos'], 1)

    for p in particles:
        pygame.draw.circle(screen, RED, (int(p['pos'][0]), int(p['pos'][1])), particle_RADIUS)

    if is_dragging:
        pygame.draw.line(screen, GREEN, drag_start_pos, current_mouse_pos, 2)
        s = pygame.Surface((particle_RADIUS*2, particle_RADIUS*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (255, 0, 0, 100), (particle_RADIUS, particle_RADIUS), particle_RADIUS)
        screen.blit(s, (drag_start_pos[0]-particle_RADIUS, drag_start_pos[1]-particle_RADIUS))

    pygame.draw.rect(screen, GRAY, button_rect)
    pygame.draw.rect(screen, DARK_GRAY, button_rect, 2)
    text_surf = font.render("Clear", True, BLACK)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)

    pygame.display.flip()

pygame.quit()