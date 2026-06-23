# Including Files (#include)

The #include command line can be placed anywhere in the program, but usually all inclusions are placed at the beginning of the source code. Call format:

```
#include <file_name>
#include "file_name"

```

Examples:

```
#include <WinUser32.mqh>
#include "mylib.mqh"

```

The preprocessor replaces the line #include <file_name> with the content of the file WinUser32.mqh. Angle brackets indicate that the WinUser32.mqh file will be taken from the standard directory (usually it is terminal_installation_directory\MQL5\Include). The current directory is not included in the search.

If the file name is enclosed in quotation marks, the search is made in the current directory (which contains the main source file). The standard directory is not included in the search.

See also

[Standard Library](/en/docs/standardlibrary), [Importing Functions](/en/docs/basis/preprosessor/import)
