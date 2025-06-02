import pygame
import sys

class MenuManager:
    def __init__(self, screen, clock, width, height, fps, colors):
        self.screen = screen
        self.clock = clock
        self.width = width
        self.height = height
        self.fps = fps
        self.colors = colors

    def main_menu(self):
        menu_running = True
        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    menu_running = False

            self.screen.fill(self.colors["black"])
            font = pygame.font.SysFont(None, 72)
            title = font.render("Main Menu", True, self.colors["white"])
            self.screen.blit(title, (self.width//2 - title.get_width()//2, self.height//2 - 100))

            font_small = pygame.font.SysFont(None, 36)
            prompt = font_small.render("Press any button to Start", True, self.colors["white"])
            self.screen.blit(prompt, (self.width//2 - prompt.get_width()//2, self.height//2))

            pygame.display.flip()
            self.clock.tick(self.fps)

    def pause_menu(self):
        pause_running = True
        while pause_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    pause_running = False

            self.screen.fill(self.colors["black"])
            font = pygame.font.SysFont(None, 72)
            title = font.render("Paused", True, self.colors["white"])
            self.screen.blit(title, (self.width//2 - title.get_width()//2, self.height//2 - 50))

            font_small = pygame.font.SysFont(None, 36)
            prompt = font_small.render("Press anu button to Resume", True, self.colors["white"])
            self.screen.blit(prompt, (self.width//2 - prompt.get_width()//2, self.height//2 + 20))

            pygame.display.flip()
            self.clock.tick(self.fps)

    def game_over_menu(self, score, waves_cleared):
        game_over_running = True
        while game_over_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    game_over_running = False

            self.screen.fill(self.colors["black"])
            font = pygame.font.SysFont(None, 72)
            title = font.render("Game Over", True, self.colors["red"])
            self.screen.blit(title, (self.width//2 - title.get_width()//2, self.height//2 - 100))

            font_small = pygame.font.SysFont(None, 36)
            prompt = font_small.render(f"Score: {score}", True, self.colors["white"])
            self.screen.blit(prompt, (self.width//2 - prompt.get_width()//2, self.height//2 - 20))

            waves_cleared_text = font_small.render(f"Waves cleared: {waves_cleared}", True, self.colors['white'])
            self.screen.blit(waves_cleared_text, (self.width//2 - waves_cleared_text.get_width()//2, self.height//2 + 10))

            prompt2 = font_small.render("Press any button to Restart", True, self.colors["white"])
            self.screen.blit(prompt2, (self.width//2 - prompt2.get_width()//2, self.height//2 + 40))

            pygame.display.flip()
            self.clock.tick(self.fps)
