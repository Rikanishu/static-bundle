# static-bundle #
**Yet another asset management library for Python**

---
A set of base utilities which provide asset management and builds making.

It primary aims to single-page applications and was developed to create conveinment working environment primary for AngularJS but it may work with another architectures, not even with SPA, on development and build release (production) modes. 

It has extensible architectre, some system classes can be extended for your needs. 

The library is not production ready yet.

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

See ```examples/bundles``` or check this example.

Suppose your application has the following asset files directory tree:

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

So you need to declare some bundles config to gain builds making and collecting links:

```python
from static_bundle import (JsBundle,
                           StandardBuilder,
                           BuilderConfig,
                           CssBundle)

css1 = CssBundle("css")
css1.add_file("example1.less")
css1.add_file("example2.css")

js1 = JsBundle("js")
js1.add_file("vendors/example1.js")
js1.add_file("vendors/example2.js")

js2 = JsBundle("js/include")
# modules depends on app.js
js2.add_file("app.js")
# this step adds all JS files in modules dir
js2.add_directory("modules")

...

# for development env:
conf = BuilderConfig(input_dir="src", output_dir="public", env="development")

# for production env:
conf = BuilderConfig(input_dir="src", output_dir="public", env="production")

builder = StandardBuilder(conf)
builder.create_asset("Styles").add_bundle(css1)
builder.create_asset("Vendors", minify=True).add_bundle(js1)
builder.create_asset("Application", minify=True).add_bundle(js2)

# run make_build once, before production deploy was maked and use collect_links on runtime

# builder.make_build()
builder.collect_links()

...

# and in template:
# this methods render script and style tags with paths, see their outputs

#on head
builder.render_asset("Styles")

#on body end
builder.render_asset("Vendors")
builder.render_asset("Application")

```

And also you need to render tags in template.
For example this is builder asset output in development environment
`builder.render_asset(...)` :

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

And the same function output when the production environment used:

```
Styles:
<link rel="stylesheet" href="/css/example1.css" />
<link rel="stylesheet" href="/css/example2.css" />

Vendors:
<script type="text/javascript" src="/Vendors.js"></script>

Application:
<script type="text/javascript" src="/Application.js"></script>

```
