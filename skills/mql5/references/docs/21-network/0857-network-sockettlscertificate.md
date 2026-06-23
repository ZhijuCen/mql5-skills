# SocketTlsCertificate

Get data on the certificate used to secure network connection.

```
bool  SocketTlsCertificate(
   int           socket,               // socket
   string&       subject,              // certificate owner
   string&       issuer,               // certificate issuer
   string&       serial,               // certificate serial number
   string&       thumbprint,           // certificate print
   datetime&     expiration            // certificate expiration
   );

```

Parameters

socket

[in]  Socket handle returned by the [SocketCreate](/en/docs/network/socketcreate) function. When an incorrect handle is passed, the error 5270 (ERR_NETSOCKET_INVALIDHANDLE) is written to [_LastError](/en/docs/predefined/_lasterror).

subject

[in]  Certificate owner name. Corresponds to the Subject field.

issuer

[in]  Certificate issuer name. Corresponds to the Issuer field.

serial

[in]  Certificate serial number. Corresponds to the SerialNumber field.

thumbprint

[in]  Certificate print. Corresponds to the SHA-1 hash from the entire certificate file (all fields including the issuer signature).

expiration

[in]  Certificate expiration date in the [datetime](/en/docs/basis/types/integer/datetime) format.

Return Value

Returns true if successful, otherwise false.

Note

Certificate data can be requested only after establishing a secure connection using [SocketTlsHandshake](/en/docs/network/sockettlshandshake).

In case of a certificate obtaining error, the error 5275 (ERR_NETSOCKET_NO_CERTIFICATE) is written to [_LastError](/en/docs/predefined/_lasterror).

The function can be called only from Expert Advisors and scripts, as they run in their own execution threads. If calling from an indicator, [GetLastError()](/en/docs/check/getlasterror) returns the error 4014 – "Function is not allowed for call".

Example:

```
//+------------------------------------------------------------------+
//|                                                SocketExample.mq5 |
//|                        Copyright 2018, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright   "Copyright 2000-2024, MetaQuotes Ltd."
#property link        "https://www.mql5.com"
#property version     "1.00"
#property description "Add Address to the list of allowed ones in the terminal settings to let the example work"
#property script_show_inputs
 
input string Address="www.mql5.com";
input int    Port   =80;
bool         ExtTLS =false;
//+------------------------------------------------------------------+
//| Send command to the server                                       |
//+------------------------------------------------------------------+
bool HTTPSend(int socket,string request)
  {
   char req[];
   int  len=StringToCharArray(request,req)-1;
   if(len<0)
      return(false);
//--- if secure TLS connection is used via the port 443
   if(ExtTLS)
      return(SocketTlsSend(socket,req,len)==len);
//--- if standard TCP connection is used
   return(SocketSend(socket,req,len)==len);
  }
//+------------------------------------------------------------------+
//| Read server response                                             |
//+------------------------------------------------------------------+
bool HTTPRecv(int socket,uint timeout)
  {
   char   rsp[];
   string result;
   uint   timeout_check=GetTickCount()+timeout;
//--- read data from sockets till they are still present but not longer than timeout
   do
     {
      uint len=SocketIsReadable(socket);
      if(len)
        {
         int rsp_len;
         //--- various reading commands depending on whether the connection is secure or not
         if(ExtTLS)
            rsp_len=SocketTlsRead(socket,rsp,len);
         else
            rsp_len=SocketRead(socket,rsp,len,timeout);
         //--- analyze the response
         if(rsp_len>0)
           {
            result+=CharArrayToString(rsp,0,rsp_len);
            //--- print only the response header
            int header_end=StringFind(result,"\r\n\r\n");
            if(header_end>0)
              {
               Print("HTTP answer header received:");
               Print(StringSubstr(result,0,header_end));
               return(true);
              }
           }
        }
     }
   while(GetTickCount()<timeout_check && !IsStopped());
   return(false);
  }
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
   int socket=SocketCreate();
//--- check the handle
   if(socket!=INVALID_HANDLE)
     {
      //--- connect if all is well
      if(SocketConnect(socket,Address,Port,1000))
        {
         Print("Established connection to ",Address,":",Port);
 
         string   subject,issuer,serial,thumbprint;
         datetime expiration;
         //--- if connection is secured by the certificate, display its data
         if(SocketTlsCertificate(socket,subject,issuer,serial,thumbprint,expiration))
           {
            Print("TLS certificate:");
            Print("   Owner:  ",subject);
            Print("   Issuer:  ",issuer);
            Print("   Number:     ",serial);
            Print("   Print: ",thumbprint);
            Print("   Expiration: ",expiration);
            ExtTLS=true;
           }
         //--- send GET request to the server
         if(HTTPSend(socket,"GET / HTTP/1.1\r\nHost: www.mql5.com\r\nUser-Agent: MT5\r\n\r\n"))
           {
            Print("GET request sent");
            //--- read the response
            if(!HTTPRecv(socket,1000))
               Print("Failed to get a response, error ",GetLastError());
           }
         else
            Print("Failed to send GET request, error ",GetLastError());
        }
      else
        {
         Print("Connection to ",Address,":",Port," failed, error ",GetLastError());
        }
      //--- close a socket after using
      SocketClose(socket);
     }
   else
      Print("Failed to create a socket, error ",GetLastError());
  }
//+------------------------------------------------------------------+

```
