# Signal service client program in MQL5

So, according to our decision, the text in the service messages will be in JSON format.

In the most common version, JSON is a text description of an object, similar to how it is done for structures in MQL5. The object is enclosed in curly brackets, inside which its properties are written separated by commas: each property has an identifier in quotes, followed by a colon and the value of the property. Here properties of several primitive types are supported: strings, integers and real numbers, booleans true/false, and empty value null. In addition, the property value can, in turn, be an object or an array. Arrays are described using square brackets, within which the elements are separated by commas. For example,

```
{
   "string": "this is a text",
   "number": 0.1,
   "integer": 789735095,
   "enabled": true,
   "subobject" :
   {
      "option": null
   },
   "array":
   [
      1, 2, 3, 5, 8
   ]
}

```

Basically, the array at the top level is also valid JSON. For example,

```
[
   {
      "command": "buy",
      "volume": 0.1,
      "symbol": "EURUSD",
      "price": 1.0
   },
   {
      "command": "sell",
      "volume": 0.01,
      "symbol": "GBPUSD",
      "price": 1.5
   }
]

```

To reduce traffic in application protocols using JSON, it is customary to abbreviate field names to several letters (often to one).

Property names and string values are enclosed in double-quotes. If you want to specify a quote within a string, it must be escaped with a backslash.

The use of JSON makes the protocol versatile and extensible. For example, for the service being designed (trading signals and, in a more general case, account state copying), the following message structure can be assumed:

```
{
  "origin": "publisher_id",    // message sender ("Server" in technical message)
  "msg" :                      // message (text or JSON) as received from the sender
   {
     "trade" :                 // current trading commands (if there is a signal)
      {
        "operation": ...,      // buy/sell/close
         "symbol": "ticker",
         "volume": 0.1,
        ... // other signal parameters
      },
     "account":                // account status
      {
        "positions":           // positions
         {
           "n": 10,            // number of open positions
           [ { ... },{ ... } ] // array of properties of open positions
         },
        "pending_orders":      // pending orders
         {
            "n": ...
            [ { ... } ]
         }
         "drawdown": 2.56,
         "margin_level": 12345,
        ... // other status parameters
      },
     "hardware":               // remote control of the "health" of the PC
      {
         "memory": ...,
         "ping_to_broker": ...
      }
   }
}

```

Some of these features may or may not support specific implementations of client programs (everything that they do not "understand", they will simply ignore). In addition, subject to the condition that there are no conflicts in the names of properties at the same level, each information provider can add its own specific data to JSON. The messaging service will simply forward this information. Of course, the program on the receiving side must be able to interpret these specific data.

The book comes with a JSON parser called ToyJson ("toy" JSON, file toyjson.mqh) which is small and inefficient and does not support the full capabilities of the format specification (for example, in terms of processing of escape sequences). It was written specifically for this demo service, adjusted for the expected, not very complex, structure of information about trading signals. We will not describe it in detail here, and the principles of its use will become clear from the source code of the MQL client of the signal service.

For your projects and for the further development of this project, you can choose other JSON parsers available in the codebase on the mql5.com site.

One element (container or property) per ToyJson is described by the JsValue class object. There are several overloads of the method put(key, value) defined, that can be used for the addition of named internal properties as in a JSON object or put(value), to add a value as in a JSON array. Also, this object can represent a single value of a primitive type. To read the properties of a JSON object, you can apply to JsValue a notation of the operator [] followed by the required property name in parentheses. Obviously, integer indexes are supported for accessing inside a JSON array.

Having formed the required configuration of related objects JsValue, you can serialize it into JSON text using the stringify(string&buffer) method.

The second class in toyjson.mqh — JsParser — allows you to perform the reverse operation: turn the text with the JSON description into a hierarchical structure of JsValue objects.

Taking into account the classes for working with JSON, let's start writing an Expert Advisor MQL5/Experts/MQL5Book/p7/wsTradeCopier/wstradecopier.mq5, which will be able to perform both roles in the transaction copy service: a provider of information about trades made on the account or a recipient of this information from the service to reproduce these trades.

The volume and content of the information sent is, from a political point of view, at the discretion of the provider and may differ significantly depending on the scenario (purpose) of using the service. In particular, it is possible to copy only ongoing transactions or the entire account balance along with pending orders and protective levels. In our example, we will only indicate the technical implementation of information transfer, and then you can choose a specific set of objects and properties at your discretion.

