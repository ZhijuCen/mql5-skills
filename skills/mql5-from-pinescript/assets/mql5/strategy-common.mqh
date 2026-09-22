//+------------------------------------------------------------------+
//|                                       strategy-common.mqh         |
//|  Shared EA plumbing for Pine `strategy.*` ports                   |
//|  (skills/mql5-from-pinescript).                                   |
//|                                                                    |
//|  Execution model mirrors TradingView's broker emulator:            |
//|    - signals are evaluated on CLOSED bars only (backfill for        |
//|      warm-up state, then one evaluation per new bar)                |
//|    - orders are sent on the first tick of the NEXT bar (= next-bar- |
//|      open fill)                                                     |
//|    - SL/TP bracket is attached on the fill tick (brief naked window |
//|      on live, same-tick in tester; see port records)                |
//|    - stop triggers are intrabar (broker-side), like the emulator    |
//+------------------------------------------------------------------+
#ifndef STRATEGY_COMMON_MQH
#define STRATEGY_COMMON_MQH

#include <Trade\Trade.mqh>

//--- forward declarations (MQL5 requires declaration before use)
double ClampLots(double raw);
bool   IsNa(const double v);
color  BlendMarkerGray(void);

//+------------------------------------------------------------------+
//| One OHLCV bar of the backfill series                              |
//+------------------------------------------------------------------+
struct PineBar
  {
   datetime time;
   double   o;
   double   h;
   double   l;
   double   c;
   double   v;       // real volume if the broker provides it, else tick volume
  };

//+------------------------------------------------------------------+
//| Ascending closed-bar series.  Index count-1 = newest closed bar.   |
//| Pine `x[k]` (k bars ago) == Get(k); chronological i in the walks   |
//| uses At(i).                                                         |
//+------------------------------------------------------------------+
class CPineSeries
  {
private:
   PineBar         m_bars[];

public:
   void            Reset(void)                     { ArrayFree(m_bars); }
   int             Count(void) const               { return(ArraySize(m_bars)); }
   datetime        LastTime(void) const            { return(m_bars[ArraySize(m_bars) - 1].time); }
   PineBar         At(const int i) const            { return(m_bars[i]); }
   PineBar         Get(const int kAgo) const        { return(m_bars[ArraySize(m_bars) - 1 - kAgo]); }

   bool            Append(const PineBar &b)
     {
      int n = ArraySize(m_bars);
      if(n > 0 && b.time <= m_bars[n - 1].time)
         return(false);
      ArrayResize(m_bars, n + 1);
      m_bars[n] = b;
      return(true);
     }
  };

//+------------------------------------------------------------------+
//| Load all closed bars (cap: maxBars) into `out`, ASCENDING.         |
//| The caller appends them one by one and runs its per-bar compute in  |
//| that order - that is what makes var-state / recursive indicators    |
//| match Pine. Returns the count; 0 on failure.                        |
//+------------------------------------------------------------------+
int SeriesLoadClosed(PineBar &out[], const int maxBars)
  {
   ArrayFree(out);
   int total = iBars(_Symbol, _Period);
   int want  = MathMin(total - 1, maxBars);        // exclude the forming bar
   if(want < 100)
      return(0);
   MqlRates rt[];
   ArraySetAsSeries(rt, true);                     // rt[0] = newest bar
   int got = CopyRates(_Symbol, _Period, 1, want, rt); // start at 1: skip forming
   if(got <= 0)
      return(0);
   ArrayResize(out, got);
   for(int i = got - 1, j = 0; i >= 0; i--, j++)    // ascending order
     {
      out[j].time = rt[i].time;
      out[j].o = rt[i].open;
      out[j].h = rt[i].high;
      out[j].l = rt[i].low;
      out[j].c = rt[i].close;
      out[j].v = (rt[i].real_volume > 0 ? (double)rt[i].real_volume : (double)rt[i].tick_volume);
     }
   return(got);
  }

//+------------------------------------------------------------------+
//| Append the just-closed bar (series index 1); true if it is NEW     |
//+------------------------------------------------------------------+
bool SeriesAppendClosed(CPineSeries &s)
  {
   MqlRates rt[];
   ArraySetAsSeries(rt, true);
   if(CopyRates(_Symbol, _Period, 1, 1, rt) != 1)
      return(false);
   if(s.Count() > 0 && rt[0].time <= s.LastTime())
      return(false);
   PineBar b;
   b.time = rt[0].time;
   b.o = rt[0].open;
   b.h = rt[0].high;
   b.l = rt[0].low;
   b.c = rt[0].close;
   b.v = (rt[0].real_volume > 0 ? (double)rt[0].real_volume : (double)rt[0].tick_volume);
   s.Append(b);
   return(true);
  }

