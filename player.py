import pygame
from settings import *
from support import *
from timer import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.import_assests()
        self.status = "down_idle"
        self.frame_index = 0

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        self.timers = {"tool use": Timer(350, self.use_tool)}

        self.selected_tool = "axe"

    def use_tool(self):
        print(self.selected_tool)

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timers["tool use"].active:
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = "left"
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = "right"
            else:
                self.direction.x = 0

            if keys[pygame.K_SPACE]:
                self.timers["tool use"].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0
            
            if keys[pygame.K_1]:
                self.selected_tool = "water"

            if keys[pygame.K_2]:
                self.selected_tool = "axe"

            if keys[pygame.K_3]:
                self.selected_tool = "hoe"

    def import_assests(self):
        self.animations = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
            "up_idle": [],
            "down_idle": [],
            "left_idle": [],
            "right_idle": [],
            "up_hoe": [],
            "down_hoe": [],
            "left_hoe": [],
            "right_hoe": [],
            "up_axe": [],
            "down_axe": [],
            "left_axe": [],
            "right_axe": [],
            "up_water": [],
            "down_water": [],
            "left_water": [],
            "right_water": [],
        }

        for animation in self.animations.keys():
            full_path = "../Scufed_StarDoo/character/" + animation
            self.animations[animation] = import_folder(full_path)
        print(self.animations)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split("_")[0] + "_idle"
            if self.timers["tool use"].active:
                print("tool is being used")
                self.status = self.status.split("_")[0] + "_" + self.selected_tool

    def update_timer(self):
        for timer in self.timers.values():
            timer.update()

    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        # print(self.direction)
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timer()
        self.move(dt)
        self.animate(dt)
