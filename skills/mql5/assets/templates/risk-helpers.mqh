//+------------------------------------------------------------------+
//| risk-helpers.mqh — SL/lot sizing primitives.                     |
//| Companion doc: skills/mql5/SKILL.md §5 (Risk Management).         |
//|                                                                   |
//| Required when including from .mq5 source:                         |
//|     #include "../templates/risk-helpers.mqh"                     |
//| (path is relative to the EA's location under MQL5/Experts/...).   |
//+------------------------------------------------------------------+
#ifndef __RISK_HELPERS_MQH__
#define __RISK_HELPERS_MQH__

//+------------------------------------------------------------------+
//| PointValue: profit-currency per 1-point move for 1 lot.           |
//|                                                                   |
//| Foundation for ALL risk calculations. Note:                       |
//|   SYMBOL_TRADE_TICK_VALUE  = profit per *tick* (broker step)      |
//|   PointValue               = profit per *point* (smallest unit)   |
//|   For most Forex: TickSize == Point, so they coincide;            |
//|   for futures/metals they can differ.                             |
//+------------------------------------------------------------------+
double PointValue(string symbol) {
    double point    = SymbolInfoDouble(symbol, SYMBOL_POINT);
    double contract = SymbolInfoDouble(symbol, SYMBOL_TRADE_CONTRACT_SIZE);
    ENUM_SYMBOL_CALC_MODE mode =
        (ENUM_SYMBOL_CALC_MODE)SymbolInfoInteger(symbol, SYMBOL_TRADE_CALC_MODE);

    switch (mode) {
        case SYMBOL_CALC_MODE_FUTURES:
        case SYMBOL_CALC_MODE_EXCH_FUTURES:
        case SYMBOL_CALC_MODE_EXCH_FUTURES_FORTS:
            return point * SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE)
                                / SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE);

        // SYMBOL_CALC_MODE_FOREX / _NO_LEVERAGE / CFD / CFDINDEX /
        // CFDLEVERAGE / EXCH_STOCKS / EXCH_STOCKS_MOEX all share the
        // point * contract formula.
        case SYMBOL_CALC_MODE_FOREX:
        case SYMBOL_CALC_MODE_FOREX_NO_LEVERAGE:
        case SYMBOL_CALC_MODE_CFD:
        case SYMBOL_CALC_MODE_CFDINDEX:
        case SYMBOL_CALC_MODE_CFDLEVERAGE:
        case SYMBOL_CALC_MODE_EXCH_STOCKS:
        case SYMBOL_CALC_MODE_EXCH_STOCKS_MOEX:
        default:
            return point * contract;
    }
}

//+------------------------------------------------------------------+
//| FindFXRate: locate a Forex pair for currency conversion.          |
//|                                                                   |
//| Returns +1 if `result` is from/to, -1 if to/from, 0 if not found. |
//| Used when SYMBOL_CURRENCY_PROFIT != ACCOUNT_CURRENCY              |
//| (e.g. USDJPY: profit=JPY, account=USD).                           |
//+------------------------------------------------------------------+
int FindFXRate(string from, string to, string &result) {
    for (int i = 0; i < SymbolsTotal(true); i++) {
        string sym = SymbolName(i, true);
        ENUM_SYMBOL_CALC_MODE m =
            (ENUM_SYMBOL_CALC_MODE)SymbolInfoInteger(sym, SYMBOL_TRADE_CALC_MODE);
        if (m != SYMBOL_CALC_MODE_FOREX &&
            m != SYMBOL_CALC_MODE_FOREX_NO_LEVERAGE) continue;
        string base   = SymbolInfoString(sym, SYMBOL_CURRENCY_BASE);
        string profit = SymbolInfoString(sym, SYMBOL_CURRENCY_PROFIT);
        if (base == from && profit == to) { result = sym; return +1; }
        if (base == to   && profit == from) { result = sym; return -1; }
    }
    return 0;
}

//+------------------------------------------------------------------+
//| CalcSLFromRisk: risk% + lots → SL price (Direction B).            |
//|                                                                   |
//| Given account balance, risk %, and FIXED lot size, compute where  |
//| the stop-loss must be placed. When profit_currency !=             |
//| account_currency, convert the risk amount via a live FX rate.     |
//+------------------------------------------------------------------+
double CalcSLFromRisk(string symbol, double balance, double riskPct,
                      double lots, double openPrice, bool isBuy) {
    double pv = PointValue(symbol);
    if (pv == 0 || lots == 0) return 0;

    double riskAmount = balance * riskPct / 100.0;

    string profCy = SymbolInfoString(symbol, SYMBOL_CURRENCY_PROFIT);
    string accCy  = AccountInfoString(ACCOUNT_CURRENCY);
    if (profCy != accCy) {
        string rateSym = "";
        int dir = FindFXRate(accCy, profCy, rateSym);
        if (dir == 0) { Print("Cannot convert ", profCy, "→", accCy); return 0; }
        MqlTick tick;
        SymbolInfoTick(rateSym, tick);
        double rate = (dir > 0) ? tick.bid : 1.0 / tick.ask;
        riskAmount *= rate;  // riskAmount now in profit currency
    }

    double points  = riskAmount / (pv * lots);
    double slPrice = points * SymbolInfoDouble(symbol, SYMBOL_POINT);
    int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
    return isBuy
        ? NormalizeDouble(openPrice - slPrice, digits)
        : NormalizeDouble(openPrice + slPrice, digits);
}

//+------------------------------------------------------------------+
//| CalcLotsFromSL: SL price + risk% → lot size (Direction C).       |
//|                                                                   |
//| Given a FIXED stop-loss price, compute the lot size so the loss   |
//| matches the risk budget. Lot is normalized to broker step and     |
//| clamped to [VOLUME_MIN, VOLUME_MAX]. If rawLots < minLot, the     |
//| clamp inflates risk — skip the trade, do NOT silently accept.    |
//| Verify the final loss with OrderCalcProfit before opening.        |
//+------------------------------------------------------------------+
double CalcLotsFromSL(string symbol, double balance, double riskPct,
                      double openPrice, double slPrice) {
    double pv = PointValue(symbol);
    if (pv == 0) return 0;

    double riskAmount = balance * riskPct / 100.0;

    string profCy = SymbolInfoString(symbol, SYMBOL_CURRENCY_PROFIT);
    string accCy  = AccountInfoString(ACCOUNT_CURRENCY);
    if (profCy != accCy) {
        string rateSym = "";
        int dir = FindFXRate(accCy, profCy, rateSym);
        if (dir == 0) return 0;
        MqlTick tick;
        SymbolInfoTick(rateSym, tick);
        double rate = (dir > 0) ? tick.bid : 1.0 / tick.ask;
        riskAmount *= rate;
    }

    double slDistPrice = MathAbs(openPrice - slPrice);
    if (slDistPrice == 0) return 0;

    double point   = SymbolInfoDouble(symbol, SYMBOL_POINT);
    double points  = slDistPrice / point;
    double rawLots = riskAmount / (pv * points);

    double minLot  = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN);
    double maxLot  = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX);
    double lotStep = SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP);

    double lot = MathFloor(rawLots / lotStep) * lotStep;
    lot = MathMax(lot, minLot);
    lot = MathMin(lot, maxLot);
    return NormalizeDouble(lot, 2);
}

#endif // __RISK_HELPERS_MQH__
