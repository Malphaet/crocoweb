# Copyleft (c) 2016 Cocobug All Rights Reserved.
# coding=utf-8
from tree_parser import *

class HTMLPage(object):
    "Basic HTML object"
    def __init__(self,name,variables={}):
        self.html=""
        self.name=name
        self.variables=variables
    def load(self,path):
        try:
            with open(path) as a:
                self.html=a.read()
        except:
            print "Error loading model"

    def replace(self,lang,variables=None):
        if variables==None:
            variables=self.variables
        for var,langs in variables.iteritems():
            self.html.replace("%_"+var+"_%",langs[lang])

    def export(self):
        "Generate the HTML code and output it"
        return self.html

class Container(object):
    "Side menus and title, acess to all special pages"
    def __init__(self,name,variables,menus):
        HTMLPage.__init__(self,name,variables)
        self.menus=menus

    def generate(self):
        self.html=""

class Data(object):
    "Webpage itself"
    def __init__(self):
        HTMLPage.__init__(self)

class DualContainer(Container):
    "Dual view"
    pass

class DualData(Data):
    "Dual view"
    pass

def DataType(ext):
    "Return some kind of general types depending on the extention"
    data={"image":[".jpg",".png",".svg",".tiff",".jpeg"],
        "audio":[".ogg",".aiff",".mp3"],
        "text":[".txt",".md"],
        "video":[".mov",".mp4"]}
    for typename,extension in data.iteritems():
        if ext in extension:
            return typename
    return None

def makeContainer(tree):
    

if __name__ == '__main__':
    pass
