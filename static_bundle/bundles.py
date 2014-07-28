# encoding: utf-8

import os
import static_bundle
from static_bundle.utils import _prepare_path
from static_bundle.paths import FilePath, DirectoryPath
from static_bundle.files import CssFileResult, JsFileResult
from static_bundle.minifiers import DefaultMinifier, UglifyJsMinifier
from static_bundle.handlers import LessCompilerPrepareHandler


class AbstractBundle(object):
    """
    Base bundle class
    Bundle is set of static files

    @param path: Relative or absolute path
        If is relative path, it will be concatenated with bundle input dir
    @param: static_dir_name: Public static dir, used "static" by default

    @type path: one of (unicode, str)
    @type prepare_handlers: one of (list, None)
    """

    def __init__(self, path, prepare_handlers=None):
        path = _prepare_path(path)
        abs_path = os.path.isabs(path)
        self.abs_path = abs_path
        if abs_path:
            self.abs_bundle_path = _prepare_path(path)
            self.rel_bundle_path = None
        else:
            self.abs_bundle_path = None
            self.rel_bundle_path = path
        self.files = []

        if prepare_handlers is None:
            # default handlers
            self.prepare_handlers_chain = [
                LessCompilerPrepareHandler()
            ]
        else:
            self.prepare_handlers_chain = prepare_handlers

        self.input_dir = None

    @property
    def path(self):
        """
        Check if absolute path is not resolved yet
        """
        assert self.abs_path and self.abs_bundle_path, "Can't resolve absolute path in bundle"
        return self.abs_bundle_path

    def init_build(self, build_group, builder):
        """
        Called when builder group collect files
        Resolves absolute url if relative passed

        @type build_group:
        @type builder: rdr.components.static_bundle.builders.StandardBuilder
        """
        if not self.abs_path:
            rel_path = self.rel_bundle_path
            if type(rel_path) is list:
                rel_path = _prepare_path(rel_path)
            self.abs_bundle_path = _prepare_path([builder.config.input_dir, rel_path])
            self.abs_path = True
        self.input_dir = builder.config.input_dir

    def add_file(self, file_path):
        """
        Add single file to bundle
        @type: file_path: one of (unicode, str)
        """
        self.files.append(FilePath(file_path, self))

    def add_directory(self, path, exclusions=None):
        """
        Add directory to bundle

        @param exclusions: List of excluded paths

        @type: path: one of (unicode, str)
        @type exclusions: list
        """
        self.files.append(DirectoryPath(path, self, exclusions=exclusions))

    def add_path_object(self, path_object):
        """
        Add custom path object

        @type: path_object: static_bundle.paths.AbstractPath
        """
        self.files.append(path_object)

    def add_prepare_handler(self, prepare_handler):
        """
        Add prepare handler to bundle

        @type: prepare_handler: static_bundle.handlers.AbstractPrepareHandler
        """
        self.prepare_handlers_chain.append(prepare_handler)

    def prepare(self):
        """
        Called when builder run collect files in builder group

        @rtype: list[static_bundle.files.StaticFileResult]
        """
        result_files = self.collect_files()
        for prepare_handler in self.prepare_handlers_chain:
            result_files = prepare_handler.prepare(result_files, self)
        return result_files

    def collect_files(self):
        result_files = []
        if not self.files:
            self.add_directory("")
        for path_object in self.files:
            path_files = path_object.get_files()
            if path_files:
                result_files.extend(path_files)
        return result_files

    def get_extension(self):
        raise NotImplementedError

    def get_type(self):
        raise NotImplementedError

    def get_result_class(self):
        raise NotImplementedError

    def get_default_minifier(self):
        return DefaultMinifier()


class JsBundle(AbstractBundle):

    def get_extension(self):
        return 'js'

    def get_type(self):
        return static_bundle.TYPE_JS

    def get_result_class(self):
        return JsFileResult

    def get_default_minifier(self):
        return UglifyJsMinifier()


class CssBundle(AbstractBundle):

    def get_extension(self):
        return 'css'

    def get_type(self):
        return static_bundle.TYPE_CSS

    def get_result_class(self):
        return CssFileResult