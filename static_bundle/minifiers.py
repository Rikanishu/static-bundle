# encoding: utf-8

import static_bundle
from static_bundle import logger
from static_bundle.utils import _read


class DefaultMinifier(object):
    """
    This is default class used in minify process
    Provides methods that called in each steps of minify

    """

    def init_build_group(self, build_group):
        """
        Called before build

        @type build_group: static_bundle.builders.BuildGroup
        """
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


class UglifyJsMinifier(DefaultMinifier):
    """
    Minifier class for UglifyJS
    """

    def __init__(self, cmd='uglifyjs'):
        self.cmd = cmd

    def contents(self, f, text):
        file_content = self._read(f.abs_path) + "\r\n"
        if f.type == static_bundle.TYPE_JS:
            file_content = self.uglify(file_content)
        text += file_content
        return text

    def uglify(self, content):
        try:
            import subprocess
            pipe = subprocess.Popen([self.cmd], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            if pipe.poll() is not 0:
                stdout, stderr = pipe.communicate(content)
                if stderr:
                    logger.warning("[UglifyJS] Non-empty stderr: %s" % stderr)
                if pipe.poll() is not 0:
                    pipe.terminate()
                return stdout
        except OSError as e:
            if e.errno == 2:
                logger.warning("[UglifyJS] UglifyJS executable is required for minify: %s" % e)
            else:
                logger.warning("[UglifyJS] Error: %s" % e)
        except Exception as e:
            logger.warning("[UglifyJS] Error    : %s" % e)

        return content
