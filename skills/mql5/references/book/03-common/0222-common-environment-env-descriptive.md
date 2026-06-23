# Terminal and program string properties

The MQLInfoString and TerminalInfoString functions can be used to find out several string properties of the terminal and MQL program.

| Identifier | Description |
| --- | --- |
| MQL_PROGRAM_NAME | The name of the running MQL program |
| MQL_PROGRAM_PATH | Path for this running MQL program |
| TERMINAL_LANGUAGE | Terminal language |
| TERMINAL_COMPANY | Name of the company (broker) |
| TERMINAL_NAME | Terminal name |
| TERMINAL_PATH | The folder from which the terminal is launched |
| TERMINAL_DATA_PATH | The folder where terminal data is stored |
| TERMINAL_COMMONDATA_PATH | The shared folder of all client terminals installed on the computer |

The name of the running program (MQL_PROGRAM_NAME) usually coincides with the name of the main module (mq5 file) but may differ. In particular, if your source code compiles to a [library](/en/book/advanced/libraries) which is imported into another MQL program (Expert Advisor, indicator, script, or service), then the MQL_PROGRAM_NAME property will return the name of the main program, not the library (the library is not an independent program that can be run).

We discussed the arrangement of working terminal folders in [Working with files](/en/book/common/files). Using the listed properties, you can find out where the terminal is installed (TERMINAL_PATH), as well as find the working data of the current terminal instance (TERMINAL_DATA_PATH) and of all instances (TERMINAL_COMMONDATA_PATH).

A simple script EnvDescription.mq5 logs all these properties.

```
void OnStart()
{
   PRTF(MQLInfoString(MQL_PROGRAM_NAME));
   PRTF(MQLInfoString(MQL_PROGRAM_PATH));
   PRTF(TerminalInfoString(TERMINAL_LANGUAGE));
   PRTF(TerminalInfoString(TERMINAL_COMPANY));
   PRTF(TerminalInfoString(TERMINAL_NAME));
   PRTF(TerminalInfoString(TERMINAL_PATH));
   PRTF(TerminalInfoString(TERMINAL_DATA_PATH));
   PRTF(TerminalInfoString(TERMINAL_COMMONDATA_PATH));
}

```

Below is an example result.

```
MQLInfoString(MQL_PROGRAM_NAME)=EnvDescription / ok
MQLInfoString(MQL_PROGRAM_PATH)= »
» C:\Program Files\MT5East\MQL5\Scripts\MQL5Book\p4\EnvDescription.ex5 / ok
TerminalInfoString(TERMINAL_LANGUAGE)=Russian / ok
TerminalInfoString(TERMINAL_COMPANY)=MetaQuotes Software Corp. / ok
TerminalInfoString(TERMINAL_NAME)=MetaTrader 5 / ok
TerminalInfoString(TERMINAL_PATH)=C:\Program Files\MT5East / ok
TerminalInfoString(TERMINAL_DATA_PATH)=C:\Program Files\MT5East / ok
TerminalInfoString(TERMINAL_COMMONDATA_PATH)= »
» C:\Users\User\AppData\Roaming\MetaQuotes\Terminal\Common / ok

```

The interface language of the terminal can be found not only as a string in the TERMINAL_LANGUAGE property but also as a code page number (see the TERMINAL_CODEPAGE property in the next section).
