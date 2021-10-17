import pygame, os
from pygame.locals import *

from .drops import Drop
from scripts.UI.text import Text
from scripts.data.json_functions import load_json

class Inventory:
    inv_length = 10
    equip_length = 2
    inv = True
    eq = False
    inv_index = 0
    eq_index = 0
        
    def __init__(self, resol, player, inv_img, equipment_imgs):
        self.resol = resol
        self.player = player
        self.inv_img = inv_img
        self.equipment_imgs = equipment_imgs

        #self.inv_text = Text(0, 0, "Inventory", os.path.join("assets", "Fonts", "DefaultFont.TTF"), 24, (255,255,255))
        #self.eq_text = Text(0, 0, "Equipment", os.path.join("assets", "Fonts", "DefaultFont.TTF"), 24, (255,255,255))
        self.quant_texts = [Text(0, 0, "0", os.path.join("assets", "Fonts", "DefaultFont.TTF"), 16, (255,255,255)) for _ in range(self.inv_length)]
        #self.quant_texts = [Text(0, 0, "0", os.path.join("assets", "Fonts", "Font.png"), (255,255,255)) for _ in range(self.inv_length)]
        
        self.update_slots()
        
    def draw_inventory(self, win, screen_size):
        if self.inv:
            win.blit(self.inv_surf, (screen_size[0]-self.inv_surf.get_width()-10, 10))

            if self.inv_index <= 4:
                pygame.draw.rect(win, (0,0,0), ((screen_size[0]-self.inv_surf.get_width()-10)+(self.inv_index*60), 10, 54, 54),3)
            else:
                if self.resol:
                    if round((self.resol[0]/self.resol[1])*100) <= 133:
                        pygame.draw.rect(win, (0,0,0), ((screen_size[0]-self.inv_surf.get_width()-10)+((self.inv_index-5)*60), 70, 54, 54), 3)
                    else:
                        pygame.draw.rect(win, (0,0,0), ((screen_size[0]-self.inv_surf.get_width()-10)+(self.inv_index*60), 10, 54, 54), 3)
                else:
                    pygame.draw.rect(win, (0,0,0), ((screen_size[0]-self.inv_surf.get_width()-10)+(self.inv_index*60), 10, 54, 54), 3)
        else:
            if len(self.player.equipment) == 2:
                offset = 90
            else:
                offset = 60
            win.blit(self.eq_surf, ((screen_size[0]-self.inv_surf.get_width()-10+offset), 10))

            pygame.draw.rect(win, (0,0,0), ((screen_size[0]-self.inv_surf.get_width()-10+offset)+(self.eq_index*60), 10, 54, 54),3)

    def update_slots(self):
        if self.resol:
            if round((self.resol[0]/self.resol[1])*100) <= 133:
                self.inv_surf = pygame.Surface((53*(int(len(self.player.inventory)*0.5))+10*(int(len(self.player.inventory)*0.5)-1), 53*(int(len(self.player.inventory)*0.2))+10*(int(len(self.player.inventory)*0.2)-1)), SRCALPHA)
            else:
                self.inv_surf = pygame.Surface((53*len(self.player.inventory)+10*(len(self.player.inventory)-1), 53), SRCALPHA)
        else:
            self.inv_surf = pygame.Surface((53*len(self.player.inventory)+10*(len(self.player.inventory)-1), 53), SRCALPHA)
        self.eq_surf = pygame.Surface((53*len(self.player.equipment)+10*(len(self.player.equipment)-1), 53), SRCALPHA)

        #self.inv_surf.set_colorkey((0,0,0))
        #self.eq_surf.set_colorkey((0,0,0))

        y = 0
        x = 0
        no = 0
        item_x = 3
        item_y =  3
        quant_x = 48
        quant_y = 38
        text_i = 0
        for i in self.player.inventory:
            self.inv_surf.blit(self.inv_img, (x, y))
            if len(i) > 0:
                self.inv_surf.blit(self.equipment_imgs[i[0]], (item_x, item_y))
                if i[1] != 1:
                    self.quant_texts[text_i].text = str(i[1])
                    self.quant_texts[text_i].x = quant_x-self.quant_texts[text_i].get_width()
                    self.quant_texts[text_i].y = 10+quant_y-self.quant_texts[text_i].get_height()

                    self.quant_texts[text_i].render(self.inv_surf)

            item_x += 60
            quant_x += 60
            x += 60
            no += 1
            text_i += 1

            if self.resol:
                if round((self.resol[0]/self.resol[1])*100) <= 133 and no >= 5:
                    x = 0
                    y += 60
                    item_y += 60
                    item_x = 3
                    no = 0


        x = 0
        item_x = 3
        item_y = 3
        for item in self.player.equipment:
            self.eq_surf.blit(self.inv_img, (x, 0))
            self.eq_surf.blit(self.equipment_imgs[item], (item_x, item_y))
            
            x += 60
            item_x += 60

    def select_item(self, event):
        if self.inv:
            if event.type == KEYDOWN:
                if event.key >= K_0 and event.key <= K_9:
                    self.inv_index = event.key - K_1
                    if event.key == K_0:
                        self.inv_index = 9
                
                if event.key >= K_KP_1 and event.key <= K_KP_0:
                    self.inv_index = event.key - K_KP_1

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    if not self.inv_index <= 0:
                        self.inv_index -= 1
                    else:
                        self.inv_index = 9
                if event.button == 5:
                    if not self.inv_index >= 9:
                        self.inv_index += 1
                    else:
                        self.inv_index = 0
        else:
            if len(self.player.equipment) < 3:
                if event.type == KEYDOWN:
                    if event.key >= K_1 and event.key <= K_2:
                        self.eq_index = event.key - K_1
                    
                    if event.key >= K_KP_1 and event.key <= K_KP_2:
                        self.eq_index = event.key - K_KP_1

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 4:
                        if not self.eq_index <= 0:
                            self.eq_index -= 1
                        else:
                            self.eq_index = 1
                    if event.button == 5:
                        if not self.eq_index >= 1:
                            self.eq_index += 1
                        else:
                            self.eq_index = 0
            else:
                if event.type == KEYDOWN:
                    if event.key >= K_1 and event.key <= K_3:
                        self.eq_index = event.key - K_1
                    
                    if event.key >= K_KP_1 and event.key <= K_KP_3:
                        self.eq_index = event.key - K_KP_1

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 4:
                        if not self.eq_index <= 0:
                            self.eq_index -= 1
                        else:
                            self.eq_index = 2
                    if event.button == 5:
                        if not self.eq_index >= 2:
                            self.eq_index += 1
                        else:
                            self.eq_index = 0

    def equip_item(self, player_loc):
        d = None
        if self.inv:
            self.inv = False

            equipment = load_json(["scripts", "data", "equipment.json"])

            if len(self.player.inventory[self.inv_index]) > 0:
                item = self.player.inventory[self.inv_index][0]
            else:
                self.inv = True
                return

            if item in equipment[0].keys():
                ind = 0
            elif item in equipment[1].keys():
                ind = 1
            else:
                self.inv = True
                return


            l = list(equipment[ind].keys())

            if not item in self.player.equipment:
                if ind == 0:
                    if equipment[0][item]["Class"] not in self.player.Pclass:
                        self.inv = True
                        return
                    else:
                        if self.player.Pclass[0] == equipment[0][item]["Class"]:
                            s = 0
                        elif self.player.Pclass[1] == equipment[0][item]["Class"]:
                            s = 1
                elif ind == 1:
                    if len(self.player.equipment) < 3:
                        s = 1
                    else:
                        s = 2

                if self.player.inventory[self.inv_index][1] > 1:
                    self.player.inventory[self.inv_index][1] -= 1
                else:
                    self.player.inventory[self.inv_index] = []

                if self.player.equipment[s] != "Fist" and self.player.equipment[s] != "No Shield":
                    x = False
                    for i, stuff in enumerate(self.player.inventory):
                        if len(self.player.inventory[i]) and self.player.inventory[i][0] == self.player.equipment[s]:
                            self.player.inventory[i][1] += 1
                            x = True
                            break
                        elif self.player.inventory[i] == []:
                            self.player.inventory[i] = [self.player.equipment[s], 1]
                            x = True
                            break
                    if not x:
                        d = [item, Drop(player_loc[0], player_loc[1], self.equipment_imgs[item]), 3*60]
                del self.player.equipment[s]
                self.player.equipment.insert(s, item)

                if ind == 0:
                    self.player.stats["Attack"][s] = equipment[0][item]["AP"]
                else:
                    self.player.stats["Defense"] = equipment[1][item]["DP"]

                self.update_slots()
                self.player.generate_bars()
            else:
                self.inv = True
                return
        else:
            if self.player.equipment[self.eq_index] != "Fist" and self.player.equipment[self.eq_index] != "No Shield":
                x = False
                for i, item in enumerate(self.player.inventory):
                    if len(item) > 0 and self.player.equipment[self.eq_index] == item[0]:
                        self.player.inventory[i][1] += 1
                        x = True
                        break
                if not x:
                    for i, slot in enumerate(self.player.inventory):
                        if slot == []:
                            self.player.inventory[i] = [self.player.equipment[self.eq_index], 1]
                            x = True
                            break
                    if not x:
                        d = [item, Drop(player_loc[0], player_loc[1], self.equipment_imgs[item]), 3*60]

                del self.player.equipment[self.eq_index]
                if self.eq_index == 0:
                    self.player.equipment.insert(0, "Fist")
                    self.player.stats["Attack"][self.eq_index] = 1
                else:
                    if len(self.player.equipment) < 2:
                        self.player.equipment.insert(1, "No Shield")
                        self.player.stats["Defense"] = 0
                    else:
                        if self.eq_index == 1:
                            self.player.equipment.insert(1, "Fist")
                            self.player.stats["Attack"][self.eq_index] = 1
                        else:
                            self.player.equipment.insert(2, "No Shield")
                            self.player.stats["Defense"] = 0
                    
                self.update_slots()
                self.player.generate_bars()
                self.inv = True

        return d
    
    def throw_item(self, player_loc):
        item = None
        if self.inv:
            item = self.player.inventory[self.inv_index]
            
            if len(item) > 0:
                if item[1] > 1:
                    self.player.inventory[self.inv_index][1] -= 1
                else:
                    self.player.inventory[self.inv_index] = []

                self.update_slots()
                return [item[0], Drop(player_loc[0], player_loc[1], self.equipment_imgs[item[0]]), 3*60]
        else:
            if self.player.equipment[self.eq_index] != "Fist" and self.player.equipment[self.eq_index] != "No Shield":
                item = self.player.equipment[self.eq_index]
                del self.player.equipment[self.eq_index]
                if self.eq_index == 0:
                    self.player.equipment.insert(0, "Fist")
                    self.player.stats["Attack"][self.eq_index] = 1
                else:
                    if len(self.player.equipment) < 2:
                        self.player.equipment.insert(1, "No Shield")
                        self.player.stats["Defense"] = 0
                    else:
                        if self.eq_index == 1:
                            self.player.equipment.insert(1, "Fist")
                            self.player.stats["Attack"][self.eq_index] = 1
                        else:
                            self.player.equipment.insert(2, "No Shield")
                            self.player.stats["Defense"] = 0

                self.update_slots()
                self.player.generate_bars()
                if item: return [item, Drop(player_loc[0], player_loc[1], self.equipment_imgs[item]), 3*60]

    def grab_item(self, item, quantity=1):
        for i, slot in enumerate(self.player.inventory):
            if len(slot) == 0:
                self.player.inventory[i] = [item, quantity]
                self.update_slots()
                return True
            else:
                if slot[0] == item:
                    items = load_json(["scripts", "data", "items.json"])
                    if self.player.inventory[i][1] < items[item]["stack"]:
                        self.player.inventory[i][1] += quantity
                        self.update_slots()
                        return True
