# Sending files to an FTP server

MetaTrader 5 supports sending files to an FTP server. For this feature to work, you must enter the necessary FTP details in the settings dialog on the FTP tab: FTP server address, login, password, and optionally the path for placing files on the server. If your computer is on the network of an ISP that has not allocated a public IP address for you, then you will probably need to turn on the passive mode.

Sending files directly from an MQL program is supported by the SendFTP function.

bool SendFTP(const string filename, const string path = NULL)

The function sends a file with the specified name to the FTP server from the terminal settings. If necessary, you can specify a different path than the one configured in advance. If the path parameter is not specified, the directory described in the settings is used.

The uploaded file must be located in the folder MQL5/Files or its subfolders.

The function returns an indicator of success (true) or error (false). Potential errors in _LastError include:

- 4514 — ERR_FTP_SEND_FAILED — failed to send a file via FTP
- 4519 — ERR_FTP_NOSERVER — FTP server not specified
- 4520 — ERR_FTP_NOLOGIN — FTP login was not specified
- 4521 — ERR_FTP_FILE_ERROR — the specified file was not found in the MQL5/Files directory
- 4522 — ERR_FTP_CONNECT_FAILED — an error occurred while connecting to the FTP server
- 4523 — ERR_FTP_CHANGEDIR — the directory for uploading the file was not found on the FTP server
- 4524 — ERR_FTP_CLOSED — the connection to the FTP server was closed

The function blocks the execution of the MQL program until the operation is completed. In this regard, the function is not allowed to be used in indicators.

Also, the SendFTP function is not executed in the strategy tester.

The terminal only supports sending a single file to an FTP server. All other FTP commands are not available from MQL5.

The example script NetFtp.mq5 takes a screenshot of the current chart and tries to send it via FTP.

```
void OnStart()
{
   const string filename = _Symbol + "-" + PeriodToString() + "-"
      + (string)(ulong)TimeTradeServer() + ".png";
   PRTF(ChartScreenShot(0, filename, 300, 200));
   Print("Sending file: " + filename);
   PRTF(SendFTP(filename, "/upload")); // 0 (success) or FTP_CONNECT_FAILED(4522), FTP_CHANGEDIR(4523), etc.
}

```
