# encoding: utf-8

import os
import subprocess


class AbstractPrepareHandler(object):
    """
    Handlers is extensions of build process,
    prepare links returned in bundle

    Bundle doesn't check that input files exist
    """

    def prepare(self, input_files, bundle):
        """
        @type input_files: list
        @type bundle: static_bundle.bundles.AbstractBundle
        @rtype: list
        """
        raise NotImplementedError


class LessCompilerPrepareHandler(AbstractPrepareHandler):
    def __init__(self, cmd="lessc", postfix=""):
        self.cmd = cmd
        self.postfix = postfix

    def prepare(self, input_files, bundle):
        out = []
        for input_file in input_files:
            if input_file.extension == "less" and os.path.isfile(input_file.abs_path):
                output_file = self.get_compile_file(input_file, bundle)
                self.compile(input_file, output_file)
                out.append(output_file)
            else:
                out.append(input_file)
        return out

    def get_compile_file(self, input_file, bundle):
        result_file_class = bundle.get_result_class()
        return result_file_class(
            self.replace_file_name(input_file.rel_path),
            self.replace_file_name(input_file.abs_path)
        )

    def replace_file_name(self, path):
        return path.replace(".less", self.postfix + ".css")

    def compile(self, input_file, output_file):
        out_modify_time = -1
        if os.path.isfile(output_file.abs_path):
            out_modify_time = os.path.getmtime(output_file.abs_path)
        in_modify_time = os.path.getmtime(input_file.abs_path)
        if in_modify_time >= out_modify_time:
            subprocess.call([self.cmd, input_file.abs_path, output_file.abs_path], shell=False)

