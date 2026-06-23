# Library file search order

If the library name is specified without a path or with a relative path, the search is performed according to different rules depending on the type of library.

System libraries (DLL) are loaded according to the rules of the operating system. If the library is already loaded (for example, by another Expert Advisor, or even from another client terminal launched in parallel), then the call goes to the already loaded library. Otherwise, the search goes in the following sequence:

1. The folder from which the compiled EX5 program that imported the DLL was launched.
2. The MQL5/Libraries folder.
3. The folder where the running MetaTrader 5 terminal is located.
4. System folder (usually inside Windows).
5. Windows directory.
6. The current working folder of the terminal process (may be different from the terminal's location folder).
7. Folders listed in the PATH system variable.

In the #import directives, it is not recommended to use a fully qualified loadable module name of the form Drive:/Directory/FileName.dll.

If the DLL uses another DLL in its work, then in the absence of the second DLL, the first one will not be able to load.

The search for an imported EX5 library is performed in the following sequence:

1. Folder for launching the importing EX5 program.
2. Folder MQL5/Libraries of specific terminal instance.
3. Folder MQL5/Libraries in the common folder of all MetaTrader 5 terminals (Common/MQL5/Libraries).

Before loading an MQL program, a general list of all EX5 library modules is formed, where the supported modules are to be used both from the program itself and from libraries from this list. It's called a dependency list and can become a very branched "tree".

For EX5 libraries, the terminal also provides a one-time download of reusable modules.

Regardless of the type of the library, each instance of it works with its own data related to the context of the calling Expert Advisor, script, service, or indicator. Libraries are not a tool for shared access to MQL5 variables or arrays.

EX5 libraries and DLLs run on the thread of the calling module.

There are no regular means to find in the library code where it was loaded from.
