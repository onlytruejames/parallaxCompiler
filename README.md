# parallaxCompiler

A way to make cool presentations with JSON

A couple of years ago, I saw a [news story](https://www.bbc.co.uk/news/resources/idt-sh/who_stole_burmas_royal_ruby) on the BBC. One of their long reads. You scrolled down and cool things happened in the background. A few months later, I made one myself for school, and I've made a few more since then. I wrote this compiler so I could make them quicker, and I'm happy with the result. It needs improving, but it works. It also allows scrolling by button pressing (n for next and p for previous, support *will* be added for customisation soon).

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

---

## pageTitle

pageTitle accepts a string. It corresponds to `<title>`.

---

## content

content is where your content goes. It accepts a list of tags. These are:
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

`title` accepts a string. It corresponds to `<h1>`.

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

`content` accepts a list. In turn, the list accepts strings. Each item corresponds to `<li>`.

---

### img

`img` accepts a dictionary. It corresponds to `<img>`. The dictionary should be like this:

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

`link` defines a link. It is formatted like this:
```json
{"link": {
  "src": "https://james.chaosgb.co.uk",
  "newTab": true,
  "content": [
    {"text": "Hello"}
  ]
}}
```
Anything that can go in `content` can go in here. I see a lot of potential for this to go wrong, such as parallaxes being links, but 

---

## parallax

`parallax` defines a parallax transition. It accepts a dictionary. The dictionary should look like this:

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

Special tags are made up of strings and can be used in nearly every context. There are currently 2 special tags: `scrollpoint` and `hr`. This is how you use them:

```json
[
  "special"
]
```

---

### scrollpoint

`scrollpoint` tells the button-activated scrolling that it can scroll to this point in the page.

---

### hr

`hr` adds a horizontal line to the page. It corresponds to `<hr>`.
