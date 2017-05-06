import os

def container(pagetitle="#_pagetitle_#",websitename="#_websitename_#",menu="\{menu\}",page="\{page\}"):
    "Return the global appearance of the website"
    return """<!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>{pagetitle}</title>
        <!-- BOOTSTRAP STYLES-->
        <link href="assets/css/bootstrap.css" rel="stylesheet" />
        <!-- FONTAWESOME STYLES-->
        <link href="assets/css/font-awesome.css" rel="stylesheet" />
        <!-- CUSTOM STYLES-->
        <link href="assets/css/custom.css" rel="stylesheet" />
        <!-- GOOGLE FONTS-->
        <link href='http://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css' />
    </head>
    <body>
        <div id="wrapper">
            <div class="navbar navbar-inverse navbar-fixed-top">
                <div class="adjust-nav">
                    <div class="navbar-header">
                        <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".sidebar-collapse">
                            <span class="icon-bar"></span>
                            <span class="icon-bar"></span>
                            <span class="icon-bar"></span>
                        </button>
                        <a class="navbar-brand" href="#"><i class="fa fa-square-o "></i>&nbsp;{websitename}</a>
                    </div>
                    <!-- <div class="navbar-collapse collapse">
                    <ul class="nav navbar-nav navbar-right">
                    <li><a href="#">Login</a></li>
                </ul>
            </div> -->
        </div>
    </div>
    <!-- /. NAV TOP  -->
    <nav class="navbar-default navbar-side" role="navigation">
        <div class="sidebar-collapse">
            <ul class="nav" id="main-menu">
                {MENU}
            </ul>
        </div>
    </nav>
    <!-- /. NAV SIDE  -->
    <div id="page-wrapper" >
        {PAGE}
    </div>
    <!-- /. PAGE WRAPPER  -->
    </div>
    <!-- /. WRAPPER  -->
    <!-- SCRIPTS -AT THE BOTOM TO REDUCE THE LOAD TIME-->
    <!-- JQUERY SCRIPTS -->
    <script src="assets/js/jquery-1.10.2.js"></script>
    <!-- BOOTSTRAP SCRIPTS -->
    <script src="assets/js/bootstrap.min.js"></script>
    <!-- METISMENU SCRIPTS -->
    <script src="assets/js/jquery.metisMenu.js"></script>
    <!-- CUSTOM SCRIPTS -->
    <script src="assets/js/custom.js"></script>
    </body>
    </html>""".format(MENU=menu,PAGE=page,websitename=websitename,pagetitle=pagetitle)


def menu(previous="",menulist="\{menulist\}",articles="#_articles_#"):
    "Return the menu list"
    return """<li class="text-center user-image-back">
        <img src="assets/img/logo.png" class="img-responsive" />
    </li>
    {previous}
    <li  class="active">
        <a href="#"><i class="fa fa-folder"></i>{articles}<span class="fa arrow"></span></a>
        <ul class="nav nav-second-level">
        {menulist}
        </ul>
    """.format(previous=previous,menulist=menulist,articles=articles)

def content(content="\{content\}",title="\{title\}"):
    return """<div id="page-inner">
        <div class="row">
            <div class="col-md-12">
                <h2>{title}</h2>
                {content}
            </div>
        </div>
        <hr />
    </div>""".format(content=content,title=title)

# Inner functions
icons={"image":"picture-o","audio":"music","text":"book","video":"film","folder":"folder","other":"file","previous":"arrow-left"} #"gear":"gear","edit":"edit"

def geticon(datatype):
    "Get an Icon for the given datatype"
    try:
        return icons[datatype]
    except:
        return icons["other"]

def menuitem(text,link,datatype):
    "Generate a menu link"
    print (datatype)
    return """<li><a href="{link}"><i class="fa fa-{datatype} "></i>{text}</a></li>""".format(text=text,link=link,datatype=geticon(datatype))

def makeSubNodelist(subnode,lang,getdatatype):
    items=[]
    for node in subnode.get_next_nodes():
        if node.name[0]!="_":
            items.append(menuitem(node.get_title(lang),node.path,getdatatype(node.path)))
    for node in subnode.get_next_subtree():
        #print(node,node.name)
        if node.name[0]!="_":
            items.append(menuitem(node.get_title(lang),node.path,"folder"))
    return items
