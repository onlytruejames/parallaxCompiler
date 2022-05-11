# parallaxCompiler

A way to make cool presentations with JSON

A couple of years ago, I saw a [news story](https://www.bbc.co.uk/news/resources/idt-sh/who_stole_burmas_royal_ruby) on the BBC, and I thought it was a pretty cool type of presentation. A few months later, I made one myself for school, and I've made a few more since then. I wrote this compiler so I could make them quicker, and I'm happy with the result. It needs improving, but it works. It also allows scrolling by button pressing (n for next and p for previous, support *should* be added for customisation soon).
This documentation provides reference for calling the compiler, reference for the syntax so it can compile, and reference for what each keyword compiles to, so the document can be easily modified.

---

# Module docs

## compile

`compile` accepts a list and returns a string. It formats all the **valid** data. If something is incorrect, it *should* ignore it and carry on. If it doesn't, put the error on the issues section. This is how you use it:
```python
parallaxCompiler.compile([
  {"parallax": {
    "url": "https://shutplea.se",
    "heading": "This is a test"
  }},
  {"content": [
    {"text": "This is an example!"}
  ]}
])
```

---

## getKeywords

`getKeywords` can be useful when you need a list of supported keywords in your version. It does *not* include special tags.

```python
parallaxCompiler.getKeywords()
```

---

## getSpecials

`getSpecials` can be useful when you need a list of special tags.

```python
parallaxCompiler.getSpecials()
```

---

## getStrictKeywords

`getStrictKeywords` can be useful when you need a list of supported keywords in your version *and* what they contain. Good luck trying to use the data it gives you, it's a nightmare...

```python
parallaxCompiler.getStrictKeywords()
```

---

# Formatting Docs

## Format

As of now, to make a presentation, you start with a JSON file with a list in it:

```json
[

]
```

You can add a few tags into here, which each have tags that can be added into them. There are also special tags, which are supposed to be able to be used anywhere.

---

## Main

Main is the JSON list you start with. In here, there can be three tags:
```json
[
  {"pageTitle": ""},
  {"content": []},
  {"parallax": {}}
]
```

On it's own, the list will pass:

```html
"<html><head><style>body{font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;margin: 0%;}h1{background-color: black;text-align: center;margin: 0%;color: white;}.parallax{height: 1024px;background-attachment: fixed;background-repeat: none;background-size: cover;background-position: top;}.content {margin: 10px;}.h1{background-color: transparent;text-align: center;margin: 0%;color: black;}iframe{border: 1px solid black;margin-left: auto;margin-right: auto;display: block;width: 90%;height: 480px;}a {color: blue;text-decoration: none;}a:hover {color: orangered;}hr{width: 75%;}li{line-height: 50px;}img{border: 1px solid black;margin-left: auto;margin-right: auto;display: block;}p, li{margin-left: 2%;margin-right: 2%;}</style></head><body></body></html>```

---

## pageTitle

pageTitle accepts a string. It corresponds to `<title>` and is added into `<head>`.

---

## content

content is where your content goes, and it corresponds to `<div class="content">`. It accepts a list of tags. These are:
```json
[
  {"title": ""},
  {"text": ""},
  {"list": {}},
  {"img": {}}
]
```

---

### title

`title` is a dictionary which accepts a string. It corresponds to `<h1 class="h1"></h1>`.

---

### text

`text` accepts a string. It corresponds to `<p>`.

---

### list

`list` accepts a dictionary. It corresponds to `<ul>` or `<ol>`. The dictionary should be like this:

```json
{
  "ordered": "bool",
  "entries": []
}
```

`ordered` accepts a boolean, but it is not mandatory. It determines whether the list is ordered or unordered. By default it is unordered.

`entries` accepts a list. In turn, the list accepts strings. Each item corresponds to `<li>`.

---

### img

`img` accepts a dictionary. It corresponds to `<img src="" width="" height="">`. The dictionary should be like this:

```json
{
  "url": "",
  "width": "int",
  "height": "int"
}
```

`url` determines the URL of the image. It accepts a string.

`width` determines the width of the image. It accepts an integer. It is not mandatory.

`height` determines the height of the image. It accepts an integer. It is not mandatory.

---

### link

`link` defines a link. It corresponds to `<a href="" target=""><div class="content"></div</a>`. It is formatted like this:
```json
{"link": {
  "src": "https://james.chaosgb.co.uk",
  "newTab": true,
  "content": [
    {"text": "Hello"}
  ]
}}
```
The `content` parameter is the same as `content` from earlier on. 

---

## parallax

`parallax` defines a parallax transition, corresponding to `<div class="parallax" style="background-image: url({url});">{heading}</div>`. It accepts a dictionary. The dictionary should look like this:

```json
{
  "url": "",
  "heading": ""
}
```

`url` defines the background url of the transition. It accepts a string.

`heading` defines the heading of the transition. It corresponds to `<h1>`. It is not mandatory.

---

## Special tags

Special tags are made can be used in nearly every context. There are currently 4 special tags. They are currently the only ones that can be just strings.

---

### scrollpoint

`scrollpoint` tells the button-activated scrolling that it can scroll to this point in the page.

```json
[
  "scrollpoint"
]
```

---

### trigger

`trigger` does the same as `scrollpoint` but it's a dictionary and triggers a preset function when scrolled to. It accepts a function with or without brackets at the end. The function will always be called with a boolean first parameter. If you need any other parameters, just put them in brackets at the end. Examples below.

```json
[
  {"trigger": "run"}, //calls run(true) when scrolled to and run(false) when scrolled from
  {"trigger": "run()"}, //calls run(true) when scrolled to and run(false) when scrolled from
  {"trigger": "run(1, 'string')"} //calls run(true, 1, 'string') when scrolled to and run(false, 1, 'string') when scrolled from
]
```

---

### hr

`hr` adds a horizontal line to the page. It corresponds to `<hr>`.

### script

`script` is used for Javascript. It corresponds to `<script>`.

### style

`style` is used for CSS. It corresponds to `<style>`