In the code, we will describe 3 structures which are inherited from built-in structures and which provide information "packing" in JSON:

- MqlTradeRequestWeb — MqlTradeRequest
- MqlTradeResultWeb — MqlTradeResult
- DealMonitorWeb — DealMonitor*

The last structure in the list, strictly speaking, is not built-in, but is defined by us in the file [DealMonitor.mqh](/en/book/automation/experts/experts_historydealget_funcs), yet it is filled on the standard set of deal properties.

The constructor of each of the derived structures populates the fields based on the transmitted primary source (trade request, its result, or deal). Each structure implements the asJsValue method, which returns a pointer to the JsValue object that reflects all the properties of the structure: they are added to the JSON object using the JsValue::put method. For example, here is how it is done in the case of MqlTradeRequest:

```
struct MqlTradeRequestWeb: public MqlTradeRequest
{
   MqlTradeRequestWeb(const MqlTradeRequest &r)
   {
      ZeroMemory(this);
      action = r.action;
      magic = r.magic;
      order = r.order;
      symbol = r.symbol;
      volume = r.volume;
      price = r.price;
      stoplimit = r.stoplimit;
      sl = r.sl;
      tp = r.tp;
      type = r.type;
      type_filling = r.type_filling;
      type_time = r.type_time;
      expiration = r.expiration;
      comment = r.comment;
      position = r.position;
      position_by = r.position_by;
   }
   
   JsValue *asJsValue() const
   {
      JsValue *req = new JsValue();
      // main block: action, symbol, type
      req.put("a", VerboseJson ? EnumToString(action) : (string)action);
      if(StringLen(symbol) != 0) req.put("s", symbol);
      req.put("t", VerboseJson ? EnumToString(type) : (string)type);
      
      // volumes
      if(volume != 0) req.put("v", TU::StringOf(volume));
      req.put("f", VerboseJson ? EnumToString(type_filling) : (string)type_filling);
      
      // block with prices
      if(price != 0) req.put("p", TU::StringOf(price));
      if(stoplimit != 0) req.put("x", TU::StringOf(stoplimit));
      if(sl != 0) req.put("sl", TU::StringOf(sl));
      if(tp != 0) req.put("tp", TU::StringOf(tp));
   
      // block of pending orders
      if(TU::IsPendingType(type))
      {
         req.put("t", VerboseJson ? EnumToString(type_time) : (string)type_time);
         if(expiration != 0) req.put("d", TimeToString(expiration));
      }
   
      // modification block
      if(order != 0) req.put("o", order);
      if(position != 0) req.put("q", position);
      if(position_by != 0) req.put("b", position_by);
      
      // helper block
      if(magic != 0) req.put("m", magic);
      if(StringLen(comment)) req.put("c", comment);
   
      return req;
   }
};

```

We transfer all properties to JSON (this is suitable for the account monitoring service), but you can leave only a limited set.

For properties that are enumerations, we have provided two ways to represent them in JSON: as an integer and as a string name of an enumeration element. The choice of method is made using the input parameter VerboseJson (ideally, it should be written in the structure code not directly but through a constructor parameter).

```
input bool VerboseJson = false;

```

Passing only numbers would simplify coding because, on the receiving side, it is enough to cast them to the desired enumeration type in order to perform "mirror" actions. However, numbers make it difficult for a person to perceive information, and they may need to analyze the situation (message). Therefore, it makes sense to support an option for the string representation, as being more "friendly", although it requires additional operations in the receiving algorithm.

The input parameters also specify the server address, the application role, and connection details separately for the provider and the subscriber.

```
enum TRADE_ROLE
{
   TRADE_PUBLISHER,  // Trade Publisher
   TRADE_SUBSCRIBER  // Trade Subscriber
};
   
input string Server = "ws://localhost:9000/";
input TRADE_ROLE Role = TRADE_PUBLISHER;
input bool VerboseJson = false;
input group "Publisher";
input string PublisherID = "PUB_ID_001";
input string PublisherPrivateKey = "PUB_KEY_FFF";
input string SymbolFilter = ""; // SymbolFilter (empty - current, '*' - any)
input ulong MagicFilter = 0;    // MagicFilter (0 - any)
input group "Subscriber";
input string SubscriberID = "SUB_ID_100";
input string SubscribeToPublisherID = "PUB_ID_001";
input string SubscriberAccessKey = "fd3f7a105eae8c2d9afce0a7a4e11bf267a40f04b7c216dd01cf78c7165a2a5a";
input string SymbolSubstitute = "EURUSD=GBPUSD"; // SymbolSubstitute (<from>=<to>,...)
input ulong SubscriberMagic = 0;

```

