# DLL connection specifics

The following entities cannot be passed as parameters into functions imported from a DLL:

- Classes (objects and pointers to them)
- Structures containing dynamic arrays, strings, classes, and other complex structures
- Arrays of strings or the above complex objects

All simple type parameters are passed by value unless explicitly stated that they are passed by reference. When passing a string, the buffer address of the copied string is passed; if the string is passed by reference, then the buffer address of this particular string is passed to the function imported from the DLL without copying.

When passing an array to DLL, the address of the data buffer beginning is always passed (regardless of the [AS_SERIES](/en/book/common/arrays/arrays_as_series) flag). The function inside the DLL knows nothing about the AS_SERIES flag, the passed array is an array of unknown length, and an additional parameter is needed to specify its size.

When describing the prototype of an imported function, you can use parameters with default values.

When importing DLLs, you should give permission to use them in the properties of a specific MQL program or in the general settings of the terminal. In this regard, in the [Permissions](/en/book/common/environment/env_permissions) section, we presented the script EnvPermissions.mq5, which, in particular, has a function for reading the contents of the Windows system clipboard using system DLLs. This function was provided optionally: its call was commented out because we did not know how to work with libraries. Now, we will transfer it to a separate script LibClipboard.mq5.

Running the script may prompt the user for confirmation (since DLLs are disabled by default for security reasons). If necessary, enable the option in the dialog, on the tab with dependencies.

Header files are provided in the directory MQL5/Include/WinApi, which also includes #import directives for much-needed system functions such as clipboard management (openclipboard, GetClipboardData, and CloseClipboard), memory management (GlobalLock and GlobalUnlock), Windows windows, and many others. We will include only two files: winuser.mqh and winbase.mqh. They contain the required import directives and, indirectly, through the connection to windef.mqh, Windows term macros (HANDLE and PVOID):

```
#define HANDLE  long
#define PVOID   long
   
#import "user32.dll"
...
int             OpenClipboard(HANDLE wnd_new_owner);
HANDLE          GetClipboardData(uint format);
int             CloseClipboard(void);
...
#import
   
#import "kernel32.dll"
...
PVOID           GlobalLock(HANDLE mem);
int             GlobalUnlock(HANDLE mem);
...
#import

```

In addition, we import the lstrcatW function from the kernel32.dll library because we are not satisfied with its description in winbase.mqh provided by default: this gives the function a second prototype, suitable for passing the PVOID value in the first parameter.

```
#include <WinApi/winuser.mqh>
#include <WinApi/winbase.mqh>
   
#define CF_UNICODETEXT 13 // one of the standard exchange formats - Unicode text
#import "kernel32.dll"
string lstrcatW(PVOID string1, const string string2);
#import

```

The essence of working with the clipboard is to "capture" access to it using OpenClipboard, after which you should get a data handle (GetClipboardData), convert it to a memory address (GlobalLock), and finally copy the data from system memory to your variable (lstrcatW). Next, the occupied resources are released in reverse order (GlobalUnlock and CloseClipboard).

```
void ReadClipboard()
{
   if(OpenClipboard(NULL))
   {
      HANDLE h = GetClipboardData(CF_UNICODETEXT);
      PVOID p = GlobalLock(h);
      if(p != 0)
      {
         const string text = lstrcatW(p, "");
         Print("Clipboard: ", text);
         GlobalUnlock(h);
      }
      CloseClipboard();
   }
}

```

Try copying the text to the clipboard and then running the script: the contents of the clipboard should be logged. If the buffer contains an image or other data that does not have a textual representation, the result will be empty.

Functions imported from a DLL follow the binary executable linking convention of Windows API functions. To ensure this convention, compiler-specific keywords are used in the source text of programs, such as, for example, __stdcall in C or C++. These linking rules imply the following:

- The calling function (in our case, the MQL program) must see the prototype of the called (imported from the DLL) function in order to correctly stack the parameters on the stack.
- The calling function (in our case, the MQL program) stacks parameters in reverse order, from right to left — this is the order in which the imported function reads the parameters passed to it.
- Parameters are passed by value, except for those that are explicitly passed by reference (in our case, strings).
- The imported function reads the parameters passed to it and clears the stack.

