# Setting data send and receive timeouts for sockets

Since network connections are unreliable, all operations with Socket functions support a centralized timeout setting. If data reading or sending is not completed successfully within the specified time, the function will stop trying to perform the corresponding action.

You can set timeouts for receiving and sending data using the SocketTimeouts function.

bool SocketTimeouts(int socket, uint timeout_send, uint timeout_receive)

Both timeouts are given in milliseconds and affect all functions on the specified socket at the system level.

The [SocketRead](/en/book/advanced/network/network_socket_send_read) function has its own timeout parameter, with which you can additionally control the timeout during a particular call of the SocketRead function.

SocketTimeouts returns true if successful and false otherwise.

By default, there are no timeouts, which means waiting indefinitely for all data to be received or sent.
