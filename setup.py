#!/usr/bin/env python
# Filename:                setup.py
# Description:             Uses setuptools' to define entry_points
# Supported Langauge(s):   Python 2.7.x
# Time-stamp:              <2015-03-13 00:33:12 jfulton> 
# -------------------------------------------------------
import setuptools

setuptools.setup(
    name="nova_dirsvc_plugin",
    version=1,
    packages=['nova_dirsvc_plugin'],
    entry_points={
        'nova.hooks': [
            'create_instance=nova_dirsvc_plugin.hooks:SaveToDirSvc',
            'delete_instance=nova_dirsvc_plugin.hooks:DeleteFromDirSvc',
        ]
    },
)
