# constants.py
# -*- coding: utf-8 -*-
# A part from Quick Notetaker add-on
# Copyright (C) 2021 NV Access Limited, Mohammad Suliman, Eilana Benish
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import globalVars
import os

CONFIG_PATH = globalVars.appArgs.configPath

QUICK_NOTETAKER_PATH = os.path.join(
    CONFIG_PATH, "addons", "quickNotetaker", "globalPlugins")

QUICK_NOTETAKER_PATH_DEV = os.path.join(
    CONFIG_PATH, "scratchpad", "globalPlugins", "quickNotetaker")

# Remember to comment out in production
# QUICK_NOTETAKER_PATH = QUICK_NOTETAKER_PATH_DEV

DATA_DIR_PATH = os.path.join(CONFIG_PATH, "Quick Notetaker data")

DATA_FILE_PATH = os.path.join(DATA_DIR_PATH, "notes.json")

PANDOC_PATH = os.path.join(
    QUICK_NOTETAKER_PATH, "quickNotetaker", "lib", "pandoc-2.14.2", "pandoc")

PANDOC_PATH_DEV = os.path.join(
    QUICK_NOTETAKER_PATH_DEV, "lib", "pandoc-2.14.2", "pandoc")

# Remember to comment out in production
# PANDOC_PATH = PANDOC_PATH_DEV

TEMP_FILES_PATH = os.path.join(QUICK_NOTETAKER_PATH, "tempFiles")

DEFAULT_DOCUMENTS_PATH = os.path.normpath(
    os.path.expanduser("~/documents/quickNotetaker"))
