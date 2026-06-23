# Establishing and breaking a network socket connection

In the previous sections, we got acquainted with the high-level MQL5 network functions: each of them provides support for a specific application protocol. For example, SMTP is used to send emails (SendMail), FTP is used for file transfer (SendFTP), and HTTP allows receiving web documents (WebRequest). All the mentioned standards are based on a lower, transport layer TCP (Transmission Control Protocol). It is not the last in the hierarchy as there are also lower ones, but we will not discuss them here.

The standard implementation of application protocols hides many technical nuances inside and eliminates the need for the programmer to routinely following specifications for hours. However, it does not have flexibility and does not take into account the advanced features embedded in the standards. Therefore, sometimes it is required to program network communication at the TCP level, that is, at the socket level.

A socket can be viewed as analogous to a file on a disk: a socket is also described by an integer descriptor by which data can be read or written, but this happens in a distributed network infrastructure. Unlike files, the number of sockets on a computer is limited, and therefore the socket descriptor must be requested from the system in advance before being associated with a network resource (address, URL). Let's also say in advance that access to information via a socket is streaming, that is, it is impossible to "rewind" a certain "pointer" to the beginning, as in a file.

Write and read threads do not intersect but can affect future read or write data since the transmitted information is often interpreted by servers and client programs as control commands. Protocol standards define if a stream contains commands or data.

The SocketCreate function allows the creation of an "empty" socket descriptor in MQL5.

int SocketCreate(uint flags = 0)

Its only parameter is reserved for the future to specify the bit pattern of the flags that determine the mode of the socket, but at the moment only one stub flag is supported: SOCKET_DEFAULT corresponds to the current mode and can be omitted. At the system level, this is equivalent to a socket in blocking mode (this may be of interest to network programmers).

If successful, the function returns the socket handle. Otherwise, it returns INVALID_HANDLE.

A maximum of 128 sockets can be created from one MQL program. When the limit is exceeded, error 5271 (ERR_NETSOCKET_TOO_MANY_OPENED) is logged into _LastError.

After we have opened the socket, it should be associated with a network address.

bool SocketConnect(int socket, const string server, uint port, uint timeout)

The SocketConnect function makes a socket connection to the server at the specified address and port (for example, web servers typically run on ports 80 or 443 for HTTP and HTTPS, respectively, and SMTP on port 25). The address can be either a domain name or an IP address.

The timeout parameter allows you to set a timeout in milliseconds to wait for a server response.

The function returns a sign of a successful connection (true) or error (false). The error code is written to _LastError, for example, 5272 (ERR_NETSOCKET_CANNOT_CONNECT).

Please note that the connection address must be added to the list of allowed addresses in the terminal settings (dialog Service -> Settings -> Advisors).

After you have finished working with the network, you should release the socket with SocketClose.

bool SocketClose(const int  socket)

The SocketClose function closes the socket by its handle, opened earlier using the SocketCreate function. If the socket was previously connected via SocketConnect, the connection will be broken.

The function also returns an indicator of success (true) or error (false). In particular, when passing an invalid handle to _LastError, error 5270 (ERR_NETSOCKET_INVALIDHANDLE) is logged.

Let's remind you that all functions of this and subsequent sections are prohibited in indicators: there, an attempt to work with sockets will result in error 4014 (ERR_FUNCTION_NOT_ALLOWED, "The system function is not allowed to be called").

Consider an introductory example, the SocketConnect.mq5 script. In the input parameters, you can specify the address and port of the server. We are supposed to start testing with regular web servers like mql5.com.

```
input string Server = "www.mql5.com";
input uint Port = 443;

```

In the function OnStart we just create a socket and bind it to a network resource.

```
void OnStart()
{
   PRTF(Server);
   PRTF(Port);
   const int socket = PRTF(SocketCreate());
   if(PRTF(SocketConnect(socket, Server, Port, 5000)))
   {
      PRTF(SocketClose(socket));
   }
}

```

If all the settings in the terminal are correct and it is connected to the Internet, we will get the following "report".

```
Server=www.mql5.com / ok
Port=443 / ok
SocketCreate()=1 / ok
SocketConnect(socket,Server,Port,5000)=true / ok
SocketClose(socket)=true / ok

```
