import json

class Config():
    def __init__(self, file="settings.json"):
        fo = open(file)
        self.file=file
        self.settings = json.load(fo)
        fo.close()

    def save(self):
        fo = open(self.file, "w+")
        json.dump(self.settings, fo)
        fo.close()