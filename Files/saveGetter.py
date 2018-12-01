import json

class saveGetter:
    def __init__(self, game, slot, loadind=False):
        self.name = slot
        self.game = game
        self.data = self.game.data
        self.playerA1 = {}

        if not loadind:
            self.playerA1 = {
                'damage': 1,
                'defense': 0,
                'speed': 2,
                'life': self.difficulty()[0],
                'maxLife': self.difficulty()[1],
                'backToNormal': True,
                'magicBook': 0,
                'cooldown': 30,
                'magicCooldown': 0
            }
        else:
            rawArchive = open(('../SaveFiles/'+ self.name + '.json'), 'r')
            self.jsonArchive = json.load(rawArchive)
            rawArchive.close()
            for i in self.jsonArchive:
                if isinstance(i, dict):
                    for key, value in i.items():
                        self.playerA1[key] = value
                else:
                    self.game.mapsAlreadyPlayed = i
            self.name = 'Slot 0'


        self.architecture = [self.playerA1, self.game.mapsAlreadyPlayed]
        try:
            if self.name == 'Slot 0' and loadind is None:
                rawArchive = open(('../SaveFiles/' + self.name + '.json'), 'w')
            rawArchive = open(('../SaveFiles/' + self.name + '.json'), 'r')
            self.jsonArchive = json.load(rawArchive)
            rawArchive.close()

        except Exception:
            rawArchive = open(('../SaveFiles/' + self.name + '.json'), 'w')
            json.dump(self.architecture, rawArchive, indent=2, sort_keys=True)
            self.jsonArchive = json.load(rawArchive)
            rawArchive.close()

    def update(self, player1):
        self.updatePlayer1(player1)
        print(self.playerA1)
        self.architecture = [self.playerA1, self.game.mapsAlreadyPlayed]
        print(self.playerA1)

        rawArchive = open(('../SaveFiles/' + self.name + '.json'), 'w')
        json.dump(self.architecture, rawArchive, indent=2, sort_keys=True)
        print(self.playerA1)
        rawArchive.close()

    def updatePlayer1(self, player):
        self.playerA1 = {
            'damage': player.damage,
            'defense': player.defense,
            'speed': player.speed,
            'life': player.life,
            'maxLife': player.maxLife,
            'magicBook': player.magic,
            'cooldown': player.hab1cooldown,
            'magicCooldown': player.bookMagicCooldown,
            'backToNormal': player.backToNormal
        }

    def difficulty(self):
        self.difficultyGet = self.data.getParameter('difficulty')
        if self.difficultyGet == 'easy':
            return (8, 8)
        elif self.difficultyGet == 'normal':
            return  (6, 6)
        elif self.difficultyGet == 'hard':
            return (4, 4)
        else:
            return (10, 10)

    def returnPlayer1(self):
        return self.playerA1

    def returnMapsPlayed(self):
        return self.game.mapsAlreadyPlayed