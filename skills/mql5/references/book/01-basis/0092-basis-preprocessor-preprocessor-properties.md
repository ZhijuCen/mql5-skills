# General program properties (#property)

Using the #property directive, a programmer can set some properties of an MQL program. Some of these properties are general, that is, applicable to any program, and we will consider them here. The remaining properties are typical for specific types of MQL5 programs and will be discussed in the relevant sections of Part 5 when describing the MQL5 API.

Directive #property has the following format:

```
#property key value

```

The key is one of the properties listed in the following table, in the first column. The second column specifies how the value will be interpreted.

| Property | Value |
| --- | --- |
| copyright | String with information about the copyright holder |
| link | String with a link to the developer's site |
| version | String with the program version number (for the MQL5 Market, it must be in the "X.Y" format, where X and Y are integers corresponding to the major and minor build numbers) |
| description | Line with program description (several  #description  directives are allowed and their contents are combined) |
| icon | String, path to the file with the program logo in ICO format |
| stacksize | Integer specifying the size of the stack in bytes (by default it is from 4 to 16 MB, depending on the type of program and environment, 1 MB = 1024*1024 bytes); if necessary, the size increases up to 64 MB (maximum) |

All aforementioned string properties are the source of information for the program's properties dialog, which opens when it starts. However, for scripts, this dialog is not displayed by default. To change this behavior, you must additionally specify the #property [script_show_inputs](/en/book/applications/script_service/scripts) directive. In addition, information about the rights is displayed in a tooltip when hovering the mouse cursor over the program in the MetaTrader 5 Navigator.

The copyright, link, and version properties have already been seen in all the previous examples in this book.

The stack size stacksize is a recommendation: if the compiler finds local variables (usually arrays) in the source code that exceed the specified value, the stack will be automatically increased during compilation, but up to no more than 64 MB. If the limit is exceeded, the program will not even be able to start: in the log (tab Log, and not Experts) the error "Stack size of 64MB exceeded. Reduce the memory occupied by local variables" will occur.

Please note that such analysis and launch prevention only take into account a fixed snapshot of the program at the time of launch. In the case of recursive function calls, the stack memory consumption can increase significantly and lead to a stack overflow error, but already at the program execution stage. For more information about the stack, see the note in [Describing arrays](/en/book/basis/arrays/arrays_declaration).

The #property directives work only in the compiled mq5 file, and are ignored in all those included with #include.
