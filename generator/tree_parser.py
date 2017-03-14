# Copyleft (c) 2016 Cocobug All Rights Reserved.
import os,sys,file_parser

class WebTree(object):
    "The tree of all website evolves during runtime as the files are requested"
    def __init__(self,path):
        self.website_path=path
        self.name=""
        self.generation=""
        self.path=""
        self.get_config()

    def make_walk(self,subpath=""):
        "Walk the directory and subdirectories and make the tree from it"
        for (dirpath, dirnames, filenames) in os.walk(os.path.join(self.website_path,subpath)):
            print dirpath, dirnames, filenames

    def get_config(self):
        "Get the basic config from the website"
        self.config_path=os.path.join(self.website_path,self.path,"_config.txt")
        self.config_file=file_parser.parse_file(self.config_path)
        self.variables=self.config_file.variables

    def get_variable(self,varname,filter_lang="*"):
        "Get the corresponding variable"
        self.config_file.get_variable(varname,filter_lang)

    def convert_local(self,files):
        pass

    def print_webtree(self):
        "Print a representation of the Tree"
        print self
        print self.name

    def __repr__(self):
        return "WebTree of website "+self.website_path

    def __contain__(self,var):
        "Define the __in__ membership in the variables"
        try:
            self.get_variable(var)
            return True
        except:
            return False

class WebSubTree(WebTree):
    "Share some methods with the main tree, only describes one folder"
    def __init__(self):
        pass

    def get_variable(self,varname,filter_lang):
        "Get the variable, either in it's config or one of the above"
        try:
            self.config_file.get_variable(varname,filter_lang)
        except:
            self.parent_node.get_variable(varname,filter_lang)

class WebNode(object):
    "A webfile, as seen from the tree, contains a link to a WebPage, generated from itself"
    def __init__(self):
        pass
    def get_variable(self,varname,filter_lang):
        "Get the corresponding variable, first in the Webnode, then the config and repeating up until the Root"
        try:
            self.file.get_variable(varname,filter_lang)
        except:
            try:
                self.config_file.get_variable(varname,filter_lang)
            except:
                self.parent_node.get_variable(varname,filter_lang)

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
    s.print_webtree()
    s.make_walk()
