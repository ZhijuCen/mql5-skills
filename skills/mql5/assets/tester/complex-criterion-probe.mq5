//+------------------------------------------------------------------+
//| complex-criterion-probe.mq5                                      |
//|                                                                  |
//| Probe used to reverse-engineer MT5's "Complex Criterion"         |
//| (OptimizationCriterion=7) and to read its exact value.           |
//|                                                                  |
//| Trades a parameterised schedule and, in OnTester(), appends one  |
//| CSV row per pass containing ALL ENUM_STATISTICS values plus      |
//| STAT_COMPLEX_CRITERION at full double precision.                 |
//|                                                                  |
//| Usage                                                            |
//|   1. Copy to MQL5/Experts/, compile (space-free path!).          |
//|   2. Single test  -> one row (exact criterion for that pass).    |
//|      Grid / genetic -> one row per pass (calibration set).       |
//|   3. Rows land in  <instance>/Tester/Agent-*/MQL5/Files/         |
//|      ccprobe.csv   (one file per local agent; concatenate them). |
//|                                                                  |
//| Key trick for isolating a statistic: vary ONLY InpLot. That      |
//| scales profit / EP / DD / DD% and leaves T, PF, RF, SR, win rate |
//| and the trade sequence bit-identical, giving a clean 1-D cut.    |
//|                                                                  |
//| See references/quick-ref-complex-criterion.md for the resulting  |
//| formula and for the calibration procedure.                       |
//+------------------------------------------------------------------+
#property version   "1.10"
#property description "Dump all TesterStatistics + complex criterion (reverse-engineering probe)"

input int    InpEntryPeriod = 8;      // bars between entries
input double InpLot         = 0.10;   // lot
input int    InpTPPoints    = 600;    // take profit (points, 0 = off)
input int    InpSLPoints    = 600;    // stop loss (points, 0 = off)
input int    InpHoldBars    = 12;     // close after N bars
input int    InpDirection   = 0;      // 0 = always buy, 1 = always sell, 2 = alternate

long     m_barCount = 0;
datetime m_lastBar  = 0;
ulong    m_ticket   = 0;
int      m_barsHeld = 0;
int      m_tradeNo  = 0;

//+------------------------------------------------------------------+
int OnInit()
  {
   m_barCount = 0;
   m_lastBar  = 0;
   m_ticket   = 0;
   m_barsHeld = 0;
   m_tradeNo  = 0;
   return(INIT_SUCCEEDED);
  }

//+------------------------------------------------------------------+
//| Symbols reject DEAL requests whose filling mode is unsupported.  |
//+------------------------------------------------------------------+
ENUM_ORDER_TYPE_FILLING FillMode()
  {
   long f = SymbolInfoInteger(_Symbol, SYMBOL_FILLING_MODE);
   if((f & SYMBOL_FILLING_IOC) != 0) return(ORDER_FILLING_IOC);
   if((f & SYMBOL_FILLING_FOK) != 0) return(ORDER_FILLING_FOK);
   return(ORDER_FILLING_RETURN);
  }

//+------------------------------------------------------------------+
bool OpenTrade(bool isBuy)
  {
   double pt    = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   double price = isBuy ? SymbolInfoDouble(_Symbol, SYMBOL_ASK)
                        : SymbolInfoDouble(_Symbol, SYMBOL_BID);
   MqlTradeRequest req;
   MqlTradeResult  res;
   ZeroMemory(req);
   ZeroMemory(res);
   req.action       = TRADE_ACTION_DEAL;
   req.symbol       = _Symbol;
   req.volume       = InpLot;
   req.type         = isBuy ? ORDER_TYPE_BUY : ORDER_TYPE_SELL;
   req.price        = price;
   req.sl           = (InpSLPoints > 0) ? (isBuy ? price - InpSLPoints * pt
                                                 : price + InpSLPoints * pt) : 0.0;
   req.tp           = (InpTPPoints > 0) ? (isBuy ? price + InpTPPoints * pt
                                                 : price - InpTPPoints * pt) : 0.0;
   req.deviation    = 50;
   req.magic        = 777001;
   req.type_filling = FillMode();
   if(!OrderSend(req, res))
      return(false);
   m_ticket = res.order;
   return(true);
  }

//+------------------------------------------------------------------+
void CloseTrade()
  {
   if(m_ticket == 0)
      return;
   if(!PositionSelectByTicket(m_ticket))
     {
      m_ticket   = 0;
      m_barsHeld = 0;
      return;
     }
   MqlTradeRequest req;
   MqlTradeResult  res;
   ZeroMemory(req);
   ZeroMemory(res);
   req.action       = TRADE_ACTION_DEAL;
   req.position     = m_ticket;
   req.symbol       = _Symbol;
   req.volume       = PositionGetDouble(POSITION_VOLUME);
   req.type         = (PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY)
                      ? ORDER_TYPE_SELL : ORDER_TYPE_BUY;
   req.price        = (req.type == ORDER_TYPE_SELL)
                      ? SymbolInfoDouble(_Symbol, SYMBOL_BID)
                      : SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   req.deviation    = 50;
   req.magic        = 777001;
   req.type_filling = FillMode();
   if(!OrderSend(req, res))
      PrintFormat("CCPROBE close failed retcode=%d", res.retcode);
   m_ticket   = 0;
   m_barsHeld = 0;
  }

