#!/usr/bin/env python
# encoding: utf-8
import os
import sys

# for testing
PACKAGE_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(PACKAGE_ROOT)

from static_bundle import (JsBundle,
                           StandardBuilder,
                           BuilderConfig,
                           CssBundle,
                           LessCompilerPrepareHandler)

css1 = CssBundle("css")
css1.add_file("example1.less")
css1.add_file("example2.css")

js1 = JsBundle("js")
js1.add_file("vendors/example1.js")
js1.add_file("vendors/example2.js")

js2 = JsBundle("js/include")
# modules depends on app.js
js2.add_file("app.js")
js2.add_directory("modules")


def create_builder(conf):
    builder = StandardBuilder(conf)
    builder.create_group("Styles").add_bundle(css1)
    builder.create_group("Vendors", minify=True).add_bundle(js1)
    builder.create_group("Application", minify=True).add_bundle(js2)
    return builder


def check():
    conf = BuilderConfig(input_dir="src", output_dir="public", env="development")
    development_builder = create_builder(conf)
    development_builder.collect_links()

    print("=" * 60)
    print(" Development static data ")
    print("=" * 60)
    print(development_builder.render_include_group("Styles"))
    print("Vendors:")
    print(development_builder.render_include_group("Vendors"))
    print("Application:")
    print(development_builder.render_include_group("Application"))

    conf.env = "production"
    production_builder = create_builder(conf)
    production_builder.make_build()
    production_builder.collect_links()

    print("=" * 60)
    print(" Production static data [with bundle generation] ")
    print("=" * 60)
    print("Styles:")
    print(production_builder.render_include_group("Styles"))
    print("Vendors:")
    print(production_builder.render_include_group("Vendors"))
    print("Application:")
    print(production_builder.render_include_group("Application"))


if __name__ == '__main__':
    check()