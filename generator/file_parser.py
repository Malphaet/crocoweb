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
        self.reserved=set(["model"])
        self.reserved_prefix="reserved_"
        self.content=[]

    def init_reserved(self,*others):
        "Init all the reserved variables, note that no protections are used, so use them at your own risk"
        for i in others:
            self.reserved.add(i)
        for key in self.reserved:
            setattr(self,key,"")

    def set_reserved(self,var):
        setattr(self,self.reserved_prefix+key,"")

    def get_reserved(self,var):
        getattr(self,var)

    def add_content(self,text,lang):
        self.content.append([text,lang])

    def get_next_line(self,lang="*"):
        "Get a line of text, with a filter if needed"
        pass

    def get_lang(self,lang):
        "Will make sense if I ever use a translation table and not a clusterf*ck of strings"
        return lang

    def add_variable(self,var,value):
        """Add the folowing variable and update the necessary constants
        Takes a variable (with an eventual langague tag) and it's value"""
        var,lang,value=create_lang(var,value)
        if var in self.reserved:
            setattr(self,var,value)
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
    page.init_reserved()
    with open(file_name) as f:
        try:
            while True: # Parse the config file
                line=f.readline()
                if not line: # Wait for the last line
                    break
                if line.startswith("----"): # Not really a good practice, but meh
                    break
                if line!=os.linesep: # Now parsing config files
                    var,value=re_config_line.match(line).groups()
                    page.add_variable(var,value)
            while True: # The config lines are now parsed, will now enter the nightmare of standart lines
                line=f.readline()
                if not line: # Wait for the last line
                    break
                match=re_text_line.match(line)  #Will always match since there is a .* in the regex
                beg_lang,end_lang,text=match.groups()
                used_langs={}
                page_text=[]
                if beg_lang: #Will now add a lang to witch the programe should write
                    if beg_lang in used_langs:
                        used_langs[beg_lang]+=1
                    else:
                        used_langs[beg_lang]=1
                elif end_lang:
                    if end_lang in used_langs:
                        used_langs[end_lang]-=1
                    else:
                        used_langs[end_lang]=0 # This should never happen, but...users
                elif text:
                    line_langs=[]
                    for l in used_langs:
                        if used_langs[l]>0:
                            line_langs.append(l)
                    if len(used_langs)==0: # If no langs are used, print in every lang
                        used_langs=["*"]
                    page.add_content(text,line_langs)

        except re.error:
            print "Error parsing",file_name,"contain a non parsable line:"
            print " >",line
        except:
            traceback.print_exc()
    return page

re_config_line=re.compile("(?P<variable>.+): (?P<value>.*)")
re_text_line=re.compile("__(?P<beg_lang>\w+)__|__/(?P<end_lang>\w+)__|(?P<text>.*)")

if __name__ == '__main__':
    page=parse_file("sites/example_website/_config.txt")
    print page.variables
    print page.list_of_lang