//+------------------------------------------------------------------+
//| Pine-faithful smoothing states (seeded exactly once per stream):   |
//|   CEma  - ta.ema  (SMA seed, then k = 2/(n+1))                     |
//|   CRma  - ta.rma  (SMA seed, then k = 1/n  - Wilder)               |
//|   CSma  - ta.sma  (rolling window)                                 |
//| EMPTY_VALUE until the seed window is full (= Pine `na`).           |
//+------------------------------------------------------------------+
class CEma
  {
private:
   int             m_len;
   int             m_seen;
   double          m_val;
   double          m_sum;

public:
                     CEma(void) : m_len(0), m_seen(0), m_val(EMPTY_VALUE), m_sum(0.0) {}
   void              Init(const int len)   { m_len = len; m_seen = 0; m_val = EMPTY_VALUE; m_sum = 0.0; }
   bool              Defined(void) const  { return(m_val != EMPTY_VALUE); }
   double            Value(void) const    { return(m_val); }

   void              Update(const double x)
     {
      if(m_len < 1) { m_val = x; m_seen = 1; return; }
      if(m_seen < m_len)
        {
         m_sum += x;
         m_seen++;
         m_val = (m_seen == m_len) ? m_sum / m_len : EMPTY_VALUE;
         return;
        }
      m_val = m_val + (2.0 / (m_len + 1)) * (x - m_val);
     }
  };

class CRma
  {
private:
   int             m_len;
   int             m_seen;
   double          m_val;
   double          m_sum;

public:
                     CRma(void) : m_len(0), m_seen(0), m_val(EMPTY_VALUE), m_sum(0.0) {}
   void              Init(const int len)   { m_len = len; m_seen = 0; m_val = EMPTY_VALUE; m_sum = 0.0; }
   bool              Defined(void) const  { return(m_val != EMPTY_VALUE); }
   double            Value(void) const    { return(m_val); }

   void              Update(const double x)
     {
      if(m_len < 1) { m_val = x; m_seen = 1; return; }
      if(m_seen < m_len)
        {
         m_sum += x;
         m_seen++;
         m_val = (m_seen == m_len) ? m_sum / m_len : EMPTY_VALUE;
         return;
        }
      m_val = m_val + (x - m_val) / m_len;
     }
  };

class CSma
  {
private:
   int             m_len;
   double          m_buf[];

public:
                     CSma(void) : m_len(0) {}
   void              Init(const int len)   { m_len = len; ArrayResize(m_buf, 0); }
   bool              Defined(void) const  { return(ArraySize(m_buf) >= m_len && m_len > 0); }
   double            Value(void) const
     {
      if(!Defined())
         return(EMPTY_VALUE);
      double sum = 0.0;
      for(int i = 0; i < m_len; i++)
         sum += m_buf[i];
      return(sum / m_len);
     }

   void              Update(const double x)
     {
      int n = ArraySize(m_buf);
      if(n < m_len)
        {
         ArrayResize(m_buf, n + 1);
         m_buf[n] = x;
         return;
        }
      for(int i = n - 1; i > 0; i--)
         m_buf[i] = m_buf[i - 1];
      m_buf[0] = x;                                // newest at [0]
     }
  };

//+------------------------------------------------------------------+
//| Manual ADX (Pine ta.dmi(len,len): RMA-smoothed TR/+DM/-DM -> DX    |
//| -> RMA). Call once per closed bar with that bar + previous bar.    |
//+------------------------------------------------------------------+
class CAdxState
  {
private:
   CRma            m_rTr;
   CRma            m_rPd;
   CRma            m_rNd;
   CRma            m_rDx;
   bool            m_hasPrev;
   double          m_prevH;
   double          m_prevL;

public:
                     CAdxState(void) : m_hasPrev(false), m_prevH(0.0), m_prevL(0.0) {}
   void              Init(const int len)
     {
      m_rTr.Init(len);
      m_rPd.Init(len);
      m_rNd.Init(len);
      m_rDx.Init(len);
      m_hasPrev = false;
     }

   double            Update(const double h, const double l, const double tr)
     {
      if(!m_hasPrev)
        {
         m_prevH = h;
         m_prevL = l;
         m_hasPrev = true;
         m_rTr.Update(tr);
         m_rPd.Update(0.0);
         m_rNd.Update(0.0);
         return(EMPTY_VALUE);
        }
      double up = h - m_prevH;
      double dn = m_prevL - l;
      double pdm = (up > dn && up > 0) ? up : 0.0;
      double ndm = (dn > up && dn > 0) ? dn : 0.0;
      m_prevH = h;
      m_prevL = l;
      m_rTr.Update(tr);
      m_rPd.Update(pdm);
      m_rNd.Update(ndm);
      double sTr = m_rTr.Value();
      if(!m_rTr.Defined() || !m_rPd.Defined() || !m_rNd.Defined() || sTr <= 0.0)
         return(EMPTY_VALUE);
      double pdi  = 100.0 * m_rPd.Value() / sTr;
      double ndi  = 100.0 * m_rNd.Value() / sTr;
      double sum  = pdi + ndi;
      double dx   = (sum > 0.0) ? 100.0 * MathAbs(pdi - ndi) / sum : 0.0;
      m_rDx.Update(dx);
      return(m_rDx.Value());
     }
  };

