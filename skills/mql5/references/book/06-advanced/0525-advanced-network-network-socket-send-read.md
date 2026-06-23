# Reading and writing data over an insecure socket connection

Historically, sockets provide data transfer over a simple connection by default. Data transmission in an open form allows technical means to analyze all traffic. In recent years, security issues have been taken more seriously and therefore TLS (Transport Layer Security) technology has been implemented almost everywhere: it provides on-the-fly encryption of all data between the sender and the recipient. In particular, for Internet connections, the difference lies in the HTTP (simple connection) and HTTPS (secure) protocols.

MQL5 provides different sets of Socket functions for working with simple and secure connections. In this section, we will get acquainted with the simple mode, and later we will move to the protected one.

To read data from a socket, use the SocketRead function.

int SocketRead(int socket, uchar &buffer[], uint maxlen, uint timeout)

The socket descriptor is obtained from [SocketCreate](/en/book/advanced/network/network_socket_create_connect) and connected to a network resource using [Socket Connect](/en/book/advanced/network/network_socket_create_connect).

The buffer parameter is a reference to the array into which the data will be read. If the array is dynamic, its size increases by the number of bytes read, but it cannot exceed INT_MAX (2147483647). You can limit the number of read bytes in the maxlen parameter. Data that does not fit will remain in the socket's internal buffer: it can be obtained by the following call SocketRead. The value of maxlen must be between 1 and INT_MAX (2147483647).

The timeout parameter specifies the time (in milliseconds) to wait for the read to complete. If no data is received within this time, the attempts are terminated and the function exits with the result -1.

-1 is also returned on error, while the error code in _LastError, for example, 5273 (ERR_NETSOCKET_IO_ERROR), means that the connection established via SocketConnect is now broken.

If successful, the function returns the number of bytes read.

When setting the read timeout to 0, the default value of 120000 (2 minutes) is used.

To write data to a socket, use the SocketSend function.

Unfortunately, the function names SocketRead and SocketSend are not "symmetric": the reverse operation for "read" is "write", and for "send" is "receive". This may be unfamiliar to developers with experience who worked with networking APIs on other platforms.

int SocketSend(int socket, const uchar &buffer[], uint maxlen)

The first parameter is a handle to a previously created and opened socket. When passing an invalid handle, _LastError receives error 5270 (ERR_NETSOCKET_INVALIDHANDLE). The buffer array contains the data to be sent with the data size being specified in the maxlen parameter (the parameter was introduced for the convenience of sending part of the data from a fixed array).

The function returns the number of bytes written to the socket on success and -1 on error.

System-level errors (5273, ERR_NETSOCKET_IO_ERROR) indicate a disconnect.

The script SocketReadWriteHTTP.mq5 demonstrates how sockets can be used to implement work over the HTTP protocol, that is, request information about a page from a web server. This is a small part of what the [WebRequest](/en/book/advanced/network/network_http) function does for us "behind the scenes".

Let's leave the default address in the input parameters: the site "www.mql5.com". The port number was chosen to be 80 because that is the default value for non-secure HTTP connections (although some servers may use a different port: 81, 8080, etc.). Ports reserved for secure connections (in particular, the most popular 443) are not yet supported by this example. Also, in the Server parameter, it is important to enter the name of the domain and not a specific page because the script can only request the main page, i.e., the root path "/".

```
input string Server = "www.mql5.com";
input uint Port = 80;

```

In the main function of the script, we will create a socket and open a connection on it with the specified parameters (the timeout is 5 seconds).

```
void OnStart()
{
   PRTF(Server);
   PRTF(Port);
   const int socket = PRTF(SocketCreate());
   if(PRTF(SocketConnect(socket, Server, Port, 5000)))
   {
      ...
   }
}

```

Let's take a look at how the HTTP protocol works. The client sends requests in the form of specially designed headers (strings with predefined names and values), including, in particular, the web page address, and the server sends the entire web page or operation status in response, also using special headers for this. The client can request a web page with a GET request, send some data with a POST request, or check the status of the web page with a frugal HEAD request. In theory, there are many more HTTP methods — you can learn about them in the HTTP protocol specification.

Thus, the script must generate and send an HTTP header over the socket connection. In its simplest form, the following HEAD request allows you to get meta information about the page (we could replace HEAD with GET to request the entire page but there are some complications; we will discuss this later).

```
HEAD / HTTP/1.1
Host: _server_
User-Agent: MetaTrader 5
                                     // <- two newlines in a row \r\n\r\n

```

The forward slash after "HEAD" (or another method) is the shortest possible path on any server to the root directory, which usually results in the main page being displayed. If we wanted a specific web page, we could write something like "GET /en/forum/ HTTP/1.1" and get the table of contents of the English language forums from mql5.com. Specify a real domain instead of the "_server_" string.

