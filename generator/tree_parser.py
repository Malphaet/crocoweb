# Copyleft (c) 2016 Cocobug All Rights Reserved.
# -*- coding: utf_8 -*-

import os,sys

try:
    from generator import file_parser
    from generator.model import dual
except:
    import file_parser
    from model import dual

class WebTree(object):
    "The tree of all website evolves during runtime as the files are requested"
    def __init__(self,website_path,path=""):
        self.website_path=website_path
        self.name=""
        self.generation=""
        self.path=path
        self.full_path=os.path.join(website_path,path)
        self.get_config()
        self.make_tree()

    def get_title(self,filter_lang):
        "Try to give the human-readable title of the node, default to the name"
        try:
            return self.get_variable("title",filter_lang)
        except:
            return self.name

    def get_one(self,array_of_variables,filter_lang="",default=None):
        "Try to get one of the equivalent variables"
        for var in array_of_variables:
            try:
                return self.get_variable(var,filter_lang)
            except:
                pass
        return default

    def make_tree(self):
        "Walk the directory and subdirectories and make the tree from it, note that the WebTree only have one Subtree, containing other subtrees"
        self.tree=WebSubTree(self.website_path,"")
        self.tree.parent_node=self

    def get_config(self):
        "Get the basic config from the website"
        self.config_path=os.path.join(self.website_path,self.path,"_config.txt")
        self.config_file=file_parser.parse_file(self.config_path)
        self.variables=self.config_file.variables
        self.name=self.path.split("_")[0]#self.config_file.name #Should actually, rename the file to allow customs names in _config

    def get_variable(self,varname,filter_lang="*"):
        "Get the corresponding variable"
        return self.config_file.get_variable(varname,filter_lang)

    def convert_local(self,files):
        pass

    def print_webtree(self,lang="en",prefix=""):
        "Print a representation of the Tree"
        print (self)
        self.tree.print_webtree(lang,prefix)

    def __repr__(self):
        return "{} @ {}".format(self.__class__.__name__,self.full_path)

    def __contain__(self,var):
        "Define the __in__ membership in the variables"
        try:
            self.get_variable(var)
            return True
        except:
            return False

class WebSubTree(WebTree):
    "Share some methods with the main tree, only describes one folder"
    def __init__(self,website_path,path):
        self.subtree={}
        self.nodes={}
        WebTree.__init__(self,website_path,path)
        #self.name=os.path.split(path)[-1]

    def get_variable(self,varname,filter_lang):
        "Get the variable, either in it's config or one of the above"
        try:
            return self.config_file.get_variable(varname,filter_lang)
        except:
            return self.parent_node.get_variable(varname,filter_lang)

    def get_config(self):
        "Try to init a config, if not just use an empty variable set"
        try:
            WebTree.get_config(self)
            #self.get_config() # It does make more sense to have your own no ?
        except:
            #print("Can't find config")
            self.variables={}

    def make_tree(self):
        """List all directories, make Nodes or Subtree from it and init them
        For every subtree/node informations will be stored on the langagues used
        (Subtree[[en]->Subtree,[fr]->Subtree])* """
        self.subtree={}
        self.nodes={}

        # This generator is deeply flawed, and should create temp nodes every time it meets a _lang folder then split from it
        for f in os.listdir(self.full_path):
            name=os.path.join(self.full_path,f)
            path=os.path.join(self.path,f)
            #print self.name
            if os.path.isdir(name):
                var,lang=file_parser.create_lang(f)
                new=WebSubTree(self.website_path,path)
                new.parent_node=self
                new.name=os.path.join(self.name,var) # Attempt to fix
                self.subtree=file_parser.add_to_table(var,lang,new,self.subtree)
            else:
                var,lang=file_parser.create_lang(os.path.splitext(f)[0])
                new=WebNode(self.website_path,path)
                new.parent_node=self
                new.name=os.path.join(self.name,var)
                self.nodes=file_parser.add_to_table(var,lang,new,self.nodes)
        #print( self, self.subtree)
        #print( self.nodes)

    def get_next_nodes(self,filter_lang="*"):
        "Get all nodes in the following language"
        for node in self.nodes:
            yield self.get_node(node,filter_lang)

    def get_node(self,name,filter_lang=""):
        "Get a node with a specific name"
        if name in self.nodes:
            if filter_lang=="": #No specific lang, so all langs are returned, should disapear soon I think
                return self.nodes[name]
            if filter_lang in self.nodes[name]:
                return self.nodes[name][filter_lang]
            return self.nodes[name]["*"] # Specific language unavailable, all languages returned, better luck here
        raise IndexError("The node "+name+" doesn't exist")

    def get_next_subtree(self,filter_lang="*"):
        "Get all subtrees"
        for tree in self.subtree:
            yield self.get_subtree(tree,filter_lang)

    def get_subtree(self,name,filter_lang="*"):
        "Get a tree with a specific name"
        if name in self.subtree:
            if filter_lang=="": #No specific lang, so all langs are returned, should disapear soon I think
                return self.subtree[name]
            if filter_lang in self.subtree[name]:
                return self.subtree[name][filter_lang]
            #print self.subtree[name]
            return self.subtree[name]["*"] # specific language unavailable, all languages returned, better luck here
        raise IndexError("The tree "+subtree+" doesn't exist")

    def get_content(self,name,filter_lang=""):
        "Get the content of the node in the specified language"
        return self.get_node(name,filter_lang).get_content(filter_lang)

    def print_webtree(self,lang="en",prefix=""):
        "Print the tree and recurse"
        for node in self.get_next_nodes(lang):
             print( "{} [{}] {}".format(prefix,lang,node))
             print( prefix+" +-----------")
             newL="\n{} [{}] | ".format(prefix,lang)
             print ("{} [{}] | {}".format(prefix,lang,node.get_content(lang).replace('\n',newL)))
        for tree in self.get_next_subtree(lang):
            print( "{} [{}] {}".format(prefix,lang,node))
            tree.print_webtree(lang,prefix+"    ")

