
import tcod as libtcod
from random import randint
from components.fighter import Fighter
from components.ai import BasicMonster
from components.item import Item
from entity import Entity
from items_functions import heal


from map_objects.tile import Tile
from map_objects.rectangle import Rect
from render_functions import RenderOrder

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.intialize_tiles()

    def intialize_tiles(self):
        #iterating list over a list(mapping) to get tiles = false
        tiles = [[Tile(True) for y in range (self.height)]  for x in range(self.width)]
        return tiles
    
    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room, max_items_per_room):        
        #creates the map
        rooms = []
        num_rooms = 0
        
        for r in range(max_rooms):
            #random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            #random positioning for room without exceeding the boundaries of map
            #minus one as last digit is exclusive
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            #create rect rooms
            new_room = Rect(x, y, w, h)

            #check if other rooms intersects with new room
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            
            else:
                # this means there are no intersections, so this room is valid
                # place them to the map's tiles
                self.create_room(new_room)

                # center coordinates of new room
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                # this is the first room, where the player starts at
                    player.x = new_x
                    player.y = new_y
                    
                else:
                    #all rooms after the first will be connect to the previous room with a tunnel
                        
                    #center coord of prev rooms
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    #randomize the flow of tunnel whether start horizontal or vert.
                    if randint(0,1) == 1:
                        #move HORIZONtal then vert
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                        
                    else:
                        #move vert then horizontal
                        self.create_v_tunnel(prev_y,new_y,prev_x)
                        self.create_h_tunnel(prev_x,new_x,new_y)
                
                self.place_entities(new_room, entities, max_monsters_per_room, max_items_per_room)
                
                rooms.append(new_room)
                num_rooms += 1
    
    def create_room(self, room): #function to iterate list to create map
        # go through the tiles in the rectangle and make them passable
        #* the reason for adding 1 to x1 and y1 is so that the original value b4 adding is a wall
        # the reason we dont subtract 1 to act as wall from x2 and y2 as python range excludes final value alrdy
        for x in range(room.x1 +1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight =  False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1,x2), max(x1,x2) + 1):
            #add one because last digit is exclusive but for this case needs to be included
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False
    
    #algo for vetical tunnels
    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1,y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    #ensure they are blocked
    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False

    #to place enemies in the map
    def place_entities(self, room, entities, max_monsters_per_room, max_items_per_room):
        #will create a random generated number of monsters in a room so as to not feel repetitive
        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        for i in range(number_of_monsters):
            #randomise room location to put the monsters in
            #take note that x1 and x2 is from rect class 
            x = randint(room.x1 +1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0,100) < 80:
                    fighter_component = Fighter(hp=10, defense=0, power=3)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'O', libtcod.desaturated_green, 'ORC', blocks=True, fighter=fighter_component, ai=ai_component, render_order=RenderOrder.ACTOR)
                else:
                    fighter_component = Fighter(hp = 16, defense=1 ,power=4)
                    ai_component = BasicMonster()
                    
                    monster = Entity(x, y, 'T', libtcod.darker_green, 'Troll', blocks=True, fighter=fighter_component, ai=ai_component, render_order=RenderOrder.ACTOR)
            
                entities.append(monster)
        
        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 -1)
            y = randint(room.y1 +1, room.y2 -1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_component = Item(use_function=heal, amount = 4)
                item = Entity(x, y, "!", libtcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM, item=item_component)

                entities.append(item)