Parameters SymbolFilter and MagicFilter in the provider group allow you to limit the monitored trading activity to a given symbol and magic number. An empty value in SymbolFilter means to control only the current symbol of the chart, to intercept any trades, enter the symbol '*'. The signal provider will use for this purpose the FilterMatched function, which accepts the symbol and magic number of the transaction.

```
bool FilterMatched(const string s, const ulong m)
{
   if(MagicFilter != 0 && MagicFilter != m)
   {
      return false;
   }
   
   if(StringLen(SymbolFilter) == 0)
   {
      if(s != _Symbol)
      {
         return false;
      }
   }
   else if(SymbolFilter != s && SymbolFilter != "*")
   {
      return false;
   }
   
   return true;
}

```

The SymbolSubstitute parameter in the input group of the subscriber allows the substitution of the symbol received in messages with another one, which will be used for copy trading. This feature is useful if the names of tickers of the same financial instrument differ between brokers. But this parameter also performs the function of a permissive filter for repeating signals: only the symbols specified here will be traded. For example, to allow signal trading for the EURUSD symbol (even without ticker substitution), you need to set the string "EURUSD=EURUSD" in the parameter. The symbol from the signal messages is indicated to the left of the sign '=', and the symbol for trading is indicated to the right.

The character substitution list is processed by the FillSubstitutes function during initialization and then used to substitute and resolve the trade by the FindSubstitute function.

```
string Substitutes[][2];
   
void FillSubstitutes()
{
   string list[];
   const int n = StringSplit(SymbolSubstitute, ',', list);
   ArrayResize(Substitutes, n);
   for(int i = 0; i < n; ++i)
   {
      string pair[];
      if(StringSplit(list[i], '=', pair) == 2)
      {
         Substitutes[i][0] = pair[0];
         Substitutes[i][1] = pair[1];
      }
      else
      {
         Print("Wrong substitute: ", list[i]);
      }
   }
}
   
string FindSubstitute(const string s)
{
   for(int i = 0; i < ArrayRange(Substitutes, 0); ++i)
   {
      if(Substitutes[i][0] == s) return Substitutes[i][1];
   }
   return NULL;
}

```

To communicate with the service, we define a class derived from WebSocketClient. It is needed, first of all, to start trading on a signal when a message arrives in the onMessage handler. We will return to this issue a little later after we consider the formation and sending of signals on the provider side.

```
class MyWebSocket: public WebSocketClient<Hybi>
{
public:
   MyWebSocket(const string address): WebSocketClient(address) { }
   
   void onMessage(IWebSocketMessage *msg) override
   {
      ...
   }
};
   
MyWebSocket wss(Server);

```

Initialization in OnInit turns on the timer (for a periodic call wss.checkMessages(false)) and preparation of custom headers with user details, depending on the selected role. Then we open the connection with the wss.open(custom) call.

```
int OnInit()
{
   FillSubstitutes();
   EventSetTimer(1);
   wss.setTimeOut(1000);
   Print("Opening...");
   string custom;
   if(Role == TRADE_PUBLISHER)
   {
      custom = "Sec-Websocket-Protocol: X-MQL5-publisher-"
         + PublisherID + "-" + PublisherPrivateKey + "\r\n";
   }
   else
   {
      custom = "Sec-Websocket-Protocol: X-MQL5-subscriber-"
         + SubscriberID + "-" + SubscribeToPublisherID
         + "-" + SubscriberAccessKey + "\r\n";
   }
   return wss.open(custom) ? INIT_SUCCEEDED : INIT_FAILED;
}

```

The mechanism of copying, i.e., intercepting transactions and sending information about them to a web service, is launched in the OnTradeTransaction handler. As we know, this is not the only way and it would be possible to analyze the "snapshot" of the account state in OnTrade.

