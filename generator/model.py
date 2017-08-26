# Copyleft (c) 2016 Cocobug All Rights Reserved.
# -*- coding: utf_8 -*-

import re,traceback,os,markdown

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

def makeHTMLName(text):
    "Get the link assotitated with the node (name.html)"
    return os.path.splitext(text)[0]+".html"#splitext(node.name)[0:-1].join(os.filesep)

def makeContainer(module,site,current_node,previous_node,lang,makeHTMLName=makeHTMLName,depth="",langswitch=""):
    article_list=module.makeSubNodelist(current_node.parent_node,lang,getDataType,makeHTMLName)
    if previous_node==None:
        previous=""
    else:
        previous=module.menuitem(site.get_variable("previous",lang),"../"+makeHTMLName("index"),"previous")
    menu=module.menu(previous=previous,menulist="\n".join(article_list),articles=site.get_variable("articles",lang),depth=depth)
    return menu

def makeAllData(module,list_of_data):
    "Obsolete, use makeiFrame instead"
    return module.mix_data(list_of_data)

def makeiFrame(module,list_of_nodes):
    return module.iframe(list_of_nodes)

def makeData(module,current_node,lang):
    content=markdown.markdown(unicode(current_node.get_content(lang).decode("utf-8")))
    return module.content(content=content.encode('utf-8'),title=current_node.get_one(["article_title",'title',"article_name","name"],lang))

def makePage(module,site,lang,menu,data,depth,langswitch):
    return module.container(pagetitle=site.get_title(lang),websitename=site.get_one(['websitename',"webtitle","name","title"],lang),menu=menu,page=data,depth=depth,langswitch=langswitch)

def makeLangSwitch(module,list_of_lang,selected_lang):
    return module.langselect(list_of_lang,selected_lang)

def pathAssets(module):
    return module.assets()

if __name__ == '__main__':
    site=makeWebsite("sites/example_website")

    lang="fr"
    current_node=site.tree.get_node("index",lang)
    previous_node=site.tree.get_node("index",lang)

    menu=makeContainer(dual,site,current_node,previous_node,lang,depth="",langswitch="")
    data=makeData(dual,current_node,lang)

    page=makePage(dual,site,lang,menu,data,depth="")
    with open("site_base/dual/test.html","w+") as f:
        f.write(page)
    print(page)
