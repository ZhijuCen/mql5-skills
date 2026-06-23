# Data Structures

MQL5 Language offers 12 predefined [structures](/en/docs/basis/types/classes):

- [MqlDateTime](/en/docs/constants/structures/mqldatetime) is intended for working with [date and time](/en/docs/dateandtime);

- [MqlParam](/en/docs/constants/structures/mqlparam) can send input parameters when creating a handle of the indicator using the [IndicatorCreate()](/en/docs/series/indicatorcreate) function;

- [MqlRates](/en/docs/constants/structures/mqlrates) is intended for manipulating the [historical data](/en/docs/series), it contains information about the price, volume and spread;
- [MqlBookInfo](/en/docs/constants/structures/mqlbookinfo) is intended for obtaining information about the [Depth of Market](/en/docs/marketinformation);
- [MqlTradeRequest](/en/docs/constants/structures/mqltraderequest) is used for creating a trade request for [trade operations](/en/docs/constants/tradingconstants/enum_trade_request_actions);

- [MqlTradeCheckResult](/en/docs/constants/structures/mqltradecheckresult) is intended for [checking](/en/docs/trading/ordercheck) the prepared [trade request](/en/docs/constants/structures/mqltraderequest) before [sending](/en/docs/trading/ordersend) it;

- [MqlTradeResult](/en/docs/constants/structures/mqltraderesult) contains a trade server reply to a [trade request](/en/docs/constants/structures/mqltraderequest), sent by [OrderSend()](/en/docs/trading/ordersend) function;

- [MqlTradeTransaction](/en/docs/constants/structures/mqltradetransaction) contains description of a trade transaction;

- [MqlTick](/en/docs/constants/structures/mqltick) is designed for fast retrieval of the most requested information about current prices.

- [Economic calendar structures](/en/docs/constants/structures/mqlcalendar) are used to obtain data on the economic calendar events sent to the MetaTrader 5 platform in real time. [Economic calendar functions](/en/docs/calendar) allow analyzing macroeconomic parameters immediately after new reports are released, since relevant values are broadcast directly from the source with no delay.
