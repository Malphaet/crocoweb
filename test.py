# Copyleft (c) 2016 Cocobug All Rights Reserved.

from minitest import minitest

import types
from blessings import Terminal
from generator import *

#import vkyweb

term=Terminal()
unit=minitest.testUnit
group=minitest.testGroup

testVky=group(name="vkyWeb_all",terminal=term,verbose=1,align=40)
#testConfig=group()
#testParser=group(name="parser",terminal=term,prefix="| ")
#testTree=group(name="tree",terminal=term,prefix="| ")
#testModel=group(name="model",terminal=term,prefix="| ")

#testVky.addTest(testParser)
#testVky.addTest(testTree)
#testVky.addTest(testModel)

#testParser time
class CustomError(Exception):
    """docstring for CustomError."""
    def __init__(self, name,text):
        super(CustomError, self).__init__(text)
        self.name

class testParser(unit):
    """Testing the file parser"""
    def __init__(self):
        super(testParser, self).__init__("file_parser")

    def test(self):
        self.results=[]

        try:
            #raise IOError("Impossible to load config")
            config=file_parser.parse_file("sites/example_website/_config.txt")
            self.addResult("parser:load",True,"")
        except Exception as e:
            #config={} # Add a default config to help the rest of tests ?
            self.addResult("parser:load",False,e)

        try:
            if (type(config)==file_parser.WebPage):
                self.addResult("parser_config",True,"")
            else:
                raise TypeError("config is supposed to be a WebPage")
        except:
            self.addResult("parser_config",False,e)

        try:
            if type(config.variables)==dict:
                self.addResult("parser_config:var:type",True,"")
            else:
                raise TypeError("config is not a dict")
        except Exception as e:
            self.addResult("parser_config:var:type",False,e)


        try:
            for lang in ["*","en","fr"]:
                if lang not in config.list_of_lang:
                    raise ValueError("lang {} not in config".format(lang))
            self.addResult("parser_config:lang",True,"")
        except Exception as e:
            self.addResult('parser_config:lang',False,e)


        try:
            if type(config.content)==list:
                for e in config.content:
                    if len(e)!=2:
                        raise IndexError("line is not formated with [text,[lang]]")
                self.addResult("parser_config:content",True,"")
            else:
                raise TypeError("content is supposed to be a list of lines&langs")
        except Exception as e:
            self.addResult('parser_config:content',False,e)


        try:
            gen=config.get_next_line("*")
            if type(gen)==types.GeneratorType:
                pass
            self.addResult("parser_config:generator",True,"")
        except Exception as e:
            self.addResult("parser_config:generator",False,e)
        for l in config.get_next_line("*"):
            print l
        #print index.content
        return self.results

testVky.addTest(testParser())

testVky.test()
