# A part from Quick Notetaker add-on
# Copyright (C) 2021 NV Access Limited, Mohammad Suliman, Eilana Benish
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import config
import os
import wx


def initialize():
    configSpec = {
        "notesDocumentsPath": f"string(default={os.path.normpath(os.path.expanduser('~/documents/quickNotetaker'))})",
        "askWhereToSaveDocx": "boolean(default=False)",
        "openFileAfterCreation": "boolean(default=False)",
        "captureActiveWindowTitle": "boolean(default=True)",
        "rememberTakerSizeAndPos": "boolean(default=False)",
        "autoAlignText": "boolean(default=true)",
        "takerXPos": f"integer(default={wx.DefaultPosition.x})",
        "takerYPos": f"integer(default={wx.DefaultPosition.y})",
        "takerWidth": "integer(default=500)",
        "takerHeight": "integer(default=500)",
    }
    config.conf.spec["quickNotetaker"] = configSpec


def getValue(key):
    return config.conf["quickNotetaker"][key]


def setValue(key, value):
    config.conf["quickNotetaker"][key] = value
