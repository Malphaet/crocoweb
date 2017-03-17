# Copyleft (c) 2016 Cocobug All Rights Reserved.
# coding=utf-8
from tree_parser import *
import re,traceback


re_vars=re.compile(".*\#_(?P<variable>.*)_\#")

class HTMLPage(object):
    "Basic HTML object"
    def __init__(self,name,node):
        self.html=""
        self.name=name
        self.node=node
        self.path=""

    def load(self,path):
        self.path=path
        try:
            with open(path) as a:
                self.model=a.read()
        except:
            print "Error loading model"

    def replace(self,lang):
        self.html=""
        for line in self.model.splitlines():
            #print line
            try:
                variable=re_vars.match(line).groups()[0]
                if variable!=None:
                    line=line.replace("#_"+variable+"_#",self.node.get_variable(variable,lang))
            except AttributeError:
                pass
            except:
                print traceback.print_exc()
            self.html+=line
            self.html+=os.linesep
        #print self.html

    def export(self):
        "Generate the HTML code and output it"
        return self.html

class Container(HTMLPage):
    "Side menus and title, acess to all special pages"
    def __init__(self,name,node):
        super(Container,self).__init__(name,node)

class Data(HTMLPage):
    "Webpage itself"
    def __init__(self,name,node):
        super(Data,self).__init__(name,node)

class DualContainer(Container):
    "Dual view"
    def __init__(self,name,node):
        super(DualContainer,self).__init__(name,node)


class DualData(Data):
    "Dual view"
    def __init__(self,name,node):
        super(DualData,self).__init__(name,node)

    def replace(self,lang):
        self.html=self.model
        self.html=self.html.replace("#_content_#",self.node.get_content("fr"))
        self.html=self.html.replace("#_name_#",self.node.get_variable("title","fr"))

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
    cont=makeContainer(site)
    data=makeData(site.tree.get_node("index","fr"))
    makePage(site,cont,data)
