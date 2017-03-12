# Copyleft (c) 2016 Cocobug All Rights Reserved.
import os,sys,fileparser

class WebTree(object):
    "The tree of all website evolves during runtime as the files are requested"
    def __init__(self,path):
        self.website_path=path
    def list_dir(self,subpath=""):
        "List all files in the directory"
        pass

    def convert_local(self,files):
        pass

class WebSubTree(Tree):
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
        webt=Webtree(website)
        return webt
    else:
        raise IOError("Unable to find the specified website")

if __name__ == '__main__':
    # Do all the nominal tests
    pass
