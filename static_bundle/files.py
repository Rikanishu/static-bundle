# encoding: utf-8

import static_bundle
from static_bundle.utils import _get_path_extension


class StaticFileResult(object):
    """
    Result file class
    This type represents each file after build

    @type: path_relative: one of (unicode, str)
    @type: path_absolute: one of (unicode, str, None)
    """

    def __init__(self, path_relative, path_absolute=None):
        self.rel_path = path_relative
        self.abs_path = path_absolute

    def render_include(self):
        """
        Render file include in template
        """
        return ''

    @property
    def type(self):
        raise NotImplementedError

    @property
    def extension(self):
        path = self.abs_path or self.rel_path
        return _get_path_extension(path) if path else ''


class CssFileResult(StaticFileResult):

    def render_include(self):
        return '<link rel="stylesheet" href="%s" />' % self.rel_path

    @property
    def type(self):
        return static_bundle.TYPE_CSS


class JsFileResult(StaticFileResult):

    def render_include(self):
        return '<script type="text/javascript" src="%s"></script>' % self.rel_path

    @property
    def type(self):
        return static_bundle.TYPE_JS