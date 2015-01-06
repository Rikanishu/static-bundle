# encoding: utf-8

import os
import shutil


FPATH = os.path.dirname(os.path.realpath(__file__))
MOCKUPS_PATH = FPATH + '/mockups'


def clear_mockups_out():
    shutil.rmtree(MOCKUPS_PATH + '/out')

def remove_if_exists(fpath):
    if os.path.exists(fpath):
        os.remove(fpath)