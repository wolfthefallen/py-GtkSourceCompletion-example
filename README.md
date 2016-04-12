# Python Sample of using GtkSourceCompletion
how to use the auto completion in the GtkSourceView
- ctrl-space to for auto competition
- up and down arrows to select the word
- tab to insert
- shift enter for carriage return if auto complete window is open

Examples in use

1. Auto complete that pulls words from the buffer that is attached to the GtkSourceView
2. Auto complete that that pulls words from a buffer that is not attached to a view, basicly a keyword repo.
3. Auto Complete where you define your own Completion provider.
    1. which works with GtkTextIter(s), and regex(s).
    2. and also suggest Hello World!

## [GtkSourceCompletion](https://developer.gnome.org/gtksourceview/stable/ch03.html)
General notes for understanding
a GtkSourceCompletion is generated on creation of a GtkSourceView
You need to assign it a GtkSourceProvider for Completion window to pop-up.

GtkSourceCompletionWords is used to create a standard GtkSourceProvider.
CompletionWords is will auto populate matches base off of text that is provided
in the GtkTextBuff (You can you GtkSourceBuffer since it inherits GtkTextBuffer).

Since the backend of the completion is drive by Pango and GtkTextIter(s) it will only
suggest words based on Pango Language algorithm(s). So if you want to do auto completetion
with special characters you will need to design your own Completion Provider.

