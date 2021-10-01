# A part from Quick Notetaker add-on
# Copyright (C) 2021 NV Access Limited, Mohammad Suliman, Eilana Benish
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import os
import gui
import wx
from . import addonConfig
import addonHandler

addonHandler.initTranslation()


class QuickNotetakerPanel(gui.SettingsPanel):

    # Translators: the title of the Quick Notetaker panel in NVDA's settings
    title = _("Quick Notetaker")

    def makeSettings(self, settingsSizer):
        sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
        # Translators: the label of the control in Quick Notetaker settings panel for choosing a default folder where the add-on documents will be saved
        directoryGroupText = _("Default documents directory:")
        groupSizer = wx.StaticBoxSizer(
            wx.VERTICAL, self, label=directoryGroupText)
        groupHelper = sHelper.addItem(
            gui.guiHelper.BoxSizerHelper(self, sizer=groupSizer))
        groupBox = groupSizer.GetStaticBox()
        # Translators: the label of a button to browse for a directory
        browseText = _("Browse...")
        dirDialogTitle = _(
            # Translators: The title of the dialog presented when browsing for the directory where quick notetaker documents will be stored
            "Select a default directory where the documents of Quick Notetaker will be stored")
        directoryPathHelper = gui.guiHelper.PathSelectionHelper(
            groupBox, browseText, dirDialogTitle)
        directoryEntryControl = groupHelper.addItem(directoryPathHelper)
        self.documentDirectoryEdit = directoryEntryControl.pathControl
        self.documentDirectoryEdit.Value = addonConfig.getValue(
            "notesDocumentsPath")
        askWhereToSaveDocxText = _(
            # Translators: the label of a check box in Quick Notetaker settings panel
            "Ask me each time &where to save the note's corresponding Microsoft Word document")
        self.askWhereToSaveDocxCheckbox = sHelper.addItem(
            wx.CheckBox(self, label=askWhereToSaveDocxText))
        self.askWhereToSaveDocxCheckbox.Value = addonConfig.getValue(
            "askWhereToSaveDocx")
        openFileAfterCreationText = _(
            # Translators: the label of a check box in Quick Notetaker settings panel
            "&Open the note's corresponding Microsoft Word document after saving or updating")
        self.openAfterCreationCheckbox = sHelper.addItem(
            wx.CheckBox(self, label=openFileAfterCreationText))
        self.openAfterCreationCheckbox.Value = addonConfig.getValue(
            "openFileAfterCreation")
        captureActiveWindowTitleText = _(
            # Translators: the label of a check box in Quick Notetaker settings panel
            "&Capture the active window title when creating a new note")
        self.captureActiveWindowTitleCheckbox = sHelper.addItem(
            wx.CheckBox(self, label=captureActiveWindowTitleText))
        self.captureActiveWindowTitleCheckbox.Value = addonConfig.getValue(
            "captureActiveWindowTitle")
        rememberTakerSizeAndPosText = _(
            # Translators: the label of a check box in Quick Notetaker settings panel
            "&Remember the note taker window size and position")
        self.rememberTakerSizeAndPosCheckbox = sHelper.addItem(
            wx.CheckBox(self, label=rememberTakerSizeAndPosText))
        self.rememberTakerSizeAndPosCheckbox.Value = addonConfig.getValue(
            "rememberTakerSizeAndPos")
        autoAlignTextText = _(
            # Translators: the label of a check box in Quick Notetaker settings panel
            "Au&to align text when editing notes (relevant for RTL languages)")
        self.autoAlignTextCheckbox = sHelper.addItem(
            wx.CheckBox(self, label=autoAlignTextText))
        self.autoAlignTextCheckbox.Value = addonConfig.getValue(
            "autoAlignText")

    def onSave(self):
        addonConfig.setValue(
            "notesDocumentsPath",
            os.path.normpath(self.documentDirectoryEdit.Value))
        addonConfig.setValue(
            "askWhereToSaveDocx",
            self.askWhereToSaveDocxCheckbox.Value)
        addonConfig.setValue(
            "openFileAfterCreation",
            self.openAfterCreationCheckbox.Value)
        addonConfig.setValue(
            "captureActiveWindowTitle",
            self.captureActiveWindowTitleCheckbox.Value)
        addonConfig.setValue(
            "rememberTakerSizeAndPos",
            self.rememberTakerSizeAndPosCheckbox.Value)
        addonConfig.setValue(
            "autoAlignText",
            self.autoAlignTextCheckbox.Value)
