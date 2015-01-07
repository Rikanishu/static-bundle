#!/usr/bin/env python
# encoding: utf-8

import sys
sys.path.append('..')

from static_bundle import (JsBundle,
                           StandardBuilder,
                           BuilderConfig,
                           CssBundle,
                           OtherFilesBundle)

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

# all files in directory others
other1 = OtherFilesBundle("others")

def create_builder(conf):
    builder = StandardBuilder(conf)
    builder.create_asset("Styles", minify=True).add_bundle(css1)
    builder.create_asset("Vendors", minify=True, merge=True).add_bundle(js1)
    builder.create_asset("Application", minify=True, merge=True).add_bundle(js2)
    builder.create_asset("AllOtherFiles").add_bundle(other1)
    return builder


def check():
    conf = BuilderConfig(input_dir="src", output_dir="public", env="development", copy_only_bundles=True)
    development_builder = create_builder(conf)
    development_builder.collect_links()

    print("=" * 60)
    print(" Development static data ")
    print("=" * 60)
    print(development_builder.render_asset("Styles"))
    print("Vendors:")
    print(development_builder.render_asset("Vendors"))
    print("Application:")
    print(development_builder.render_asset("Application"))

    conf.env = "production"
    production_builder = create_builder(conf)
    production_builder.make_build()
    production_builder.collect_links()

    print("=" * 60)
    print(" Production static data [with bundle generation] ")
    print("=" * 60)
    print("Styles:")
    print(production_builder.render_asset("Styles"))
    print("Vendors:")
    print(production_builder.render_asset("Vendors"))
    print("Application:")
    print(production_builder.render_asset("Application"))


if __name__ == '__main__':
    check()