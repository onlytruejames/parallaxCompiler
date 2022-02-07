from ast import Raise
import json

data = json.load(open(input("Input the name of the JSON file you want to load:\n"), "r"))

acceptedKeywords = {
    "body": [
        {"pageTitle": "str"},
        {"content": "list"},
        {"parallax": "list"}
    ],
    "parallax": [
        {"url": "str"},
        {"title": "str"}
    ],
    "content": [
        {"title": "str"},
        {"text": "str"},
        {"list": "list"},
        {"img": "list"}
    ],
    "list": [
        {"ordered": "bool"},
        {"content": "list"}
    ],
    "img": [
        {"url": "str"},
        {"width": "int"},
        {"height": "int"}
    ],
    "special": [
        "scrollpoint",
        "line"
    ]
}

head = ""
body = ""

totalScrollpoints = 0

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

def parseScrollpoint():
    return f"""<div id="scroll{totalScrollpoints}"></div>"""

def parseParallax(line):
    line = line["parallax"]
    html = ""
    if line["url"]:
        if line["title"]:
            html = f'<div class="parallax" style="background-image: url({line["url"]});"><h1>{line["title"]}</h1></div>'
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
        if typeOf["special"] == False:
            html += f"""{parseTypes[typeOf["key"]](line)}
            """
        elif typeOf["special"]:
            html += f"""{parseTypes[line]()}
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

def parseBreakLine():
    return "<hr>"

parseTypes = {
    "parallax": parseParallax,
    "content": parseContent,
    "pageTitle": parsePageTitle,
    "title": parseTitle,
    "text": parseText,
    "list": parseList,
    "scrollpoint": parseScrollpoint,
    "img": parseImg,
    "breakLine": parseBreakLine
}

lineNum = 0
for line in data:
    print(line)
    lineData = getType(line, "body")
    if lineData:
        if lineData["special"]:
            if line == "scrollpoint":
                body += f"{parseScrollpoint()}\n"
                totalScrollpoints += 1
        else:
            HTMLine = parseTypes[lineData["key"]](line)
            if HTMLine:
                if HTMLine["place"] == "head":
                    head += f"{HTMLine['content']}\n"
                elif HTMLine["place"] == "body":
                    body += f"{HTMLine['content']}\n"
    lineNum += 1

html = f"""<html><head>
{head}
<style>
{open("style.css", "r").read()}
</style>
</head>
<body>
{body}
</body>
</html>"""

open("out.html", "w").write(html)