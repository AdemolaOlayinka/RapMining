# created by Ademola Olayinka
# 21 April 2017

class Tree(object):
    #Word generator object
    def __init__(self, name='root', children=None):
        self.name = name
        self.firstChildren = []
        self.secondChildren = []