//+------------------------------------------------------------------+
void OnTick()
  {
   datetime bt     = (datetime)SeriesInfoInteger(_Symbol, _Period, SERIES_LASTBAR_DATE);
   bool     newBar = (bt != m_lastBar);
   if(newBar)
     {
      m_lastBar = bt;
      m_barCount++;
     }

   if(m_ticket != 0)
     {
      if(!PositionSelectByTicket(m_ticket))
        {
         m_ticket   = 0;
         m_barsHeld = 0;
        }
      else
        {
         m_barsHeld++;
         if(m_barsHeld >= InpHoldBars)
            CloseTrade();
         return;
        }
     }
   if(!newBar)
      return;
   if(m_barCount % InpEntryPeriod != 0)
      return;

   bool isBuy = (InpDirection == 0) ? true
              : (InpDirection == 1 ? false : ((m_tradeNo % 2) == 0));
   if(OpenTrade(isBuy))
      m_tradeNo++;
  }

//+------------------------------------------------------------------+
//| One CSV row per pass. Print() is suppressed during optimization, |
//| so the file is the only reliable channel.                        |
//+------------------------------------------------------------------+
double OnTester()
  {
   double cc = TesterStatistics(STAT_COMPLEX_CRITERION);

   int h = FileOpen("ccprobe.csv", FILE_READ | FILE_WRITE | FILE_CSV | FILE_ANSI, ';');
   if(h != INVALID_HANDLE)
     {
      FileSeek(h, 0, SEEK_END);
      if(FileTell(h) == 0)
         FileWrite(h, "ep_period", "lot", "tp", "sl", "hold", "dir",
                   "cc", "trades", "deals", "profit", "expected_payoff",
                   "profit_factor", "recovery_factor", "sharpe",
                   "bal_dd", "bal_dd_pct", "eq_dd", "eq_dd_pct",
                   "gross_profit", "gross_loss", "win_trades", "loss_trades",
                   "max_conwins", "max_conlosses", "balance_min",
                   "max_profit_trade", "max_loss_trade", "bal_dd_rel",
                   "eq_dd_rel", "custom");
      FileWrite(h,
                IntegerToString(InpEntryPeriod), DoubleToString(InpLot, 4),
                IntegerToString(InpTPPoints), IntegerToString(InpSLPoints),
                IntegerToString(InpHoldBars), IntegerToString(InpDirection),
                DoubleToString(cc, 10),
                IntegerToString((int)TesterStatistics(STAT_TRADES)),
                IntegerToString((int)TesterStatistics(STAT_DEALS)),
                DoubleToString(TesterStatistics(STAT_PROFIT), 2),
                DoubleToString(TesterStatistics(STAT_EXPECTED_PAYOFF), 8),
                DoubleToString(TesterStatistics(STAT_PROFIT_FACTOR), 8),
                DoubleToString(TesterStatistics(STAT_RECOVERY_FACTOR), 8),
                DoubleToString(TesterStatistics(STAT_SHARPE_RATIO), 8),
                DoubleToString(TesterStatistics(STAT_BALANCE_DD), 6),
                DoubleToString(TesterStatistics(STAT_BALANCEDD_PERCENT), 6),
                DoubleToString(TesterStatistics(STAT_EQUITY_DD), 6),
                DoubleToString(TesterStatistics(STAT_EQUITYDD_PERCENT), 6),
                DoubleToString(TesterStatistics(STAT_GROSS_PROFIT), 2),
                DoubleToString(TesterStatistics(STAT_GROSS_LOSS), 2),
                IntegerToString((int)TesterStatistics(STAT_PROFIT_TRADES)),
                IntegerToString((int)TesterStatistics(STAT_LOSS_TRADES)),
                DoubleToString(TesterStatistics(STAT_MAX_CONWINS), 4),
                DoubleToString(TesterStatistics(STAT_MAX_CONLOSSES), 4),
                DoubleToString(TesterStatistics(STAT_BALANCEMIN), 4),
                DoubleToString(TesterStatistics(STAT_MAX_PROFITTRADE), 4),
                DoubleToString(TesterStatistics(STAT_MAX_LOSSTRADE), 4),
                DoubleToString(TesterStatistics(STAT_BALANCE_DD_RELATIVE), 6),
                DoubleToString(TesterStatistics(STAT_EQUITY_DD_RELATIVE), 6),
                DoubleToString(TesterStatistics(STAT_CUSTOM_ONTESTER), 10));
      FileClose(h);
     }
   else
      PrintFormat("CCPROBE FileOpen failed err=%d", GetLastError());

   return(0.0);
  }
//+------------------------------------------------------------------+
