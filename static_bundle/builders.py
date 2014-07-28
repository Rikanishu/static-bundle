# encoding: utf-8

import os
from static_bundle.utils import _write, _copy_file


class Asset(object):
    """
    Asset / Build group type
    Bundles in different build groups can be minified or prepared with different methods
    Objects has a fluent interface

    @param name: unique name of build group in bundle
    @param multitype: When multitype disabled, bundles will be checked for all having same type
        for example JS or CSS
    @param minify: Use minify with [minifier]

    @type builder: StandardBuilder
    @type name: one of (unicode, str)
    @type minifier: one of (static_bundle.minifiers.DefaultMinifier, None)
    @type multitype: bool
    @type minify: bool
    @type files_encoding: str
    """

    def __init__(self, builder, name,
                 minifier=None, multitype=False,
                 minify=False, files_encoding="utf-8"):
        self.builder = builder
        self.name = name
        self.multitype = multitype
        self.minify = minify or minifier is not None
        self.minifier = minifier
        self.files_encoding = files_encoding

        self.bundles = []
        self.files = []

    def add_bundle(self, bundle):
        """
        Add some bundle to build group

        @type bundle: static_bundle.bundles.AbstractBundle
        @rtype: BuildGroup
        """
        if not self.multitype and self.has_bundles():
            first_bundle = self.get_first_bundle()
            if first_bundle.get_type() != bundle.get_type():
                raise Exception(
                    'Different bundle types for one BuildGroup: %s[%s -> %s]'
                    'check types or set multitype parameter to True'
                    % (self.name, first_bundle.get_type(), bundle.get_type())
                )
        self.bundles.append(bundle)
        return self

    def collect_files(self):
        """
        Return collected files links

        @rtype: list[static_bundle.files.StaticFileResult]
        """
        self.files = []
        for bundle in self.bundles:
            bundle.init_build(self, self.builder)
            bundle_files = bundle.prepare()
            self.files.extend(bundle_files)
        return self

    def get_minifier(self):
        if self.minifier is None:
            if not self.has_bundles():
                raise Exception("Unable to get default minifier, no bundles in build group")
            minifier = self.get_first_bundle().get_default_minifier()
        else:
            minifier = self.minifier
        minifier.init_asset(self)
        return minifier

    def has_bundles(self):
        return len(self.bundles) > 0

    def get_first_bundle(self):
        return self.bundles[0]

    def enable_minify(self):
        self.minify = True
        return self

    def disable_minify(self):
        self.minify = False
        return self


class StandardBuilder(object):
    """
    Builder
    Provide build / collect links strategy for static files

    @type config: static_bundle.configs.BuilderConfig
    """

    def __init__(self, config):
        self.config = config
        self.assets = {}

    def create_asset(self, name, **kwargs):
        """
        Create asset

        @type name: one of(unicode, str)
        @rtype: Asset
        """
        group = Asset(self, name, **kwargs)
        self.assets[name] = group
        return group

    def remove_asset(self, name):
        """
        Remove asset by name

        @type name: one of(unicode, str)
        """
        if name in self.assets:
            del self.assets[name]

    def get_asset(self, name):
        """
        Get asset by name

        @type name: one of(unicode, str)
        """
        assert self.has_asset(name), "Asset is not created yet, use has_asset for checking"
        return self.assets[name]

    def has_asset(self, name):
        """
        Check asset exists by name

        @type name: one of(unicode, str)
        """
        return name in self.assets

    def render_asset(self, name):
        result = ""
        if self.has_asset(name):
            asset = self.get_asset(name)
            if asset.files:
                for f in asset.files:
                    result += f.render_include() + "\r\n"
        return result

    def render_include_group(self, name):
            return self.render_asset(name)

    def collect_links(self, env=None):
        """
        Return links without build files
        """
        for asset in self.assets.values():
            if asset.has_bundles():
                asset.collect_files()
        if env is None:
            env = self.config.env
        if env == "production":
            self._minify(emulate=True)
        self._add_url_prefix()

    def make_build(self):
        """
        Move files / make static build
        """
        copy_excludes = {}
        for asset in self.assets.values():
            if asset.has_bundles():
                asset.collect_files()
                if asset.minify and asset.files:
                    for f in asset.files:
                        copy_excludes[f.abs_path] = f
        if not os.path.exists(self.config.output_dir):
            os.makedirs(self.config.output_dir)
        for root, dirs, files in os.walk(self.config.input_dir):
            for fpath in files:
                current_file_path = os.path.join(root, fpath)
                if current_file_path not in copy_excludes:
                    _copy_file(current_file_path,
                               current_file_path.replace(self.config.input_dir, self.config.output_dir, 1))
        self._minify()

    def _minify(self, emulate=False):
        for asset in self.assets.values():
            if asset.minify and asset.files:
                bundle = asset.get_first_bundle()
                asset_file = bundle.get_result_class()
                asset_file_name = asset.name + "." + bundle.get_extension()
                asset_file_abs_path = os.path.join(self.config.output_dir, asset_file_name)
                asset_file_rel_path = '/' + asset_file_name
                if not emulate:
                    group_minifier = asset.get_minifier()
                    text = group_minifier.before()
                    for f in asset.files:
                        text = group_minifier.contents(f, text)
                    text = group_minifier.after(text)
                    _write(asset_file_abs_path, text, asset.files_encoding)
                asset.files = [asset_file(asset_file_rel_path, asset_file_abs_path)]

    def _add_url_prefix(self):
        for asset in self.assets.values():
            if asset.files:
                for file_result in asset.files:
                    file_result.rel_path = self.config.url_prefix + file_result.rel_path.lstrip('/')