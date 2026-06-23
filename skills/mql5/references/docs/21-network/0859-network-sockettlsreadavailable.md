# SocketTlsReadAvailable

Read all available data from secure TLS connection.

```
int  SocketTlsReadAvailable(
   int           socket,               // socket
   uchar&        buffer[],             // buffer for reading data from socket
   const uint    buffer_maxlen         // number of bytes to read
   );

```

Parameters

socket

[in]  Socket handle returned by the [SocketCreate](/en/docs/network/socketcreate) function. When an incorrect handle is passed to [_LastError](/en/docs/predefined/_lasterror), the error 5270 (ERR_NETSOCKET_INVALIDHANDLE) is activated.

buffer

[out]  Reference to the [uchar](/en/docs/basis/types/integer/integertypes) type array the data is read in. Dynamic array size is increased by the number of read bytes. The array size cannot exceed [INT_MAX](/en/docs/constants/namedconstants/typeconstants) (2147483647).

buffer_maxlen

[in]  Number of bytes to read to the buffer[] array. Data not fitting into the array remain in the socket. They can be received by the next SocketTlsReadAvailable or  [SocketTlsRead](/en/docs/network/sockettlsread) call. buffer_maxlen cannot exceed [INT_MAX](/en/docs/constants/namedconstants/typeconstants) (2147483647).

Return Value

If successful, return the number of read bytes. In case of an error, -1 is returned.

Note

If an error occurs on a system socket when executing the function, connection established via [SocketConnect](/en/docs/network/socketconnect) is discontinued.

In case of a data reading error, the error 5273 (ERR_NETSOCKET_IO_ERROR) is written in [_LastError](/en/docs/predefined/_lasterror).

The function can be called only from Expert Advisors and scripts, as they run in their own execution threads. If calling from an indicator, [GetLastError()](/en/docs/check/getlasterror) returns the error 4014 – "Function is not allowed for call".

Example:

