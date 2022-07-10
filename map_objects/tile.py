class Tile:
    '''
    Tile on the map. May be blocked or block sight
    '''
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked
        self.explored = False

        #by default if tile is blocked, it blocks sight
        if block_sight is None:
            block_sight = blocked
        
        self.block_sight = block_sight