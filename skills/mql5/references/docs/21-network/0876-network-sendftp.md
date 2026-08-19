# SendFTP

Sends a file at the address, specified in the setting window of the "FTP" tab.

```
bool  SendFTP(
   string  filename,          // file to be send by ftp
   string  ftp_path=NULL      // ftp catalog
   );

```

Parameters

filename

[in]   Name of sent file.

ftp_path=NULL

[in]   FTP catalog. If a directory is not specified, directory described in settings is used.

Return Value

In case of failure returns 'false'.

Note

Sent file must be located in the folder terminal_directory\MQL5\files or its subfolders. Sending isn't performed if FTP address and/or access password are not specified in settings.

SendFTP() function does not work in the [Strategy Tester](/en/docs/runtime/testing#alert_etc).

Example:

```
//+------------------------------------------------------------------+
//|                                                      SendFTP.mq5 |
//|                                  Copyright 2024, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com
#property version     "1.00"
 
#define   FILENAME  "SomeFile.bin"
#define   PATH      NULL
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart(void)
  {
//--- check permission to send files to the FTP address in the terminal
   if(!TerminalInfoInteger(TERMINAL_FTP_ENABLED))
     {
      Print("Error. The client terminal does not have permission to send messages to the FTP-address");
      return;
     }
//--- send file
   ResetLastError();
   if(!SendFTP(FILENAME, PATH))
      Print("SendFTP() failed. Error ",GetLastError());
  }

```
