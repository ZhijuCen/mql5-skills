//+------------------------------------------------------------------+
//| EA skeleton — minimal Expert Advisor scaffold for MQL5.          |
//| CTrade + risk-based SL/TP + magic-number isolation.              |
//| Companion doc: skills/mql5/SKILL.md §2 / §9.                    |
//+------------------------------------------------------------------+
#property copyright "Your Name"
#property link      ""
#property version   "1.00"

#include <Trade\Trade.mqh>

input double RiskPercent   = 1.0;    // Risk % per trade
input int    Slippage      = 10;     // Max slippage in points
input int    MagicNumber   = 12345;  // EA magic number

#define EA_MAGIC MagicNumber

CTrade trade;
bool   IsHedging;
datetime lastBarTime = 0;

#include "../templates/risk-helpers.mqh"

//+------------------------------------------------------------------+
//| CTrade setup — call once in OnInit().                            |
//+------------------------------------------------------------------+
void SetupTrade() {
    trade.SetExpertMagicNumber(EA_MAGIC);
    trade.SetMarginMode();
    trade.SetTypeFillingBySymbol(Symbol());
    trade.SetDeviationInPoints(Slippage);
}

//+------------------------------------------------------------------+
//| Account margin mode detection: hedging vs netting.               |
//+------------------------------------------------------------------+
bool DetectHedging() {
    return ((ENUM_ACCOUNT_MARGIN_MODE)
        AccountInfoInteger(ACCOUNT_MARGIN_MODE)
        == ACCOUNT_MARGIN_MODE_RETAIL_HEDGING);
}

//+------------------------------------------------------------------+
//| New-bar detector — call first in OnTick() to skip intra-bar      |
//| processing unless you specifically want tick-level decisions.    |
//+------------------------------------------------------------------+
bool IsNewBar() {
    datetime barTime = iTime(_Symbol, _Period, 0);
    if (barTime == lastBarTime) return false;
    lastBarTime = barTime;
    return true;
}

//+------------------------------------------------------------------+
int OnInit() {
    IsHedging = DetectHedging();
    SetupTrade();
    return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
void OnDeinit(const int reason) {
    // Cleanup (release indicator handles, timers)
}

//+------------------------------------------------------------------+
void OnTick() {
    if (!IsNewBar()) return;

    // Example: buy with 1% risk, 500-point SL.
    double bid   = SymbolInfoDouble(_Symbol, SYMBOL_BID);
    double slPts = 500;
    double sl    = CalcSLFromPoints(_Symbol, bid, slPts, /*isBuy=*/true);
    double lots  = CalcLotsFromSL(_Symbol,
        AccountInfoDouble(ACCOUNT_BALANCE), RiskPercent, bid, sl);

    // Verify loss matches risk budget — required before opening.
    double profit;
    OrderCalcProfit(ORDER_TYPE_BUY, _Symbol, lots, bid, sl, profit);
    PrintFormat("SL=%.5f lots=%.2f expected_loss=%.2f",
                sl, lots, profit);

    // trade.Buy(lots, _Symbol, 0, sl, 0, "EA Signal");
}

//+------------------------------------------------------------------+
double OnTester() {
    // Custom optimization criterion — gate on minimum trade count.
    if (TesterStatistics(STAT_TRADES) < 30) return 0;
    return TesterStatistics(STAT_PROFIT_FACTOR);
}

//+------------------------------------------------------------------+
//| Iterate open positions on this symbol and magic (hedging).       |
//+------------------------------------------------------------------+
int CountMyPositions() {
    int n = 0;
    uint total = PositionsTotal();
    for (uint i = 0; i < total; i++) {
        if (PositionGetSymbol(i) == _Symbol &&
            PositionGetInteger(POSITION_MAGIC) == EA_MAGIC) n++;
    }
    return n;
}

//+------------------------------------------------------------------+
//| Direction A: stop-loss distance in points → SL price.             |
//+------------------------------------------------------------------+
double CalcSLFromPoints(string symbol, double openPrice,
                        int slPoints, bool isBuy) {
    double point       = SymbolInfoDouble(symbol, SYMBOL_POINT);
    double slDistPrice = slPoints * point;
    int    digits      = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
    return isBuy
        ? NormalizeDouble(openPrice - slDistPrice, digits)
        : NormalizeDouble(openPrice + slDistPrice, digits);
}

//+------------------------------------------------------------------+
//| Open a position with retcode check. NEVER skip the retcode test.  |
//+------------------------------------------------------------------+
bool OpenWithCheck(CTrade &t, const string symbol,
                   const ENUM_ORDER_TYPE type, double lots,
                   double price, double sl, double tp,
                   const string comment) {
    bool ok = t.PositionOpen(symbol, type, lots, price, sl, tp, comment);
    if (!ok || t.ResultRetcode() != TRADE_RETCODE_DONE) {
        PrintFormat("Trade failed: retcode=%u (%s)",
                    t.ResultRetcode(), t.ResultRetcodeDescription());
        return false;
    }
    return true;
}
//+------------------------------------------------------------------+
