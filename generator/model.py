# Copyleft (c) 2016 Cocobug All Rights Reserved.
# coding=utf-8
from tree_parser import *
from model import dual
import re,traceback

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

def makeContainer(node):
    c=DualContainer(node.name,node)
    #print node.variables
    #print node.config_file
    c.load("generator/model/dual_menu.html")
    c.replace("fr")
    return c

def makeData(node):
    c=DualData(node.name,node)
    c.load("generator/model/dual_page.html")
    c.replace("fr")
    return c

def makePage(node,cont,data):
    c=DualContainer(node.name,node)
    c.load("generator/model/dual_container.html")
    c.replace('fr')
    cont_t=cont.export()
    data_t=data.export()
    print c.export().replace("##PAGE##",data_t).replace("##MENU##",cont_t)

if __name__ == '__main__':
    site=makeWebsite("sites/example_website")
    print dual.menuitem('da',"ma","text")
    #cont=makeContainer(site)
    #data=makeData(site.tree.get_node("index","fr"))
    #makePage(site,cont,data)
