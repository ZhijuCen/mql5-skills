# DatabaseExecute

Executes a request to a specified database.

```
bool  DatabaseExecute(
   int     database,      // database handle received in DatabaseOpen
   string  sql            // SQL request
   );

```

Parameters

database

[in]  Database handle received in [DatabaseOpen()](/en/docs/database/databaseopen).

sql

[in]  SQL request.

Return Value

Return true if successful, otherwise false. To get the error code, use GetLastError(), the possible responses are:

- ERR_INTERNAL_ERROR (4001)                   –  critical runtime error;
- ERR_INVALID_PARAMETER (4003)              –  sql parameter contains an empty string;
- ERR_NOT_ENOUGH_MEMORY (4004)          –  insufficient memory;
- ERR_WRONG_STRING_PARAMETER (5040)  – error converting a request into a UTF-8 string;
- ERR_DATABASE_INTERNAL (5120)              – internal database error;
- ERR_DATABASE_INVALID_HANDLE (5121)   – invalid database handle;
- ERR_DATABASE_EXECUTE (5124)               –  request execution error.

Example:

```
//--- symbol statistics
struct Symbol_Stats
  {
   string            name;             // symbol name
   int               trades;           // number of trades for the symbol
   double            gross_profit;     // total profit for the symbol
   double            gross_loss;       // total loss for the symbol
   double            total_commission; // total commission for the symbol
   double            total_swap;       // total swaps for the symbol
   double            total_profit;     // total profit excluding swaps and commissions
   double            net_profit;       // net profit taking into account swaps and commissions
   int               win_trades;       // number of profitable trades
   int               loss_trades;      // number of losing trades
   double            expected_payoff;  // expected payoff for the trade excluding swaps and commissions
   double            win_percent;      // percentage of winning trades
   double            loss_percent;     // percentage of losing trades
   double            average_profit;   // average profit
   double            average_loss;     // average loss
   double            profit_factor;    // profit factor
  };
 
//--- Magic Number statistics
struct Magic_Stats
  {
   long              magic;            // EA's Magic Number
   int               trades;           // number of trades for the symbol
   double            gross_profit;     // total profit for the symbol
   double            gross_loss;       // total loss for the symbol
   double            total_commission; // total commission for the symbol
   double            total_swap;       // total swaps for the symbol
   double            total_profit;     // total profit excluding swaps and commissions
   double            net_profit;       // net profit taking into account swaps and commissions
   int               win_trades;       // number of profitable trades
   int               loss_trades;      // number of losing trades
   double            expected_payoff;  // expected payoff for the trade excluding swaps and commissions
   double            win_percent;      // percentage of winning trades
   double            loss_percent;     // percentage of losing trades
   double            average_profit;   // average profit
   double            average_loss;     // average loss
   double            profit_factor;    // profit factor
  };
 
//--- entry hour statistics
struct Hour_Stats
  {
   char              hour_in;          // market entry hour
   int               trades;           // number of trades in this entry hour
   double            volume;           // volume of trades in this entry hour
   double            gross_profit;     // total profit in this entry hour
   double            gross_loss;       // total loss in this entry hour
   double            net_profit;       // net profit taking into account swaps and commissions
   int               win_trades;       // number of profitable trades
   int               loss_trades;      // number of losing trades
   double            expected_payoff;  // expected payoff for the trade excluding swaps and commissions
   double            win_percent;      // percentage of winning trades
   double            loss_percent;     // percentage of losing trades
   double            average_profit;   // average profit
   double            average_loss;     // average loss
   double            profit_factor;    // profit factor
  };
 
int ExtDealsTotal=0;;
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- create the file name
   string filename=IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN))+"_stats.sqlite";
//--- open/create the database in the common terminal folder
   int db=DatabaseOpen(filename, DATABASE_OPEN_READWRITE | DATABASE_OPEN_CREATE | DATABASE_OPEN_COMMON);
   if(db==INVALID_HANDLE)
     {
      Print("DB: ", filename, " open failed with code ", GetLastError());
      return;
     }
//--- create the DEALS table
   if(!CreateTableDeals(db))
     {
      DatabaseClose(db);
      return;
     }
   PrintFormat("Deals in the trading history: %d ", ExtDealsTotal);
 
//--- get trading statistics per symbols
   int request=DatabasePrepare(db, "SELECT r.*,"
                               "   (case when r.trades != 0 then (r.gross_profit+r.gross_loss)/r.trades else 0 end) as expected_payoff,"
                               "   (case when r.trades != 0 then r.win_trades*100.0/r.trades else 0 end) as win_percent,"
                               "   (case when r.trades != 0 then r.loss_trades*100.0/r.trades else 0 end) as loss_percent,"
                               "   r.gross_profit/r.win_trades as average_profit,"
                               "   r.gross_loss/r.loss_trades as average_loss,"
                               "   (case when r.gross_loss!=0.0 then r.gross_profit/(-r.gross_loss) else 0 end) as profit_factor "
                               "FROM "
                               "   ("
                               "   SELECT SYMBOL,"
                               "   sum(case when entry =1 then 1 else 0 end) as trades,"
                               "   sum(case when profit > 0 then profit else 0 end) as gross_profit,"
                               "   sum(case when profit < 0 then profit else 0 end) as gross_loss,"
                               "   sum(swap) as total_swap,"
                               "   sum(commission) as total_commission,"
                               "   sum(profit) as total_profit,"
                               "   sum(profit+swap+commission) as net_profit,"
                               "   sum(case when profit > 0 then 1 else 0 end) as win_trades,"
                               "   sum(case when profit < 0 then 1 else 0 end) as loss_trades "
                               "   FROM DEALS "
                               "   WHERE SYMBOL <> '' and SYMBOL is not NULL "
                               "   GROUP BY SYMBOL"
                               "   ) as r");
   if(request==INVALID_HANDLE)
     {
      Print("DB: ", filename, " request failed with code ", GetLastError());
      DatabaseClose(db);
      return;
     }
   Symbol_Stats stats[], symbol_stats;
   ArrayResize(stats, ExtDealsTotal);
   int i=0;
//--- get records from request results
   for(; DatabaseReadBind(request, symbol_stats) ; i++)
     {
      stats[i].name=symbol_stats.name;
      stats[i].trades=symbol_stats.trades;
      stats[i].gross_profit=symbol_stats.gross_profit;
      stats[i].gross_loss=symbol_stats.gross_loss;
      stats[i].total_commission=symbol_stats.total_commission;
      stats[i].total_swap=symbol_stats.total_swap;
      stats[i].total_profit=symbol_stats.total_profit;
      stats[i].net_profit=symbol_stats.net_profit;
      stats[i].win_trades=symbol_stats.win_trades;
      stats[i].loss_trades=symbol_stats.loss_trades;
      stats[i].expected_payoff=symbol_stats.expected_payoff;
      stats[i].win_percent=symbol_stats.win_percent;
      stats[i].loss_percent=symbol_stats.loss_percent;
      stats[i].average_profit=symbol_stats.average_profit;
      stats[i].average_loss=symbol_stats.average_loss;
      stats[i].profit_factor=symbol_stats.profit_factor;
     }
   ArrayResize(stats, i);
   Print("Trade statistics by Symbol");
   ArrayPrint(stats);
   Print("");
//--- delete the request
   DatabaseFinalize(request);
 
//--- get trading statistics for Expert Advisors by Magic Numbers
   request=DatabasePrepare(db, "SELECT r.*,"
                           "   (case when r.trades != 0 then (r.gross_profit+r.gross_loss)/r.trades else 0 end) as expected_payoff,"
                           "   (case when r.trades != 0 then r.win_trades*100.0/r.trades else 0 end) as win_percent,"
                           "   (case when r.trades != 0 then r.loss_trades*100.0/r.trades else 0 end) as loss_percent,"
                           "   r.gross_profit/r.win_trades as average_profit,"
                           "   r.gross_loss/r.loss_trades as average_loss,"
                           "   (case when r.gross_loss!=0.0 then r.gross_profit/(-r.gross_loss) else 0 end) as profit_factor "
                           "FROM "
                           "   ("
                           "   SELECT MAGIC,"
                           "   sum(case when entry =1 then 1 else 0 end) as trades,"
                           "   sum(case when profit > 0 then profit else 0 end) as gross_profit,"
                           "   sum(case when profit < 0 then profit else 0 end) as gross_loss,"
                           "   sum(swap) as total_swap,"
                           "   sum(commission) as total_commission,"
                           "   sum(profit) as total_profit,"
                           "   sum(profit+swap+commission) as net_profit,"
                           "   sum(case when profit > 0 then 1 else 0 end) as win_trades,"
                           "   sum(case when profit < 0 then 1 else 0 end) as loss_trades "
                           "   FROM DEALS "
                           "   WHERE SYMBOL <> '' and SYMBOL is not NULL "
                           "   GROUP BY MAGIC"
                           "   ) as r");
   if(request==INVALID_HANDLE)
     {
      Print("DB: ", filename, " request failed with code ", GetLastError());
      DatabaseClose(db);
      return;
     }
   Magic_Stats EA_stats[], magic_stats;
   ArrayResize(EA_stats, ExtDealsTotal);
   i=0;
//--- print
   for(; DatabaseReadBind(request, magic_stats) ; i++)
     {
      EA_stats[i].magic=magic_stats.magic;
      EA_stats[i].trades=magic_stats.trades;
      EA_stats[i].gross_profit=magic_stats.gross_profit;
      EA_stats[i].gross_loss=magic_stats.gross_loss;
      EA_stats[i].total_commission=magic_stats.total_commission;
      EA_stats[i].total_swap=magic_stats.total_swap;
      EA_stats[i].total_profit=magic_stats.total_profit;
      EA_stats[i].net_profit=magic_stats.net_profit;
      EA_stats[i].win_trades=magic_stats.win_trades;
      EA_stats[i].loss_trades=magic_stats.loss_trades;
      EA_stats[i].expected_payoff=magic_stats.expected_payoff;
      EA_stats[i].win_percent=magic_stats.win_percent;
      EA_stats[i].loss_percent=magic_stats.loss_percent;
      EA_stats[i].average_profit=magic_stats.average_profit;
      EA_stats[i].average_loss=magic_stats.average_loss;
      EA_stats[i].profit_factor=magic_stats.profit_factor;
     }
   ArrayResize(EA_stats, i);
   Print("Trade statistics by Magic Number");
   ArrayPrint(EA_stats);
   Print("");
//--- delete the request
   DatabaseFinalize(request);
 
//--- make sure that hedging system for open position management is used on the account
   if((ENUM_ACCOUNT_MARGIN_MODE)AccountInfoInteger(ACCOUNT_MARGIN_MODE)!=ACCOUNT_MARGIN_MODE_RETAIL_HEDGING)
     {
      //--- deals cannot be transformed to trades using a simple method through transactions, therefore complete operation
      DatabaseClose(db);
      return;
     }
 
//--- now create the TRADES table based on the DEALS table
   if(!CreateTableTrades(db))
     {
      DatabaseClose(db);
      return;
     }
//--- fill in the TRADES table using an SQL query based on DEALS table data
   if(DatabaseTableExists(db, "DEALS"))
      //--- populate the TRADES table
      if(!DatabaseExecute(db, "INSERT INTO TRADES(TIME_IN,HOUR_IN,TICKET,TYPE,VOLUME,SYMBOL,PRICE_IN,TIME_OUT,PRICE_OUT,COMMISSION,SWAP,PROFIT) "
                          "SELECT "
                          "   d1.time as time_in,"
                          "   d1.hour as hour_in,"
                          "   d1.position_id as ticket,"
                          "   d1.type as type,"
                          "   d1.volume as volume,"
                          "   d1.symbol as symbol,"
                          "   d1.price as price_in,"
                          "   d2.time as time_out,"
                          "   d2.price as price_out,"
                          "   d1.commission+d2.commission as commission,"
                          "   d2.swap as swap,"
                          "   d2.profit as profit "
                          "FROM DEALS d1 "
                          "INNER JOIN DEALS d2 ON d1.position_id=d2.position_id "
                          "WHERE d1.entry=0 AND d2.entry=1     "))
        {
         Print("DB: fillng the table TRADES failed with code ", GetLastError());
         return;
        }
 
//--- get trading statistics by market entry hours
   request=DatabasePrepare(db, "SELECT r.*,"
                           "   (case when r.trades != 0 then (r.gross_profit+r.gross_loss)/r.trades else 0 end) as expected_payoff,"
                           "   (case when r.trades != 0 then r.win_trades*100.0/r.trades else 0 end) as win_percent,"
                           "   (case when r.trades != 0 then r.loss_trades*100.0/r.trades else 0 end) as loss_percent,"
                           "   r.gross_profit/r.win_trades as average_profit,"
                           "   r.gross_loss/r.loss_trades as average_loss,"
                           "   (case when r.gross_loss!=0.0 then r.gross_profit/(-r.gross_loss) else 0 end) as profit_factor "
                           "FROM "
                           "   ("
                           "   SELECT HOUR_IN,"
                           "   count() as trades,"
                           "   sum(volume) as volume,"
                           "   sum(case when profit > 0 then profit else 0 end) as gross_profit,"
                           "   sum(case when profit < 0 then profit else 0 end) as gross_loss,"
                           "   sum(profit) as net_profit,"
                           "   sum(case when profit > 0 then 1 else 0 end) as win_trades,"
                           "   sum(case when profit < 0 then 1 else 0 end) as loss_trades "
                           "   FROM TRADES "
                           "   WHERE SYMBOL <> '' and SYMBOL is not NULL "
                           "   GROUP BY HOUR_IN"
                           "   ) as r");
   if(request==INVALID_HANDLE)
     {
      Print("DB: ", filename, " request failed with code ", GetLastError());
      DatabaseClose(db);
      return;
     }
   Hour_Stats hours_stats[], h_stats;
   ArrayResize(hours_stats, ExtDealsTotal);
   i=0;
//--- print
   for(; DatabaseReadBind(request, h_stats) ; i++)
     {
      hours_stats[i].hour_in=h_stats.hour_in;
      hours_stats[i].trades=h_stats.trades;
      hours_stats[i].volume=h_stats.volume;
      hours_stats[i].gross_profit=h_stats.gross_profit;
      hours_stats[i].gross_loss=h_stats.gross_loss;
      hours_stats[i].net_profit=h_stats.net_profit;
      hours_stats[i].win_trades=h_stats.win_trades;
      hours_stats[i].loss_trades=h_stats.loss_trades;
      hours_stats[i].expected_payoff=h_stats.expected_payoff;
      hours_stats[i].win_percent=h_stats.win_percent;
      hours_stats[i].loss_percent=h_stats.loss_percent;
      hours_stats[i].average_profit=h_stats.average_profit;
      hours_stats[i].average_loss=h_stats.average_loss;
      hours_stats[i].profit_factor=h_stats.profit_factor;
     }
   ArrayResize(hours_stats, i);
   Print("Trade statistics by entry hour");
   ArrayPrint(hours_stats);
   Print("");
//--- delete the request
   DatabaseFinalize(request);
 
//--- close database
   DatabaseClose(db);
   return;
  }
/*
Deals in the trading history: 2771 
Trade statistics by Symbol
      [name] [trades] [gross_profit] [gross_loss] [total_commission] [total_swap] [total_profit] [net_profit] [win_trades] [loss_trades] [expected_payoff] [win_percent] [loss_percent] [average_profit] [average_loss] [profit_factor]
[0] "AUDUSD"      112      503.20000   -568.00000           -8.83000    -24.64000      -64.80000    -98.27000           70            42          -0.57857      62.50000       37.50000          7.18857      -13.52381         0.88592
[1] "EURCHF"      125      607.71000   -956.85000          -11.77000    -45.02000     -349.14000   -405.93000           54            71          -2.79312      43.20000       56.80000         11.25389      -13.47676         0.63512
[2] "EURJPY"      127     1078.49000  -1057.83000          -10.61000    -45.76000       20.66000    -35.71000           64            63           0.16268      50.39370       49.60630         16.85141      -16.79095         1.01953
[3] "EURUSD"      233     1685.60000  -1386.80000          -41.00000    -83.76000      298.80000    174.04000          127           106           1.28240      54.50644       45.49356         13.27244      -13.08302         1.21546
[4] "GBPCHF"      125     1881.37000  -1424.72000          -22.60000    -51.56000      456.65000    382.49000           80            45           3.65320      64.00000       36.00000         23.51712      -31.66044         1.32052
[5] "GBPJPY"      127     1943.43000  -1776.67000          -18.84000    -52.46000      166.76000     95.46000           76            51           1.31307      59.84252       40.15748         25.57145      -34.83667         1.09386
[6] "GBPUSD"      121     1668.50000  -1438.20000           -7.96000    -49.93000      230.30000    172.41000           77            44           1.90331      63.63636       36.36364         21.66883      -32.68636         1.16013
[7] "USDCAD"       99      405.28000   -475.47000           -8.68000    -31.68000      -70.19000   -110.55000           51            48          -0.70899      51.51515       48.48485          7.94667       -9.90563         0.85238
[8] "USDCHF"      206     1588.32000  -1241.83000          -17.98000    -65.92000      346.49000    262.59000          131            75           1.68199      63.59223       36.40777         12.12458      -16.55773         1.27902
[9] "USDJPY"      107      464.73000   -730.64000          -35.12000    -34.24000     -265.91000   -335.27000           50            57          -2.48514      46.72897       53.27103          9.29460      -12.81825         0.63606
 
Trade statistics by Magic Number
    [magic] [trades] [gross_profit] [gross_loss] [total_commission] [total_swap] [total_profit] [net_profit] [win_trades] [loss_trades] [expected_payoff] [win_percent] [loss_percent] [average_profit] [average_loss] [profit_factor]
[0]     100      242     2584.80000  -2110.00000          -33.36000    -93.53000      474.80000    347.91000          143            99           1.96198      59.09091       40.90909         18.07552      -21.31313         1.22502
[1]     200      254     3021.92000  -2834.50000          -29.45000    -98.22000      187.42000     59.75000          140           114           0.73787      55.11811       44.88189         21.58514      -24.86404         1.06612
[2]     300      250     2489.08000  -2381.57000          -34.37000    -96.58000      107.51000    -23.44000          134           116           0.43004      53.60000       46.40000         18.57522      -20.53078         1.04514
[3]     400      224     1272.50000  -1283.00000          -24.43000    -64.80000      -10.50000    -99.73000          131            93          -0.04687      58.48214       41.51786          9.71374      -13.79570         0.99182
[4]     500      198     1141.23000  -1051.91000          -27.66000    -63.36000       89.32000     -1.70000          116            82           0.45111      58.58586       41.41414          9.83819      -12.82817         1.08491
[5]     600      214     1317.10000  -1396.03000          -34.12000    -68.48000      -78.93000   -181.53000          116            98          -0.36883      54.20561       45.79439         11.35431      -14.24520         0.94346
 
Trade statistics by entry hour
     [hour_in] [trades] [volume] [gross_profit] [gross_loss] [net_profit] [win_trades] [loss_trades] [expected_payoff] [win_percent] [loss_percent] [average_profit] [average_loss] [profit_factor]
[ 0]         0       50  5.00000      336.51000   -747.47000   -410.96000           21            29          -8.21920      42.00000       58.00000         16.02429      -25.77483         0.45020
[ 1]         1       20  2.00000      102.56000    -57.20000     45.36000           12             8           2.26800      60.00000       40.00000          8.54667       -7.15000         1.79301
[ 2]         2        6  0.60000       38.55000    -14.60000     23.95000            5             1           3.99167      83.33333       16.66667          7.71000      -14.60000         2.64041
[ 3]         3       38  3.80000      173.84000   -200.15000    -26.31000           22            16          -0.69237      57.89474       42.10526          7.90182      -12.50938         0.86855
[ 4]         4       60  6.00000      361.44000   -389.40000    -27.96000           27            33          -0.46600      45.00000       55.00000         13.38667      -11.80000         0.92820
[ 5]         5       32  3.20000      157.43000   -179.89000    -22.46000           20            12          -0.70187      62.50000       37.50000          7.87150      -14.99083         0.87515
[ 6]         6       18  1.80000       95.59000   -162.33000    -66.74000           11             7          -3.70778      61.11111       38.88889          8.69000      -23.19000         0.58886
[ 7]         7       14  1.40000       38.48000   -134.30000    -95.82000            9             5          -6.84429      64.28571       35.71429          4.27556      -26.86000         0.28652
[ 8]         8       42  4.20000      368.48000   -322.30000     46.18000           24            18           1.09952      57.14286       42.85714         15.35333      -17.90556         1.14328
[ 9]         9      118 11.80000     1121.62000   -875.21000    246.41000           72            46           2.08822      61.01695       38.98305         15.57806      -19.02630         1.28154
[10]        10      206 20.60000     2280.59000  -2021.80000    258.79000          115            91           1.25626      55.82524       44.17476         19.83122      -22.21758         1.12800
[11]        11      138 13.80000     1377.02000   -994.18000    382.84000           84            54           2.77420      60.86957       39.13043         16.39310      -18.41074         1.38508
[12]        12      152 15.20000     1247.56000  -1463.80000   -216.24000           84            68          -1.42263      55.26316       44.73684         14.85190      -21.52647         0.85227
[13]        13       64  6.40000      778.27000   -516.22000    262.05000           36            28           4.09453      56.25000       43.75000         21.61861      -18.43643         1.50763
[14]        14       62  6.20000      536.93000   -427.47000    109.46000           38            24           1.76548      61.29032       38.70968         14.12974      -17.81125         1.25606
[15]        15       50  5.00000      699.92000   -413.00000    286.92000           28            22           5.73840      56.00000       44.00000         24.99714      -18.77273         1.69472
[16]        16       88  8.80000      778.55000   -514.00000    264.55000           51            37           3.00625      57.95455       42.04545         15.26569      -13.89189         1.51469
[17]        17       76  7.60000      533.92000  -1019.46000   -485.54000           44            32          -6.38868      57.89474       42.10526         12.13455      -31.85813         0.52373
[18]        18       52  5.20000      237.17000   -246.78000     -9.61000           24            28          -0.18481      46.15385       53.84615          9.88208       -8.81357         0.96106
[19]        19       52  5.20000      407.67000   -150.36000    257.31000           30            22           4.94827      57.69231       42.30769         13.58900       -6.83455         2.71129
[20]        20       18  1.80000       65.92000    -89.09000    -23.17000            9             9          -1.28722      50.00000       50.00000          7.32444       -9.89889         0.73993
[21]        21       10  1.00000       41.86000    -32.38000      9.48000            7             3           0.94800      70.00000       30.00000          5.98000      -10.79333         1.29277
[22]        22       14  1.40000       45.55000    -83.72000    -38.17000            6             8          -2.72643      42.85714       57.14286          7.59167      -10.46500         0.54408
[23]        23        2  0.20000        1.20000     -1.90000     -0.70000            1             1          -0.35000      50.00000       50.00000          1.20000       -1.90000         0.63158
*/  
  
//+------------------------------------------------------------------+
//| Creates the DEALS table                                          |
//+------------------------------------------------------------------+
bool CreateTableDeals(int database)
  {
//--- if the DEALS table already exists, delete it
   if(!DeleteTable(database, "DEALS"))
     {
      return(false);
     }
//--- check if the table exists
   if(!DatabaseTableExists(database, "DEALS"))
      //--- create the table
      if(!DatabaseExecute(database, "CREATE TABLE DEALS("
                          "ID          INT KEY NOT NULL,"
                          "ORDER_ID    INT     NOT NULL,"
                          "POSITION_ID INT     NOT NULL,"
                          "TIME        INT     NOT NULL,"
                          "TYPE        INT     NOT NULL,"
                          "ENTRY       INT     NOT NULL,"
                          "SYMBOL      CHAR(10),"
                          "VOLUME      REAL,"
                          "PRICE       REAL,"
                          "PROFIT      REAL,"
                          "SWAP        REAL,"
                          "COMMISSION  REAL,"
                          "MAGIC       INT,"
                          "HOUR        INT,"
                          "REASON      INT);"))
        {
         Print("DB: create the DEALS table  failed with code ", GetLastError());
         return(false);
        }
//---  request the entire trading history
   datetime from_date=0;
   datetime to_date=TimeCurrent();
//--- request the history of deals in the specified interval
   HistorySelect(from_date, to_date);
   ExtDealsTotal=HistoryDealsTotal();
//--- add deals to the table
   if(!InsertDeals(database))
      return(false);
//--- the table has been successfully created
   return(true);
  }
//+------------------------------------------------------------------+
//| Deletes a table with the specified name from the database        |
//+------------------------------------------------------------------+
bool DeleteTable(int database, string table_name)
  {
   if(!DatabaseExecute(database, "DROP TABLE IF EXISTS "+table_name))
     {
      Print("Failed to drop the DEALS table with code ", GetLastError());
      return(false);
     }
//--- the table has been successfully deleted
   return(true);
  }
//+------------------------------------------------------------------+
//| Adds deals to the database table                                 |
//+------------------------------------------------------------------+
bool InsertDeals(int database)
  {
//--- Auxiliary variables
   ulong    deal_ticket;         // deal ticket
   long     order_ticket;        // the ticket of the order by which the deal was executed
   long     position_ticket;     // ID of the position to which the deal belongs
   datetime time;                // deal execution time
   long     type ;               // deal type
   long     entry ;              // deal direction
   string   symbol;              // the symbol fro which the deal was executed
   double   volume;              // operation volume
   double   price;               // price
   double   profit;              // financial result
   double   swap;                // swap
   double   commission;          // commission
   long     magic;               // Magic number (Expert Advisor ID)
   long     reason;              // deal execution reason or source
   char     hour;                // deal execution hour
   MqlDateTime time_strusture;
//--- go through all deals and add them to the database
   bool failed=false;
   int deals=HistoryDealsTotal();
// --- lock the database before executing transactions
   DatabaseTransactionBegin(database);
   for(int i=0; i<deals; i++)
     {
      deal_ticket=    HistoryDealGetTicket(i);
      order_ticket=   HistoryDealGetInteger(deal_ticket, DEAL_ORDER);
      position_ticket=HistoryDealGetInteger(deal_ticket, DEAL_POSITION_ID);
      time= (datetime)HistoryDealGetInteger(deal_ticket, DEAL_TIME);
      type=           HistoryDealGetInteger(deal_ticket, DEAL_TYPE);
      entry=          HistoryDealGetInteger(deal_ticket, DEAL_ENTRY);
      symbol=         HistoryDealGetString(deal_ticket, DEAL_SYMBOL);
      volume=         HistoryDealGetDouble(deal_ticket, DEAL_VOLUME);
      price=          HistoryDealGetDouble(deal_ticket, DEAL_PRICE);
      profit=         HistoryDealGetDouble(deal_ticket, DEAL_PROFIT);
      swap=           HistoryDealGetDouble(deal_ticket, DEAL_SWAP);
      commission=     HistoryDealGetDouble(deal_ticket, DEAL_COMMISSION);
      magic=          HistoryDealGetInteger(deal_ticket, DEAL_MAGIC);
      reason=         HistoryDealGetInteger(deal_ticket, DEAL_REASON);
      TimeToStruct(time, time_strusture);
      hour= (char)time_strusture.hour;
      //--- add each deal to the table using the following request
      string request_text=StringFormat("INSERT INTO DEALS (ID,ORDER_ID,POSITION_ID,TIME,TYPE,ENTRY,SYMBOL,VOLUME,PRICE,PROFIT,SWAP,COMMISSION,MAGIC,REASON,HOUR)"
                                       "VALUES (%d, %d, %d, %d, %d, %d, '%s', %G, %G, %G, %G, %G, %d, %d,%d)",
                                       deal_ticket, order_ticket, position_ticket, time, type, entry, symbol, volume, price, profit, swap, commission, magic, reason, hour);
      if(!DatabaseExecute(database, request_text))
        {
         PrintFormat("%s: failed to insert deal #%d with code %d", __FUNCTION__, deal_ticket, GetLastError());
         PrintFormat("i=%d: deal #%d  %s", i, deal_ticket, symbol);
         failed=true;
         break;
        }
     }
//--- check for transaction execution errors
   if(failed)
     {
      //--- roll back all transactions and unlock the database
      DatabaseTransactionRollback(database);
      PrintFormat("%s: DatabaseExecute() failed with code ", __FUNCTION__, GetLastError());
      return(false);
     }
//--- all transactions have been performed successfully - record changes and unlock the database
   DatabaseTransactionCommit(database);
   return(true);
  }
//+------------------------------------------------------------------+
//| Creates the TRADES table                                         |
//+------------------------------------------------------------------+
bool CreateTableTrades(int database)
  {
//--- if the TRADES table already exists, delete it
   if(!DeleteTable(database, "TRADES"))
      return(false);
//--- check if the table exists
   if(!DatabaseTableExists(database, "TRADES"))
      //--- create the table
      if(!DatabaseExecute(database, "CREATE TABLE TRADES("
                          "TIME_IN     INT     NOT NULL,"
                          "HOUR_IN     INT     NOT NULL,"
                          "TICKET      INT     NOT NULL,"
                          "TYPE        INT     NOT NULL,"
                          "VOLUME      REAL,"
                          "SYMBOL      CHAR(10),"
                          "PRICE_IN    REAL,"
                          "TIME_OUT    INT     NOT NULL,"
                          "PRICE_OUT   REAL,"
                          "COMMISSION  REAL,"
                          "SWAP        REAL,"
                          "PROFIT      REAL);"))
        {
         Print("DB: create the TRADES table failed with code ", GetLastError());
         return(false);
        }
//--- the table has been successfully created
   return(true);
  }
//+------------------------------------------------------------------+

```

See also

[DatabasePrepare](/en/docs/database/databaseprepare), [DatabaseFinalize](/en/docs/database/databasefinalize)
