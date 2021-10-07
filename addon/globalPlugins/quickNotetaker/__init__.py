# __init__.py
# -*- coding: utf-8 -*-
# A part from Quick Notetaker add-on
# Copyright (C) 2021 NV Access Limited, Mohammad Suliman, Eilana Benish
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from logHandler import log
import globalPluginHandler
from scriptHandler import script
import gui
from . import dialogs
from .dialogs import NoteTakerDialog, NotesManagerDialog
from .settingsPanel import QuickNotetakerPanel
from . import notesManager
import os
from .constants import TEMP_FILES_PATH
from . import addonConfig
import api
import addonHandler


addonHandler.initTranslation()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    def __init__(self, *args, **kwargs):
        super(GlobalPlugin, self).__init__(*args, **kwargs)
        addonConfig.initialize()
        notesManager.initialize()
        try:
            os.mkdir(addonConfig.getValue("notesDocumentsPath"))
        except FileNotFoundError:
            # The user has no documents directory
            # Create the add-on documents folder in the user root folder instead
            addonConfig.setValue("notesDocumentsPath", os.path.expanduser("~\\QuickNotetaker"))
            os.mkdir(addonConfig.getValue("notesDocumentsPath"))
        except FileExistsError:
            pass
        try:
            os.mkdir(TEMP_FILES_PATH)
        except FileExistsError:
            pass
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(
            QuickNotetakerPanel)

    def terminate(self):
        super(GlobalPlugin, self).terminate()
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(
            QuickNotetakerPanel)
        if not os.path.isdir(TEMP_FILES_PATH):
            return
        for file in os.listdir(TEMP_FILES_PATH):
            os.remove(os.path.join(TEMP_FILES_PATH, file))

    # Translators: the name of the add-on category in input gestures
    scriptCategory=_("Quick Notetaker")

    @ script(
        # Translators: the description for the command to open the notetaker dialog
        description=_("Shows the Notetaker interface for writing a new note"),
        gesture="kb:NVDA+alt+n"
    )
    def script_showNoteTakerUI(self, gesture):
        noteTitle=None
        if addonConfig.getValue("captureActiveWindowTitle"):
            noteTitle=api.getForegroundObject().name
        gui.mainFrame.prePopup()
        dialogs.noteTakerInstance=NoteTakerDialog(noteTitle=noteTitle)
        dialogs.noteTakerInstance.Show()
        gui.mainFrame.postPopup()

    @ script(
        description=_(
            # Translators: the description for the command to open the Notes Manager
            "Shows the Notes Manager interface for viewing and managing notes"),
        gesture="kb:NVDA+alt+v"
    )
    def script_showNotesManagerDialogUI(self, gesture):
        gui.mainFrame.prePopup()
        dialogs.notesManagerInstance=NotesManagerDialog()
        dialogs.notesManagerInstance.Show()
        gui.mainFrame.postPopup()
