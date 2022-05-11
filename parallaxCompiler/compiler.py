from cgi import parse_header
import json

strictKeywords = {
    "main": [
        {"pageTitle": "str"},
        {"content": "list"},
        {"parallax": "list"}
    ],
    "parallax": [
        {"url": "str"},
        {"heading": "str"}
    ],
    "content": [
        {"title": "str"},
        {"text": "str"},
        {"list": "dict"},
        {"img": "dict"},
        {"link": "dict"}
    ],
    "list": {
        "ordered": "bool",
        "entries": "list"
    },
    "img": {
        "url": "str",
        "width": "int",
        "height": "int"
    },
    "link": {
        "src": "str",
        "newTab": "bool",
        "content": "list"
    }, 
    "special": [
        "scrollpoint",
        "hr",
        "trigger",
        "script",
        "style"
    ]
}

keywords = [
    {"parallax": "dict"},
    {"content": "list"},
    {"pageTitle": "str"},
    {"title": "str"},
    {"text": "str"},
    {"list": "dict"},
    {"img": "dict"},
    {"link": "dict"}
]

def getKeywords():
    return keywords

def getStrictKeywords():
    return strictKeywords

def getSpecials():
    return strictKeywords["special"]

def getKeys(keyList):
    returnList = []
    for entry in keyList:
        returnList.append(list(entry.keys())[0])
    return returnList

def getType(line, callPoint):
    if type(line) == dict:
        key = list(line.keys())[0]
        if key in getKeys(strictKeywords[callPoint]):
            return {
                "key": key,
                "special": False,
                "type": "dict"
            }
    if line in strictKeywords["special"]:
        return {
            "special": True
        }
    if list(line.keys())[0] in strictKeywords["special"]:
        return {
            "special": True
        }
    print(f"There's an illegal string type on the line that looks like\n{line}")
    return False

def parseParallax(line):
    line = line["parallax"]
    html = ""
    try:
        if line["heading"]:
            heading = f"<h1>{line['heading']}</h1>"
    except:
        heading = ""
    try:
        if line["url"]:
            html = f'<div class="parallax" style="background-image: url({line["url"]});">{heading}</div>'
        return {
            "place": "body",
            "content": html
        }
    except:
        return False

def parsePageTitle(line):
    return {
        "place": "head",
        "content": f"<title>{line['pageTitle']}</title>"
    }

def parseContent(line):
    html = ""
    lines = line["content"]
    del line
    for line in lines:
        typeOf = getType(line, "content")
        if typeOf:
            if typeOf["special"]:
                html += parseSpecials(line)
            else:
                html += f"""{parseTypes[typeOf["key"]](line)}
                """
    return {
        "place": "body",
        "content": html
    }

def parseTitle(line):
    return f"""<h1 class="h1">{line["title"]}</h1>"""

def parseText(line):
    return f"""<p>{line["text"]}</p>"""

def parseLink(line):
    newTab = ""
    line = line["link"]
    if line["newTab"]:
        newTab = """ target="_blank\""""
    return f"""<a href="{line["src"]}{newTab}">{parseContent(line)["content"]}</a>"""

def parseList(line):
    li = line["list"]
    try:
        if li["ordered"]:
            ordered = True
        else:
            ordered = False
    except:
        ordered = False
    if ordered:
        line = "<ol>"
    else:
        line = "<ul>"
    for point in li["entries"]:
        line += f"<li>{point}</li>"
    if ordered:
        line += "</ol>"
    else:
        line += "</ul>"
    return line

def parseImg(line):
    try:
        if line["img"]["width"]:
            width = f" width={line['img']['width']}"
        else:
            width = ""
    except:
        width = ""
    try:
        if line["img"]["height"]:
            height = f" height={line['img']['height']}"
        else:
            height = ""
    except:
        height = ""
    return f"""<img src="{line["img"]["url"]}"{width}{height}>"""

def parseSpecials(line):
    if line in strictKeywords["special"]:
        return parseTypes[line]()
    elif list(line.keys())[0] in strictKeywords["special"]:
        return parseTypes[list(line.keys())[0]](line)
    else:
        return ""

