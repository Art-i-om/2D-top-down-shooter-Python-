import random
import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()

        self.shoot_sounds = [
            pygame.mixer.Sound("assets/sounds/shoot_bullet/laserSmall_000.ogg"),
            pygame.mixer.Sound("assets/sounds/shoot_bullet/laserSmall_001.ogg"),
            pygame.mixer.Sound("assets/sounds/shoot_bullet/laserSmall_002.ogg"),
            pygame.mixer.Sound("assets/sounds/shoot_bullet/laserSmall_003.ogg"),
            pygame.mixer.Sound("assets/sounds/shoot_bullet/laserSmall_004.ogg")
        ]

        self.explosion_sounds = [
            pygame.mixer.Sound("assets/sounds/explosion/explosionCrunch_000.ogg"),
            pygame.mixer.Sound("assets/sounds/explosion/explosionCrunch_001.ogg"),
            pygame.mixer.Sound("assets/sounds/explosion/explosionCrunch_003.ogg"),
            pygame.mixer.Sound("assets/sounds/explosion/explosionCrunch_004.ogg")
        ]

        # pygame.mixer.music.load("assets/sounds/music/spaceEngineLow_001.ogg")
        # pygame.mixer.music.set_volume(0.2)

    def play_shoot(self):
        shoot_sound: pygame.mixer.Sound = random.choice(self.shoot_sounds)
        shoot_sound.play()

    def play_explosion(self):
        explosion_sound: pygame.mixer.Sound = random.choice(self.explosion_sounds)
        explosion_sound.play()

    @staticmethod
    def play_music():
        pygame.mixer.music.play(-1)

    @staticmethod
    def stop_music():
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        all_sounds = self.shoot_sounds + self.explosion_sounds
        for s in all_sounds:
            s.set_volume(volume)

    @staticmethod
    def mute():
        pygame.mixer.pause()

    @staticmethod
    def unmute():
        pygame.mixer.unpause()
