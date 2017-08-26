#!/usr/bin/env python

# Copyleft (c) 2016 Cocobug All Rights Reserved.

import argparse,os,sys
from generator import *
choosen_model=models.dual

def saveData(path,data):
    with open(path,"w+") as f:
        f.write(data)

def savePath(path):
    return os.path.join(save_path,path)

def saveMenus():
    pass

def HTMLNameCreator(lang,ext="html"):
    ext,lang=ext,lang
    def makeHTMLName(node):
        return "{}_{}.{}".format(node.name,lang,ext)
    return makeHTMLName

def iFrameFromNode(node):
    "Return the list of pages that should be in the frames"
    names=[]
    for l in args.l:
        names.append(os.path.basename(HTMLNameCreator("content_"+l,ext=args.extension)(node)))
    return names

def gen_all_nodes_menu(tree,lang,depth):
    previous_node=tree #maybe need to be sent via parameter, nonetheless very secondary
    # TODO: look for index in all nodes, create it if needed
    for current_node in tree.get_next_nodes(lang):
        if (os.path.basename(current_node.name)[0]!="_"): #Likely add a visible: true/false tag in the future
            filename=htmlNamer(current_node)
            if args.verbose:
                print "Generating {} menus".format(filename)
            save=savePath(filename)

            menu=model.makeContainer(choosen_model,website,current_node,previous_node,lang,htmlNamer,depth)
            frames=model.makeiFrame(choosen_model,iFrameFromNode(current_node))
            page=model.makePage(choosen_model,website,lang,menu,frames,depth)

            saveData(save,page)
    depth="../"+depth
    for new in tree.get_next_subtree(lang):
        try:
            if args.verbose:
                print("Creating {}".format(new.path))
            os.makedirs(savePath(new.path))
        except OSError:
            pass
        gen_all_nodes_menu(new,lang,depth)

def gen_all_nodes_content(tree,lang):
    for current_node in tree.get_next_nodes(lang):
        file_name=htmlContentNamer(current_node)
        if args.verbose:
            print "Generating {} content".format(file_name)
        save=savePath(file_name)
        content=model.makeData(choosen_model,current_node,lang)

        saveData(save,content)

    for t in tree.get_next_subtree(lang):
        gen_all_nodes_content(t,lang)


parser = argparse.ArgumentParser(description='Website on-the-fly & static generator')

# The argparse should look like this:
# vkyweb.py PATH_TO_WEBSITE --update(only update) --verbose(show as much as possible) --dry(don't actually write anything) -d(destination if not current folder) -m(custom model) -l(only use theese languages)
parser.add_argument('website_path',metavar="path_to_the_website",type=str,help="Path to the website to parse")
parser.add_argument("--verbose",action="store_true",help="Verbosity to display")
parser.add_argument('--update',action="store_true",help="Only update, don't rewrite")
parser.add_argument("--dry",action="store_true",help="Dry run, don't write anything")
parser.add_argument("-d",metavar="destination",type=str,default=".",help="Destination to write to")
parser.add_argument("-l",metavar="langs",type=str,nargs="+",help="List of langs to generate the site to")
parser.add_argument('--extension',type=str,default="html", help="The extension to give to all generated files")
#parser.add_argument("--model",metavar="model",type=str,help="model to use")
#parser.add_argument("--merge",metavar="merge",type=str,help="don't use iframes, merge all content")

args=parser.parse_args()

# Make tree
if not (os.path.exists(args.website_path)):
    if args.verbose:
        print("Path {} does not exist".format(args.website_path))
    sys.exit()
website=tree_parser.makeWebsite(args.website_path)
save_path=args.d #Directly in the dest folder, no meta folder created !

# Making the directory if needed
if not args.dry:
    try:
        if args.verbose:
            print("Creating {}".save_path)
        os.makedirs(save_path)
    except OSError:
        pass
#website.print_webtree(lang="fr",prefix=" * ")

# Walk & generate
if args.verbose:
    print("Website will be generated in {} at {}".format(args.l,args.d))

for lang in args.l: #Generate every page in .lang.html (with both contents)
    htmlNamer=HTMLNameCreator(lang,args.extension)
    htmlContentNamer=HTMLNameCreator("content_"+lang,args.extension)
    previous_node=website.tree.get_node("index",lang)
    gen_all_nodes_menu(website.tree,lang,depth="")
    gen_all_nodes_content(website.tree,lang)

    #for tree in website.tree.get_next_subtree():
    #    previous_node=tree # For now, you can't get higher than index
#for every lang, do a mix of print_webtree and makeContainer
    #container=model.makeContainer(s)
