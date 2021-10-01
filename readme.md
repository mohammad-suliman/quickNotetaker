# Quick Notetaker add-on for NVDA

The Quick Notetaker add-on is a wonderful tool which allows writing
notes quickly and easily in anytime and from any app the user is using.
Whether the user is watching a video for example, or participating in a
meeting on Zoom, teams or Google meet, they can easily and smoothly open
the notetaker and take a note. In order to create a quick note, NVDA +
Alt + n key combination can be used, a floating window appears at the
top left corner of the screen, so the note can be typed there.

Every note that is being Created can optionally get the active window
title, and as such, the note content can get the context in which this
note was created by having the note title as the active window title the
user was using. This behavior can be changed from the add-on settings,
where the user can decide whether the active window title is captured
when creating a new note.

## The Notetaker dialog

-   The note edit area: When opening the Notetaker interface the focus
    will be in this edit area. Writing with Markdown (a markup language
    to easily produce HTML content) is supported also. For more info on
    Markdown visit [the Markdown guide
    page](https://www.markdownguide.org/).

-   Preview note: to view the note in an HTML window.

-   Copy: to copy the note as is to the clipboard.

-   Copy HTML code: to copy the HTML code representing the note. A
    useful feature for those who write in Markdown.

-   A checkbox to allow saving the note as Microsoft Word also, or updating the corresponding one if it exists.

-   A save and close button.

-   A discard button to discard changes when desired. When unsaved changes exist, a warning message is displayed to the user asking if they are sure they want to exit and discard their changes.

## The Notes Manager interface

### Opening and closing this interface

-   NVDA + Alt + v will launch the Notes Manager interface.

-   Using either the Escape key or the close button found at the bottom
    of this window will close this interface.

### The notes list

The notes are organized in a tabular list which includes:

1.  The note title: If the note hasn’t got the active window title, the
    first line of the note will be the note title displayed in this
    list.

2.  Last edited time stamp.

3.  A preview text of the note content.

### The options available in Notes Manager interface 

-   View note: to view the note in an HTML window.

-   Edit note: opens the note to be edited using Notetaker interface.

-   Copy note: copies the note content as is to the clipboard.

-   Create a Microsoft Word document: Creates a Microsoft Word document
    representing this note in case it has no such document.

-   Open in Microsoft Word: opens the Microsoft Word document attached
    to this note in case it has a one.

-   Copy HTML code: copies the HTML code representing this note. A
    useful feature for those who write in Markdown.

-   Delete note: displays a warning before performing the note deletion.

-   New note: the Notetaker interface can be reached from this interface
    to create a new note.

-   Open settings: opening the add-on settings is also possible from
    here.

-   Close: to close the window.

## The add-on settings

The add-on settings are a part of NVDA’s settings interface. To reach
those settings, the user needs to open the NVDA menu using NVDA key + n,
choose preferences &gt; settings, and then arrow down until reaching
Quick Notetaker category.

Using the settings interface the user can:

-   Default documents directory: to choose the default directory where
    Quick Notetaker documents will be saved. The user can press the
    “Browse” button to change the path of this directory.

-   Ask me each time where to save the note's corresponding Microsoft
    Word document: a checkbox (not checked by default) – to show the
    dialog for choosing the location where the document will be saved on
    each save or update operation for the note’s Microsoft Word document
    if such a one exists.

-   Open the note's corresponding Microsoft Word document after saving
    or updating: a checkbox (not checked by default) – to allow the user
    to choose whether the Microsoft Word document will be opened after a
    save or update operation in case the note has such document.

-   Capture the active window title when creating a new note: a checkbox
    (checked by default) – to allow the note to get the active window
    title the user was using when they created the note. This title will
    be also the title of the Microsoft Word document for the note in
    case it has a one.

-   Remember the note taker window size and position: a checkbox (not
    checked by default) – to tell the add-on to remember the size and
    the position of the Notetaker dialog when creating or editing a
    note. As such, when the user opens the dialog next time, the
    position and the size will be the same as the last time the dialog
    was used. The default position of this dialog is at the top left
    corner of the screen.

-   Auto align text when editing notes (relevant for RTL languages): a
    checkbox (checked by default) – to control whether the text when
    creating or editing a note should be auto aligned according to the
    language used. This is mostly relevant for right to left languages.
    For example, if the language used is Arabic or Hebrew, then the text
    will be right aligned when this option is chosen, if the language is
    English or French, then the text will be left aligned.

## Keyboard shortcuts

-   NVDA + Alt + n: to open the Notetaker interface.

-   NVDA + Alt + v: to open the Notes Manager interface.

### Keyboard shortcuts in the different interfaces

<table>
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<thead>
<tr class="header">
<th>Interface</th>
<th>Command</th>
<th>Keyboard shortcut</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>Notetaker</td>
<td>Focus the note edit area</td>
<td>Alt + n</td>
</tr>
<tr class="even">
<td>Notetaker</td>
<td>Align text to the right</td>
<td>Control + r</td>
</tr>
<tr class="odd">
<td>Notetaker</td>
<td>Align text to the left</td>
<td>Control + l</td>
</tr>
<tr class="even">
<td>Notetaker</td>
<td>Preview note in an HTML window</td>
<td>Alt + r</td>
</tr>
<tr class="odd">
<td>Notetaker</td>
<td>Copy</td>
<td>Alt + p</td>
</tr>
<tr class="even">
<td>Notetaker</td>
<td>Copy HTML code</td>
<td>Alt + h</td>
</tr>
<tr class="odd">
<td>Notetaker</td>
<td>Save note as a Microsoft Word document</td>
<td>Alt + w</td>
</tr>
<tr class="even">
<td>Notetaker</td>
<td>Update the note corresponding Microsoft Word document</td>
<td>Alt + w</td>
</tr>
<tr class="odd">
<td>Notetaker</td>
<td>Save and close</td>
<td>Alt + s</td>
</tr>
<tr class="even">
<td>Notetaker</td>
<td>Discard</td>
<td>Alt + d</td>
</tr>
<tr class="odd">
<td>Notetaker</td>
<td>Open notes Manager</td>
<td>Alt + m</td>
</tr>
<tr class="even">
<td>Notes Manager</td>
<td>View note</td>
<td>Alt + v</td>
</tr>
<tr class="odd">
<td>Notes Manager</td>
<td>Edit note</td>
<td>Alt + e</td>
</tr>
<tr class="even">
<td>Notes Manager</td>
<td>Copy note</td>
<td>Alt + p</td>
</tr>
<tr class="odd">
<td>Notes Manager</td>
<td>Open in Microsoft Word (if such a document exists)</td>
<td>Alt + o</td>
</tr>
<tr class="even">
<td>Notes Manager</td>
<td>Create a word document for a saved note</td>
<td>Alt + w</td>
</tr>
<tr class="odd">
<td>Notes Manager</td>
<td>Copy HTML code</td>
<td>Alt + h</td>
</tr>
<tr class="even">
<td>Notes Manager</td>
<td>Delete note</td>
<td>Alt + d</td>
</tr>
<tr class="odd">
<td>Notes Manager</td>
<td>New note</td>
<td>Alt + n</td>
</tr>
<tr class="even">
<td>Notes Manager</td>
<td>Open settings</td>
<td>Alt + s</td>
</tr>
<tr class="odd">
<td>Notes Manager</td>
<td>Close the interface</td>
<td>Alt + c</td>
</tr>
<tr class="even">
<td>The settings interface</td>
<td>Ask me each time where to save the note's corresponding Microsoft Word document</td>
<td>Alt + w</td>
</tr>
<tr class="odd">
<td>The settings interface</td>
<td>Open the note's corresponding Microsoft Word document after saving or updating</td>
<td>Alt + o</td>
</tr>
<tr class="even">
<td>The settings interface</td>
<td>Capture the active window title when creating a new note</td>
<td>Alt + c</td>
</tr>
<tr class="odd">
<td>The settings interface</td>
<td>Remember the note taker window size and position</td>
<td>Alt + r</td>
</tr>
<tr class="even">
<td>The settings interface</td>
<td>Auto align text when editing notes (relevant for RTL languages)</td>
<td>Alt + t</td>
</tr>
</tbody>
</table>

## Acknowledgements

-   The add-on comes bundled with Pandoc, a wonderful tool which allows
    converting documents between different formats. Without this tool
    the add-on won’t be able to offer the capabilities it offers. For
    more info on Pandoc [visit the Pandoc
    homepage](https://pandoc.org/).

-   The add-on also relies on a Python Markdown package called
    markdown2. For more info on this package [visit the package GitHub
    page](https://github.com/trentm/python-markdown2).

-   A great thanks to NV Access, add-on authors, and contributors!
    Several parts of the add-on were inspired by your magnificent work
    and effort, so please keep up this brilliant ecosystem and the
    cooperation.