def parseTrigger(line):
    global totalScrollpoints
    html = f"""<div id="scroll{totalScrollpoints}" trigger="{line["trigger"]}"></div>"""
    totalScrollpoints += 1
    return html

def parseScript(line):
    return f"""<script>{line["script"]}</script>"""

def parseStyle(line):
    return f"""<style>{line["style"]}</style>"""

def parseHR():
    return "<hr>"

def parseScrollpoint():
    global totalScrollpoints
    html = f"""<div id="scroll{totalScrollpoints}"></div>"""
    totalScrollpoints += 1
    return html

parseTypes = {
    "parallax": parseParallax,
    "content": parseContent,
    "pageTitle": parsePageTitle,
    "title": parseTitle,
    "text": parseText,
    "list": parseList,
    "img": parseImg,
    "specials": parseSpecials,
    "hr": parseHR,
    "trigger": parseTrigger,
    "scrollpoint": parseScrollpoint,
    "link": parseLink,
    "script": parseScript,
    "style": parseStyle
}

def compile(data):
    try:
        assert (type(data) == list)
    except:
        raise Exception(f"parseInput requires a list. You gave it {type(data)}.")
    head = ""
    body = ""
    global totalScrollpoints
    totalScrollpoints = 0
    for line in data:
        lineData = getType(line, "main")
        if lineData:
            if lineData["special"]:
                body += f"{parseSpecials(line)}\n"
            else:
                HTMLine = parseTypes[lineData["key"]](line)
                if HTMLine:
                    if HTMLine["place"] == "head":
                        head += f"{HTMLine['content']}\n"
                    elif HTMLine["place"] == "body":
                        body += f"{HTMLine['content']}\n"

    if totalScrollpoints > 0:
        script = "<script>" + """
        console.log("This site was built with the Parallax Compiler by James Young");
        console.log("https://github.com/onlytruejames/parallaxCompiler");
        console.log("https://james.chaosgb.co.uk");
        
        var stage = 0;
        var prEval = false;

function keyPress(e){
	pressed = false;
    if (e.key === "n"){
		stage++;
		pressed = true;
	}
	if (e.key === "p"){
		stage--;
		pressed = true;
	}
	if (stage<0){
		stage = 0;
	}
	if (stage>maxStage){
		stage = maxStage;
	}
	if (pressed===true){
        var elem = document.getElementById(`scroll${stage}`);
        elem.scrollIntoView({behavior: "smooth"});
        if (prEval){
            eval(`${prEval}(false${prEndBits})`);
            prEval = false;
        }
        if (elem.getAttribute("trigger")){
            trig = elem.getAttribute("trigger");
            if (trig.endsWith(")") && !trig.endsWith("()")){
                endBits = trig.split("(");
                endBits = endBits[endBits.length - 1].split(")");
                endBits = `, ${endBits[endBits.length - 2]}`;
            }
            else{
                endBits = "";
            }
            eval(`${trig}(true${endBits});`);
            prEval = elem.getAttribute("trigger");
            prEndBits = endBits;
        }
	}
}
document.addEventListener('keydown', keyPress);""".replace("maxStage", str(totalScrollpoints)) + "</script>"
    else:
        script = ""

    css = """body{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    margin: 0%;
}
h1{
    background-color: black;
    text-align: center;
    margin: 0%;
    color: white;
}
.parallax{
    height: 1024px;
    background-attachment: fixed;
    background-repeat: none;
    background-size: cover;
    background-position: top;
}
.content {
    margin: 10px;
}
.h1{
    background-color: transparent;
    text-align: center;
    margin: 0%;
    color: black;
}
iframe{
    border: 1px solid black;
    margin-left: auto;
    margin-right: auto;
    display: block;
    width: 90%;
    height: 480px;
}
a {
    color: blue;
    text-decoration: none;
}
a:hover {
    color: orangered;
}
hr{
    width: 75%;
}
li{
    line-height: 50px;
}
img{
    border: 1px solid black;
    margin-left: auto;
    margin-right: auto;
    display: block;
}
p, li{
    margin-left: 2%;
    margin-right: 2%;
}"""

    return f"""<html><head>
    {head}
    <style>
    {css}
    </style>
    {script}
    </head>
    <body>
    {body}
    </body>
    </html>""".replace("\n    ", "").replace("\n", "")
