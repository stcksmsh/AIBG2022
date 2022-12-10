class Tile():
    q = int
    r = int
    health = int
    wormHoleId = int
    tileType = 0 # defines type of tile:
    # -2    Asteroid
    # -1    Boss
    #  0    Empty
    #  1    Health
    #  2    Experience
    #  3    Black hole
    #  4    Wormhole
    playerIdx = 0

    def __setitem__(self, key, value):
        print('test')
        return self.__setitem__(self, key+14, value)

    def __getitem__(self, key):
        return self.__getitem__(self, key+14)

    def convertType(s):
        match s:
            case 'WORMHOLE':
                return 4
            case 'BLACKHOLE':
                return 3
            case 'EXPERIENCE':
                return 2
            case 'HEALTH':
                return 1
            case 'EMPTY':
                return 0
            case 'BOSS':
                return -1
            case 'ASTEROID':
                return -2        

    def getDistance(self, t):
        return abs(self.q - t.q) + abs(self.r - t.r)   

    def takeDamage(self, dmg): # Returns true if player destroys an asteroid
        self.health -= dmg
        return self.tileType == -2 and self.health <= 0