def container(pagetitle="#_pagetitle_#",websitename="#_websitename_#",menu="##MENU##",page="##PAGE##"):
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


def menu(previous="#_previous_#",menulist="\{menulist\}",articles="#_articles_#",preferences="#_preferences_#",about='#_about_#'):
    "Return the menu list"
    return """<li class="text-center user-image-back">
        <img src="assets/img/logo.png" class="img-responsive" />
    </li>
    <li><a href="index.html"><i class="fa fa-arrow-left "></i>{previous}</a></li>
    <li  class="active">
        <a href="#"><i class="fa fa-folder"></i>{articles}<span class="fa arrow"></span></a>
        <ul class="nav nav-second-level">
        {menulist}
        </ul>
        <li><a href="index.html"><i class="fa fa-gear "></i>{preferences}</a></li>
        <li><a href="#"><i class="fa fa-edit "></i>{about}</a></li>
    """.format(previous=previous,menulist=menulist,articles=articles,preferences=preferences,about=about)

# Inner functions
icons={"image":"picture-o","audio":"music","text":"book","video":"film","folder":"folder","other":"file"} #"gear":"gear","edit":"edit"

def geticon(datatype):
    try:
        return icons[datatype]
    except:
        return icons["other"]

def menuitem(text,link,datatype):
    "Generate a menu link"
    return """<li><a href="{link}"><i class="fa fa-{datatype} "></i>{text}</a></li>""".format(text=text,link=link,datatype=geticon(datatype))
