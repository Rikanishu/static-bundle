# encoding: utf-8

import os
from static_bundle.utils import _prepare_path


class BuilderConfig(object):
    """
     Standard builder config
     Used construct args for making

     @type input_dir: one of (unicode, str)
     @type output_dir: one of (unicode, str)
     @type env: one of (unicode, str)

     """

    def __init__(self, input_dir, output_dir, env='production', url_prefix='/'):
        assert input_dir and output_dir, "Input and output paths are required"
        self.input_dir = BuilderConfig.init_path(input_dir)
        self.output_dir = BuilderConfig.init_path(output_dir)
        self.url_prefix = url_prefix
        self.env = env

    @classmethod
    def init_path(cls, path):
        path = _prepare_path(path)
        if os.path.isabs(path):
            return path
        return os.path.abspath(os.path.join(os.getcwd(), path))