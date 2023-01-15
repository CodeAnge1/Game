import time
import pygame
import random
import sys
import os
from settings import *
from debug import debug
from debug import font


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Pickaxe(pygame.sprite.Sprite):
    def __init__(self, pos, sheets, columns, rows, x, y):
        super().__init__()
        self.frames_pickaxe_attack_right = []
        self.frames_pickaxe_attack_left = []
        self.cut_sheet(self.frames_pickaxe_attack_left, sheets[0], columns, rows)
        self.cut_sheet(self.frames_pickaxe_attack_right, sheets[1], columns, rows)
        self.cur_frame = 0
        self.image = self.frames_pickaxe_attack_left[self.cur_frame]
        self.rect = self.rect.move(pos)
        self.display_surface = pygame.display.get_surface()
        self.direction = pygame.math.Vector2()
        self.hitbox = self.rect.inflate(-28, -16)
        self.speed = 5
        self.side = "left"

    def cut_sheet(self, group, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                group.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def change_direction(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        if keys[pygame.K_a]:
            self.direction.x = -1
            self.side = "left"
            self.image = self.frames_pickaxe_attack_left[self.cur_frame]
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.side = "right"
            self.image = self.frames_pickaxe_attack_right[self.cur_frame]
        else:
            self.direction.x = 0

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames_pickaxe_attack_left)
        if self.side == "left":
            self.image = self.frames_pickaxe_attack_left[self.cur_frame]
        if self.side == "right":
            self.image = self.frames_pickaxe_attack_right[self.cur_frame]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def movement(self):
        self.change_direction()


class Resource(pygame.sprite.Sprite):

    def __init__(self, pos, groups, columns, rows, image_name, resource_hp):
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()
        self.hp = resource_hp
        self.frames = []
        self.cut_sheet(load_image(image_name), columns, rows)
        self.cur_frame = 0

        self.image = self.frames[self.cur_frame]

        self.pos = pos
        self.rect = self.image.get_rect(topleft=(self.pos[0] * TILE_SIZE, self.pos[1] * TILE_SIZE - 25))
        self.rect = self.rect.inflate(-32, -32)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def get_damage(self):
        if 0 < self.hp < 5:
            self.cur_frame += 1
            self.image = self.frames[self.cur_frame]
        else:
            game.resources.remove(self)
            game.level.visible_sprites.remove(self)
            game.level.obstacle_sprites.remove(self)
            game.level.impossible_positions.remove((self.pos[1], self.pos[0]))
            game.level.possible_positions.append((self.pos[1], self.pos[0]))


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, groups, obstacles_sprites, sheets, columns, rows, x, y):
        super().__init__(groups)
        self.frames_right_with_pickaxe = []
        self.frames_left_with_pickaxe = []
        self.frames_right_without_pickaxe = []
        self.frames_left_without_pickaxe = []
        self.cut_sheet(self.frames_left_with_pickaxe, sheets[0], columns, rows)
        self.cut_sheet(self.frames_right_with_pickaxe, sheets[1], columns, rows)
        self.cut_sheet(self.frames_left_without_pickaxe, sheets[2], columns, rows)
        self.cut_sheet(self.frames_right_without_pickaxe, sheets[3], columns, rows)
        self.cur_frame = 0
        self.image = self.frames_left_with_pickaxe[self.cur_frame]
        self.rect = self.rect.move(pos)
        self.display_surface = pygame.display.get_surface()
        self.direction = pygame.math.Vector2()
        self.hitbox = self.rect.inflate(-28, -16)
        self.speed = 5
        self.obstacles_sprite = obstacles_sprites
        self.side = "left"
        self.is_attack = False

    def cut_sheet(self, group, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                group.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def attack(self, mouse_pos):
        self.is_attack = True
        # print("mouse:", mouse_pos)
        # print("offset:", game.level.visible_sprites.offset)
        # print("player_pos:", game.level.player.get_pos())
        # print(game.attack_count)
        for resource in game.resources:
            if (resource.rect.x < (mouse_pos[0] + game.level.visible_sprites.offset.x) < resource.rect.x + 64) and \
                    (resource.rect.y < (mouse_pos[1] + game.level.visible_sprites.offset.y) < resource.rect.y + 64):
                resource.hp -= 1
                resource.get_damage()
                break
        # print()

    def change_direction(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        if keys[pygame.K_a]:
            self.direction.x = -1
            self.side = "left"
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.side = "right"
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect = self.hitbox

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacles_sprite:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
        if direction == 'vertical':
            for sprite in self.obstacles_sprite:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top

    def get_pos(self):
        return self.rect.x, self.rect.y

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames_left_with_pickaxe)
        if self.side == "left":
            if self.is_attack:
                self.image = self.frames_left_without_pickaxe[self.cur_frame]
            else:
                self.image = self.frames_left_with_pickaxe[self.cur_frame]
        if self.side == "right":
            if self.is_attack:
                self.image = self.frames_right_without_pickaxe[self.cur_frame]
            else:
                self.image = self.frames_right_with_pickaxe[self.cur_frame]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def movement(self):
        self.change_direction()
        self.move(self.speed)


class Tile(pygame.sprite.Sprite):

    def __init__(self, pos, groups, tile_name):
        super().__init__(groups)
        if tile_name:
            self.image = load_image(tile_name)
            self.rect = self.image.get_rect(topleft=pos)
        else:
            self.rect = pygame.rect.Rect((pos[0] - 12, pos[1], TILE_SIZE, TILE_SIZE))


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = CameraMovement()
        self.ground_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.possible_positions = []
        self.impossible_positions = []
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(MAP):
            for col_index, col in enumerate(row):
                x, y = col_index * TILE_SIZE, row_index * TILE_SIZE
                if col == ' ':
                    self.possible_positions.append((row_index, col_index))
                if col == 'x':
                    Tile((x, y - TILE_SIZE // 2), [self.obstacle_sprites], None)
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, [load_image("animation/marshmallow_left_idle_with_pickaxe.png"), load_image("animation/marshmallow_right_idle_with_pickaxe.png"), load_image("animation/marshmallow_left_idle_without_pickaxe.png"), load_image("animation/marshmallow_right_idle_without_pickaxe.png")], 8, 5, 64, 64)
                    self.pickaxe = Pickaxe((x + 174, y - 122), [load_image("animation/pickaxe_attack_left.png"), load_image("animation/pickaxe_attack_right.png")], 7, 6, 64, 64)

    def run(self):
        self.visible_sprites.update()
        self.visible_sprites.draw(self.player)
        self.player.movement()
        self.pickaxe.movement()
        if self.player.is_attack:
            self.pickaxe.update()
            self.pickaxe.draw(self.display_surface)


class CameraMovement(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

        self.floor_surf = load_image("static_images/first_island.png").convert()
        self.floor_rect = self.floor_surf.get_rect()

    def draw(self, player):
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            self.offset.x = player.rect.centerx - self.display_surface.get_width() // 2
            self.offset.y = player.rect.centery - self.display_surface.get_height() // 2

            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)


class Game:
    def __init__(self):
        self.game_is_started = False
        self.game_is_paused = False
        pygame.init()
        size = WIDTH, HEIGHT
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Game_name")
        self.running = True
        self.clock = pygame.time.Clock()
        self.pickaxe_attack_animation = False
        self.anim_is_end = True
        self.is_up = True
        self.attack_count = 0
        self.mouse_pos = ()
        self.resources = []
        self.level = Level()
        for i in range(2):
            pos = random.choice(self.level.possible_positions)
            self.level.impossible_positions.append(pos)
            self.level.possible_positions.remove(pos)
            ore = Resource((pos[1], pos[0]), [self.level.visible_sprites, self.level.obstacle_sprites], 5, 1, "static_images/iron_ore.png", 5)
            self.resources.append(ore)

    def run(self):
        while self.running:
            self.screen.fill(COLORS["background"])
            if self.game_is_started:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.is_up = False
                        self.pickaxe_attack_animation = True
                        if self.anim_is_end and self.pickaxe_attack_animation:
                            self.level.player.attack(event.pos)
                        self.attack_count = 1
                        self.anim_is_end = False
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        self.is_up = True
                        self.attack_count = 0
                        self.pickaxe_attack_animation = False
                    if event.type == pygame.MOUSEMOTION:
                        self.mouse_pos = event.pos

                self.level.run()
                self.clock.tick(60)
                if self.level.pickaxe.frames_pickaxe_attack_left[-1] == self.level.pickaxe.image or self.level.pickaxe.frames_pickaxe_attack_right[-1] == self.level.pickaxe.image:
                    self.anim_is_end = True
                    self.pickaxe_attack_animation = False
                    self.level.player.is_attack = False
            else:
                menu = Menu(["game_menu/background.png", "game_menu/start_btn.png", "game_menu/exit_btn.png"])
                menu.draw()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        menu.update(event.pos)
            pygame.display.flip()
        pygame.quit()


class Menu:
    def __init__(self, image_names):
        self.display_surface = pygame.display.get_surface()

        self.back_image = load_image(image_names[0])
        self.back_rect = self.back_image.get_rect()

        self.btn_start_image = load_image(image_names[1])
        self.btn_start_rect = self.btn_start_image.get_rect(topleft=(WIDTH // 2 - 205, HEIGHT // 2 - 153))

        self.btn_exit_image = load_image(image_names[2])
        self.btn_exit_rect = self.btn_start_image.get_rect(topleft=(WIDTH // 2 - 100, HEIGHT - 250))

    def start_game(self):
        game.game_is_started = True

    def exit_game(self):
        sys.exit()

    def draw(self):
        self.display_surface.blit(self.back_image, self.back_rect)
        self.display_surface.blit(self.btn_start_image, self.btn_start_rect)
        self.display_surface.blit(self.btn_exit_image, self.btn_exit_rect)

    def update(self, pos):
        if (self.btn_start_rect[0] < pos[0] < self.btn_start_rect[0] + self.btn_start_rect[2]) and \
                (self.btn_start_rect[1] < pos[1] < self.btn_start_rect[1] + self.btn_start_rect[3]):
            self.start_game()
        elif (self.btn_exit_rect[0] < pos[0] < self.btn_exit_rect[0] + self.btn_exit_rect[2]) and \
                (self.btn_exit_rect[1] < pos[1] < self.btn_exit_rect[1] + self.btn_exit_rect[3]):
            self.exit_game()


if __name__ == "__main__":
    game = Game()
    game.run()
