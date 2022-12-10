class Player():
    playerId = int
    q = int
    r = int
    maxHealth = int
    health = int
    power = int
    level = int
    kills = int
    deaths =  int
    score = int
    trapped = bool
    trapDuration = int
    kd = float
    experience = int

    def __init__(self):
        self.maxHealth = 1000
        self.health = self.maxHealth
        self.level = 1
        self.power = 150
        self.kills = 0
        self.deaths = 0
        self.score = 0
        self.trapped = False
        self.trapDuration = 0
        self.kd = 0
        self.experience = 0

    def gainExperience(self, exp) -> None:
        self.experience += exp
        if(self.experience >= 1000 and self.level < 5):
            self.experience -= 1000
            self.power += 50
            self.level += 1
            self.maxHealth += 300
            self.health = self.maxHealth

    def illegalMove(self):
        self.takeDamage(self.maxHealth/10)

    def regenHealth(self):
        self.health += 100

    def takeDamage(self, dmg) -> bool: # Returns if the player survived the attack
        self.health -= dmg
        if(self.health <= 0):
            self.health = self.maxHealth
            return False
        return True

    def getStuck(self):
        self.trapDuration = 2
        self.trapped = True