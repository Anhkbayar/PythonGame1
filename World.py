from Player import Character
from Healthbar import healthbar
from ItemBox import itembox, decoration, exit, spike

class world():
    def __init__(self):
        self.obstacle_list = []
        
    def process_data(self, data, img_list, tilesize, enemy_group, item_box_group, item_boxes, decs_group, exit_group, spike_group):
        self.level_len = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * tilesize
                    img_rect.y = y * tilesize
                    tile_data = (img, img_rect)
                    if tile == 0:
                        player = Character('Player', x*tilesize, y*tilesize, 2, 4, 10)
                        health_bar = healthbar(10, 10, player.health, player.health )
                    elif tile == 1:
                        enemy = Character('Enemy', x*tilesize, y*tilesize, 2, 2, 30)
                        enemy_group.add(enemy)
                    elif tile >= 2 and tile <= 4:
                        decs = decoration(img, x*tilesize, y*tilesize, tilesize)
                        decs_group.add(decs)   
                    elif tile == 5: 
                        exits = exit(img, x*tilesize, y*tilesize, tilesize)
                        exit_group.add(exits)   
                    elif tile == 6:
                        item_box = itembox('Health', x*tilesize, y*tilesize, item_boxes, tilesize)
                        item_box_group.add(item_box)   
                    elif tile == 7:
                        item_box =  itembox('Rock', x*tilesize, y*tilesize, item_boxes, tilesize)
                        item_box_group.add(item_box)
                    elif tile == 8:
                        spikes = spike(img, x*tilesize, y*tilesize, tilesize)
                        spike_group.add(spikes)                    
                    elif tile >=9 and tile <= 17:
                        self.obstacle_list.append(tile_data)
    
        return player, health_bar
    
    def draw(self, screen, screen_scroll):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
