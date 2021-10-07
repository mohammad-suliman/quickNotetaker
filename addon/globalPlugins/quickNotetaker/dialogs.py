# dialogs.py
# -*- coding: utf-8 -*-
# A part from Quick Notetaker add-on
# Copyright (C) 2021 NV Access Limited, Mohammad Suliman, Eilana Benish
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import wx
import gui
from gui import guiHelper
from gui import nvdaControls
from gui.dpiScalingHelper import DpiScalingHelperMixin, DpiScalingHelperMixinWithoutInit
from gui.settingsDialogs import NVDASettingsDialog
from logHandler import log
import ui
from .lib.markdown2 import markdown
import weakref
import api
import re
from . import notesManager
from .helpers import *
from . import addonConfig
from .settingsPanel import QuickNotetakerPanel
import addonHandler


addonHandler.initTranslation()


#: Stores a Notes Manager instance if it exists
notesManagerInstance = None


#: Stores a Notes Taker instance if it exists
noteTakerInstance = None


class NoteTakerDialog(wx.Dialog):

    @classmethod
    def _instance(cls):
        """ type: () -> NoteTakerDialog
        return None until this is replaced with a weakref.ref object. Then the instance is retrieved
        with by treating that object as a callable.
        """
        return None

    def __new__(cls, *args, **kwargs):
        instance = NoteTakerDialog._instance()
        if instance is None:
            return super(NoteTakerDialog, cls).__new__(cls, *args, **kwargs)
        return instance

    def _getDialogSizeAndPosition(self):
        dialogSize = wx.Size(500, 500)
        dialogPos = wx.DefaultPosition
        if addonConfig.getValue("rememberTakerSizeAndPos"):
            log.debug(
                "Setting Quick Notetaker Notetaker window position and size")
            dialogSize = wx.Size(
                addonConfig.getValue("takerWidth"),
                addonConfig.getValue("takerHeight")
            )
            dialogPos = wx.Point(
                x=addonConfig.getValue("takerXPos"),
                y=addonConfig.getValue("takerYPos")
            )
        return dialogSize, dialogPos

    def __init__(self, currentNote=None, noteTitle=None):
        if NoteTakerDialog._instance() is not None:
            return
        NoteTakerDialog._instance = weakref.ref(self)

        dialogSize, dialogPos = self._getDialogSizeAndPosition()
        # Translators: the title for the Quick Notetaker Notetaker window
        title = _("Notetaker - Quick Notetaker")
        if noteTitle:
            title = f"{noteTitle} - {title}"

        super().__init__(
            gui.mainFrame,
            title=title,
            size=dialogSize,
            pos=dialogPos,
            style=wx.CAPTION | wx.CLOSE_BOX | wx.RESIZE_BORDER | wx.STAY_ON_TOP
        )

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        sHelper = guiHelper.BoxSizerHelper(self, wx.VERTICAL)
        # Translators: a lable of a button in Notetaker dialog
        openManagerButton = wx.Button(self, label=_("Open Notes &Manager..."))
        openManagerButton.Bind(wx.EVT_BUTTON, self.onOpenManager)
        sHelper.addItem(openManagerButton, flag=wx.ALIGN_CENTER)
        if notesManagerInstance:
            openManagerButton.Disable()
        buttonsHelper = guiHelper.ButtonHelper(wx.HORIZONTAL)
        preViewButton = buttonsHelper.addButton(
            self,
            # Translators: a lable of a button in Notetaker dialog
            label=_("P&review note..."))
        preViewButton.Bind(wx.EVT_BUTTON, self.onPreview)
        # Translators: a lable of a button in Notetaker dialog
        copyButton = buttonsHelper.addButton(self, label=_("Co&py"))
        copyButton.Bind(wx.EVT_BUTTON, self.onCopy)
        copyHtmlButton = buttonsHelper.addButton(
            self,
            # Translators: a lable of a button in Notetaker dialog
            label=_("Copy &HTML code"))
        copyHtmlButton.Bind(wx.EVT_BUTTON, self.onCopyAsHtml)
        sHelper.addItem(buttonsHelper.sizer)

        sizer = wx.BoxSizer(wx.VERTICAL)
        # Translators: The lable of the note content edit area in Notetaker dialog
        label = wx.StaticText(self, label=_("&Note content:"))
        sizer.Add(label, flag=wx.ALIGN_CENTER_HORIZONTAL)
        sizer.AddSpacer(guiHelper.SPACE_BETWEEN_ASSOCIATED_CONTROL_VERTICAL)
        self.noteEditArea = wx.TextCtrl(
            self, style=wx.TE_RICH2 | wx.TE_MULTILINE)
        self.noteEditArea.Bind(wx.EVT_TEXT, self.onCharacter)
        self.noteEditArea.Bind(wx.EVT_KEY_UP, self.onKeyUp)
        sizer.Add(self.noteEditArea, proportion=1, flag=wx.EXPAND)
        sHelper.addItem(sizer, proportion=1, flag=wx.EXPAND)
        if noteTitle:
            self.noteEditArea.SetValue(noteTitle + "\n\n")
            self.noteEditArea.SetInsertionPointEnd()
        self.currentNote = currentNote
        if self.currentNote:
            self.noteEditArea.SetValue(self.currentNote.content)
        self.noteEditArea.SetFocus()

        if self.currentNote and self.currentNote.docxPath:
            # Translators: The label of the check box in Notetaker dialog when editing a note which has Word document attached to it
            checkboxText = _(
                "Update the corresponding Microsoft &Word document also")
        else:
            # Translators: The label of the check box in Notetaker dialog when creating a new note or when editing an existing note with no Word document attached to it
            checkboxText = _("Save as Microsoft &Word document also")
        self.saveAswordCheckBox = sHelper.addItem(
            wx.CheckBox(self, label=checkboxText))
        if self.currentNote and self.currentNote.docxPath:
            self.saveAswordCheckBox.Value = True
        buttons = guiHelper.ButtonHelper(wx.HORIZONTAL)
        saveButton = buttons.addButton(
            self,
            id=wx.ID_OK,
            # Translators: a lable of a button in Notetaker dialog
            label=_("&Save and close"))
        saveButton.SetDefault()
        saveButton.Bind(wx.EVT_BUTTON, self.onsaveChanges)
        discardButton = buttons.addButton(
            self,
            id=wx.ID_CLOSE,
            # Translators: a lable of a button in Notetaker dialog
            label=_("&Discard"))
        discardButton.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
        sHelper.addDialogDismissButtons(buttons, True)
        mainSizer.Add(sHelper.sizer, proportion=1, flag=wx.EXPAND)
        self.SetSizer(mainSizer)
        self.Bind(wx.EVT_CLOSE, self.onDiscard)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)
        self.EscapeId = wx.ID_CLOSE

    def onDestroy(self, evt):
        global noteTakerInstance
        noteTakerInstance = None
        evt.Skip()

    def onPreview(self, evt):
        mdContent = self.noteEditArea.GetValue()
        mdContent = handleMdContent(mdContent)
        htmlContent = markdown(mdContent, extras=["markdown-in-html"])
        title = getTitle(mdContent)
        ui.browseableMessage(htmlContent, title, True)

    def onsaveChanges(self, evt):
        newContent = self.noteEditArea.GetValue()
        if self.saveAswordCheckBox.Value:
            self.saveAsWord(newContent)
            return
        if self.currentNote:
            notesManager.updateNote(self.currentNote.id, newContent)
        else:
            notesManager.saveNewNote(newContent)
        self._savePositionInformation()
        self._clean()

    def onDiscard(self, evt):
        textAreaContent = self.noteEditArea.GetValue()
        if not textAreaContent:
            self._savePositionInformation()
            self._clean()
            return
        if self.currentNote and self.currentNote.content == textAreaContent:
            self._savePositionInformation()
            self._clean()
            return
        res = gui.messageBox(
            # Translators: The message which asks the user whether they want to exit and discard changes in Notetaker dialog
            _("Are you sure you want to exit and discard changes?"),
            # Translators: The title of the message which asks the user whether they want to exit and discard changes in Notetaker dialog
            _("Warning"),
            style=wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL,
            parent=self)
        if res == wx.YES:
            self._savePositionInformation()
            self._clean()

    def _savePositionInformation(self):
        position = self.GetPosition()
        addonConfig.setValue("takerXPos", position.x)
        addonConfig.setValue("takerYPos", position.y)
        size = self.GetSize()
        addonConfig.setValue("takerWidth", size.width)
        addonConfig.setValue("takerHeight", size.height)

    def onOpenManager(self, evt):
        global notesManagerInstance
        if notesManagerInstance:
            gui.messageBox(
                # Translators: the message shown to the user when opening Notes Manager is not possible because a one is already opened
                _("Couldn't open Notes Manager! A Notes Manager window is already opened."),
                # Translators: the title of the message telling the user that opening Notes Manager wasn't possible
                _("Warning"),
                style=wx.ICON_WARNING | wx.OK,
                parent=self
            )
            return
        gui.mainFrame.prePopup()
        notesManagerInstance = NotesManagerDialog()
        notesManagerInstance.Show()
        gui.mainFrame.postPopup()

    def onKeyUp(self, evt):
        if evt.GetModifiers() == wx.MOD_CONTROL:
            if evt.GetKeyCode() == ord("R"):
                self.noteEditArea.SetLayoutDirection(wx.Layout_RightToLeft)
            elif evt.GetKeyCode() == ord("L"):
                self.noteEditArea.SetLayoutDirection(wx.Layout_LeftToRight)
        evt.Skip()

    def onCharacter(self, evt):
        content = self.noteEditArea.GetValue()
        if not addonConfig.getValue("autoAlignText"):
            evt.Skip()
            return
        res = handleTextAlignment(
            content, self.noteEditArea.GetLayoutDirection())
        if res == Align.ALIGN_TO_LEFT:
            self.noteEditArea.SetLayoutDirection(wx.Layout_LeftToRight)
        elif res == Align.ALIGN_TO_RIGHT:
            self.noteEditArea.SetLayoutDirection(wx.Layout_RightToLeft)
        evt.Skip()

    def onCopy(self, evt):
        content = self.noteEditArea.GetValue()
        res = api.copyToClip(content, False)
        if res == True:
            # Translators: The message which tells the user that copying the note was successful
            ui.message(_("Copied to clipboard!"))

    def onCopyAsHtml(self, evt):
        content = self.noteEditArea.GetValue()
        res = api.copyToClip(
            markdown(content, extras=["markdown-in-html"]), False)
        if res == True:
            # Translators: The message which tells the user that copying the note was successful
            ui.message(_("Copied to clipboard!"))

    def saveAsWord(self, newContent):
        docxPath = ""
        if self.currentNote and self.currentNote.docxPath:
            docxPath = self.currentNote.docxPath
        elif addonConfig.getValue("askWhereToSaveDocx"):
            docxPath = askUserWhereToSave(self, newContent)
            if docxPath is None:
                return
        saveAsWord(
            newContent,
            docxPath,
            self._saveAsWordCallback,
            self.currentNote.id if self.currentNote else None
        )
        self._savePositionInformation()
        self._clean()

    def _saveAsWordCallback(self, outputFilePath, dirWasChanged, mdContent, noteID):
        if noteID:
            notesManager.updateNote(noteID, mdContent, outputFilePath)
        else:
            notesManager.saveNewNote(mdContent, outputFilePath)
        notifyDirWasChanged(dirWasChanged)
        if notesManagerInstance:
            notesManagerInstance.refreshAllNotesList(
                notesManagerInstance.notesList.GetFirstSelected())

    def _clean(self):
        self.DestroyChildren()
        self.Destroy()


