# Programmatically closing the terminal and setting a return code

The MQL5 API contains several functions not only for reading but also for modifying the program environment. One of the most radical of them is TerminalClose. Using this function, an MQL program can close the terminal (without user confirmation!).

bool TerminalClose(int retcode)

The function has one parameter retcode which is the code returned by the terminal64.exe process to the Windows operating system. Such codes can be analyzed in batch files (*.bat and *.cmd), as well as in shell scripts (Windows Script Host (WSH), which supports VBScript and JScript, or Windows PowerShell (WPS), with .ps* files) and other automation tools (for example, the built-in Windows scheduler, the Linux support subsystem under Windows with *.sh files, etc.).

The function does not immediately stop the terminal, but sends a termination command to the terminal.

If the result of the call is true, it means that the command has been successfully "accepted for consideration", and the terminal will try to close as quickly as possible, but correctly (generating a notification and stopping other running MQL programs). In the calling code, of course, all preparations must also be made for the immediate termination of work (in particular, all previously opened files should be closed), and after the function call, control should be returned to the terminal.

Another function associated with the process return code is SetReturnError. It allows you to pre-assign this code without sending an immediate close command.

void SetReturnError(int retcode)

The function sets the code that the terminal process will return to the Windows system after closing.

Please note that the terminal does not need to be forcibly closed by the TerminalClose function. Regular closing of the terminal by the user will also occur with the specified code. Also, this code will enter the system if the terminal closes due to an unexpected critical error.

If the SetReturnError function was called repeatedly and/or from different MQL programs, the terminal will return the last set code.

Let's test these functions using the EnvClose.mq5 script.

```
#property script_show_inputs
   
input int ReturnCode = 0;
input bool CloseTerminalNow = false;
   
void OnStart()
{
   if(CloseTerminalNow)
   {
      TerminalClose(ReturnCode);
   }
   else
   {
      SetReturnError(ReturnCode);
   }
}

```

To test it in action, we also need the file envrun.bat (located in the folder MQL5/Files/MQL5Book/).

```
terminal64.exe
@echo Exit code: %ERRORLEVEL%

```

In fact, it only launches the terminal, and after its completion displays the resulting code to the console. The file should be placed in the terminal folder (or the current instance of MetaTrader 5 from among several installed in the system should be registered in the PATH system variable).

For example, if we start the terminal using the bat file, and execute the script EnvClose.mq5, for example, with parameters ReturnCode=100, CloseTerminalNow=true, we will see something like this in the console:

```
Microsoft Windows [Version 10.0.19570.1000]
(c) 2020 Microsoft Corporation. All rights reserved.
C:\Program Files\MT5East>envrun
C:\Program Files\MT5East>terminal64.exe
Exit code: 100
C:\Program Files\MT5East>

```

As a reminder, MetaTrader 5 supports various options when launched from the command line (see details in the documentation section [Running the trading platform](https://www.metatrader5.com/en/terminal/help/start_advanced/start#command_line)). Thus, it is possible to organize, for example, batch testing of various Expert Advisors or settings, as well as sequential switching between thousands of monitored accounts, which would be unrealistic to achieve with the constant parallel operation of so many instances on one computer.
