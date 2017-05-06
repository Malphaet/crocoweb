# Copyleft (c) 2016 Cocobug All Rights Reserved.
# coding=utf-8

import re,traceback,os

try:
    from tree_parser import *
    from models import dual
except:
    from generator.models import dual
    from generator import tree_parser

def getDataType(name):
    "Return some kind of general types depending on the extention"
    ext=os.path.splitext(name)[-1]
    data={"image":[".jpg",".png",".svg",".tiff",".jpeg"],
        "audio":[".ogg",".aiff",".mp3"],
        "text":[".txt",".md"],
        "video":[".mov",".mp4"]}
    for typename,extension in data.items():
        if ext in extension:
            return typename
    return "other"

def makeContainer(module,site,current_node,previous_node,lang):
    article_list=module.makeSubNodelist(site.tree,lang,getDataType)
    previous=module.menuitem(site.get_variable("previous",lang),previous_node.path,"previous")
    menu=module.menu(previous=previous,menulist="\n".join(article_list),articles=site.get_variable("articles",lang))
    return menu

def makeData(module,current_node,lang):
    return module.content(content=current_node.get_content(lang),title=current_node.get_one(["article_title",'title',"article_name","name"],lang))

def makePage(module,site,lang,menu,data):
    return module.container(pagetitle=site.get_title(lang),websitename=site.get_one(['websitename',"webtitle","name","title"],"fr"),menu=menu,page=data)

if __name__ == '__main__':
    site=makeWebsite("sites/example_website")

    lang="fr"
    current_node=site.tree.get_node("index",lang)
    previous_node=site.tree.get_node("index",lang)

    menu=makeContainer(dual,site,current_node,previous_node,lang)
    data=makeData(dual,current_node,lang)

    page=makePage(dual,site,lang,menu,data)
    with open("site_base/dual/test.html","w+") as f:
        f.write(page)
    print(page)
