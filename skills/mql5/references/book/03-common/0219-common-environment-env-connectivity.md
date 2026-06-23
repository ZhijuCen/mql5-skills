# Checking network connections

As you know, the MetaTrader 5 platform is a distributed system that includes several links. In addition to the client terminal and broker server, it includes the MQL5 community, the Market, cloud services, and much more. In fact, the client part is also distributed, consisting of a terminal and testing agents which can be deployed on multiple computers on a local network. In this case, the connection between any links can potentially be broken for one reason or another. Although the MetaTrader 5 infrastructure tries to automatically restore its functionality, it is not always possible to do this quickly.

Therefore, in MQL programs, one should take into account the possibility of a connection loss. The MQL5 API allows you to control the most important connections: with the trade server and the MQL5 community. The following properties are available in TerminalInfoInteger.

| Identifier | Description |
| --- | --- |
| TERMINAL_CONNECTED | Connection to the trading server |
| TERMINAL_PING_LAST | The last known ping to the trade server in microseconds |
| TERMINAL_COMMUNITY_ACCOUNT | Availability of MQL5.community authorization data in the terminal |
| TERMINAL_COMMUNITY_CONNECTION | Connection to MQL5.community |
| TERMINAL_MQID | Availability of MetaQuotes ID for sending push notifications |

All properties except TERMINAL_PING_LAST are boolean flags. TERMINAL_PING_LAST contains a value of type int.

In addition to the connection, an MQL program often needs to make sure that the data it has is up to date. In particular, the checked TERMINAL_CONNECTED flag does not yet mean that the quotes you are interested in are synchronized with the server. To do this, you need to additionally check SymbolIsSynchronized or SeriesInfoInteger(..., SERIES_SYNCHRONIZED). These features will be discussed in the chapter on [timeseries](/en/book/applications/timeseries).

The TerminalInfoDouble function supports another interesting property: TERMINAL_RETRANSMISSION. It denotes the percentage of network packets resent in TCP/IP protocol for all running applications and services on this computer. Even on the fastest and most properly configured network, packet loss sometimes occurs and, as a result, there will be no confirmation of packet delivery between the recipient and the sender. In such cases, the lost packet is resent. The terminal itself does not count the TERMINAL_RETRANSMISSION indicator but requests it once a minute in the operating system.

A high value of this metric may indicate external problems (Internet connection, your provider, local network, or computer issues), which can worsen the quality of the terminal connection.

If there is a confirmed connection to the community (TERMINAL_COMMUNITY_CONNECTION), an MQL program can query the user's current balance by calling TerminalInfoDouble(TERMINAL_COMMUNITY_BALANCE). This allows you to use an automated subscription to paid trading signals (API documentation is available on the [mql5.com](https://www.mql5.com/ru/docs/signals) website).

Let's check the listed properties using the script EnvConnection.mq5.

```
void OnStart()
{
   PRTF(TerminalInfoInteger(TERMINAL_CONNECTED));
   PRTF(TerminalInfoInteger(TERMINAL_PING_LAST));
   PRTF(TerminalInfoInteger(TERMINAL_COMMUNITY_ACCOUNT));
   PRTF(TerminalInfoInteger(TERMINAL_COMMUNITY_CONNECTION));
   PRTF(TerminalInfoInteger(TERMINAL_MQID));
   PRTF(TerminalInfoDouble(TERMINAL_RETRANSMISSION));
   PRTF(TerminalInfoDouble(TERMINAL_COMMUNITY_BALANCE));
}

```

Here is a log example (the values will match your settings).

```
TerminalInfoInteger(TERMINAL_CONNECTED)=1 / ok
TerminalInfoInteger(TERMINAL_PING_LAST)=49082 / ok
TerminalInfoInteger(TERMINAL_COMMUNITY_ACCOUNT)=0 / ok
TerminalInfoInteger(TERMINAL_COMMUNITY_CONNECTION)=0 / ok
TerminalInfoInteger(TERMINAL_MQID)=0 / ok
TerminalInfoDouble(TERMINAL_RETRANSMISSION)=0.0 / ok
TerminalInfoDouble(TERMINAL_COMMUNITY_BALANCE)=0.0 / ok

```
