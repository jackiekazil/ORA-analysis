#!/usr/bin/env python

import fileinput, glob, os, re, sys

def save_dir(save_dir_path):
    try:
        os.mkdir(save_dir_path)
        print "Creating output directory: ", os.path.abspath(save_dir_path)
    except OSError:
        print "Output folder specified already exists, the script will continue folder using that folder for output."
        pass
