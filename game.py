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

    def __init__(self, pos, groups, columns, rows, image_name, resource_hp, resource_name):
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()
        self.hp = resource_hp
        self.frames = []
        self.cut_sheet(load_image(image_name), columns, rows)
        self.cur_frame = 0
        self.resource_name = resource_name

        self.image = self.frames[self.cur_frame]

        self.pos = pos
        if self.resource_name == "tree":
            self.rect = pygame.rect.Rect(self.pos[0] * TILE_SIZE - 20, self.pos[1] * TILE_SIZE - 100, 64, 128)
        else:
            self.rect = self.image.get_rect(topleft=(self.pos[0] * TILE_SIZE, self.pos[1] * TILE_SIZE - 25))
            self.rect = self.image.get_rect(topleft=(self.pos[0] * TILE_SIZE, self.pos[1] * TILE_SIZE - 25))
            self.rect = self.rect.inflate(-32, -20)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def get_damage(self):
        if 0 < self.hp:
            self.cur_frame += 1
            self.image = self.frames[self.cur_frame]
        else:
            game.resources.remove(self)
            game.level.visible_sprites.remove(self)
            game.level.obstacle_sprites.remove(self)
            game.level.impossible_positions.remove((self.pos[1], self.pos[0]))
            game.level.possible_positions.append((self.pos[1], self.pos[0]))
            game.inventory.append_item(self.resource_name, random.randint(1, 2))


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, groups, obstacles_sprites, sheets, columns, rows, x, y):
        super().__init__(groups)
        self.money_count = 0
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
        for resource in game.resources:
            if resource.resource_name == "tree":
                if (resource.rect.x < (mouse_pos[0] + game.level.visible_sprites.offset.x) < resource.rect.x + 64) and \
                        (resource.rect.y < (
                                mouse_pos[1] + game.level.visible_sprites.offset.y) < resource.rect.y + 128):
                    resource.hp -= 1
                    resource.get_damage()
                    break
            else:
                if (resource.rect.x < (mouse_pos[0] + game.level.visible_sprites.offset.x) < resource.rect.x + 64) and \
                        (resource.rect.y < (mouse_pos[1] + game.level.visible_sprites.offset.y) < resource.rect.y + 64):
                    resource.hp -= 1
                    resource.get_damage()
                    break

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
        self.money_img = load_image("game_menu/money_image.png")
        self.money_rect = self.money_img.get_rect(topleft=(5, HEIGHT - 80))
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
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites,
                                         [load_image("animation/marshmallow_left_idle_with_pickaxe.png"),
                                          load_image("animation/marshmallow_right_idle_with_pickaxe.png"),
                                          load_image("animation/marshmallow_left_idle_without_pickaxe.png"),
                                          load_image("animation/marshmallow_right_idle_without_pickaxe.png")], 8, 5, 64,
                                         64)
                    self.pickaxe = Pickaxe((x + 174, y - 122), [load_image("animation/pickaxe_attack_left.png"),
                                                                load_image("animation/pickaxe_attack_right.png")], 7, 6,
                                           64, 64)

    def add_new_space(self, level_name):
        self.possible_positions.clear()
        for i in self.obstacle_sprites:
            if str(i) == "<Tile Sprite(in 1 groups)>":
                self.obstacle_sprites.remove(i)
        for row_index, row in enumerate(level_name):
            for col_index, col in enumerate(row):
                x, y = col_index * TILE_SIZE, row_index * TILE_SIZE
                if col == ' ':
                    self.possible_positions.append((row_index, col_index))
                if col == 'x':
                    Tile((x, y - TILE_SIZE // 2), [self.obstacle_sprites], None)
        for i in self.impossible_positions:
            self.possible_positions.remove(i)

    def run(self):
        self.visible_sprites.update()
        self.visible_sprites.draw(self.player)
        self.player.movement()
        self.pickaxe.movement()
        if self.player.is_attack:
            self.pickaxe.update()
            self.pickaxe.draw(self.display_surface)
        self.money_count_text = font.render(str(self.player.money_count), True, "white")
        self.money_count_rect = self.money_count_text.get_rect(topleft=(75, HEIGHT - 53))
        self.display_surface.blit(self.money_count_text, self.money_count_rect)
        self.display_surface.blit(self.money_img, self.money_rect)


class CameraMovement(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

        self.floor_surf = load_image("islands/first_island.png").convert()
        self.floor_rect = self.floor_surf.get_rect()
        self.floor_surf_island_2 = load_image("islands/second_island.png").convert()
        self.floor_rect_island_2 = self.floor_surf.get_rect(topleft=(-832, -768))

    def draw(self, player):
        if game.buy.islands_count == 1:
            floor_offset_pos = self.floor_rect.topleft - self.offset
            self.display_surface.blit(self.floor_surf, floor_offset_pos)
        if game.buy.islands_count == 2:
            floor_offset_pos = self.floor_rect_island_2.topleft - self.offset
            self.display_surface.blit(self.floor_surf_island_2, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            self.offset.x = player.rect.centerx - self.display_surface.get_width() // 2
            self.offset.y = player.rect.centery - self.display_surface.get_height() // 2

            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)


# class Forge:
#     def __init__(self):
#         pass
#
#
# class Furnace(pygame.sprite.Sprite):
#     def __init__(self, groups):
#         super().__init__(groups)
#         self.display_surface = pygame.display.get_surface()
#         self.image = load_image("buildings\Furnace.png")
#         self.pos = ()
#         self.is_build = False
#         self.rect = pygame.rect.Rect((-100, -100, 0, 0))
#
#     def build(self):
#         if not self.is_build:
#             if game.inventory.item_in_inventory("rock"):
#                 if game.inventory.get_item_count("rock") >= 10:
#                     game.inventory.remove_item("rock", 10)
#                     self.is_build = True
#                     pos = game.mouse_pos[0] // TILE_SIZE, game.mouse_pos[1] // TILE_SIZE
#                     # game.level.possible_positions.remove((self.pos[1], self.pos[0]))
#                     self.pos = pos
#                     self.rect = pygame.rect.Rect(self.pos[0] * TILE_SIZE, self.pos[1] * TILE_SIZE, 45, 45)
#                     self.rect.inflate(20, 10)
#
#     def draw(self):
#         self.display_surface.blit(self.image, self.rect)
#
#
# class BuildMenu:
#     def __init__(self):
#         self.display_surface = pygame.display.get_surface()
#         self.building_image = load_image("game_menu/inventory_image.png")
#         self.building_image_rect = self.building_image.get_rect(topleft=(WIDTH // 2 - 100, 5))
#
#     def draw(self, screen):
#         screen.blit(self.building_image, self.building_image_rect)


class Inventory:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.items = {"rock": 200}
        self.images = {"bush": load_image("resources_images/berry.png"),
                       "coal_ore": load_image("resources_images/coal.png"),
                       "gold_ore": load_image("resources_images/gold_stone.png"),
                       "iron_ore": load_image("resources_images/iron_stone.png"),
                       "rock": load_image("resources_images/stone.png"),
                       "tree": load_image("resources_images/wood.png")}
        self.background_image = load_image("game_menu/inventory_background.png")
        self.background_rect = self.background_image.get_rect(topleft=(WIDTH // 2 - 437, HEIGHT // 2 - 123))
        self.inventory_image = load_image("game_menu/inventory_image.png")
        self.inventory_image_rect = self.inventory_image.get_rect(topleft=(WIDTH // 2 - 100, 5))

    def append_item(self, item_name, item_count):
        if item_name in self.items.keys():
            self.items[item_name] = int(self.items[item_name]) + item_count
        else:
            self.items[item_name] = item_count

    def remove_item(self, item_name, item_count):
        if item_name in self.items.keys():
            self.items[item_name] = int(self.items[item_name]) - item_count
        else:
            return

    def get_item_count(self, item):
        return self.items[item]

    def item_in_inventory(self, item):
        return item in self.items.keys()

    def draw(self, screen):
        if game.inventory_menu:
            screen.blit(self.background_image, self.background_rect)
            self.offset = (104, 0)
            offset = (0, 0)
            counter = 0
            for k in self.items.keys():
                if counter == 9:
                    counter = 0
                    self.offset = (100, 100)
                offset = (self.offset[0] * counter, self.offset[1])
                screen.blit(self.images[k], self.images[k].get_rect(
                    topleft=(((WIDTH // 2 - 415 + offset[0]), HEIGHT // 2 - 85 + offset[1]))))
                count_text = font.render(str(self.items[k]), True, "white")
                count_rect = count_text.get_rect(
                    topleft=((WIDTH // 2 - 415 + offset[0]) + 40, (HEIGHT // 2 - 85 + offset[1]) + 40))
                screen.blit(count_text, count_rect)
                counter += 1


class Game:
    def __init__(self):
        self.game_is_started = False
        self.game_is_paused = False
        self.inventory_menu = False
        self.land_purchase_menu = False
        self.buy_menu = False
        self.sell_menu = False
        self.escape_count = 0
        self.inventory = Inventory()
        self.in_game_menu = InGameMenu()
        self.sell = ItemSell()
        self.buy = LandPurchase()
        # self.build = BuildMenu()
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
        self.resources_list = ["bush.png", "bush.png", "bush.png", "coal_ore.png", "coal_ore.png",
                               "iron_ore.png", "rock.png", "iron_ore.png", "rock.png",
                               "rock.png", "rock.png", "tree.png", "tree.png", "gold_ore.png"]
        self.resource_generate_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.resource_generate_event, 40000)
        self.level = Level()
        pos = random.choice(self.level.possible_positions)
        # self.furnace = Furnace([self.level.visible_sprites, self.level.obstacle_sprites])
        # self.forge = Forge([self.level.visible_sprites, self.level.obstacle_sprites])
        for i in range(random.randint(3, 9)):
            self.resource_generate()

    def resource_generate(self):
        pos = random.choice(self.level.possible_positions)
        self.level.impossible_positions.append(pos)
        self.level.possible_positions.remove(pos)
        resource_file = random.choice(self.resources_list)
        if resource_file == "iron_ore.png":
            res = Resource((pos[1], pos[0]), [self.level.visible_sprites, self.level.obstacle_sprites], 3,
                           3, f"resources_images/{resource_file}", 9, resource_file.split('.')[0])
        elif resource_file == "rock.png":
            res = Resource((pos[1], pos[0]), [self.level.visible_sprites, self.level.obstacle_sprites], 5,
                           1, f"resources_images/{resource_file}", 5, resource_file.split('.')[0])
        elif resource_file == "tree.png":
            res = Resource((pos[1], pos[0]), [self.level.visible_sprites, self.level.obstacle_sprites], 7,
                           1, f"resources_images/{resource_file}", 7, resource_file.split('.')[0])
        elif resource_file == "coal_ore.png":
            res = Resource((pos[1], pos[0]), [self.level.visible_sprites, self.level.obstacle_sprites], 7,
                           1, f"resources_images/{resource_file}", 7, resource_file.split('.')[0])
        elif resource_file == "bush.png":
            res = Resource((pos[1], pos[0]), [self.level.visible_sprites, self.level.obstacle_sprites], 2,
                           1, f"resources_images/{resource_file}", 2, resource_file.split('.')[0])
        elif resource_file == "gold_ore.png":
            res = Resource((pos[1], pos[0]), [self.level.visible_sprites, self.level.obstacle_sprites], 13,
                           1, f"resources_images/{resource_file}", 13, resource_file.split('.')[0])
        self.resources.append(res)

    def run(self):
        while self.running:
            self.screen.fill(COLORS["background"])
            if self.game_is_started:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.game_is_paused = not self.game_is_paused
                            if self.escape_count % 2 == 0:
                                self.inventory_menu = True
                            else:
                                self.inventory_menu = False
                                self.build_menu = False
                                self.land_purchase_menu = False
                            self.escape_count += 1
                    if event.type == pygame.MOUSEMOTION:
                        self.mouse_pos = event.pos
                    if self.game_is_paused:
                        # if self.build_menu:
                        #     # self.furnace.build()
                        # # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        # #     self.inventory_menu = False
                        #     # if (self.build.building_image_rect[0] < self.mouse_pos[0] < self.build.building_image_rect[
                        #     #     0] + self.build.building_image_rect[2]) and \
                        #     #         (self.build.building_image_rect[1] < self.mouse_pos[1] <
                        #     #          self.build.building_image_rect[1] + self.build.building_image_rect[3]):
                        #     #     self.build_menu = True
                        #     #     self.inventory_menu = False
                        #     #     self.land_purchase_menu = False
                        #     if (self.inventory.inventory_image_rect[0] < self.mouse_pos[0] <
                        #         self.inventory.inventory_image_rect[0] + self.inventory.inventory_image_rect[2]) and \
                        #             (self.inventory.inventory_image_rect[1] < self.mouse_pos[1] <
                        #              self.inventory.inventory_image_rect[1] + self.inventory.inventory_image_rect[3]):
                        #         self.build_menu = False
                        #         self.inventory_menu = True
                        #         self.land_purchase_menu = False
                        self.inventory.draw(self.screen)
                        # self.build.draw(self.screen)
                    else:
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            self.is_up = False
                            self.pickaxe_attack_animation = True
                            if self.anim_is_end and self.pickaxe_attack_animation:
                                self.level.player.attack(event.pos)
                            self.attack_count = 1
                            self.anim_is_end = False
                            if self.game_is_paused:
                                self.in_game_menu.update()
                        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            self.is_up = True
                            self.attack_count = 0
                            self.pickaxe_attack_animation = False
                        if event.type == self.resource_generate_event:
                            if self.level.possible_positions:
                                self.resource_generate()

                self.level.run()
                if self.game_is_paused:
                    self.inventory.draw(self.screen)
                    self.in_game_menu.draw(self.screen)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.in_game_menu.update()
                    # self.build.draw(self.screen)
                self.clock.tick(60)
                if self.level.pickaxe.frames_pickaxe_attack_left[-1] == self.level.pickaxe.image or \
                        self.level.pickaxe.frames_pickaxe_attack_right[-1] == self.level.pickaxe.image:
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
            debug(
                f"player_pos = {self.level.player.get_pos()}, offset = {self.level.visible_sprites.offset}, mouse = {self.mouse_pos}")
            pygame.display.flip()
        pygame.quit()


class ItemSell:
    def __init__(self):
        self.image = load_image("game_menu/sell_menu.png")
        self.rect = self.image.get_rect(topleft=(WIDTH // 2 - 32, 5))
        self.prices = {"bush": 3,
                       "coal_ore": 10,
                       "gold_ore": 35,
                       "iron_ore": 25,
                       "rock": 10,
                       "tree": 7}

    def sell_all(self):
        for k, v in game.inventory.items.items():
            game.inventory.items[k] = 0
            game.level.player.money_count += v * self.prices[k]


class LandPurchase:
    def __init__(self):
        self.image = load_image("game_menu/buy_menu.png")
        self.rect = self.image.get_rect(topleft=(WIDTH // 2 + 36, 5))
        self.islands_count = 1
        self.second_island_is_buy = False

    def buy_island(self):
        if not self.second_island_is_buy:
            if game.level.player.money_count >= 100:
                game.level.player.money_count -= 100
                self.islands_count = 2
                game.level.add_new_space(MAP_LEVEL_2)
                self.second_island_is_buy = True


class InGameMenu:
    def __init__(self):
        pass

    def is_inventory(self):
        game.inventory_menu = True

    def is_buy(self):
        game.buy.buy_island()

    def draw(self, screen):
        screen.blit(game.inventory.inventory_image, game.inventory.inventory_image_rect)
        screen.blit(game.sell.image, game.sell.rect)
        screen.blit(game.buy.image, game.buy.rect)

    def update(self):
        if (game.inventory.inventory_image_rect[0] < game.mouse_pos[0] < game.inventory.inventory_image_rect[
                0] + game.inventory.inventory_image_rect[2]) and \
                    (game.inventory.inventory_image_rect[1] < game.mouse_pos[1] <
                     game.inventory.inventory_image_rect[1] + game.inventory.inventory_image_rect[3]):
            self.is_inventory()
        if (game.sell.rect[0] < game.mouse_pos[0] < game.sell.rect[
            0] + game.sell.rect[2]) and \
                (game.sell.rect[1] < game.mouse_pos[1] <
                 game.sell.rect[1] + game.sell.rect[3]):
            game.sell.sell_all()
        if (game.buy.rect[0] < game.mouse_pos[0] < game.buy.rect[
            0] + game.buy.rect[2]) and \
                (game.buy.rect[1] < game.mouse_pos[1] <
                 game.buy.rect[1] + game.buy.rect[3]):
            self.is_buy()


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
