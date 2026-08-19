# SocketTlsHandshake

Initiate secure TLS (SSL) connection to a specified host via TLS Handshake protocol. During Handshake, a client and a server agree on connection parameters: applied protocol version and data encryption method.

```
bool  SocketTlsHandshake(
   int           socket,               // socket
   const string  host                  // host address
   );

```

Parameters

socket

[in]  Socket handle returned by the [SocketCreate](/en/docs/network/socketcreate) function. When an incorrect handle is passed, the error 5270 (ERR_NETSOCKET_INVALIDHANDLE) is written to [_LastError](/en/docs/predefined/_lasterror).

host

[in]  Address of a host a secure connection is established with.

Return Value

Returns true if successful, otherwise false.

Notes

Before a secure connection, the program should establish a standard TCP connection with the host using [SocketConnect](/en/docs/network/socketconnect).

If secure connection fails, the error 5274 (ERR_NETSOCKET_HANDSHAKE_FAILED) is written to [_LastError](/en/docs/predefined/_lasterror).

There is no need to call the function when [connecting](/en/docs/network/socketconnect) to the port 443. This is a standard TCP port used for secure TLS (SSL) connections.

The function can be called only from Expert Advisors and scripts, as they run in their own execution threads. If calling from an indicator, [GetLastError()](/en/docs/check/getlasterror) returns the error 4014 – "Function is not allowed for call".

Example:

```
//+------------------------------------------------------------------+
//|                                           SocketTlsHandshake.mq5 |
//|                                  Copyright 2024, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com
#property version     "1.00"
 
#define   SERVER    "smtp.gmail.com"
#define   PORT      587
//+------------------------------------------------------------------+
//| Switch manually to secure connection                             |
//+------------------------------------------------------------------+
bool TlsHandshake(int socket)
  {
//--- get server greeting
   string rsp;
 
   if(!RecvString(socket,rsp))
      return(false);
//--- greet server
   if(!SendString(socket,"EHLO my.domain.com\r\n"))
      return(false);
//--- get a server response with a list of supported commands
   if(!RecvString(socket,rsp))
      return(false);
//--- print greeting
   Print("SERVER: ",rsp);
//--- inform the server that we want to switch from an insecure connection to a secure one using TLS
   if(!SendString(socket,"STARTTLS\r\n"))
      return(false);
//--- get server response
   if(!RecvString(socket,rsp))
      return(false);
//--- in the example, we do not check the server response about readiness to switch to TLS ('Ready to start TLS')
 
//--- initiate a secure TLS (SSL) connection to the specified host using the TLS Handshake protocol
   if(SocketTlsHandshake(socket,InpTimeout))
      return(true);
 
   Print("SocketTlsHandshake() failed. Error ",GetLastError());
   return(false);
  }
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
//--- connect to SERVER via PORT
   if(!SocketConnect(socket,SERVER,PORT,10000))
     {
      Print("SocketConnect() failed. Error ",GetLastError());
     }
   else
     {
      //--- insecure connection established
      PrintFormat("%s connection has been established to %s:%d",(PORT==443 ? "A secured" : "An unsecured"),SERVER,PORT);
      //--- switch to secure connection
      if(PORT!=443 && TlsHandshake(socket))
        {
         PrintFormat("Unsecured connection to %s:%d switched to secured",SERVER,PORT);
         //--- if connection is protected by certificate, display its data
         string   subject,issuer,serial,thumbprint;
         datetime expiration;
 
         if(SocketTlsCertificate(socket,subject,issuer,serial,thumbprint,expiration))
           {
            Print("TLS certificate:");
            Print("   Owner:      ",subject);
            Print("   Issuer:     ",issuer);
            Print("   Number:     ",serial);
            Print("   Print:      ",thumbprint);
            Print("   Expiration: ",expiration);
           }
        }
     }
//--- close the socket after use
   SocketClose(socket);
   /*
   result:
   An unsecured connection has been established to smtp.gmail.com:587
   SERVER: 220 smtp.gmail.com ESMTP a640c23a62f3a-a9b1f298319sm82305866b.105 - gsmtp
 
   SERVER: 250-smtp.gmail.com at your service, [37.193.40.122]
   250-SIZE 35882577
   250-8BITMIME
   250-STARTTLS
   250-ENHANCEDSTATUSCODES
   250-PIPELINING
   250-CHUNKING
   250 SMTPUTF8
 
   SERVER: 220 2.0.0 Ready to start TLS
 
   SocketTlsHandshake(): A secure connection to smtp.gmail.com:587 is now established
   TLS certificate:
      Owner:  /CN=smtp.gmail.com
      Issuer:  /C=US/O=Google Trust Services/CN=WR2
      Number:     1f:f4:db:2a:5a:e6:dc:52:0a:4c:05:ce:81:cc:c3:f7
      Print: d6be8af229b5329cd3d4c2789c02aa94f89b421c
      Expiration: 2024.12.30 08:25:30
   */
  }
//+------------------------------------------------------------------+
//| Send string to server                                            |
//+------------------------------------------------------------------+
bool SendString(int socket,const string str)
  {
//--- convert the string to a character array
   uchar data[];
   int   size=StringToCharArray(str,data,0,str.Length(),CP_UTF8);
//--- send data to the socket
   ResetLastError();
   if(SocketSend(socket,data,size)==size)
      return(true);
//--- data sending error
   Print("Failed to send data to server. Error ",GetLastError());
   return false;
  }
//+------------------------------------------------------------------+
//| Get a string from the server                                     |
//+------------------------------------------------------------------+
bool RecvString(int socket,string& result,uint timeout_ms=1000)
  {
//--- wait for data to appear on the socket
   ulong wait_time_end=GetMicrosecondCount()+timeout_ms*1000;
 
   while(!SocketIsReadable(socket))
     {
      Sleep(10);
      //--- timed out waiting for data - return NULL as response
      if(wait_time_end<GetMicrosecondCount())
        {
         Print("ERROR: No response from server");
         return(false);
        }
     }
//--- read data from socket
   uchar  data[128];
   uint   size=0;
   string resp=NULL;
 
   do
     {
      uchar b[1];
      int   n=SocketRead(socket,b,1,1000);
 
      if(n < 0)
         break;
 
      if(n)
        {
         data[size++]=b[0];
 
         if(size==data.Size())
           {
            resp += CharArrayToString(data,0,data.Size(),CP_UTF8);
            size = 0;
           }
        }
     }
   while(SocketIsReadable(socket));
//--- copy the read data into the string
   if(size)
      resp+=CharArrayToString(data,0,size,CP_UTF8);
//--- if string is empty, then error
   if(!resp.Length())
     {
      Print("ERROR: No response from server");
      return(false);
     }
//--- return the string
   result=resp;
   return(true);
  }

```