//+------------------------------------------------------------------+
//| True range of bar i given bar i-1's close (Pine ta.tr / ta.atr)    |
//+------------------------------------------------------------------+
double TrueRangeAt(const PineBar &b, const double prevClose)
  {
   return(MathMax(b.h - b.l, MathMax(MathAbs(b.h - prevClose), MathAbs(b.l - prevClose))));
  }

//+------------------------------------------------------------------+
//| Money-risk position sizing (Pine "units = risk / stopDist"):       |
//| lots so a stop-out loses exactly riskPercent of equity.            |
//| Returns 0 when the risk cannot buy at least the volume minimum     |
//| (skill rule: never round a sub-minimum risk up - skip the trade).  |
//+------------------------------------------------------------------+
double LotsFromRiskPct(const double riskPct, const double stopDistPrice)
  {
   if(stopDistPrice <= 0.0)
      return(0.0);
   double tickSize = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
   double tickVal  = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
   if(tickSize <= 0.0 || tickVal <= 0.0)
      return(0.0);
   double riskMoney = AccountInfoDouble(ACCOUNT_EQUITY) * riskPct / 100.0;
   double lots = riskMoney * tickSize / (stopDistPrice * tickVal);
   return(ClampLots(lots));
  }

//+------------------------------------------------------------------+
//| Notional sizing: lots worth `pct`% of equity at `price`            |
//| (Pine default_qty_type = percent_of_equity / "Equity %" mode).     |
//+------------------------------------------------------------------+
double LotsFromEquityPct(const double pct, const double price)
  {
   double contract = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_CONTRACT_SIZE);
   if(price <= 0.0 || contract <= 0.0)
      return(0.0);
   double notional = AccountInfoDouble(ACCOUNT_EQUITY) * pct / 100.0;
   return(ClampLots(notional / (price * contract)));
  }

//+------------------------------------------------------------------+
//| Clamp to broker volume constraints (min/max/step); 0 if below min  |
//+------------------------------------------------------------------+
double ClampLots(double raw)
  {
   if(raw <= 0.0)
      return(0.0);
   double vmin = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   double vmax = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
   double vstep = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
   if(vstep > 0.0)
      raw = MathFloor(raw / vstep) * vstep;        // floor to step (no up-rounding)
   if(vmin > 0.0 && raw < vmin - 1e-12)
      return(0.0);                                 // sub-minimum -> skip (skill rule)
   if(vmax > 0.0 && raw > vmax)
      raw = vmax;
   if(vstep > 0.0)
      raw = MathFloor(raw / vstep) * vstep;        // re-floor after max clamp
   return(raw);
  }

//+------------------------------------------------------------------+
//| Queued entry state: filled when the broker session reopens (10018) |
//+------------------------------------------------------------------+
struct SPendingEntry
  {
   bool   active;
   bool   announced;
   bool   isBuy;
   double lots;
   double slAbs;
   double tpAbs;
   double slDist;
   double tpDist;
   long   magic;
   string cmt;
  };
SPendingEntry g_pending;

void ResetPending(void)
  {
   g_pending.active    = false;
   g_pending.announced = false;
  }

bool EntryPending(void)
  {
   return(g_pending.active);
  }

