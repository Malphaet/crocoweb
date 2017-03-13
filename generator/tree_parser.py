# Copyleft (c) 2016 Cocobug All Rights Reserved.
import os,sys,file_parser

class WebTree(object):
    "The tree of all website evolves during runtime as the files are requested"
    def __init__(self,path):
        self.website_path=path
        self.name=""
        self.generation=""
        self.variable={"/":{}}
        self.get_config()

    def make_walk(self,subpath=""):
        "Walk the directory and subdirectories and make the tree from it"
        for (dirpath, dirnames, filenames) in os.walk(os.path.join(self.website_path,subpath)):
            print dirpath, dirnames, filenames

    def get_config(self):
        "Get the basic config from the website"
        file_parser.parse_file(os.path.join(self.website_path,"_config.txt"))

    def convert_local(self,files):
        pass

    def print_webtree(self):
        print self
        print self.name

    def __repr__(self):
        return "WebTree of website "+self.website_path


class WebSubTree(WebTree):
    "Share some methods with the main tree, only describes one folder"
    def __init__(self):
        pass

class WebNode(object):
    "A webfile, as seen from the tree, contains a link to a WebPage, generated from itself"
    def __init__(self):
        pass

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
    s.list_dir()