class WebNode(WebSubTree):
    "A webfile, as seen from the tree, contains a link to a WebPage/Webfile in every langague"
    def __init__(self,website_path,path):
        self.website_path=website_path
        self.path=path
        self.full_path=os.path.join(website_path,path)
        self.content={}
        self.name,self.type=os.path.splitext(self.path)
        if self.type==".txt":
            self.open_node()

    def print_webtree(self,lang,prefix):
        raise AttributeError("WebNode doesn't have an attribute print_webtree")

    def get_variable(self,varname,filter_lang):
        "Get the corresponding variable, first in the Webnode, then the config and repeating up until the Root"
        try:
            return self.parse.get_variable(varname,filter_lang)
        except:
            try:
                return self.config_file.get_variable(varname,filter_lang)
            except:
                return self.parent_node.get_variable(varname,filter_lang)

    def open_node(self):
        "Open the file in the node, for now the parse is left linked, but later versions will ditch it asap"
        self.parse=file_parser.parse_file(self.full_path)
        self.variables=self.parse.variables
        self.content=self.parse.export()
        self.list_of_lang=self.parse.list_of_lang

    def get_content(self,filter_lang):
        """Output the content of the node, in the correct language
        (note that you shouldn't ask directly a node for it's content, rather a Subtree for a node in the correct language)"""
        try:
            return self.content[filter_lang]
        except KeyError:
            if "*" in self.content:
                return self.content["*"]
            else:
                return ""
            # if I'm asking for "*" am I asking for ANY lang or EVERY lang or ONLY "*" ?
            # for now this code will return ONLY the common part aka "*" and return an empty string if there is no common part
        except:
            raise KeyError("Can't access lang ({}) in node ({})".format(filter_lang,self))

def makeWebsite(website):
    "Take a string of the folder name containing the website, will proceed to generate all needed Objects and return the Webtree"
    if os.path.isdir(website):
        webt=WebTree(website)
        return webt
    else:
        raise IOError("Unable to find the specified website")

if __name__ == '__main__':
    import file_parser
    # Do all the nominal tests
    s=makeWebsite("sites/example_website")
    s.print_webtree("en"," > ")
    dual.container(pagetitle="#_pagetitle_#",websitename="#_websitename_#",menu="##MENU##",page="##PAGE##")
