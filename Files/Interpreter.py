import json

class Interpreter():

    def __init__(self, name='configs'):
        a = {
            'debug': False,
            'screenSize': (720, 480),
            'volume': 100,
            'fullscreen': False,
            'fps': 60
        }
        self.name = name
        try:
            try:
                rawArchive = open((self.name + '.json'), 'r')
                self.jsonArchive = json.load(rawArchive)
                rawArchive.close()
            except Exception:
                rawArchive = open((self.name + '.json'), 'w')
                json.dump(a, rawArchive, indent=4, sort_keys=True, separators=(',', ': '))
                self.jsonArchive = json.load(rawArchive)
                rawArchive.close()

        except Exception as e:
            if a['debug']:
                print("ERRO: json archive doesn't exist, please create one (configs.json) --  Real error =", e)
            else:
                pass

    def updateParameter(self, config, value):
        # collect all the info inside the archive
        rawArchive = open((self.name + '.json'), 'r')
        self.jsonArchive = json.load(rawArchive)
        rawArchive.close()

        # update all the info inside the archive
        rawArchive = open((self.name + '.json'), 'w')
        self.jsonArchive.update({config: value})
        json.dump(self.jsonArchive, rawArchive, indent=4, sort_keys=True, separators=(',', ': '))
        rawArchive.close()


    def getParameter(self, config):
        if config in self.jsonArchive:
            return self.jsonArchive.get(config)
        elif self.getParameter('debug'):
            print('Parameter not found ', config)



    def removeParameter(self, config):
        # collect all the info inside the archive
        rawArchive = open((self.name + '.json'), 'r')
        self.jsonArchive = json.load(rawArchive)
        rawArchive.close()

        # update all the info inside the archive
        rawArchive = open((self.name + '.json'), 'w')
        try:
            self.jsonArchive.pop(config)
        except Exception as e:
            if self.getParameter('debug'):
                print(e)
        json.dump(self.jsonArchive, rawArchive, indent=4, sort_keys=True, separators=(',', ': '))
        rawArchive.close()

    def getName(self):
        return self.name


# Tests
if __name__ == '__main__':
    test = Interpreter('asdsd')
    test.updateParameter('Test', '123')
    print(test.getParameter('Test'))
    print(test.getParameter('Tsest'))
    test.removeParameter('Test')

    import os
    os.remove(test.getName() + '.json')



