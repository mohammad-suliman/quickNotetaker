# helpers.py
# -*- coding: utf-8 -*-
# A part from Quick Notetaker add-on
# Copyright (C) 2022 NV Access Limited, Mohammad Suliman, Eilana Benish
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from .constants import PANDOC_PATH, TEMP_FILES_PATH, DEFAULT_DOCUMENTS_PATH
import subprocess
import re
import wx
from .lib.markdown2 import markdown
import threading
import os
from . import addonConfig
from logHandler import log
import unicodedata
from enum import Enum
from urllib.parse import urlparse
import addonHandler

addonHandler.initTranslation()


def saveAsWord(mdContent, filePath, callback, *args):
    saveThread = threading.Thread(target=_saveAsWord, args=(
        mdContent, filePath, callback, *args), daemon=True)
    saveThread.start()


def _saveAsWord(mdContent, filePath, callBack, *args):
    title = getTitle(mdContent)
    if not os.path.isdir(TEMP_FILES_PATH):
        os.mkdir(TEMP_FILES_PATH)
    with open(f"{TEMP_FILES_PATH}/{title}.md", mode="w+", encoding="utf8") as input:
        input.write(handleMdContent(mdContent))
    dirWasChanged = False
    if filePath == "":
        outputFilePath, dirWasChanged = _findAvailablePath(
            addonConfig.getValue("notesDocumentsPath"), title, "docx")
    else:
        outputFilePath = filePath
    outputFilePath, result = _runPandocCommand(
        title, outputFilePath, isRtlDocument(mdContent))
    dirWasChanged = dirWasChanged or result
    if callBack:
        callBack(outputFilePath, dirWasChanged, mdContent, *args)
    if addonConfig.getValue("openFileAfterCreation"):
        os.startfile(outputFilePath)


def _runPandocCommand(fileTitle, outputFilePath, isHtmlDocument):
    pandocArgs = [PANDOC_PATH, "-f", "markdown", "-t",
                  "docx", "-s", "-i", f"{TEMP_FILES_PATH}/{fileTitle}.md"]
    if isHtmlDocument:
        pandocArgs.extend(["-V", "dir[=rtl]"])
    pandocArgs.append("-o")
    startupInfo = subprocess.STARTUPINFO()
    startupInfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    pandocArgs.append(outputFilePath)
    try:
        subprocess.run(pandocArgs, check=True, startupinfo=startupInfo)
        return outputFilePath, False
    except subprocess.CalledProcessError:
        pandocArgs.remove(outputFilePath)
    if not os.path.isdir(addonConfig.getValue("notesDocumentsPath")):
        os.mkdir(addonConfig.getValue("notesDocumentsPath"))
    log.debug(
        "the specified directory name is invalid! Reverting to the user default one.")
    outputFilePath = os.path.join(addonConfig.getValue(
        "notesDocumentsPath"), f"{fileTitle}.docx")
    pandocArgs.append(outputFilePath)
    try:
        subprocess.run(pandocArgs, check=True, startupinfo=startupInfo)
        return outputFilePath, True
    except subprocess.CalledProcessError:
        pandocArgs.remove(outputFilePath)
    if not os.path.isdir(DEFAULT_DOCUMENTS_PATH):
        os.mkdir(DEFAULT_DOCUMENTS_PATH)
    log.debug(
        "The specified directory name is invalid! Reverting to the add-on default one.")
    outputFilePath = os.path.join(DEFAULT_DOCUMENTS_PATH, f"{fileTitle}.docx")
    pandocArgs.append(outputFilePath)
    try:
        subprocess.run(pandocArgs, check=True, startupinfo=startupInfo)
        return outputFilePath, True
    except subprocess.CalledProcessError:
        raise


def openInWord(filePath, callback, *args):
    openThread = threading.Thread(
        target=_openInWord, args=(filePath, callback, *args,), daemon=True)
    openThread.start()


def _openInWord(filePath, callback, *args):
    result = False
    try:
        os.startfile(filePath)
        result = True
    except:
        pass
    if callback:
        callback(result, *args)


def _findAvailablePath(dirName, fileTitle, extension):
    """Finds available file path if the given one is already used.
    We need this to avoid over riding existing files content"""
    dirWasChanged = False
    if not os.path.isdir(dirName):
        try:
            os.mkdir(dirName)
        except:
            log.debug(
                "The user default directory name is invalid! Reverting to the user default one.")
            if not os.path.isdir(DEFAULT_DOCUMENTS_PATH):
                os.mkdir(DEFAULT_DOCUMENTS_PATH)
            dirName = DEFAULT_DOCUMENTS_PATH
            dirWasChanged = True
    candidatePath = os.path.join(dirName, f"{fileTitle}.{extension}")
    if not os.path.isfile(candidatePath):
        return candidatePath, dirWasChanged
    for i in range(50):
        candidatePath = os.path.join(
            dirName, f"{fileTitle} ({i + 1}).{extension}")
        if not os.path.isfile(candidatePath):
            return candidatePath, dirWasChanged


