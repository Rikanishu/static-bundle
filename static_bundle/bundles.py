# encoding: utf-8

import os
import static_bundle
from static_bundle.utils import prepare_path
from static_bundle.paths import FilePath, DirectoryPath
from static_bundle.files import CssFileResult, JsFileResult, OtherFileResult
from static_bundle.minifiers import DefaultMinifier, UglifyJsMinifier, UglifyCssMinifier
from static_bundle.handlers import LessCompilerPrepareHandler


class AbstractBundle(object):
    """
    Base bundle class
    Bundle is set of static files

    :param path: Relative or absolute path
        If is relative path, it will be concatenated with bundle input dir
    :param: static_dir_name: Public static dir, used "static" by default

    :type path: str|unicode
    :type prepare_handlers: list
    """

    def __init__(self, path, prepare_handlers=None):
        path = prepare_path(path)
        abs_path = os.path.isabs(path)
        self.abs_path = abs_path
        if abs_path:
            self.abs_bundle_path = prepare_path(path)
            self.rel_bundle_path = None
        else:
            self.abs_bundle_path = None
            self.rel_bundle_path = path
        self.files = []

        self.prepare_handlers_chain = prepare_handlers

        self.input_dir = None

    @property
    def path(self):
        """
        Check if absolute path is not resolved yet
        """
        assert self.abs_path and self.abs_bundle_path, "Can't resolve absolute path in bundle"
        return self.abs_bundle_path

    def init_build(self, asset, builder):
        """
        Called when builder group collect files
        Resolves absolute url if relative passed

        :type asset: static_bundle.builders.Asset
        :type builder: static_bundle.builders.StandardBuilder
        """
        if not self.abs_path:
            rel_path = prepare_path(self.rel_bundle_path)
            self.abs_bundle_path = prepare_path([builder.config.input_dir, rel_path])
            self.abs_path = True
        self.input_dir = builder.config.input_dir

    def add_file(self, file_path):
        """
        Add single file to bundle

        :type: file_path: str|unicode
        """
        self.files.append(FilePath(file_path, self))

    def add_files(self, file_paths):
        """
        Add files list to bundle
        Same as add_file but works with multiple paths

        :param file_paths: list
        """
        for path in file_paths:
            self.add_file(path)

    def add_directory(self, path, exclusions=None):
        """
        Add directory to bundle

        :param exclusions: List of excluded paths

        :type path: str|unicode
        :type exclusions: list
        """
        self.files.append(DirectoryPath(path, self, exclusions=exclusions))

    def add_path_object(self, path_object):
        """
        Add custom path object

        :type: path_object: static_bundle.paths.AbstractPath
        """
        path_object.bundle = self
        self.files.append(path_object)

    def add_prepare_handler(self, prepare_handler):
        """
        Add prepare handler to bundle

        :type: prepare_handler: static_bundle.handlers.AbstractPrepareHandler
        """
        if self.prepare_handlers_chain is None:
            self.prepare_handlers_chain = []
        self.prepare_handlers_chain.append(prepare_handler)

    def prepare(self):
        """
        Called when builder run collect files in builder group

        :rtype: list[static_bundle.files.StaticFileResult]
        """
        result_files = self.collect_files()
        chain = self.prepare_handlers_chain
        if chain is None:
            # default handlers
            chain = [
                LessCompilerPrepareHandler()
            ]
        for prepare_handler in chain:
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

    def get_file_cls(self):
        raise NotImplementedError

    def get_default_minifier(self):
        return DefaultMinifier()


class JsBundle(AbstractBundle):

    def get_extension(self):
        return 'js'

    def get_type(self):
        return static_bundle.TYPE_JS

    def get_file_cls(self):
        return JsFileResult

    def get_default_minifier(self):
        return UglifyJsMinifier()


class CssBundle(AbstractBundle):

    def get_extension(self):
        return 'css'

    def get_type(self):
        return static_bundle.TYPE_CSS

    def get_file_cls(self):
        return CssFileResult

    def get_default_minifier(self):
        return UglifyCssMinifier()


class OtherFilesBundle(AbstractBundle):

    def __init__(self, path, extension=None, minifier=None, prepare_handlers=None):
        self.extension = extension
        self.minifier = minifier
        super(OtherFilesBundle, self).__init__(path, prepare_handlers=prepare_handlers)

    def get_extension(self):
        return self.extension

    def get_type(self):
        return static_bundle.TYPE_OTHER

    def get_file_cls(self):
        return OtherFileResult

    def get_default_minifier(self):
        return self.minifier()