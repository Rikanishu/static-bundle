# encoding: utf-8

import os
from static_bundle.utils import _prepare_path, _split_path


class AbstractPath(object):
    """
        Base path type
        Provides methods for collect links
    """

    def get_files(self):
        """
        Collect used files
        Return list with one element for single file
        and list with all files for directory path

        @rtype: list
        """
        raise NotImplementedError

    def get_abs_and_rel_paths(self, root_path, file_name, input_dir):
        """
        Return absolute and relative path for file

        @type root_path: one of (unicode, str)
        @type relative_path: one of (unicode, str)
        @type input_dir: one of (unicode, str)
        @rtype: tuple

        """
        # todo: change relative path resolving [bug on duplicate dir names in path]
        relative_dir = root_path.replace(input_dir, '')
        return os.path.join(root_path, file_name), relative_dir + '/' + file_name


class FilePath(AbstractPath):
    """
    Path type for single file
    """

    def __init__(self, file_path, bundle):
        """
        @type file_path: one of (unicode, str)
        @type bundle: static_bundle.bundles.AbstractBundle
        """
        self.file_path = _prepare_path(file_path)
        self.bundle = bundle

    def get_files(self):
        """
        @inheritdoc
        """
        abs_path, rel_path = self.get_abs_and_rel_paths(self.bundle.path, self.file_path, self.bundle.input_dir)
        result_class = self.bundle.get_file_cls()
        return [result_class(rel_path, abs_path)]


class DirectoryPath(AbstractPath):
    """
    @type directory_path: one of (unicode, str)
    @type bundle: static_bundle.bundles.AbstractBundle
    @type exclusions: list
    """

    def __init__(self, directory_path, bundle, exclusions=None):
        self.directory_path = _prepare_path(directory_path)
        self.bundle = bundle
        self.exclusions = exclusions

    def get_files(self):
        """
        @inheritdoc
        """
        result_files = []
        ext = "." + self.bundle.get_extension()
        if self.directory_path == "":
            root_path = self.bundle.path
        else:
            root_path = os.path.join(self.bundle.path, self.directory_path)
        for root, dirs, files in os.walk(root_path):
            for fpath in files:
                if fpath.endswith(ext) and (not self.exclusions or all(fpath != n for n in self.exclusions)):
                    abs_path, rel_path = self.get_abs_and_rel_paths(root, fpath, self.bundle.input_dir)
                    result_class = self.bundle.get_file_cls()
                    result_files.append(result_class(rel_path, abs_path))
        return result_files