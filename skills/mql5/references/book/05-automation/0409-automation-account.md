# Trading account information

In this chapter, we will study the last important aspect of the trading environment of MQL programs and, specifically, Expert Advisors, which we will develop in detail in the next few chapters. Let's talk about a trading account.

Having a valid account and an active connection to it are a necessary condition for the functioning of most MQL programs. Until now, we have not focused on this, but getting quotes, ticks, and, in general, the ability to open a workable chart implies a successful connection to a trading account.

In the context of Expert Advisors, an account additionally reflects the financial condition of the client, accumulates the trading history and determines the specific modes allowed for trading.

The MQL5 API allows you to get the properties of an account, starting with its number and ending with the current profit. All of them are read-only in the terminal and are installed by the broker on the server.

The terminal can only be connected to one account at a time. All MQL programs work with this account. As we have already noted in the section [Features of starting and stopping programs of various types](/en/book/applications/runtime/runtime_lifecycle), switching an account initiates a reload of the indicators and Expert Advisors attached to the charts. However, in the OnDeinit handler, the program can find the reason for deinitialization, which, when switching the account, will be equal to [REASON_ACCOUNT](/en/book/applications/runtime/runtime_oninit_ondeinit).
