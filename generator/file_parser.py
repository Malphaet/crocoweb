# Copyleft (c) 2016 Cocobug All Rights Reserved.
# coding=utf-8


import os,sys,tree_parser
import re
import traceback

class WebPage(object):
    "A webpage object, with some variables and all localisations"
    def __init__(self,path):
        self.path=path
        self.name=os.path.split(path)[-1]
        self.variables={}
        self.list_of_lang=set()
        self.reserved=["model"]
        self.init_reserved()

    def init_reserved(self):
        for key in reserved:
            self.setattr(key,"")

    def add_variable(self,var,value):
        """Add the folowing variable and update the necessary constants
        Takes a variable (with an eventual langague tag) and it's value"""
        var,lang,value=create_lang(var,value)
        if var in reserved:
            self.setattr(var,value)
        else:
            if var in self.variables:
                self.variables[var][lang]=value
            else:
                self.variables[var]={lang:value}
            self.list_of_lang.add(lang)


def create_lang(var,value):
    """Takes a variable (with an eventual language tag) and it's value and return var,lang,value
    Only the last _ determines the language, note that it could give the impression _ is ok to use in variables. It is not."""
    var=var.rsplit('_',1)
    if len(var)==2:
        return var[0],var[1],value
    return var[0],"*",value

def parse_file(file_name):
    "Parse a file and return a webpage object"
    page=WebPage(file_name)
    isconfig=True # The firsts lines are config lines
    with open(file_name) as f:
        while True:
            line=f.readline()
            if not line:
                break
            try:
                if line.startswith("----"): # Not really a good practice, but meh
                    isconfig=False
                if isconfig and line!=os.linesep: # Now parsing config files
                    var,value=re_config_line.match(line).groups()
                    page.add_variable(var,value)
                else: # The config lines are now parsed, will now enter the nightmare of standart lines

            except re.error:
                print "Error parsing",file_name,"contain a non parsable line:"
                print " >",line
            except:
                traceback.print_exc()

re_config_line=re.compile("(?P<variable>.+): (?P<value>.*)")
re_text_line=re.compile("")

if __name__ == '__main__':

    parse_file("sites/example_website/_config.txt")
