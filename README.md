# static-bundle #
**Another yet static manager for Python**

---
A set of base utilities which provide static management and builds making.
Can be extended with own PrepareHandler's and Bundle's.

### Installation ###

Via pip:
```
    pip install static-bundle
```
or from sources
```
    python setup.py install
```

### Extensions ###

 - [Flask extension](https://github.com/Rikanishu/flask-static-bundle)

### Example ###

See examples/bundles or check this example

Static directory tree:

```
├── css
│   ├── example1.css
│   ├── example1.less
│   └── example2.css
└── js
    ├── include
    │   ├── app.js
    │   └── modules
    │       ├── module1.js
    │       ├── module2.js
    │       └── module3.js
    └── vendors
        ├── example1.js
        └── example2.js
```

Example code:

```python
from static_bundle import (JsBundle,
                           StandardBuilder,
                           BuilderConfig,
                           CssBundle,
                           LessCompilerPrepareHandler)

css1 = CssBundle("css")
css1.add_file("example1.less")
css1.add_file("example2.css")
# add for less preparing
css1.add_prepare_handler(LessCompilerPrepareHandler())

js1 = JsBundle("js")
js1.add_file("vendors/example1.js")
js1.add_file("vendors/example2.js")

js2 = JsBundle("js/include")
# modules depends on app.js
js2.add_file("app.js")
js2.add_directory("modules")

...

# for development env:
conf = BuilderConfig(input_dir="src", output_dir="public", env="development")

# for production env:
conf = BuilderConfig(input_dir="src", output_dir="public", env="production")

builder = StandardBuilder(conf)
builder.create_group("Styles").add_bundle(css1)
builder.create_group("Vendors", minify=True).add_bundle(js1)
builder.create_group("Application", minify=True).add_bundle(js2)

# run make_build once, before production deploy and use collect_links on runtime
# builder.make_build()

builder.collect_links()

...

# and in template:
# this methods render script and style tags with paths, see their output

#on head
builder.render_include_group("Styles")

#on body end
builder.render_include_group("Vendors")
builder.render_include_group("Application")

```

`builder.render_include_group(...)` output:
```
Styles:
<link rel="stylesheet" href="/css/example1.css" />
<link rel="stylesheet" href="/css/example2.css" />

Vendors:
<script type="text/javascript" src="/js/vendors/example1.js"></script>
<script type="text/javascript" src="/js/vendors/example2.js"></script>

Application:
<script type="text/javascript" src="/js/include/app.js"></script>
<script type="text/javascript" src="/js/include/modules/module1.js"></script>
<script type="text/javascript" src="/js/include/modules/module2.js"></script>
<script type="text/javascript" src="/js/include/modules/module3.js"></script>

```

and when production environment used:

```
Styles:
<link rel="stylesheet" href="/css/example1.css" />
<link rel="stylesheet" href="/css/example2.css" />

Vendors:
<script type="text/javascript" src="/Vendors.js"></script>

Application:
<script type="text/javascript" src="/Application.js"></script>

```
