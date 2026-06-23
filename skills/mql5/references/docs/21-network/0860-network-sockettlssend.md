# SocketTlsSend

Send data via secure TLS connection.

```
int  SocketTlsSend(
   int           socket,               // socket
   const uchar&  buffer[],             // data buffer
   uint          buffer_len            // buffer size
   );

```

Parameters

socket

[in]  Socket handle returned by the [SocketCreate](/en/docs/network/socketcreate) function. When an incorrect handle is passed, the error 5270 (ERR_NETSOCKET_INVALIDHANDLE) is written to [_LastError](/en/docs/predefined/_lasterror).

buffer

[in]  Reference to the [uchar](/en/docs/basis/types/integer/integertypes) type array with the data to be sent.

buffer_len

[in]  'buffer' array size.

Return Value

If successful, return the number of bytes written to a socket. In case of an error, -1 is returned.

Note

If an error occurs on a system socket when executing the function, connection established via [SocketConnect](/en/docs/network/socketconnect) is discontinued.

In case of a data writing error, the error 5273 (ERR_NETSOCKET_IO_ERROR) is written to [_LastError](/en/docs/predefined/_lasterror).

The function can be called only from Expert Advisors and scripts, as they run in their own execution threads. If calling from an indicator, [GetLastError()](/en/docs/check/getlasterror) returns the error 4014 – "Function is not allowed for call".

Example:

```
//+------------------------------------------------------------------+
//|                                                SocketTlsSend.mq5 |
//|                                  Copyright 2024, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com
#property version     "1.00"
#property description "Add Address to the list of allowed ones in the terminal settings to let the example work"
#property script_show_inputs
 
input string Address="www.mql5.com";
input int    Port   =443;
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart(void)
  {
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
           }
         //--- send GET request to the server
         string request="GET / HTTP/1.1\r\nHost: www.mql5.com\r\nUser-Agent: MT5\r\n\r\n";
         char   req[];
         int    len=StringToCharArray(request,req)-1;
 
         if(len<0)
           {
            Print("StringToCharArray() failed. Error ", GetLastError());
            SocketClose(socket);
            return;
           }
         //--- if a secure TLS connection via port 443 is used
         if(SocketTlsSend(socket,req,len)==len)
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
      //--- close the socket after use
      SocketClose(socket);
     }
   else
      Print("Failed to create a socket, error ",GetLastError());
  }
//+------------------------------------------------------------------+
//| Read server response                                             |
//+------------------------------------------------------------------+
bool HTTPRecv(int socket,uint timeout_ms)
  {
//--- read data from the socket while there is some, but not longer than timeout
   char   rsp[];
   string result;
   ulong  timeout_check=GetTickCount64()+timeout_ms;
 
   do
     {
      uint len=SocketIsReadable(socket);
 
      if(len)
        {
         //--- read and parse the data of a secure TLS connection
         int rsp_len=SocketTlsRead(socket,rsp,len);
 
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

See also

[SocketTimeouts](/en/docs/network/sockettimeouts), [MathSwap](/en/docs/math/mathswap), [StringToCharArray](/en/docs/convert/stringtochararray)
