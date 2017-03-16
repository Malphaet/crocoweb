# Copyleft (c) 2016 Cocobug All Rights Reserved.
import os,sys,file_parser

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


    def make_tree(self):
        "Walk the directory and subdirectories and make the tree from it, note that the WebTree only have one Subtree, containing other subtrees"
        self.tree=WebSubTree(self.website_path,"")

    def get_config(self):
        "Get the basic config from the website"
        self.config_path=os.path.join(self.website_path,self.path,"_config.txt")
        self.config_file=file_parser.parse_file(self.config_path)
        self.variables=self.config_file.variables

    def get_variable(self,varname,filter_lang="*"):
        "Get the corresponding variable"
        return self.config_file.get_variable(varname,filter_lang)

    def convert_local(self,files):
        pass

    def print_webtree(self,prefix=""):
        "Print a representation of the Tree"
        print self
        self.tree.print_webtree(prefix)

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

    def get_variable(self,varname,filter_lang):
        "Get the variable, either in it's config or one of the above"
        try:
            return self.config_file.get_variable(varname,filter_lang)
        except:
            return self.parent_node.get_variable(varname,filter_lang)

    def get_config(self):
        "Try to init a config, if not just use an empty variable set"
        try:
            super.get_config(self)
        except:
            self.variables={}

    def make_tree(self):
        """List all directories, make Nodes or Subtree from it and init them
        For every subtree/node informations will be stored on the langagues used
        (Subtree[[en]->Subtree,[fr]->Subtree])* """
        self.subtree={}
        self.nodes={}

        for f in os.listdir(self.full_path):
            name=os.path.join(self.full_path,f)
            path=os.path.join(self.path,f)
            if os.path.isdir(name):
                var,lang=file_parser.create_lang(f)
                self.subtree=file_parser.add_to_table(var,lang,WebSubTree(self.website_path,path),self.subtree)
            else:
                var,lang=file_parser.create_lang(os.path.splitext(f)[0])
                self.nodes=file_parser.add_to_table(var,lang,WebNode(self.website_path,path),self.nodes)
        #print self, self.subtree
        #print self.nodes

    def get_all_nodes(self,filter_lang="*"):
        "Get all nodes in the following language"
        pass

    def get_node(self,name,filter_lang=""):
        "Get a node with a specific name"
        if name in self.nodes:
            if filter_lang!="": #No specific lang, so all langs are returned, should disapear soon I think
                return self.nodes
            if filter_lang in self.nodes[name]:
                return self.nodes[filter_lang]
            return self.nodes["*"] # specific language unavailable, all languages returned, better luck here
        raise IndexError("The node "+name+" doesn't exist")

    def get_content(self,name,filter_lang=""):
        "Get the content of the node in the specified language"
        return get_node(name,filter_lang).get_content(filter_lang)

    def print_webtree(self,prefix=""):
        "Print the tree and recuse"
        for item,langs in self.nodes.iteritems():
            for lang,node in langs.iteritems():
                print "{} [{}] {}".format(prefix,lang,node)
                print "-----------"
                print node.get_content("en")

        for item,langs in self.subtree.iteritems():
            for lang,node in langs.iteritems():
                print "{} [{}] {}".format(prefix,lang,node)
                node.print_webtree(prefix+"    ")

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

    def get_variable(self,varname,filter_lang):
        "Get the corresponding variable, first in the Webnode, then the config and repeating up until the Root"
        try:
            return self.config_file.get_variable(varname,filter_lang)
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
        if filter_lang in self.content:
            return self.content[filter_lang]
        return self.content["*"]

def makeWebsite(website):
    "Take a string of the folder name containing the website, will proceed to generate all needed Objects and return the Webtree"
    if os.path.isdir(website):
        webt=WebTree(website)
        return webt
    else:
        raise IOError("Unable to find the specified website")

if __name__ == '__main__':
    # Do all the nominal tests
    s=makeWebsite("sites/example_website")
    s.print_webtree(" > ")
