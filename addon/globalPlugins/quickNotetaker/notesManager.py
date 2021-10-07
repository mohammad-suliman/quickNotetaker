# notesManager.py
# -*- coding: utf-8 -*-
# A part from Quick Notetaker add-on
# Copyright (C) 2021 NV Access Limited, Mohammad Suliman, Eilana Benish
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import os
from logHandler import log
from datetime import datetime
import json
from .constants import DATA_DIR_PATH, DATA_FILE_PATH
from .helpers import getTitle


class note(object):
    """A class that represents a single note"""

    def __init__(self, id="", title="", content="", lastEdited="", lastEditedStamp="", docxPath=""):
        if not id:
            self.id = datetime.now().strftime("%Y%m%d%H%M%S")
            self.title = getTitle(content)
            self.content = content
            self.lastEdited = self.prettyFormat(datetime.now())
            self.lastEditedStamp = datetime.now().strftime("%Y%m%d%H%M%S")
            self.docxPath = docxPath
        else:
            self.id = id
            self.title = title
            self.content = content
            self.lastEdited = lastEdited
            self.lastEditedStamp = lastEditedStamp
            self.docxPath = docxPath

    def updateNote(self, newContent, docxPath):
        if newContent is not None and self.content != newContent:
            self.title = getTitle(newContent)
            self.content = newContent
            self.lastEdited = self.prettyFormat(datetime.now())
            self.lastEditedStamp = datetime.now().strftime("%Y%m%d%H%M%S")
        if docxPath is not None and self.docxPath != docxPath:
            self.docxPath = docxPath

    def prettyFormat(self, datetime):
        return f"{datetime.strftime('%d')}/{datetime.strftime('%m')}/{datetime.strftime('%Y')}, {datetime.strftime('%H')}:{datetime.strftime('%M')}"


def initialize():
    if os.path.isfile(DATA_FILE_PATH):
        return
    log.debug(f"Creating a new file {os.path.abspath(DATA_FILE_PATH)}")
    try:
        if not os.path.isdir(DATA_DIR_PATH):
            os.mkdir(DATA_DIR_PATH)
    except:
        log.error("Can't create the data file directory!")
        raise
    try:
        with open(DATA_FILE_PATH, mode="x", encoding="utf8") as file:
            file.write("[]")
    except:
        log.error("Can't create data file")
        raise


def loadAllNotes():
    with open(DATA_FILE_PATH, mode="r", encoding="utf8") as file:
        allNotes = json.load(file, object_hook=deserializeNote)
    return allNotes


def deserializeNote(dict):
    deserializedNote = note(
        dict['id'], dict['title'], dict['content'], dict['lastEdited'], dict['lastEditedStamp'], dict['docxPath'])
    return deserializedNote


def _dumpAllNotes(allNotes):
    # Backup the file content
    with open(DATA_FILE_PATH, mode="r", encoding="utf8") as file:
        allContent = file.read()
    # Sort all notes according to the last edited stamp in descending order
    allNotes.sort(key=lambda note: note.lastEditedStamp, reverse=True)
    try:
        with open(DATA_FILE_PATH, mode="w", encoding="utf8") as file:
            json.dump([note.__dict__ for note in allNotes],
                      file, indent=4, ensure_ascii=False)
    except:
        with open(dataFilePath, mode="w", encoding="utf8") as file:
            file.write(allContent)
        raise


def saveNewNote(noteContent, docxPath=""):
    newNote = note(content=noteContent, docxPath=docxPath)
    allNotes = loadAllNotes()
    allNotes.append(newNote)
    _dumpAllNotes(allNotes)


def deleteNote(noteID):
    allNotes = loadAllNotes()
    for note in allNotes:
        if note.id == noteID:
            allNotes.remove(note)
            break
    _dumpAllNotes(allNotes)


def updateNote(noteID, newContent=None, docxPath=None):
    allNotes = loadAllNotes()
    for note in allNotes:
        if note.id == noteID:
            note.updateNote(newContent, docxPath)
            break
    _dumpAllNotes(allNotes)
