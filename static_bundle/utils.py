# encoding: utf-8

import os
import shutil
import codecs


def _prepare_path(path):
    """
    Path join helper method
    Join paths if list passed

    @type path: one of (unicode, str, list)
    @rtype: one of (unicode, str)
    """
    if type(path) == list:
        return os.path.join(*path)
    return path


def _read(file_path, encoding="utf-8"):
    """
    Read helper method

    @type file_path: one of (unicode, str)
    @type encoding: one of (unicode, str)
    @rtype: one of (unicode, str)
    """
    with codecs.open(file_path, "r", encoding) as f:
        return f.read()


def _write(file_path, contents, encoding="utf-8"):
    """
    Write helper method

    @type file_path: one of (unicode, str)
    @type contents: one of (unicode, str)
    @type encoding: one of (unicode, str)
    """
    with codecs.open(file_path, "w", encoding) as f:
        f.write(contents)


def _copy_file(src, dest):
    """
    Copy file helper method

    @type src: one of (unicode, str)
    @type dest: one of (unicode, str)
    """
    dir_path = os.path.dirname(dest)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    shutil.copy2(src, dest)


def _get_path_extension(path):
    """
    Split file name and extension

    @type path: one of (unicode, str)
    @rtype: one of (unicode, str)
    """
    file_path, file_ext = os.path.splitext(path)
    return file_ext.lstrip('.')


def _split_path(path):
        """
        Helper method for absolute and relative paths resolution
        Split passed path and return each directory parts

        example: "/usr/share/dir"
        return: ["usr", "share", "dir"]

        @type path: one of (unicode, str)
        @rtype: list
        """
        result_parts = []
        #todo: check loops
        while path != "/":
            parts = os.path.split(path)
            if parts[1] == path:
                result_parts.insert(0, parts[1])
                break
            elif parts[0] == path:
                result_parts.insert(0, parts[0])
                break
            else:
                path = parts[0]
                result_parts.insert(0, parts[1])
        return result_parts