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

    def set_reserved(self,var,value=""):
        "Set a reserved variable"
        setattr(self,self.reserved_prefix+key,value)

    def get_reserved(self,var):
        "Get a reserved variable"
        return getattr(self,self.reserved_prefix+var)

    def add_content(self,text,lang):
        "Add a line of content, with the appropriates langues"
        self.content.append([text,lang])

    def get_next_line(self,filter_lang="*"):
        "Get a line of text, with a filter if needed"
        for line,lang in self.content:
            if self.match_with_lang(lang,filter_lang):
                yield line

    def match_with_lang(self,lang,filter_lang):
        """Will make sense if I ever use a translation table and not a clusterf*ck of strings"""
        for l in lang:
            if l=="*" or l==filter_lang:
                return 1
        return 0

    def get_text(self,filter):
        "Get the whole text matching the filter, note that the * filter will ONLY match if the text is meant for all, not all text"
        text=""
        for line in self.get_next_line(filter):
            text+=line
            text+=os.linesep
        return text

    def add_variable(self,var,value):
        """Add the folowing variable and update the necessary constants
        Takes a variable (with an eventual langague tag) and it's value"""
        var,lang=create_lang(var)
        if var in self.reserved:
            setattr(self,var,value)
        else:
            add_to_table(var,lang,value,self.variables)
            self.list_of_lang.add(lang)

    def get_variable(self,varname,filter_lang="*"):
        "Get a variable, if * or nothing is used a filter the program will attempt to give a global variable, or will yield one at random"
        #print "Getting",varname,filter_lang,"in",self.variables
        #if varname in self.reserved:
        #    return getattr(self,varname)

        if varname in self.variables:
            if filter_lang in self.variables[varname]:
                return self.variables[varname][filter_lang]
            else:
                if filter_lang=="*":
                    return self.variables[varname].values()[0]
                return self.variables[varname]["*"]
        raise KeyError("The variable "+varname+" doens't exist in the language "+filter_lang)

    def export(self):
        "Export the Webobject in every language"
        exp={}
        for lang in self.list_of_lang:
            exp[lang]=self.get_text(lang)
        return exp

def add_to_table(var,lang,value,table):
    "For now it works in tandem with create_lang and add to a dict with the lang"
    if var in table:
        table[var][lang]=value
    else:
        table[var]={lang:value}
    return table

def create_lang(var):
    """Takes a variable (with an eventual language tag) and it's value and return var,lang,value
    Only the last _ determines the language, note that it could give the impression _ is ok to use in variables. It is not."""
    s_var=var.rsplit('_',1)

    if len(s_var)==2:
        if "" in s_var:
            return var,"*"
        return s_var[0],s_var[1]
    return var ,"*"

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

            used_langs={} # Keep trace of all used langs and opened/closed matchs
            while True: # The config lines are now parsed, will now enter the nightmare of standart lines
                line=f.readline()
                if not line: # Wait for the last line
                    break
                match=re_text_line.match(line)  #Will always match since there is a .* in the regex
                beg_lang,end_lang,text=match.groups()
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
                    line_langs=[] # Langs used in the current line
                    for l in used_langs: #
                        if used_langs[l]>0:
                            line_langs.append(l)
                    if len(line_langs)==0: # If no langs are used, print in every lang (standart behavior)
                        line_langs=["*"]
                    page.add_content(text,line_langs)

        except re.error:
            print "Error parsing",file_name,"contain a non parsable line:"
            print " >",line
        except:
            traceback.print_exc()
    return page

re_config_line=re.compile("(?P<variable>.+): (?P<value>.*)")
re_text_line=re.compile("__(?P<beg_lang>[\*\w]+)__|__/(?P<end_lang>[\*\w]+)__|(?P<text>.*)")

if __name__ == '__main__':
    config=parse_file("sites/example_website/_config.txt")
    index=parse_file("sites/example_website/index.txt")

    #print config.variables
    #print config.list_of_lang
    #print config.content
    #for l in config.get_next_line("*"):
    #    print l
    #print index.content
    print "All text only"
    print index.get_text("*")
    print "Fr text only"
    print index.get_text("fr")
    print "En text only"
    print index.get_text("en")
