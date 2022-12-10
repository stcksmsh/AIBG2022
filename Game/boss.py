from random import randint
class Boss():
    power = int
    patternTwoSize = int # 0, 1 or 2
    patternOnePosition = int# 0, 1 or 2 
    nextPattern = int # 0 or 1, 0 for pattern1, 1 for pattern2
    cooldown = int
    attackedTiles = [
    [[(8, -2), (8, -3), (6, 2), (5, 3), (-5, -3), (-6, -2), (-8, -2), (-8, -3)],
     [(-4, -4,), (-3, -5), (-8, 4), (-8, 5), (4, 4), (3, 5), (8, -5), (8, -4)],
     [(-1, -7), (-2, -6), (-8, -7), (-8, -6), (2, 6), (1, 7)]],
    [[(i, 6-abs(i)) for i in range(-6, 7)] + [(i, -6+abs(i)) for i in range(-6, 7)],
    [(i, 8-abs(i)) for i in range(-8, 9)] + [(i, -8+abs(i)) for i in range(-8, 9)],
    [(i, 10-abs(i)) for i in range(-10, 11)] + [(i, -10+abs(i)) for i in range(-10, 11)]]]
    attackedTilesPatternOne = []

    def Attack(self) -> object:
        self.cooldown -= 1
        if(self.cooldown > 0):
            return []
        res = self.attackedTilesByMove[self.nextPattern][self.patternOnePosition if self.nextPattern == 0 else self.patternTwoSize]     
        self.nextPattern = 1 - self.nextPattern
        if(self.nextPattern == 0 and self.patternOnePosition == 2):
            self.nextPattern == 1
            self.patternOnePosition = 0
            self.cooldown = randint(3, 7)
        elif(self.nextPattern == 0):
            self.patternOnePosition += 1
        else:
            self.nextPattern = 0
            self.patternTwoSize = self.patternTwoSize + 1 if self.patternTwoSize < 2 else 0
        return res