Although the presence of "User-Agent:" is optional, it allows the program to "introduce itself" to the server, without which some servers may reject the request.

Notice the two empty lines: they mark the end of the heading. In our script, it is convenient to form the title with the following expression:

```
StringFormat("HEAD / HTTP/1.1\r\nHost: %s\r\n\r\n", Server)

```

Now we just have to send it to the server. For this purpose, we have written a simple function HTTPSend. It receives a socket descriptor and a header line.

```
bool HTTPSend(int socket, const string request)
{ 
   char req[];
   int len = StringToCharArray(request, req, 0, WHOLE_ARRAY, CP_UTF8) - 1;
   if(len < 0) return false;
   return SocketSend(socket, req, len) == len;
} 

```

Internally, we convert the string to a byte array and call SocketSend.

Next, we need to accept the server response, for which we have written the HTTPRecv function. It also expects a socket descriptor and a reference to a string where the data should be placed but is more complex.

```
bool HTTPRecv(int socket, string &result, const uint timeout)
{ 
   char response[];
   int len;         // signed integer needed for error flag -1
   uint start = GetTickCount();
   result = "";
   
   do 
   {
      ResetLastError();
      if(!(len = (int)SocketIsReadable(socket)))
      {
         Sleep(10); // wait for data or timeout
      }
      else          // read the data in the available volume
      if((len = SocketRead(socket, response, len, timeout)) > 0)
      {
         result += CharArrayToString(response, 0, len); // NB: without CP_UTF8 only 'HEAD'
         const int p = StringFind(result, "\r\n\r\n");
         if(p > 0)
         {
            // HTTP header ends with a double newline, use this
            // to make sure the entire header is received
            Print("HTTP-header found");
            StringSetLength(result, p); // cut off the body of the document (in case of a GET request)
            return true;
         }
      }
   } 
   while(GetTickCount() - start < timeout && !IsStopped() && !_LastError);
   
   if(_LastError) PRTF(_LastError);
   
   return StringLen(result) > 0;
}

```

Here we are checking in a loop the appearance of data within the specified timeout and reading it into the response buffer. The occurrence of an error terminates the loop.

Buffer bytes are immediately converted to a string and concatenated into a full response in the result variable. It is important to note that we can only use the CharArrayToString function with the default encoding for the HTTP header because only Latin letters and a few special characters from ANSI are allowed in it.

To receive a complete web document, which, as a rule, has UTF-8 encoding (but potentially has another non-Latin one, which is indicated just in the HTTP header), more tricky processing will be required: first, you need to collect all the sent blocks in one common buffer and then convert the whole thing into a string indicating CP_UTF8 (otherwise, any character encoded in two bytes can be "cut" when sent, and will arrive in different blocks; that is why we cannot expect a correct UTF-8 byte stream in individual fragment). We will improve this example in the following sections.

Having functions HTTPSend and HTTPRecv, we complete the OnStart code.

```
void OnStart()
{
      ...
      if(PRTF(HTTPSend(socket, StringFormat("HEAD / HTTP/1.1\r\nHost: %s \r\n"
         "User-Agent: MetaTrader 5\r\n\r\n", Server))))
      {
         string response;
         if(PRTF(HTTPRecv(socket, response, 5000)))
         {
            Print(response);
         }
      }
      ...
}

```

In the HTTP header received from the server, the following lines may be of interest:

- 'Content-Length:' — the total length of the document in bytes
- 'Content-Language:' — document language (for example, "de-DE, ru")
- 'Content-Type:' — document encoding (for example, "text/html; charset=UTF-8")
- 'Last-Modified:' — the time of the last modification of the document, so as not to download what is already there (in principle, we can add the 'If-Modified-Since:' header in our HTTP request)

We will talk about finding out the document length (data size) in more detail because almost all headers are optional, that is, they are reported by the server at will, and in their absence, alternative mechanisms are used. The size is important to know when to close the connection, i.e., to make sure that all the data has been received.

Running the script with default parameters produces the following result.

```
Server=www.mql5.com / ok
Port=80 / ok
SocketCreate()=1 / ok
SocketConnect(socket,Server,Port,5000)=true / ok
HTTPSend(socket,StringFormat(HEAD / HTTP/1.1
Host: %s
,Server))=true / ok
HTTP-header found
HTTPRecv(socket,response,5000)=true / ok
HTTP/1.1 301 Moved Permanently
Server: nginx
Date: Sun, 31 Jul 2022 10:24:00 GMT
Content-Type: text/html
Content-Length: 162
Connection: keep-alive
Location: https://www.mql5.com/
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Frame-Options: SAMEORIGIN

```

Please note that this site, like most sites today, redirects our request to a secure connection: this is achieved with the status code "301 Moved Permanently" and the new address "Location: https://www.mql5.com/" (protocol is important here " https"). To retry a TLS-enabled request, several other functions must be used, and we will discuss them later.
