from cgi import parse_header
import json

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
    ],
    "link": [
        "img",
        "text"
    ]
}

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

def parseLink(line):
    newTab = ""
    if line["newTab"]:
        newTab = """ target="_blank\""""
    html = f"""<a href="{line["src"]}{newTab}">"""
    for item in line:
        toAppend = getType(item, "link")
        if toAppend:
            html += parseTypes[toAppend["key"]](item)
    html += "</a>"
    return html

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
    "scrollpoint": parseScrollpoint,
    "list": parseList
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

    if totalScrollpoints > 0:
        script = "<script>" + """[
    {"pageTitle": "Test!"}, 
    "scrollpoint",
    {"parallax": {
        "url": "https://james.chaosgb.co.uk/logo.png",
        "heading": "Test"
    }},
    "scrollpoint",
    {"content": [
        {"title": "About test"},
        "hr",
        {"text": "This is some text talking about test"},
        {"text": "As you can see it goes over multiple lines"},
        {"text": "Here are some interesting things about test"},
        {"link": {
            "src": "https://james.chaosgb.co.uk",
            "newTab": true,
            "content": [
                {"img": {
                    "url": "https://james.chaosgb.co.uk/logo.png",
                    "width": 500,
                    "height": 500
                }},
                {"text": "Image"}
            ]
        }},
        "hr",
        {"list": {
            "ordered": false,
            "content": [
                "Hmmm",
                "Here's something interesting"
            ]
        }},
        "scrollpoint",
        "hr",
        {"img": {
            "url": "https://james.chaosgb.co.uk/logo.png",
            "width": 500,
            "height": 500
        }}
    ]}
]""".replace("maxStage", str(totalScrollpoints)) + "</script>"
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
    </html>"""