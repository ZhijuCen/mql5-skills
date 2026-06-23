# SocketTimeouts

Set timeouts for receiving and sending data for a socket system object.

```
bool  SocketTimeouts(
   int           socket,               // socket
   uint          timeout_send_ms,      // data sending timeout
   uint          timeout_receive_ms    // data obtaining timeout
   );

```

Parameters

socket

[in]  Socket handle returned by the [SocketCreate](/en/docs/network/socketcreate) function. When an incorrect handle is passed, the error 5270 (ERR_NETSOCKET_INVALIDHANDLE) is written to [_LastError](/en/docs/predefined/_lasterror).

timeout_send_ms

[in]  Data sending timeout in milliseconds.

timeout_receive_ms

[in]  Data obtaining timeout in milliseconds.

Return Value

Returns true if successful, otherwise false.

Note

Do not confuse system object timeouts with the ones set when reading data via [SocketRead](/en/docs/network/socketread). SocketTimeout sets timeouts once for a socket object in the operating system. These timeouts are to be applied to all functions for reading and sending data via this socket. In SocketRead, the timeout is set for a certain data reading operation.

The function can be called only from Expert Advisors and scripts, as they run in their own execution threads. If calling from an indicator, [GetLastError()](/en/docs/check/getlasterror) returns the error 4014 – "Function is not allowed for call".

Example:

```
//+------------------------------------------------------------------+
//|                                               SocketTimeouts.mq5 |
//|                                  Copyright 2024, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com
#property version     "1.00"
 
#define   TIMEOUT_SEND     5000
#define   TIMEOUT_RECEIVE  5000
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart(void)
  {
//--- create a socket and get its handle
   int socket=SocketCreate();
 
   if(socket==INVALID_HANDLE)
     {
      Print("SocketCreate() failed. Error ",GetLastError());
      return;
     }
//--- set timeouts for receiving and sending data for a socket system object
   if(SocketTimeouts(socket,TIMEOUT_SEND,TIMEOUT_RECEIVE))
      PrintFormat("timeouts were successfully set",socket,TIMEOUT_SEND,TIMEOUT_RECEIVE);
   else
      PrintFormat("SocketTimeouts(%d, %I64d, %I64d) failed. Error %d",socket,TIMEOUT_SEND,TIMEOUT_RECEIVE,GetLastError());
//--- close socket
   SocketClose(socket);
  }

```