//+------------------------------------------------------------------+
//| Market entry + bracket.  Anchor semantics (Pine variants):         |
//|   slAbs/tpAbs  - absolute levels fixed at the SIGNAL bar (0004)     |
//|   slDist/tpDist - distances from the FILL price (0005/0006;        |
//|                   EMPTY slAbs => derive from dist after fill)      |
//| Behaviour: closes any opposite position of ours first (flip),      |
//| refuses same-direction adds (pyramiding = 0), opens WITHOUT stops, |
//| then attaches the bracket on the fill tick; gap-through the stop at |
//| fill => immediate close (emulator-style stop firing).              |
//+------------------------------------------------------------------+
uint EnterWithBracket(const bool isBuy, const double lots, const double slAbs,
                      const double tpAbs, const double slDist, const double tpDist,
                      const long magic, const string cmt)
  {
   if(lots <= 0.0)
      return(TRADE_RETCODE_INVALID_VOLUME);
   CTrade trade;
   trade.SetExpertMagicNumber(magic);
   trade.SetTypeFillingBySymbol(_Symbol);
   trade.SetDeviationInPoints(10);
   //--- single-position model: close ours first, refuse same-dir adds
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || PositionGetString(POSITION_SYMBOL) != _Symbol)
         continue;
      if(PositionGetInteger(POSITION_MAGIC) != magic)
         continue;
      bool curBuy = (PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY);
      if(curBuy == isBuy)
         return(TRADE_RETCODE_DONE);              // already in - no pyramiding
      if(!trade.PositionClose(ticket))
         PrintFormat("%s: flip close failed retcode=%d", cmt, trade.ResultRetcode());
     }
   double price = isBuy ? SymbolInfoDouble(_Symbol, SYMBOL_ASK)
                        : SymbolInfoDouble(_Symbol, SYMBOL_BID);
   bool sent = (isBuy ? trade.Buy(lots, _Symbol, price, 0.0, 0.0, cmt)
                      : trade.Sell(lots, _Symbol, price, 0.0, 0.0, cmt));
   if(!sent)
     {
      uint rc = trade.ResultRetcode();
      if(rc == TRADE_RETCODE_MARKET_CLOSED)
        {
         bool first = !g_pending.active;      // announce only the first time
         g_pending.active = true;
         g_pending.isBuy  = isBuy;
         g_pending.lots   = lots;
         g_pending.slAbs  = slAbs;
         g_pending.tpAbs  = tpAbs;
         g_pending.slDist = slDist;
         g_pending.tpDist = tpDist;
         g_pending.magic  = magic;
         g_pending.cmt    = cmt;
         if(first && !g_pending.announced)
           {
            g_pending.announced = true;
            PrintFormat("%s: market closed - entry queued for retry", cmt);
           }
         return(rc);
        }
      PrintFormat("%s: entry failed retcode=%d", cmt, rc);
      return(rc);
     }
   if(g_pending.active)                            // filled (also on retry)
     {
      g_pending.active    = false;
      g_pending.announced = false;
     }
   //--- bracket on the fill tick
   if(!PositionSelect(_Symbol) || PositionGetInteger(POSITION_MAGIC) != magic)
      return(trade.ResultRetcode());
   double fill   = PositionGetDouble(POSITION_PRICE_OPEN);
   int    digits = (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS);
   double stopPts = (double)SymbolInfoInteger(_Symbol, SYMBOL_TRADE_STOPS_LEVEL) * _Point;
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   double sl = slAbs;
   double tp = tpAbs;
   if(IsNa(sl) && slDist > 0.0)
      sl = isBuy ? fill - slDist : fill + slDist;
   if(IsNa(tp) && tpDist > 0.0)
      tp = isBuy ? fill + tpDist : fill - tpDist;
   //--- gap-through: fill already beyond the stop -> fire the stop now
   if(!IsNa(sl))
     {
      if(isBuy && bid <= sl)
        {
         trade.PositionClose(_Symbol);
         PrintFormat("%s: gap through SL at fill - closed immediately", cmt);
         return(TRADE_RETCODE_DONE);
        }
      if(!isBuy && ask >= sl)
        {
         trade.PositionClose(_Symbol);
         PrintFormat("%s: gap through SL at fill - closed immediately", cmt);
         return(TRADE_RETCODE_DONE);
        }
     }
   //--- clamp to the broker minimum stop distance (skill rule 16)
   if(!IsNa(sl) && stopPts > 0.0)
     {
      if(isBuy && sl > bid - stopPts)
         sl = NormalizeDouble(bid - stopPts - _Point, digits);
      if(!isBuy && sl < ask + stopPts)
         sl = NormalizeDouble(ask + stopPts + _Point, digits);
     }
   if(!IsNa(tp) && stopPts > 0.0)
     {
      if(isBuy && tp < ask + stopPts)
         tp = NormalizeDouble(ask + stopPts + _Point, digits);
      if(!isBuy && tp > bid - stopPts)
         tp = NormalizeDouble(bid - stopPts - _Point, digits);
     }
   double curSL = IsNa(sl) ? 0.0 : NormalizeDouble(sl, digits);
   double curTP = IsNa(tp) ? 0.0 : NormalizeDouble(tp, digits);
   if(!trade.PositionModify(_Symbol, curSL, curTP))
      PrintFormat("%s: PositionModify failed retcode=%d (sl=%.5f tp=%.5f)",
                  cmt, trade.ResultRetcode(), curSL, curTP);
   return(TRADE_RETCODE_DONE);
  }

