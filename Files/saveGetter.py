import json

class saveGetter:
    def __init__(self, game, slot, player1):
        self.name = slot
        self.game = game
        self.player1 = player1

        self.playerA1 = {
            'damage': self.player1.damage,
            'defense': self.player1.defense,
            'speed': self.player1.speed,
            'life': self.player1.life,
            'maxLife': self.player1.maxLife,
            'magicBook': self.player1.magicBook
        }

        self.architecture = [self.playerA1, self.game.mapsAlreadyPlayed]
        try:
            rawArchive = open((self.name + '.json'), 'r')
            self.jsonArchive = json.load(rawArchive)
            rawArchive.close()

        except Exception:
            rawArchive = open((self.name + '.json'), 'w')
            json.dump(self.architecture, rawArchive, indent=2, sort_keys=True)
            self.jsonArchive = json.load(rawArchive)
            rawArchive.close()

    def update(self, player1):
        self.updatePlayer1(player1)
        self.architecture = [self.player1, self.game.mapsAlreadyPlayed, self.game.currentMap]

        rawArchive = open((self.name + '.json'), 'w')
        json.dump(self.architecture, rawArchive, indent=2, sort_keys=True)
        rawArchive.close()

    def updatePlayer1(self, player):
        self.playerA1 = {
            'damage': player.damage,
            'defense': player.defense,
            'speed': player.speed,
            'life': player.life,
            'maxLife': player.maxLife,
            'magicBook': player.magicBook
        }

    def returnPlayer1(self):
        return self.player1

    def returnMapsPlayed(self):
        return self.game.mapsAlreadyPlayed