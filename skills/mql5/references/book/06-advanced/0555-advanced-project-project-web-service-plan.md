# Project plan of a web service for copying trades and signals

As an end-to-end demonstration project, which we will develop throughout this chapter, we will take a simple, but at the same time quite technologically advanced product: a client-server copy trade system. The client part will be MQL programs that communicate with the central part using the [sockets](/en/book/advanced/network) technology. Considering that MQL5 allows you to work only with client sockets, you will need to choose an alternative platform for the socket server (more on that below). Thus, the project will require the symbiosis of several different technologies and the use of many sections of the MQL5 API that we have already studied, including application codes developed on their basis.

Thanks to the socket-based client-server architecture, the system can be used in different scenarios:

- for easy copying of trades between terminals on one computer;
- to establish a private (personal) communication channel between terminals on different computers, including not only in the local network but also via the Internet;
- to organize a publicly open or closed signal service requiring registration;
- to monitor trading;
- to manage your own account remotely.

In all cases, client programs will act in 2 roles: a publisher (publisher, sender) and a subscriber (recipient) of data.

We will not invent our own network protocol but will use the existing and popular WebSocket standard. Their client implementation is built into all browsers, and we will need to repeat it (with a greater or lesser degree of completeness) in MQL5. Of course, WebSocket support is also available for most popular web servers. Therefore, in any case, our developments can not only be adapted to other servers (if someone else suits) but also integrated with well-known sites that provide similar web services. Here the whole point is to strictly follow the specification of their API, built on top of WebSockets.

When developing software systems that are more complex than one standalone program, it is important to draw up an action plan and, possibly, even design a technical project, including the structure of modules, their interaction, and the sequence of coding.

So our plan includes:

1. Theoretical analysis of the WebSocket protocol;
2. Selecting and installing a web server with the implementation of a WebSocket server;
3. Creating a simple echo server (sending a copy of incoming messages back to the client) to get familiar with the technology;
4. Creating a simple client-side web page to test the functionality of the echo server from a browser;
5. Creating a simple chat server that sends messages to all connected clients, and a test web page for it;
6. Creating a messaging server between identifiable providers and subscribers, and a test web client for it;
7. Designing and implementing WebSockets in MQL5;
8. Creating a simple script as a client for an echo server;
9. Creating a simple Expert Advisor as a chat server client;
10. Finally, creating a trade copier in MQL5 which it will act as both an information provider (monitor of account changes and status) and an information consumer (reproducing trades), depending on the settings.

But before we start implementing the plan, we need to install a web server.