```
void OnTradeTransaction(const MqlTradeTransaction &transaction,
   const MqlTradeRequest &request,
   const MqlTradeResult &result)
{
   if(transaction.type == TRADE_TRANSACTION_REQUEST)
   {
      Print(TU::StringOf(request));
      Print(TU::StringOf(result));
      if(result.retcode == TRADE_RETCODE_PLACED           // successful action
         || result.retcode == TRADE_RETCODE_DONE
         || result.retcode == TRADE_RETCODE_DONE_PARTIAL)
      {
         if(FilterMatched(request.symbol, request.magic))
         {
            ... // see next block of code
         }
      }
   }
}

```

We track events about successfully completed trade requests that satisfy the conditions of the specified filters. Next, the structures of the request, the result of the request, and the deal are turned into JSON objects. All of them are placed in one common container msg under the names "req", "res", and "deal", respectively. Recall that the container itself will be included in the web service message as the "msg" property.

```
           // container to attach to service message will be visible as "msg" property:
             // {"origin" : "this_publisher_id", "msg" : { our data is here }}
            JsValue msg;
            MqlTradeRequestWeb req(request);
            msg.put("req", req.asJsValue());
            
            MqlTradeResultWeb res(result);
            msg.put("res", res.asJsValue());
            
            if(result.deal != 0)
            {
               DealMonitorWeb deal(result.deal);
               msg.put("deal", deal.asJsValue());
            }
            ulong tickets[];
            Positions.select(tickets);
            JsValue pos;
            pos.put("n", ArraySize(tickets));
            msg.put("pos", &pos);
            string buffer;
            msg.stringify(buffer);
            
            Print(buffer);
            
            wss.send(buffer);

```

Once filled, the container is output as a string into buffer, printed to the log, and sent to the server.

We can add other information to this container: account status (drawdown, loading), the number and properties of pending orders, and so on. So, just to demonstrate the possibilities for expanding the content of messages, we have added the number of open positions above. To select positions according to filters, we used the PositionFilter class object ([PositionFilter.mqh](/en/book/automation/experts/experts_positionget_funcs)):

```
PositionFilter Positions;
   
int OnInit()
{
   ...
   if(MagicFilter) Positions.let(POSITION_MAGIC, MagicFilter);
   if(SymbolFilter == "") Positions.let(POSITION_SYMBOL, _Symbol);
   else if(SymbolFilter != "*") Positions.let(POSITION_SYMBOL, SymbolFilter);
   ...
}

```

Basically, in order to increase reliability, it makes sense for the copiers to analyze the state of positions, and not just intercept transactions.

This concludes the consideration of the part of the Expert Advisor that is involved in the role of the signal provider.

As a subscriber, as we have already announced, the Expert Advisor receives messages in the MyWebSocket::onMessage method. Here the incoming message is parsed with JsParser::jsonify, and the container that was formed by the transmitting side is retrieved from the obj["msg"] property.

```
class MyWebSocket: public WebSocketClient<Hybi>
{
public:
   void onMessage(IWebSocketMessage *msg) override
   {
      Alert(msg.getString());
      JsValue *obj = JsParser::jsonify(msg.getString());
      if(obj && obj["msg"])
      {
         obj["msg"].print();
         if(!RemoteTrade(obj["msg"])) { /* error processing */ }
         delete obj;
      }
      delete msg;
   }
};

```

The RemoteTrade function implements the signal analysis and trading operations. Here it is given with abbreviations, without handling potential errors. The function provides support for both ways of representing enumerations: as integer values or as string element names. The incoming JSON object is "examined" for the necessary properties (commands and signal attributes) by applying the operator [], including several times consecutively (to access nested JSON objects).

