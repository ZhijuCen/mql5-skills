# SocketIsWritable

Check whether data can be written to a socket at the current time.

```
bool  SocketIsWritable(
   const int  socket      // socket handle
   );

```

Parameters

socket

[in]  Socket handle returned by the [SocketCreate](/en/docs/network/socketcreate) function. When an incorrect handle is passed, the error 5270 (ERR_NETSOCKET_INVALIDHANDLE) is written to [_LastError](/en/docs/predefined/_lasterror).

Return Value

Return true if writing is possible, otherwise false.

Note

This function allows you to check whether it is possible to write data to a socket right now.

If an error occurs on a system socket when executing the function, connection established via [SocketConnect](/en/docs/network/socketconnect) is discontinued.

The function can be called only from Expert Advisors and scripts, as they run in their own execution threads. If calling from an indicator, [GetLastError()](/en/docs/check/getlasterror) returns the error 4014 – "Function is not allowed for call".

Example:

```
//+------------------------------------------------------------------+
//|                                             SocketIsWritable.mq5 |
//|                                  Copyright 2024, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com
#property version     "1.00"
#property description "Add Address to the list of allowed ones in the terminal settings to let the example work"
#property script_show_inputs
 
input string Address    ="www.mql5.com";
input int    Port       =80;
bool         ExtTLS =false;
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart(void)
  {
//--- create a socket and get its handle
   int socket=SocketCreate();
//--- check the handle
   if(socket!=INVALID_HANDLE)
     {
      //--- if all is well, connect
      if(SocketConnect(socket,Address,Port,1000))
        {
         PrintFormat("Established connection to %s:%d",Address,Port);
 
         string   subject,issuer,serial,thumbprint;
         datetime expiration;
         //--- if connection is protected by certificate, display its data
         if(SocketTlsCertificate(socket,subject,issuer,serial,thumbprint,expiration))
           {
            Print("TLS certificate:");
            Print("   Owner:      ",subject);
            Print("   Issuer:     ",issuer);
            Print("   Number:     ",serial);
            Print("   Print:      ",thumbprint);
            Print("   Expiration: ",expiration);
            ExtTLS=true;
           }
         //--- send GET request to the server
         if(HTTPSend(socket,"GET / HTTP/1.1\r\nHost: www.mql5.com\r\nUser-Agent: MT5\r\n\r\n"))
           {
            Print("GET request sent");
            //--- read response
            if(!HTTPRecv(socket,1000))
               Print("Failed to get a response, error ",GetLastError());
           }
         else
            Print("Failed to send GET request, error ",GetLastError());
        }
      else
        {
         PrintFormat("Connection to %s:%d failed, error %d",Address,Port,GetLastError());
        }
      //--- display the ability to write data to the socket at the current moment in time in the journal
      if(SocketIsWritable(socket))
         Print("At the current moment in time, writing data to the socket is possible");
      else
         Print("It is not possible to write data to the socket at the current time");
      //--- close the socket after use
      if(SocketClose(socket))
         Print("Now the socket is closed");
     }
   else
      Print("Failed to create a socket, error ",GetLastError());
   /*
   result:
   At the current moment in time, writing data to the socket is possible
   Socket is closed now
   */
  }
//+------------------------------------------------------------------+
//| Send command to server                                           |
//+------------------------------------------------------------------+
bool HTTPSend(int socket,string request)
  {
//--- convert the string to a character array, discard the terminating zero
   char req[];
   int  len=StringToCharArray(request,req)-1;
 
   if(len<0)
      return(false);
//--- if a secure TLS connection via port 443 is used
   if(ExtTLS)
      return(SocketTlsSend(socket,req,len)==len);
//--- if a regular TCP connection is used
   return(SocketSend(socket,req,len)==len);
  }
//+------------------------------------------------------------------+
//| Read server response                                             |
//+------------------------------------------------------------------+
bool HTTPRecv(int socket,uint timeout_ms)
  {
   char   rsp[];
   string result;
   ulong  timeout_check=GetTickCount64()+timeout_ms;
//--- read data from the socket while there is some, but not longer than timeout
   do
     {
      uint len=SocketIsReadable(socket);
 
      if(len)
        {
         int rsp_len;
         //--- different read commands depending on whether the connection is secure or not
         if(ExtTLS)
            rsp_len=SocketTlsRead(socket,rsp,len);
         else
            rsp_len=SocketRead(socket,rsp,len,timeout_ms);
         //--- parse response
         if(rsp_len>0)
           {
            result+=CharArrayToString(rsp,0,rsp_len);
            //--- display response header only
            int header_end=StringFind(result,"\r\n\r\n");
 
            if(header_end>0)
              {
               Print("HTTP answer header received:");
               Print(StringSubstr(result,0,header_end));
               return(true);
              }
            //--- update read timeout expiration time
            timeout_check=GetTickCount64()+timeout_ms;
           }
        }
     }
   while(GetTickCount64()<timeout_check && !IsStopped());
 
   return(false);
  }

```
