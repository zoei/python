# ! -*-Encoding:utf-8 -*-

from configparser import ConfigParser

class Configer():
    def __init__(self, file):
        self.file = file
        self.config = [] 
        self.parser = ConfigParser()
        self.load()

    def load(self):
        self.parser.read(self.file) 
        self.config = self.parser.sections()

    def save(self):
        self.parser.write(open(self.file,'w'))
        
    def getconfig(self):
        return self.config

    def getparser(self):
        return self.parser