```
bool RemoteTrade(JsValue *obj)
{
   bool success = false;
   
   if(obj["req"]["a"] == TRADE_ACTION_DEAL
      || obj["req"]["a"] == "TRADE_ACTION_DEAL")
   {
      const string symbol = FindSubstitute(obj["req"]["s"].s);
      if(symbol == NULL)
      {
         Print("Suitable symbol not found for ", obj["req"]["s"].s);
         return false; // not found or forbidden
      }
      
      JsValue *pType = obj["req"]["t"];
      if(pType == ORDER_TYPE_BUY || pType == ORDER_TYPE_SELL
         || pType == "ORDER_TYPE_BUY" || pType == "ORDER_TYPE_SELL")
      {
         ENUM_ORDER_TYPE type;
         if(pType.detect() >= JS_STRING)
         {
            if(pType == "ORDER_TYPE_BUY") type = ORDER_TYPE_BUY;
            else type = ORDER_TYPE_SELL;
         }
         else
         {
            type = obj["req"]["t"].get<ENUM_ORDER_TYPE>();
         }
         
         MqlTradeRequestSync request;
         request.deviation = 10;
         request.magic = SubscriberMagic;
         request.type = type;
         
         const double lot = obj["req"]["v"].get<double>();
         JsValue *pDir = obj["deal"]["entry"];
         if(pDir == DEAL_ENTRY_IN || pDir == "DEAL_ENTRY_IN")
         {
            success = request._market(symbol, lot) && request.completed();
            Alert(StringFormat("Trade by subscription: market entry %s %s %s - %s",
               EnumToString(type), TU::StringOf(lot), symbol,
               success ? "Successful" : "Failed"));
         }
         else if(pDir == DEAL_ENTRY_OUT || pDir == "DEAL_ENTRY_OUT")
         {
            // closing action assumes the presence of a suitable position, look for it
            PositionFilter filter;
            int props[] = {POSITION_TICKET, POSITION_TYPE, POSITION_VOLUME};
            Tuple3<long,long,double> values[];
            filter.let(POSITION_SYMBOL, symbol).let(POSITION_MAGIC,
               SubscriberMagic).select(props, values);
            for(int i = 0; i < ArraySize(values); ++i)
            {
              // need a position that is opposite in direction to the deal
               if(!TU::IsSameType((ENUM_ORDER_TYPE)values[i]._2, type))
               {
                  // you need enough volume (exactly equal here!)
                  if(TU::Equal(values[i]._3, lot))
                  {
                     success = request.close(values[i]._1, lot) && request.completed();
                     Alert(StringFormat("Trade by subscription: market exit %s %s %s - %s",
                        EnumToString(type), TU::StringOf(lot), symbol,
                        success ? "Successful" : "Failed"));
                  }
               }
            }
            
            if(!success)
            {
               Print("No suitable position to close");
            }
         }
      }
   }
   return success;
}

```

This implementation does not analyze the transaction price, possible restrictions on the lot, stop levels, and other moments. We simply repeat the trade at the current local price. Also, when closing a position, a check is made for exact equality of the volume, which is suitable for hedging accounts, but not for netting, where partial closure is possible if the volume of the transaction is less than the position (and maybe more, in case of a reversal, but the DEAL_ENTRY_INOUT option is not here supported). All these points should be finalized for real application.

Let's start the server node.exe wspubsub.js and two copies of the Expert Advisor wstradecopier.mq5 on different charts, in the same terminal. The usual scenario assumes that the Expert Advisor needs to be launched on different accounts, but a "paradoxical" option is also suitable for checking the performance: we will copy signals from one symbol to another.

In one copy of the Expert Advisor, we will leave the default settings, with the role of the publisher. It should be placed on the EURUSD chart. In the second copy that runs on the GBPUSD chart, we change the role to the subscriber. The string "EURUSD=GBPUSD" in the input parameter SymbolSubstitute allows GBPUSD trading on EURUSD signals.

The connection data will be logged, with the HTTP headers and greetings we've already seen, so we'll omit them.

Let's buy EURUSD and make sure that it is "duplicated" in the same volume for GBPUSD.

The following are fragments of the log (keep in mind that due to the fact that both Expert Advisors work in the same copy of the terminal, transaction messages will be sent to both charts and therefore, to facilitate the analysis of the log, you can alternately set the filters "EURUSD" and " USDUSD"):

```
(EURUSD,H1) TRADE_ACTION_DEAL, EURUSD, ORDER_TYPE_BUY, V=0.01, ORDER_FILLING_FOK, @ 0.99886, #=1461313378
(EURUSD,H1) DONE, D=1439023682, #=1461313378, V=0.01, @ 0.99886, Bid=0.99886, Ask=0.99886, Req=2
(EURUSD,H1) {"req" : {"a" : "TRADE_ACTION_DEAL", "s" : "EURUSD", "t" : "ORDER_TYPE_BUY", "v" : 0.01,
»   "f" : "ORDER_FILLING_FOK", "p" : 0.99886, "o" : 1461313378}, "res" : {"code" : 10009, "d" : 1439023682,
»   "o" : 1461313378, "v" : 0.01, "p" : 0.99886, "b" : 0.99886, "a" : 0.99886}, "deal" : {"d" : 1439023682,
»   "o" : 1461313378, "t" : "2022.09.19 16:45:50", "tmsc" : 1663605950086, "type" : "DEAL_TYPE_BUY",
»   "entry" : "DEAL_ENTRY_IN", "pid" : 1461313378, "r" : "DEAL_REASON_CLIENT", "v" : 0.01, "p" : 0.99886,
»   "s" : "EURUSD"}, "pos" : {"n" : 1}}
 

```

