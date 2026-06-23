# CTerminalInfo

CTerminalInfo is a class for simplified access to the properties of mql5 program environment.

### Description

CTerminalInfo class provides access to the properties of mql5 program environment.

### Declaration

```
   class CTerminalInfo : public CObject

```

### Title

```
   #include <Trade\TerminalInfo.mqh>

```

```
Inheritance hierarchy
   CObject
       CTerminalInfo

```

### Class methods by groups

| Methods for access to the properties of integer type |  |
| --- | --- |
| Build | Gets the build number of the client terminal |
| IsConnected | Gets the information about connection to trade server |
| IsDLLsAllowed | Gets the information about permission of DLL usage |
| IsTradeAllowed | Gets the information about permission to trade |
| IsEmailEnabled | Gets the information about permission to send e-mails to SMTP server and login, specified in the terminal settings |
| IsFtpEnabled | Gets the information about permission to send trade reports to FTP server and login, specified in the terminal settings |
| MaxBars | Gets the information about maximum number of bars on chart |
| CodePage | Gets the information about the code page of the language in the client terminal |
| CPUCores | Gets the information about the CPU cores |
| MemoryPhysical | Gets the information about the physical memory (in Mb) |
| MemoryTotal | Gets the information about the total memory available for the terminal/agent process (in Mb) |
| MemoryAvailable | Gets the information about the free memory available for the terminal/agent process (in Mb) |
| MemoryUsed | Gets the information about the memory used by the terminal/agent process (in Mb) |
| IsX64 | Gets the information about the type of the client terminal |
| OpenCLSupport | Gets the information about the version of OpenCL supported by video card |
| DiskSpace | Gets the information about free disk space (in Mb) |
| Methods for access to the properties of string type |  |
| Language | Gets the language of the client terminal |
| Name | Gets the name of the client terminal |
| Company | Gets the company name of the client terminal |
| Path | Gets the folder of the client terminal |
| DataPath | Gets the data folder of the client terminal |
| CommonDataPath | Gets the common data folder of all client terminals, installed on the computer |
| Access to MQL5 API functions |  |
| InfoInteger | Gets the value of the property of integer type |
| InfoString | Gets the value of property of string type |

```
Methods inherited from class CObject
Prev, Prev, Next, Next, Save, Load, Type, Compare

```
