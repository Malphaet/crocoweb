# Copyleft (c) 2016 Cocobug All Rights Reserved.

from minitest import minitest

import types
from blessings import Terminal
from generator import *

#import vkyweb

term=Terminal()
unit=minitest.testUnit
group=minitest.testGroup

testVky=group(name="vkyWeb_all",terminal=term,verbose=1,align=42)
#testConfig=group()
#testParser=group(name="parser",terminal=term,prefix="| ")
#testTree=group(name="tree",terminal=term,prefix="| ")
#testModel=group(name="model",terminal=term,prefix="| ")

#testVky.addTest(testParser)
#testVky.addTest(testTree)
#testVky.addTest(testModel)

#testParser time

class testParser(unit):
    """Testing the file parser"""
    def __init__(self):
        super(testParser, self).__init__("file_parser")
        self.results=[]
        self.currentTest=""

    def addSucess(self):
        self.addResult(self.currentTest,True,"")

    def addFailure(self,msg):
        self.addResult(self.currentTest,False,msg)


    def test(self):
        try:
            config_langs=["*","en","fr"]
            #raise IOError("Impossible to load config")
            self.currentTest="parser:load"
            config=file_parser.parse_file("sites/example_website/_config.txt")
            self.addSucess()

            self.currentTest="parser_config"
            if (type(config)==file_parser.WebPage):
                self.addResult("parser_config",True,"")
            else:
                self.addFailure("config is supposed to be a WebPage")

            self.currentTest="parser_config:var:type"
            if type(config.variables)==dict:
                self.addSucess()
            else:
                self.addFailure("config is not a dict")

            self.currentTest="parser_config:lang"
            for lang in config_langs:
                if lang not in config.list_of_lang:
                    self.addFailure("lang {} not in config".format(lang))
            self.addSucess()

            self.currentTest="parser_config:content"
            if type(config.content)==list:
                for e in config.content:
                    if len(e)!=2:
                        self.addFailure("line is not formated with [text,[lang]]")
                self.addSucess()
            else:
                self.addFailure("content is supposed to be a list of lines&langs")

            self.currentTest="parser_config:generator"
            gen=config.get_next_line("*")
            if type(gen)==types.GeneratorType:
                self.addSucess()
            else:
                self.addFailure("get_next_line is supposed to be a generator")

            self.currentTest="parser_config:generator:lang"
            content_by_lang={'*':[],'fr':[],'en':[]}
            for line in config.content:
                txt,langs=line[0],line[1]
                for lang in langs:
                    if lang in ["fr","en"]:
                        content_by_lang[lang].append(txt)
                    elif lang=="*":
                        for l in config_langs:
                            content_by_lang[l].append(txt)
            succes=True
            for l in ["en","fr"]:
                generator_table=[e for e in config.get_next_line(l)]
                if len(content_by_lang[l])!=len(generator_table):
                    self.addFailure("generator and model don't have the same length [{}]".format(l))
                    succes=False
                for i in xrange(len(generator_table)):
                    if generator_table[i]!=content_by_lang[l][i]:
                        self.addFailure("generator and model have different content [{}:{}]".format(l,i))
                        succes=False
            if succes:
                self.addSucess()

            self.currentTest="parser_config:generator:type"
            for l in config.get_next_line("*"):
                if type(l)!=str:
                    self.addFailure("type is supposed to be a string")
            #print index.content
        except Exception as e:
            self.addFailure(e)

        return self.results

testVky.addTest(testParser())

testVky.test()