This shows the content of the executed request and its result, as well as a buffer with a JSON string sent to the server.

Almost instantly, on the receiving side, on the GBPUSD chart, an alert is displayed with a message from the server in a "raw" form and formatted after successful parsing in JsParser. In the "raw" form, the "origin" property is stored, in which the server lets us know who is the source of the signal.

```
(GBPUSD,H1) Alert: {"origin":"publisher PUB_ID_001", "msg":{"req" : {"a" : "TRADE_ACTION_DEAL",
»   "s" : "EURUSD", "t" : "ORDER_TYPE_BUY", "v" : 0.01, "f" : "ORDER_FILLING_FOK", "p" : 0.99886,
»   "o" : 1461313378}, "res" : {"code" : 10009, "d" : 1439023682, "o" : 1461313378, "v" : 0.01,
»   "p" : 0.99886, "b" : 0.99886, "a" : 0.99886}, "deal" : {"d" : 1439023682, "o" : 1461313378,
»   "t" : "2022.09.19 16:45:50", "tmsc" : 1663605950086, "type" : "DEAL_TYPE_BUY",
»   "entry" : "DEAL_ENTRY_IN", "pid" : 1461313378, "r" : "DEAL_REASON_CLIENT", "v" : 0.01,
»   "p" : 0.99886, "s" : "EURUSD"}, "pos" : {"n" : 1}}}
(GBPUSD,H1)        {
(GBPUSD,H1)          req = 
(GBPUSD,H1)          {
(GBPUSD,H1)            a = TRADE_ACTION_DEAL
(GBPUSD,H1)            s = EURUSD
(GBPUSD,H1)            t = ORDER_TYPE_BUY
(GBPUSD,H1)            v =  0.01
(GBPUSD,H1)            f = ORDER_FILLING_FOK
(GBPUSD,H1)            p =  0.99886
(GBPUSD,H1)            o =  1461313378
(GBPUSD,H1)          }
(GBPUSD,H1)          res = 
(GBPUSD,H1)          {
(GBPUSD,H1)            code =  10009
(GBPUSD,H1)            d =  1439023682
(GBPUSD,H1)            o =  1461313378
(GBPUSD,H1)            v =  0.01
(GBPUSD,H1)            p =  0.99886
(GBPUSD,H1)            b =  0.99886
(GBPUSD,H1)            a =  0.99886
(GBPUSD,H1)          }
(GBPUSD,H1)          deal = 
(GBPUSD,H1)          {
(GBPUSD,H1)            d =  1439023682
(GBPUSD,H1)            o =  1461313378
(GBPUSD,H1)            t = 2022.09.19 16:45:50
(GBPUSD,H1)            tmsc =  1663605950086
(GBPUSD,H1)            type = DEAL_TYPE_BUY
(GBPUSD,H1)            entry = DEAL_ENTRY_IN
(GBPUSD,H1)            pid =  1461313378
(GBPUSD,H1)            r = DEAL_REASON_CLIENT
(GBPUSD,H1)            v =  0.01
(GBPUSD,H1)            p =  0.99886
(GBPUSD,H1)            s = EURUSD
(GBPUSD,H1)          }
(GBPUSD,H1)          pos = 
(GBPUSD,H1)          {
(GBPUSD,H1)            n =  1
(GBPUSD,H1)          }
(GBPUSD,H1)        }
(GBPUSD,H1)        Alert: Trade by subscription: market entry ORDER_TYPE_BUY 0.01 GBPUSD - Successful

```

The last of the above entries indicates a successful transaction on GBPUSD. On the trading tab of the account, 2 positions should be displayed.

After some time, we close the EURUSD position, and the GBPUSD position should close automatically.

