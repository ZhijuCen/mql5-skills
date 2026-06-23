# Checking socket status

When working with a socket, it becomes necessary to check its status because distributed networks are not as reliable as a file system. In particular, the connection may be lost for one reason or another. The SocketIsConnected function allows you to find this out.

bool SocketIsConnected(const int socket)

The function checks if the socket with the specified handle (obtained from [SocketCreate](/en/book/advanced/network/network_socket_create_connect)) is connected to its network resource (specified in [Socket Connect](/en/book/advanced/network/network_socket_create_connect)) and returns true in case of success.

Another function, SocketIsReadable, lets you know if there is any data to read in the system buffer associated with the socket. This means that the computer, to which we connected at the network address, sent (and may continue to send) data to us.

uint SocketIsReadable(const int socket)

The function returns the number of bytes that can be read from the socket. In case of error, 0 is returned.

Programmers familiar with the Windows/Linux socket system APIs know that a value of 0 can also be a normal state when there is no incoming data in the socket's internal buffer. However, this function behaves differently in MQL5. With an empty system socket buffer, it speculatively returns 1, deferring the actual check for data availability until the next call to one of the read functions. In particular, this situation with a dummy result of 1 byte occurs, as a rule, the first time a function is called on a socket when the receiving internal buffer is still empty.

When executing this function, an error may occur, meaning that the connection established through SocketConnect, was broken (in _LastError we will get code 5273, ERR_NETSOCKET_IO_ERROR).

The SocketIsReadable function is useful in programs that are designed for "non-blocking" reading of data using [SocketRead](/en/book/advanced/network/network_socket_send_read). The point is that the SocketRead function when there is no data in the receive buffer, will wait for their arrival, suspending the execution of the program (by the specified timeout value).

On the other hand, a blocking read is more reliable in the sense that your program will "wake up" as soon as new data arrives, but checking for their presence with SocketIsReadable needs to be done periodically, according to some other events (usually, on a timer or in a loop).

Particular care should be taken when using the SocketIsReadable function in [TLS secure mode](/en/book/advanced/network/network_socket_tls_send_read). The function returns the amount of "raw" data, which in TLS mode is an encrypted block. If the "raw" data has not yet been accumulated in the size of the decryption block, then the subsequent call of the read function [SocketTlsRead](/en/book/advanced/network/network_socket_tls_send_read) will block program execution, waiting for the missing fragment. If the "raw" data already contains a block ready for decryption, the read function will return fewer decrypted bytes than the number of "raw" bytes. In this regard, with TLS enabled, it is recommended to always use the SocketIsReadable function in conjunction with [SocketTlsReadAvailable](/en/book/advanced/network/network_socket_tls_send_read). Otherwise, the behavior of the program will differ from what is expected. Unfortunately, MQL5 does not provide the SocketTlsIsReadable function, which is compatible with the TLS mode and does not impose the described conventions.

The similar SocketIsWritable function checks if the given socket can be written to at the current time.

bool SocketIsWritable(const int socket)

The function returns an indication of success (true) or error (false). In the latter case, the connection established through SocketConnect will be broken.

Here is a simple script SocketIsConnected.mq5 to test the functions. In the input parameters, we will provide the opportunity to enter the address and port.

```
input string Server = "www.mql5.com";
input uint Port = 443;

```

In the OnStart handler, we create a socket, connect to the site, and start checking the status of the socket in a loop. After the second iteration, we forcibly close the socket, and this should lead to an exit from the loop.

```
void OnStart()
{
   PRTF(Server);
   PRTF(Port);
   const int socket = PRTF(SocketCreate());
   if(PRTF(SocketConnect(socket, Server, Port, 5000)))
   {
      int i = 0;
      while(PRTF(SocketIsConnected(socket)) && !IsStopped())
      {
         PRTF(SocketIsReadable(socket));
         PRTF(SocketIsWritable(socket));
         Sleep(1000);
         if(++i >= 2)
         {
            PRTF(SocketClose(socket));
         }
      }
   }
}

```

The following entries are displayed in the log.

```
Server=www.mql5.com / ok
Port=443 / ok
SocketCreate()=1 / ok
SocketConnect(socket,Server,Port,5000)=true / ok
SocketIsConnected(socket)=true / ok
SocketIsReadable(socket)=0 / ok
SocketIsWritable(socket)=true / ok
SocketIsConnected(socket)=true / ok
SocketIsReadable(socket)=0 / ok
SocketIsWritable(socket)=true / ok
SocketClose(socket)=true / ok
SocketIsConnected(socket)=false / NETSOCKET_INVALIDHANDLE(5270)

```
