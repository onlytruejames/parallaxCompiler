from cgi import parse_header
import json

data = json.load(open(input("Input the name of the JSON file you want to load:\n"), "r"))

global totalScrollpoints
totalScrollpoints = 0

acceptedKeywords = {
    "body": [
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
        {"list": "list"},
        {"img": "list"}
    ],
    "list": {
        "ordered": "bool",
        "content": "list"
    },
    "img": {
        "url": "str",
        "width": "int",
        "height": "int"
    },
    "special": [
        "scrollpoint",
        "hr"
    ]
}

head = ""
body = ""

def getKeys(keyList):
    returnList = []
    for entry in keyList:
        returnList.append(list(entry.keys())[0])
    return returnList

def getType(line, callPoint):
    if type(line) == dict:
        key = list(line.keys())[0]
        if key in getKeys(acceptedKeywords[callPoint]):
            return {
                "key": key,
                "special": False,
                "type": "dict"
            }
    elif type(line) == str:
        if line in acceptedKeywords["special"]:
            return {
                "special": True
            }
    print(f"There's an illegal string type on the line that looks like\n{line}")
    return False

def parseParallax(line):
    line = line["parallax"]
    html = ""
    if line["url"]:
        if line["heading"]:
            html = f'<div class="parallax" style="background-image: url({line["url"]});"><h1>{line["heading"]}</h1></div>'
        else:
            html =  f'<div class="parallax" style="background-image: url({line["url"]});"></div>'
        return {
            "place": "body",
            "content": html
        }
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
    for point in li["content"]:
        line += f"<li>{point}</li>"
    if ordered:
        line += "</ol>"
    else:
        line += "</ul>"
    return line

def parseImg(line):
    if line["img"]["width"]:
        width = f" width={line['img']['width']}"
    else:
        width = ""
    if line["img"]["height"]:
        height = f" width={line['img']['height']}"
    else:
        height = ""
    return f"""<img src="{line["img"]["url"]}"{width}{height}>"""

def parseSpecials(line):
    if line in acceptedKeywords["special"]:
        return parseTypes[line]()
    else:
        return ""

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
    "scrollpoint": parseScrollpoint
}

lineNum = 0
for line in data:
    print(line)
    lineData = getType(line, "body")
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
    lineNum += 1

if totalScrollpoints > 0:
    script = "<script>" + open("controller.js", "r").read().replace("maxStage", str(totalScrollpoints)) + "</script>"
else:
    script = ""

html = f"""<html><head>
{head}
<style>
{open("style.css", "r").read()}
</style>
{script}
</head>
<body>
{body}
</body>
</html>"""

open("out.html", "w").write(html)