```
(EURUSD,H1) TRADE_ACTION_DEAL, EURUSD, ORDER_TYPE_SELL, V=0.01, ORDER_FILLING_FOK, @ 0.99881, #=1461315206, P=1461313378
(EURUSD,H1) DONE, D=1439025490, #=1461315206, V=0.01, @ 0.99881, Bid=0.99881, Ask=0.99881, Req=4
(EURUSD,H1) {"req" : {"a" : "TRADE_ACTION_DEAL", "s" : "EURUSD", "t" : "ORDER_TYPE_SELL", "v" : 0.01,
»   "f" : "ORDER_FILLING_FOK", "p" : 0.99881, "o" : 1461315206, "q" : 1461313378}, "res" : {"code" : 10009,
»   "d" : 1439025490, "o" : 1461315206, "v" : 0.01, "p" : 0.99881, "b" : 0.99881, "a" : 0.99881},
»   "deal" : {"d" : 1439025490, "o" : 1461315206, "t" : "2022.09.19 16:46:52", "tmsc" : 1663606012990,
»   "type" : "DEAL_TYPE_SELL", "entry" : "DEAL_ENTRY_OUT", "pid" : 1461313378, "r" : "DEAL_REASON_CLIENT",
»   "v" : 0.01, "p" : 0.99881, "m" : -0.05, "s" : "EURUSD"}, "pos" : {"n" : 0}}

```

If the deal had a type DEAL_ENTRY_IN for the first time, now it is DEAL_ENTRY_OUT. The alert confirms the receipt of the message and the successful closing of the duplicate position.

```
(GBPUSD,H1) Alert: {"origin":"publisher PUB_ID_001", "msg":{"req" : {"a" : "TRADE_ACTION_DEAL",
»   "s" : "EURUSD", "t" : "ORDER_TYPE_SELL", "v" : 0.01, "f" : "ORDER_FILLING_FOK", "p" : 0.99881,
»   "o" : 1461315206, "q" : 1461313378}, "res" : {"code" : 10009, "d" : 1439025490, "o" : 1461315206,
»   "v" : 0.01, "p" : 0.99881, "b" : 0.99881, "a" : 0.99881}, "deal" : {"d" : 1439025490,
»   "o" : 1461315206, "t" : "2022.09.19 16:46:52", "tmsc" : 1663606012990, "type" : "DEAL_TYPE_SELL",
»   "entry" : "DEAL_ENTRY_OUT", "pid" : 1461313378, "r" : "DEAL_REASON_CLIENT", "v" : 0.01,
»   "p" : 0.99881, "m" : -0.05, "s" : "EURUSD"}, "pos" : {"n" : 0}}}
...
(GBPUSD,H1)        Alert: Trade by subscription: market exit ORDER_TYPE_SELL 0.01 GBPUSD - Successful

```

Finally, next to the Expert Advisor wstradecopier.mq5, we create a project file wstradecopier.mqproj to add a description and necessary server files to it (in the old directory MQL5/Experts/p7/MQL5Book/Web/).

To summarize: we have organized a technically extensible, multi-user system for exchanging trading information via a socket server. Due to the technical features of web sockets (permanent open connection), this implementation of the signal service is more suitable for short-term and high-frequency trading, as well as for controlling arbitrage situations in quotes.

Solving the problem required combining several programs on different platforms and connecting a large number of dependencies, which is what usually characterizes the transition to the project level. The development environment is also expanded, going beyond the compiler and source code editor. In particular, the presence in the project of the client or server parts usually involves the work of different programmers responsible for them. In this case, shared projects in the cloud and with version control become indispensable.

Please note that when developing a project in the folder MQL5/Shared Projects via MetaEditor, header files from the standard directory MQL5/Include are not included in the shared storage. On the other hand, creating a dedicated folder Include inside your project and transferring the necessary standard mqh files to it will lead to duplication of information and potential discrepancies in the versions of header files. This behavior is likely to be improved in MetaEditor.

Another point for public projects is the need to administer users and authorize them. In our last example, this issue was only identified but not implemented. However, the mql5.com site provides a ready-made solution based on the well-known OAuth protocol. Anyone who has an mql5.com account can get familiar with the principle of OAuth and configure it for their web service: just find the section Applications (link looking like https://www.mql5.com/en/users/<login> /apps) in your profile. By registering a web service in mql5.com applications, you will be able to authorize users through the mql5.com website.