```
//+------------------------------------------------------------------+
//|                                       SocketTlsReadAvailable.mq5 |
//|                                  Copyright 2024, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com
#property version     "1.00"
#property script_show_inputs
//+------------------------------------------------------------------+
//| Script inputs                                                    |
//+------------------------------------------------------------------+
input string InpMethod ="GET";            // Method (HEAD,GET)
input string InpServer ="www.google.com"; // Server
input uint   InpPort   =443;              // Port
input uint   InpTimeout=5000;             // Timeouts
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart(void)
  {
   Print("Server: ",InpServer);
   Print("Port: ",InpPort);
//--- create a socket and get its handle
   const int socket=SocketCreate();
 
   if(socket==INVALID_HANDLE)
     {
      Print("SocketCreate() failed. Error ",GetLastError());
      return;
     }
//--- set timeouts for receiving and sending data for a socket system object
   if(!SocketTimeouts(socket,InpTimeout,InpTimeout))
     {
      PrintFormat("SocketTimeouts(%u, %u) failed. Error %d",InpTimeout,InpTimeout,GetLastError());
      SocketClose(socket);
      return;
     }
//--- connect to Server via Port
   if(!SocketConnect(socket,InpServer,InpPort,InpTimeout))
     {
      PrintFormat("SocketConnect('%s', %u, %u) failed. Error %d",InpServer,InpPort,InpTimeout,GetLastError());
      SocketClose(socket);
      return;
     }
//--- get data on the certificate used to secure network connection
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
   else
     {
      //--- server does not provide a certificate - report an unsecured connection and leave
      Print("The connection is not secured by a certificate");
      SocketClose(socket);
      return;
     }
//--- send a request to the server
   string request=StringFormat("%s / HTTP/1.1\r\nHost: %s\r\nUser-Agent: MetaTrader 5\r\n\r\n",InpMethod,InpServer);
 
   if(HTTPSendTLS(socket,request))
     {
      //--- request sent - get response
      Print("\nRequest sent. Starting page loading...");
      uchar response[]; // all received data (document header and body)
 
      if(!HTTPRecvTLS(socket,response,InpTimeout))
        {
         Print("There were errors while reading the page");
         SocketClose(socket);
         return;
        }
      //--- report the number of bytes of data received
      PrintFormat("%u bytes received",response.Size());
      //--- display obtained page header only
      string result    =CharArrayToString(response,0,WHOLE_ARRAY,CP_UTF8);
      int    header_end=StringFind(result,"\r\n\r\n");
 
      if(header_end>0)
        {
         Print("\nHTTP answer header received:");
         Print(StringSubstr(result,0,header_end));
        }
     }
//--- close the socket after use
   SocketClose(socket);
   /*
   result:
   Server: www.google.com
   Port: 443
   TLS certificate:
      Owner: /CN=www.google.com
      Issuer: /C=US/O=Google Trust Services/CN=WR2
      Number: 0d:43:b1:4a:bb:9c:15:96:10:e1:3d:55:23:9f:25:4e
      Print: 89167618e5017f813aff981c88ce422dc1016bdf
      Expiration: 2024.12.30 08:26:35
 
   Request sent. Starting page loading...
   HTTPRecvTLS: Document received within 27 attempts
   25185 bytes received
 
   HTTP answer header received:
   HTTP/1.1 200 OK
   Date: Fri, 25 Oct 2024 17:12:42 GMT
   Expires: -1
   Cache-Control: private, max-age=0
   Content-Type: text/html; charset=ISO-8859-1
   Content-Security-Policy-Report-Only: object-src 'none';base-uri 'self';script-src 'nonce-CUL2rdUOeAN7xIV6v0WUuQ' 'strict-dynamic' 'report-sample' 'unsafe-eval' 'unsafe-inline' https: http:;report-uri https://csp.withgoogle.com/csp/gws/other-hp
   Accept-CH: Sec-CH-Prefers-Color-Scheme
   P3P: CP="This is not a P3P policy! See g.co/p3phelp for more info."
   Server: gws
   X-XSS-Protection: 0
   X-Frame-Options: SAMEORIGIN
   Set-Cookie: AEC=AVYB7coyYMCdweTDTaWeGYzmRnxzKGqsOEosH_VkbCn8xhWkFz6v0kxQFw; expires=Wed, 23-Apr-2025 17:12:42 GMT; path=/; domain=.google.com; Secure; HttpOnly; SameSite=lax
   Set-Cookie: NID=518=J02X02Ff4v_9sMcNoUz-1SolmuG08E26Gs438ik0J_SOJUMy7of-P-qup-LaNSWVXUL8OjhOXpGIGuJQGIoEPBnzqDKCH-46_FN4J2foHeWTlGG8bVVvQ44AHWLg1OXjrGp3CUBexYdczLWNy3LxEcb7eh6mxSvFzOelPC6-vpXkaumLQ80x9gF_RpLcAYfN4ehT; expires=Sat, 26-Apr-2025 17:12:42 GMT; path=/; domain=.google.com; HttpOnly
   Alt-Svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000
   Accept-Ranges: none
   Vary: Accept-Encoding
   Transfer-Encoding: chunked
   */
  }
//+------------------------------------------------------------------+
//| Send an HTTP request over a secure connection                    |
//+------------------------------------------------------------------+
bool HTTPSendTLS(int socket,const string request)
  {
//--- convert the string to a character array, discard the terminating zero
   char req[];
   int  len=StringToCharArray(request,req,0,WHOLE_ARRAY,CP_UTF8)-1;
 
   if(len<0)
      return false;
 
   return(SocketTlsSend(socket,req,len)==len);
  }
//+------------------------------------------------------------------+
//| Get a web page via a secure connection                           |
//+------------------------------------------------------------------+
bool HTTPRecvTLS(int socket,uchar &response[],const uint timeout_ms)
  {
//--- read available data from secure TLS connection before the timeout expires
   ulong timeout_check=GetTickCount64()+timeout_ms;
   uchar block[1024];   // buffer for block data reading from socket
   uint  attempt=0;     // requested number of data blocks
   int   err    =0;     // error code
 
   ResetLastError();
 
   do
     {
      //--- read in blocks, maximum 1024 bytes
      int len=SocketTlsReadAvailable(socket,block,1024);
 
      if(len>0)
        {
         attempt++;
         //--- merge the obtained data blocks
         ArrayCopy(response,block,response.Size());
         //--- analyze the obtained data, define the header, page body, ending, or loading error, etc.
         //...
         //...
         //...
         timeout_check=GetTickCount64()+timeout_ms;
        }
      else
         Sleep(10);
 
      err=GetLastError();
     }
   while(!IsStopped() && GetTickCount()<timeout_check && !err);
//--- were there any errors while reading?
   if(err)
     {
      Print("Error ",err);
      return(false);
     }
 
   PrintFormat("%s: Document received within %d attempts",__FUNCTION__,attempt);
   return(true);
  }

```

See also

[SocketTimeouts](/en/docs/network/sockettimeouts), [MathSwap](/en/docs/math/mathswap)
