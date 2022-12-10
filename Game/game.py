from tile import Tile
from player import Player
from boss import Boss
import json
from random import randint


class Game():
    players = [Player() for i in range(4)]
    board = [[Tile() for i in range(29)] for j in range(29)]
    boss = Boss()
    currentPlayer = 1
    wormHoleCoordinates = [[] for i in range(100)]
    startCors = [(-7, 7), (14, -7), (-14, 7), (7, 7)]

    def __init__(self):
        f = open('map.json')
        j = json.load(f)
        for tiles in j['gameState']['map']['tiles']:
            for tile in tiles:
                self.board[tile['q']][tile['r']].q, self.board[tile['q']][tile['r']].r = tile['q'], tile['r']
                self.board[tile['q']][tile['r']].tileType = Tile.convertType(tile['entity']['type'])
                self.board[tile['q']][tile['r']].health = 350
                if(self.board[tile['q']][tile['r']].tileType == 4):
                    self.board[tile['q']][tile['r']].wormHoleId = tile['entity']['id']
                    self.wormHoleCoordinates[tile['entity']['id']].append((tile['q'], tile['r']))
        for player in j['gameState']['scoreBoard']['players']:
            idx = player['playerIdx']
            r = player['r']
            q = player['q']
            self.players[idx-1].q, self.players[idx-1].r = (q, r)
            self.players[idx-1].playerId = idx
            self.board[q][r].playerIdx = idx
        
    def distance(self, cors1, cors2):
        q = cors1[0] - cors2[0]
        r = cors1[1] - cors2[1]
        if(q * r < 0):
            return max(abs(q), abs(r))
        else:
            return abs(q) + abs(r)

    def respawnConsumable(self, type):
        while True:
            q = randint(-14, 15)
            r = randint(-14 + abs(q), 15 - abs(q))
            target = self.board[q][r]
            if(target.tileType == 0 and len(target.playerIds) == 0):
                target.tileType = type

    def play(self, move, cors):
        player = self.players[self.currentPlayer-1]
        playerCors = (player.q, player.r)
        if(move == 'move'):
            target = self.board[cors[0]][cors[1]]
            if(player.trapDuration == 0):
                player.trapped = False
            if(player.trapped):
                player.trapDuration -= 1
                return
            if(self.distance(playerCors, cors) <= 1 and
            self.distance(cors, (0,0)) <= 14 and
            (target.tileType >=0 or (target.tileType == -1 and target.health <=0)) and
            not (self.distance(cors, (0,0)) <= 1)):
                target.playerIdx = player.playerId
                self.board[player.q][player.r].playerIdx = 0
                player.q, player.r = cors
                match target.tileType:
                    case 1:
                        player.regenHealth()
                        self.respawnConsumable(target.tileType)
                        target.tileType = 0
                    case 2:
                        player.gainExperience(100)
                        self.respawnConsumable(target.tileType)
                        target.tileType = 0
                    case 3:
                        player.getStuck()
                    case 4:
                        if(self.wormHoleCoordinates[target.wormHoleId][0] == cors):
                            player = self.wormHoleCoordinates[target.wormHoleId][1]
                        else:
                            player = self.wormHoleCoordinates[target.wormHoleId][0]
            else:
                player.illegalMove()
        else:
            target = self.board[cors[0]][cors[1]]
            if(max(abs(player.q - cors[0]) + abs(player.r - cors[1])) > 3 or target.tileType ):
                player.illegalMove()
            elif(abs(cors[0]) <= 1 and abs(cors[1]) <= 1):
                    player.gainExperience(player.power)
            elif(target.tileType == -2 and target.health <= 0):
                if(target.takeDamage(player.power)):
                    player.gainExperience(20)
            else:
                for tPlayer in self.players:
                    if((tPlayer.q, tPlayer.r) == cors and not (tPlayer.q, tPlayer.r) == (player.q, player.r)):
                        if(not tPlayer.takeDamage(player)):
                            player.gainExperience(100)
                        player.gainExperience(30)

        self.currentPlayer += 1
        if(self.currentPlayer == 5):
            tiles = self.boss.Attack()
            for player in self.players:
                cors = (player.q, player.r)
                if(cors in tiles):
                    if( not player.takeDamage(self.boss.Attack)):
                        player.q, player.r = self.startCors[player.playerIdx-1]
            self.currentPlayer = 1

    def printStr(self):
        print('\n\n------------------------------------------------------------------------')
        for q in range(-14, 15):
            for r in range(-14, 15):
                tile = self.board[q][r]
                if(g.distance((0,0), (q, r)) > 14):
                    print('  ', end = '')
                elif(tile.tileType >= 0):
                    if(tile.playerIdx > 0):
                        print('p', tile.playerIdx, sep = '', end = '')
                    else:
                        print(' ', tile.tileType, sep = '', end = '')
                else:
                    print(tile.tileType, end = '')
            print('\n')
        print('------------------------------------------------------------------------')
        return  "test"

if __name__ == '__main__':
    g = Game()
    for i in range(100):
        g.printStr()
        print(g.players[g.currentPlayer-1].q, g.players[g.currentPlayer-1].r)
        q, r = [int(i) for i in input('next move: ').split()]
        g.play('move', (q, r))