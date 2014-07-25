# encoding: utf-8

from static_bundle.utils import _read


class DefaultMinifier(object):
    """
    This is default class used in minify process
    Provides methods that called in each steps of minify

    @type build_group: static_bundle.builders.BuildGroup
    """

    def __init__(self, build_group):
        self.build_group = build_group

    def __call__(self, build_group):
        self.build_group = build_group

    def before(self):
        """
        Called before minify
        Returned text will be prepend on head

        @rtype: one of (unicode, str)
        """
        return ""

    def contents(self, f, text):
        """
        Called for each file
        Must return file content
        Can be wrapped

        @type f: static_bundle.files.StaticFileResult
        @type text: one of (unicode, str)
        @rtype: one of (unicode, str)
        """
        text += self._read(f.abs_path) + "\r\n"
        return text

    def after(self, text):
        """
        @type text: one of (unicode, str)
        @rtype: one of (unicode, str)
        """
        return text

    def _read(self, path):
        return _read(path, self.build_group.files_encoding)