//+------------------------------------------------------------------+
void CloseOursByMagic(const long magic, const string cmt)
  {
   CTrade trade;
   trade.SetExpertMagicNumber(magic);
   trade.SetTypeFillingBySymbol(_Symbol);
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || PositionGetString(POSITION_SYMBOL) != _Symbol)
         continue;
      if(PositionGetInteger(POSITION_MAGIC) != magic)
         continue;
      if(!trade.PositionClose(ticket))
         PrintFormat("%s: close failed retcode=%d", cmt, trade.ResultRetcode());
     }
  }

//+------------------------------------------------------------------+
bool HaveOursByMagic(const long magic, bool &isBuy)
  {
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || PositionGetString(POSITION_SYMBOL) != _Symbol)
         continue;
      if(PositionGetInteger(POSITION_MAGIC) != magic)
         continue;
      isBuy = (PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY);
      return(true);
     }
   return(false);
  }

//+------------------------------------------------------------------+
//| Retry the queued entry (throttled to once per ~60 ticks).           |
//| TV's emulator fills at bar open regardless of sessions; on a        |
//| session-bound broker retrying until the market reopens is the       |
//| closest honest approximation (port records call this out).          |
//+------------------------------------------------------------------+
void RetryPendingEntry(void)
  {
   if(!g_pending.active)
      return;
   //--- attempt on EVERY call: in open-prices mode the EA sees only one
   //--- tick per bar, so any tick-gating would delay fills by many bars.
   //--- Repeated failures are silent (announced once) and cheap.
   EnterWithBracket(g_pending.isBuy, g_pending.lots, g_pending.slAbs, g_pending.tpAbs,
                    g_pending.slDist, g_pending.tpDist, g_pending.magic, g_pending.cmt);
  }

//+------------------------------------------------------------------+
bool IsNa(const double v)
  {
   return(v == EMPTY_VALUE || v != v || v >= EMPTY_VALUE - 0.5);
  }

//+------------------------------------------------------------------+
//| Entry marker arrow (Wingdings241/242 verified codes)               |
//+------------------------------------------------------------------+
void MarkerArrow(const string prefix, const int seq, const bool isEntryLong,
                 const datetime t, const double price, const color clr)
  {
   string name = prefix + "m" + IntegerToString(seq);
   if(ObjectFind(0, name) >= 0)
      return;
   if(!ObjectCreate(0, name, OBJ_ARROW, 0, t, price))
      return;
   ObjectSetInteger(0, name, OBJPROP_ARROWCODE, isEntryLong ? 241 : 242);
   ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
   ObjectSetInteger(0, name, OBJPROP_ANCHOR, isEntryLong ? ANCHOR_TOP : ANCHOR_BOTTOM);
  }

//+------------------------------------------------------------------+
//| Exit marker (circle - Pine uses an X glyph; X codes unverified)    |
//+------------------------------------------------------------------+
void MarkerCircle(const string prefix, const int seq, const bool wasLong,
                  const datetime t, const double price)
  {
   string name = prefix + "x" + IntegerToString(seq);
   if(ObjectFind(0, name) >= 0)
      return;
   if(!ObjectCreate(0, name, OBJ_ARROW, 0, t, price))
      return;
   ObjectSetInteger(0, name, OBJPROP_ARROWCODE, 159);
   ObjectSetInteger(0, name, OBJPROP_COLOR, BlendMarkerGray());
   ObjectSetInteger(0, name, OBJPROP_ANCHOR, wasLong ? ANCHOR_BOTTOM : ANCHOR_TOP);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
   ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
  }

color BlendMarkerGray(void)
  {
   return((color)0x8C8C8C);                       // Pine gray,20% - flat gray marker
  }

#endif // STRATEGY_COMMON_MQH