Here is another example of a script that uses a DLL — LibWindowTree.mq5. Its task is to go through the tree of all terminal windows and get their class names (according to registration in the system using WinApi) and titles. By windows here we mean the standard elements of the Windows interface, which also include controls. This procedure can be useful for automating work with the terminal: emulating button presses in windows, switching modes that are not available via MQL5, and so on.

To import the required system functions, let's include the header file WinUser.mqh that uses user32.dll.

```
#include <WinAPI/WinUser.mqh>

```

You can get the name of the window class and its title using the functions GetClassNameW and GetWindowTextW: they are called in the function GetWindowData.

```
void GetWindowData(HANDLE w, string &clazz, string &title)
{
   static ushort receiver[MAX_PATH];
   if(GetWindowTextW(w, receiver, MAX_PATH))
   {
      title = ShortArrayToString(receiver);
   }
   if(GetClassNameW(w, receiver, MAX_PATH))
   {
      clazz = ShortArrayToString(receiver);
   }
}

```

The 'W' suffix in function names means that they are intended for Unicode format strings (2 bytes per character), which are the most commonly used today (the 'A' suffix for ANSI strings makes sense to use only for backward compatibility with old libraries).

Given some initial handle to a Windows window, traversing up the hierarchy of its parent windows is provided by the function TraverseUp: its operation is based on the system function GetParent. For each found window, TraverseUp calls GetWindowData and outputs the resulting class name and title to the log.

```
HANDLE TraverseUp(HANDLE w)
{
   HANDLE p = 0;
   while(w != 0)
   {
      p = w;
      string clazz, title;
      GetWindowData(w, clazz, title);
      Print("'", clazz, "' '", title, "'");
      w = GetParent(w);
   }
   return p;
}

```

Traversing deep into the hierarchy is performed by the function TraverseDown: the system function FindWindowExW is used to enumerate child windows.

```
HANDLE TraverseDown(const HANDLE w, const int level = 0)
{
   // request first child window (if any)
   HANDLE child = FindWindowExW(w, NULL, NULL, NULL);
   while(child)          // oop while there are child windows
   {
      string clazz, title;
      GetWindowData(child, clazz, title);
      Print(StringFormat("%*s", level * 2, ""), "'", clazz, "' '", title, "'");
      TraverseDown(child, level + 1);
      // requesting next child window
      child = FindWindowExW(w, child, NULL, NULL);
   }
   return child;
}

```

In the OnStart function, we find the main terminal window by traversing the windows up from the handle of the current chart on which the script is running. Then we build the entire tree of terminal windows.

```
void OnStart()
{
   HANDLE h = TraverseUp(ChartGetInteger(0, CHART_WINDOW_HANDLE));
   Print("Main window handle: ", h);
   TraverseDown(h, 1);
}

```

We can also search for the required windows by class name and/or title, and therefore the main window could be immediately obtained by calling FindWindowW, since its attributes are known.

```
   h = FindWindowW("MetaQuotes::MetaTrader::5.00", NULL); 

```

Here is an example log (snippet):

```
 'AfxFrameOrView140su' ''
 'Afx:000000013F110000:b:0000000000010003:0000000000000006:00000000000306BA' 'EURUSD,H1'
 'MDIClient' ''
 'MetaQuotes::MetaTrader::5.00' '12345678 - MetaQuotes-Demo: Demo Account - Hedge - ...'
Main window handle: 263576
  'msctls_statusbar32' 'For Help, press F1'
  'AfxControlBar140su' 'Standard'
    'ToolbarWindow32' 'Timeframes'
    'ToolbarWindow32' 'Line Studies'
    'ToolbarWindow32' 'Standard'
  'AfxControlBar140su' 'Toolbox'
    'Afx:000000013F110000:b:0000000000010003:0000000000000000:0000000000000000' 'Toolbox'
      'AfxWnd140su' ''
        'ToolbarWindow32' ''
...
  'MDIClient' ''
    'Afx:000000013F110000:b:0000000000010003:0000000000000006:00000000000306BA' 'EURUSD,H1'
      'AfxFrameOrView140su' ''
        'Edit' '0.00'
    'Afx:000000013F110000:b:0000000000010003:0000000000000006:00000000000306BA' 'XAUUSD,Daily'
      'AfxFrameOrView140su' ''
        'Edit' '0.00'
    'Afx:000000013F110000:b:0000000000010003:0000000000000006:00000000000306BA' 'EURUSD,M15'
      'AfxFrameOrView140su' ''
        'Edit' '0.00'
 

```
