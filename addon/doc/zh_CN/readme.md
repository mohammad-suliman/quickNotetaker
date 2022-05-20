# NVDA 快捷笔记插件

快捷笔记插件是一个很好的工具，可以随时随地在用户使用的任何应用程序中快速而轻松地撰写笔记。
例如，无论用户是在观看视频，还是在参加Zoom、Teams 或 Google 会议，都可一件创建笔记。
只需按下 NVDA + Alt + n 组合键，屏幕的左上角就会出现一个浮动窗口。
随后就可以在新弹出的笔记窗口中创建笔记了。

在您每次创建笔记时都可以自动捕捉当前窗口的标题作为笔记的一部分，当然这是可选设置。
利用该特性，后续您可以通过笔记的标题从而得知这个笔记是在什么情况下创建的。
用户可以在插件的设置面板中调整该设置以决定插件是否自动捕捉当前窗口标题。

## Notetaker 对话框

- 笔记编辑区。

当打开记事本界面时，焦点将处于这个编辑区。支持用Markdown（一种标记语言，可以轻松转换为 HTML格式）来撰写笔记内容。
想了解更多关于 Markdown 的更多信息，请访问[Markdown指南页面](https://www.markdownguide.org/)。

- 预览笔记：在一个HTML窗口中查看已撰写的笔记。

- 复制：将笔记内容复制到剪贴板上。

- 复制 HTML 代码：复制笔记内容的 HTML 代码。对于那些用 Markdown 写作的人来说这是个很有用的功能。

- 一个复选框，可以将笔记保存为 Microsoft Word 文档，或者更新相应的笔记（如果存在）。

- 一个保存并关闭按钮。

- 一个丢弃按钮，在需要时丢弃修改。当存在未保存的修改时，会向用户显示一条警告信息，询问您是否要退出并放弃所有更改。

## 笔记管理器界面

### 打开和关闭

- NVDA + Alt + V 可以打开笔记管理器界面。

- 使用 Escape 键或窗口底部的关闭按钮可以关闭该界面。

### 笔记列表

笔记是以表格的形式呈现的，其中包括。

1.  笔记的标题。如果笔记内容中不是自动补货的窗口标题，那么会将笔记内容的第一行是为标题。

2.  最后依次编辑的时间戳。

3.  笔记内容的预览文本。

### 笔记管理器界面中的可用选项 

- 查看笔记：在一个HTML窗口中查看笔记。

- 编辑笔记：打开笔记，并在 Notetaker 界面中进行编辑。

- 复制笔记：将笔记内容复制到剪贴板上。

- 创建 Microsoft Word 文档。创建一个Microsoft Word文档

- 在 Microsoft Word 中打开：打开该笔记的 Microsoft Word 版文档。

- 复制 HTML 代码：复制该笔记的HTML代码。对于那些使用 Markdown 写作的人来说这是个很有用的功能

- 删除笔记：在删除笔记前会显示一个警告。

- 新建笔记：从这个界面可以进入Notetaker界面创建新笔记。

- 打开设置：从这里也可以打开插件的设置。

- 关闭：关闭该窗口。

## 插件的设置

插件设置是 NVDA 设置界面的一部分。
若想转到该设置，可使用 NVDA + n 打开 NVDA 菜单。
选择“选项” > “设置” 然后向下找到“快捷笔记”类别。

在设置界面，用户可以：

- 默认文档目录：选择保存笔记的默认目录，快捷笔记文档将保存在该目录下。
可以点击“浏览”按钮以更改该目录。

- 每次都询问我 Microsoft Word 文档保存到何处：一个复选框（默认情况下未选中）--显示选择文档位置的对话框。以便在笔记的每次保存或更新操作时让用户选择文档的保存位置。

- 保存或更新后，打开笔记对应的Microsoft Word文档。一个复选框（默认情况下未选中）--允许用户选择是否在保存或更新操作后打开Microsoft Word文档。

- 新建笔记时使用所聚焦窗口的标题作为笔记标题：一个复选框（默认选中）--允许捕捉用户在创建笔记时的当前窗口标题。此标题也会成为 Microsoft Word 文档的标题（如果有的话）。

- 记住笔记窗口的大小和位置：一个复选框（默认情况下未选中）--创建或编辑笔记时记住上次笔记窗口的大小和位置。
- 编辑笔记时自动对齐文本 （适用于从右到左的语言环境）：
一个复选框（默认选中）--控制文本的对齐方式，这取决于您的语言环境，例如，如果使用的语言是阿拉伯语或希伯来语，选中此选项时将右对齐，如果语言是英语或法语，选中此选项时文本将左对齐。

## 键盘快捷键

- NVDA + Alt + n：打开 Notetaker 界面。

- NVDA + Alt + v：打开笔记管理器界面。

### 不同界面中的键盘快捷键（英文）

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

## 致谢

- 插件与 Pandoc 密不可分， Pandoc 是一个很棒的工具，它能够在不同格式之间转换文档。没有此工具插件将无法实现现有功能。有关 Pandoc 的更多信息请[访问 Pandoc 主页](https://pandoc.org/)。

- 插件还依赖于一个名为 Python Markdown 的包，关于此包的更多信息请访问[Github 页面](https://github.com/trentm/python-markdown2)。

- 非常感谢 NV Access、插件作者以及贡献者！插件的很多设计灵感源于你们的作品和贡献，所以让我们一起保持这个伟大社区的活跃吧！