class NotesManagerDialog(
    DpiScalingHelperMixinWithoutInit,
    wx.Dialog  # wxPython does not seem to call base class initializer, put last in MRO
):

    @classmethod
    def _instance(cls):
        """ type: () -> NotesManagerDialog
        return None until this is replaced with a weakref.ref object. Then the instance is retrieved
        with by treating that object as a callable.
        """
        return None

    def __new__(cls, *args, **kwargs):
        instance = NotesManagerDialog._instance()
        if instance is None:
            return super(NotesManagerDialog, cls).__new__(cls, *args, **kwargs)
        return instance

    def __init__(self):
        if NotesManagerDialog._instance() is not None:
            return
        NotesManagerDialog._instance = weakref.ref(self)

# Translators: The title of the Notes Manager dialog
        title = _("Notes Manager - Quick Notetaker")
        super().__init__(
            gui.mainFrame,
            title=title,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX,
        )
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        firstTextSizer = wx.BoxSizer(wx.VERTICAL)
        listAndButtonsSizerHelper = guiHelper.BoxSizerHelper(
            self, sizer=wx.BoxSizer(wx.HORIZONTAL))

        # Translators: the label of the notes list in Notes Manager dialog
        entriesLabel = _("No&tes:")
        firstTextSizer.Add(wx.StaticText(self, label=entriesLabel))
        mainSizer.Add(
            firstTextSizer,
            border=guiHelper.BORDER_FOR_DIALOGS,
            flag=wx.TOP | wx.LEFT | wx.RIGHT
        )
        self.notesList = listAndButtonsSizerHelper.addItem(
            nvdaControls.AutoWidthColumnListCtrl(
                parent=self,
                style=wx.LC_REPORT | wx.LC_SINGLE_SEL,
            ),
            flag=wx.EXPAND,
            proportion=1,
        )
        # Translators: the name of the first column in the notes list in Notes Manager dialog
        self.notesList.InsertColumn(0, _("Title"), width=self.scaleSize(200))
        self.notesList.InsertColumn(
            # Translators: the name of the second column in the notes list in Notes Manager dialog
            1, _("Last Edited"), width=self.scaleSize(100))
        # Translators: the name of the third column in the notes list in Notes Manager dialog
        self.notesList.InsertColumn(2, _("Preivew"), width=self.scaleSize(400))
        self.notesList.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.onListItemSelected)

        # this is the group of buttons that affects the currently selected note
        entryButtonsHelper = guiHelper.ButtonHelper(wx.VERTICAL)
        self.viewButton = entryButtonsHelper.addButton(
            self,
            # Translaters: The lable of a button in Notes Manager dialog
            label=_("&View note..."))
        self.viewButton.Disable()
        self.viewButton.Bind(wx.EVT_BUTTON, self.onView)
        self.editButton = entryButtonsHelper.addButton(
            self,
            # Translaters: The lable of a button in Notes Manager dialog
            label=_("&Edit note..."))
        self.editButton.Disable()
        self.editButton.Bind(wx.EVT_BUTTON, self.onEdit)
        self.copyButton = entryButtonsHelper.addButton(
            self,
            # Translaters: The lable of a button in Notes Manager dialog
            label=_("Co&py note"))
        self.copyButton.Disable()
        self.copyButton.Bind(wx.EVT_BUTTON, self.onCopy)
        self.openInWordButton = entryButtonsHelper.addButton(
            self,
            # Translaters: The lable of the open in Word button in Notes Manager dialog in case the note has a Word document attached to it
            label=_("&Open in Microsoft Word..."))
        self.openInWordButton.Disable()
        self.openInWordButton.Bind(wx.EVT_BUTTON, self.onOpenInWord)
        self.copyHtmlButton = entryButtonsHelper.addButton(
            self,
            # Translaters: The lable of a button in Notes Manager dialog
            label=_("Copy &HTML code"))
        self.copyHtmlButton.Disable()
        self.copyHtmlButton.Bind(wx.EVT_BUTTON, self.onCopyAsHtml)
        self.deleteButton = entryButtonsHelper.addButton(
            self,
            # Translaters: The lable of a button in Notes Manager dialog
            label=_("&Delete note..."))
        self.deleteButton.Disable()
        self.deleteButton.Bind(wx.EVT_BUTTON, self.onDelete)
        listAndButtonsSizerHelper.addItem(entryButtonsHelper.sizer)

        mainSizer.Add(
            listAndButtonsSizerHelper.sizer,
            border=guiHelper.BORDER_FOR_DIALOGS,
            flag=wx.ALL | wx.EXPAND,
            proportion=1,
        )

        generalActions = guiHelper.ButtonHelper(wx.HORIZONTAL)
        # Translators: the  label of a button in Notes Manager dialog
        newNoteButton = generalActions.addButton(self, label=_("&New note..."))
        newNoteButton.Bind(wx.EVT_BUTTON, self.onNewNote)
        if noteTakerInstance:
            newNoteButton.Disable()
        # Translaters: The lable of a button in Notes Manager dialog
        openSettingsButton = generalActions.addButton(
            self, label=_("Open &settings..."))
        openSettingsButton.Bind(wx.EVT_BUTTON, self.onSettings)
        mainSizer.Add(
            generalActions.sizer,
            border=guiHelper.BORDER_FOR_DIALOGS,
            flag=wx.LEFT | wx.RIGHT
        )

        mainSizer.Add(
            wx.StaticLine(self),
            border=guiHelper.BORDER_FOR_DIALOGS,
            flag=wx.ALL | wx.EXPAND
        )

        # Translaters: The lable of a button in Notes Manager dialog
        closeButton = wx.Button(self, label=_("&Close"), id=wx.ID_CLOSE)
        closeButton.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
        mainSizer.Add(
            closeButton,
            border=guiHelper.BORDER_FOR_DIALOGS,
            flag=wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.CENTER | wx.ALIGN_RIGHT
        )
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.EscapeId = wx.ID_CLOSE

        mainSizer.Fit(self)
        self.SetSizer(mainSizer)

        self.refreshAllNotesList()
        self.SetMinSize(mainSizer.GetMinSize())
        self.SetSize(self.scaleSize((763, 509)))
        self.CentreOnScreen()
        self.notesList.SetFocus()
        self.Bind(wx.EVT_ACTIVATE, self.onActivate)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)

    def onActivate(self, evt):
        if evt.GetActive():
            self.refreshAllNotesList(self.notesList.GetFirstSelected())
        evt.Skip()

    def onDestroy(self, evt):
        global notesManagerInstance
        notesManagerInstance = None
        evt.Skip()

    def onView(self, evt):
        curNote = self._getCurrentNote()
        if not curNote:
            return
        content = handleMdContent(curNote.content)
        contentAsHtml = markdown(content, extras=["markdown-in-html"])
        ui.browseableMessage(contentAsHtml, curNote.title, True)

    def onEdit(self, evt):
        curNote = self._getCurrentNote()
        if not curNote:
            return
        global noteTakerInstance
        if noteTakerInstance:
            gui.messageBox(
                # Translators: the message shown to the user when editing the note is not possible
                _("Couldn't edit note! An open Notetaker window with unsaved changes is present."),
                # Translators: the title of the message telling the user that editing the note wasn't possible
                _("Warning"),
                style=wx.ICON_WARNING | wx.OK,
                parent=self
            )
            return
        gui.mainFrame.prePopup()
        noteTakerInstance = NoteTakerDialog(currentNote=curNote)
        noteTakerInstance.Show()
        gui.mainFrame.postPopup()

    def _getCurrentNote(self):
        index = self.notesList.GetFirstSelected()
        if index < 0:
            return
        curNote = notesManager.loadAllNotes()[index]
        return curNote

    def onNewNote(self, evt):
        global noteTakerInstance
        if noteTakerInstance:
            gui.messageBox(
                # Translators: the message shown to the user when opening Notetaker is not possible because a one is already opened
                _("Couldn't open Notetaker! A Notetaker window is already opened."),
                # Translators: the title of the message telling the user that opening Notetaker wasn't possible
                _("Warning"),
                style=wx.ICON_WARNING | wx.OK,
                parent=self
            )
            return
        gui.mainFrame.prePopup()
        noteTakerInstance = NoteTakerDialog()
        noteTakerInstance.Show()
        gui.mainFrame.postPopup()

    def onSettings(self, evt):
        gui.mainFrame._popupSettingsDialog(
            NVDASettingsDialog, QuickNotetakerPanel)

    def onClose(self, evt):
        self.DestroyChildren()
        self.Destroy()
        evt.Skip()

    def onListItemSelected(self, evt):
        self.viewButton.Enable()
        self.editButton.Enable()
        self.copyButton.Enable()
        curNote = self._getCurrentNote()
        if curNote and curNote.docxPath:
            # Translators: the lable of the open in word button in Notes Manager dialog in case the note has a Word document attached to it
            label = _("&Open in Microsoft Word...")
        else:
            # Translators: the lable of the open in word button in Notes Manager dialog in case the note has no Word document attached to it
            label = _("Create Microsoft &Word document")
            if addonConfig.getValue("askWhereToSaveDocx"):
                label += "..."
        self.openInWordButton.SetLabel(label)
        self.openInWordButton.Enable()
        self.copyHtmlButton.Enable()
        self.deleteButton.Enable()

    def refreshAllNotesList(self, activeIndex=0):
        self.notesList.DeleteAllItems()
        for note in notesManager.loadAllNotes():
            self.notesList.Append((
                note.title,
                note.lastEdited,
                getPreviewText(note.content)
            ))
        # Select the given active note or the first one if not given
        allNotesLen = len(notesManager.loadAllNotes())
        if allNotesLen > 0:
            if activeIndex == -1:
                activeIndex = allNotesLen - 1
            elif activeIndex < 0 or activeIndex >= allNotesLen:
                activeIndex = 0
            self.notesList.Select(activeIndex, on=1)
            self.notesList.SetItemState(
                activeIndex, wx.LIST_STATE_FOCUSED, wx.LIST_STATE_FOCUSED)
        else:
            self.viewButton.Disable()
            self.editButton.Disable()
            self.copyButton.Disable()
            self.openInWordButton.Disable()
            self.copyHtmlButton.Disable()
            self.deleteButton.Disable()

    def onOpenInWord(self, evt):
        curNote = self._getCurrentNote()
        if curNote and curNote.docxPath:
            openInWord(
                curNote.docxPath,
                self._openInWordCallback,
                curNote.id
            )
            return
        if not curNote:
            return
        docxPath = ""
        if addonConfig.getValue("askWhereToSaveDocx"):
            docxPath = askUserWhereToSave(self, curNote.content)
            if docxPath is None:
                return
        saveAsWord(
            curNote.content,
            docxPath,
            self._saveAsWordCallback,
            curNote.id
        )

    def _saveAsWordCallback(self, outputFilePath, dirWasChanged, mdContent, noteID):
        notesManager.updateNote(noteID, docxPath=outputFilePath)
        notifyDirWasChanged(dirWasChanged)
        if not self:
            return
        self.refreshAllNotesList(self.notesList.GetFirstSelected())

    def _openInWordCallback(self, hasSucceeded, noteID):
        if hasSucceeded:
            return
        notesManager.updateNote(noteID, docxPath="")
        gui.messageBox(
            # Translators: the message shown to the user when the note attached Word document is no longer available.
            # This message is displayed when trying to open the note's Word document from the Notes Manager dialog
            _("A document with the specified name was not found! You can create a new one so you would be able to view this note as a Microsoft Word document."),
            # Translators: the title of the message shown to the user when the note attached Word document is no longer available.
            # This message is displayed when trying to open the note's Word document from the Notes Manager dialog
            _("Warning"),
            style=wx.ICON_WARNING | wx.OK,
            parent=gui.mainFrame
        )

    def onDelete(self, evt):
        curNote = self._getCurrentNote()
        if not curNote:
            return
        res = gui.messageBox(
            # Translators: the warning messaged shown to the user when they try to delete a note from Notes Manager
            _("Are you sure you want to delete this note?"),
            # Translators: the title of the warning messaged shown to the user when they try to delete a note from Notes Manager
            _("Warning"),
            style=wx.YES_NO | wx.NO_DEFAULT,
            parent=self)
        if res != wx.YES:
            return
        notesManager.deleteNote(curNote.id)
        self.refreshAllNotesList(self.notesList.GetFirstSelected())

    def onCopy(self, evt):
        curNote = self._getCurrentNote()
        if not curNote:
            return
        res = api.copyToClip(curNote.content, False)
        if res == True:
            # Translators: the message telling the user that copying the note was successful
            ui.message(_("Copied to clipboard!"))

    def onCopyAsHtml(self, evt):
        curNote = self._getCurrentNote()
        if not curNote:
            return
        res = api.copyToClip(
            markdown(curNote.content, extras=["markdown-in-html"]), False)
        if res:
            # Translators: the message telling the user that copying the note was successful
            ui.message(_("Copied to clipboard!"))


def notifyDirWasChanged(dirWasChanged):
    if dirWasChanged:
        gui.messageBox(
            # Translators: the message which tells the user that the directory they tried to save the file in is no longer available,
            # so the file was saved in the user default one if this was possible.
            # If not, the file was saved in the quick Notetaker directory in documents folder
            _("The saved path for the Microsoft Word document no longer  exists! The document was saved in the default directory for the ad-on!"),
            # Translators: the title of the message telling the user that the directory they tried to save the document in is no longer available.
            # See the message body for more details
            _("Warning"),
            style=wx.ICON_WARNING | wx.OK,
            parent=gui.mainFrame)


def askUserWhereToSave(parent, noteContent):
    # Translators: The title of the dialog which allows the user to choose the folder where they want to save the note's corresponding Word document.
    # This dialog is displayed to the user if the option of "Ask me each time where to save the note's corresponding Word document" in quick Notetaker settings is checked
    with wx.DirDialog(parent, _("Select the folder where the document will be saved"), defaultPath=addonConfig.getValue("notesDocumentsPath")) as d:
        if d.ShowModal() == wx.ID_OK:
            return f"{d.Path}/{getTitle(noteContent)}.docx"
        else:
            return None