#: A regex for matching a URL
#: Taken from https://gist.githubusercontent.com/nishad/ff5d02394afaf8cca5818f023fb88a21/raw/cc631328b9bfc0750379847ecbe415b4df69aa67/urlmarker.py
urlPatternText =\
    r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""


def handleMdContent(mdContent):
    """Handles the Markdown content to be displayed correctly.
    - right aligns the content if needed by wrapping the rtl content with divs which have the direction attrebute set to rtl
    - wraps URLs (if any) with the needed markdown to be displayed as links"""
    mdContent = _makeRtl(mdContent)
    # Find all URLs
    urlsList = re.findall(urlPatternText, mdContent)
    result = mdContent
    for url in urlsList:
        if url:
            result = result.replace(url, f"[{url}]({url})")
    return result


def getTitle(mdContent):
    # Delete HTML tags if any
    mdContent = retrieveTextFromHtml(mdContent)
    log.debug(mdContent)
    titleText = markdown(mdContent, extras=["markdown-in-html"])
    titleText = retrieveTextFromHtml(titleText)
    log.debug(titleText)
    titleText = _removeExtraSpaces(titleText)
    lines = titleText.split("\n")
    for line in lines:
        if line:
            line = _handleUrlsInTitle(line)
            return line
    # Translators: the title given to a note if it has no title
    return _("Untitled")


def _handleUrlsInTitle(titleText):
    """replaces the full URL text (in case one or more are found in title text) by the netlok.
    For example: https://www.google.com/search becomes www.google.com.
    This is necessary to not get errors when naming the md and docx files with this title text as the add-on does"""
    # Find all URLs
    urlsList = re.findall(urlPatternText, titleText)
    result = titleText
    for url in urlsList:
        if url:
            result = result.replace(url, f"{urlparse(url).netloc}")
    return result


def getPreviewText(mdContent):
    """Gets the note's preview text to be displayed in notes list in Notes Manager"""
    # Delete HTML tags if any
    mdContent = retrieveTextFromHtml(mdContent)
    previewText = markdown(mdContent, extras=["markdown-in-html"])
    previewText = retrieveTextFromHtml(previewText)
    return previewText[:50]


def retrieveTextFromHtml(htmlText):
    """Returns the inner text of all HTML tags found in htmlText string"""
    extracted = re.sub(r"(<.*?\s*?/{0,1}>)+", " ", htmlText)
    # Remove extra spaces if any
    extracted = _removeExtraSpaces(extracted)
    return extracted


def _removeExtraSpaces(text):
    text = re.sub(r" +", " ", text)
    text = text.strip()
    return text


def _isRtlParagraph(paragraph):
    """determines if the given paragraph is rtl by relying on the first none html text letter of the paragraph"""
    rtlClasses = ["R", "AL", "AN"]
    # Delete HTML markup if it exists
    paragraphWithoutHtml = retrieveTextFromHtml(paragraph)
    lettersOnly = re.sub(r"\W+", "", paragraphWithoutHtml)
    if not lettersOnly:
        return None
    if unicodedata.bidirectional(lettersOnly[0]) in rtlClasses:
        return True
    else:
        return False


def _makeRtl(content):
    """Makes the text rtl if needed by wrapping each paragraph starting with RTL char with a div which has dir = rtl"""
    paragraphs = content.split("\n\n")
    result = []
    for paragraph in paragraphs:
        if _isRtlParagraph(paragraph):
            result.append(
                '<div dir="rtl" markdown="1">\n%s\n</div>' % paragraph)
        else:
            result.append('<div markdown="1">\n%s\n</div>' % paragraph)
    return "\n\n".join(result)


def isRtlDocument(content):
    """Determines if the document is RTL by checking if the document has atleast an rtl paragraph. If it has, then the document is rtl"""
    paragraphs = content.split("\n\n")
    for paragraph in paragraphs:
        if _isRtlParagraph(paragraph):
            return True
    return False


class Align(Enum):
    ALIGN_TO_LEFT = 1
    ALIGN_TO_RIGHT = 2
    NO_CHANGE = 3


def handleTextAlignment(text, currentAlignment):
    """Determines the alignment of the text relying on the first letter found in the text"""
    rtlClasses = ["R", "AL", "AN"]
    # Delete HTML markup if it exists
    lettersOnly = re.sub(r"\W+", "", text)
    if not lettersOnly or not addonConfig.getValue("autoAlignText"):
        return Align.NO_CHANGE
    if unicodedata.bidirectional(lettersOnly[0]) in rtlClasses and currentAlignment != wx.Layout_RightToLeft:
        return Align.ALIGN_TO_RIGHT
    elif not unicodedata.bidirectional(lettersOnly[0]) in rtlClasses and currentAlignment != wx.Layout_LeftToRight:
        return Align.ALIGN_TO_LEFT
    else:
        return Align.NO_CHANGE
