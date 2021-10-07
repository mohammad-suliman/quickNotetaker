## Users suggestions

Those are suggestions by users we document here. The suggestions haven't been discussed internally, so there is no guarantee they will make their way to production.

* Allow the notes to be tagged. Example tags might be: personal, education, miscellaneous, etc.
* Allow the notes to be organized according to their tags. Maybe a tree view can be used, maybe something else.
* Find a mechanism to allow the user to select a text and then create a note using a key stroke without the need to open any other interface. To achieve this, I think that copying to the clipboard is a mandatory intermediate stage so the add-on can access the selected text.
* Create a mechanism to get the page number the user was reading when they created the note. This info can be found in the status bar. Note however that each program might has a different method to obtain this data, so we need to take into consideration all popular programs and maybe handle each one separately.
* Make the place where we save the notes themself configurable. Currently the notes are saved in NVDA's directory in app data, and the user has no option to change this. Having this option configurable will allow the user to save the notes in an online service such as One Drive or Dropbox for example, so the notes can be synced between different devices.
* Create a mechanism to sync notes between different devices. Note that this feature will be very tricky to implement because of the complexity, and the feasibility of this as well when taking into account that NVDA may not ship with the required libraries.

## Features we plan to investigate

* Create an option to allow to send the note as email directly using the add-on interface. That is: we may have a button in the interface to open the default email program with the email body as the note content, and the subject as the title. The user needs to fil out the to field, maybe CC and BCC fields also. The first thing to check if this is technically possible.
* Allow the user to press a key combination to start to record NVDA speech in a new note. The user will have another key combination to stop recording. The note maybe saved automatically without displaying any interface, or the Notetaker interface will be opened with the recorded speech as the note content so the user can edit. Maybe this behavior needs to be configurable.
