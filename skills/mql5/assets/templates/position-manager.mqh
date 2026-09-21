//+------------------------------------------------------------------+
//| position-manager.mqh — Position management class template.        |
//|                                                                   |
//| Demonstrates the C++ MQH pattern:                                 |
//|   1. Class declaration (members + method prototypes) at the top   |
//|   2. Method implementations via ClassName::Method() below         |
//|                                                                   |
//| Usage from EA:                                                    |
//|   #include "../templates/position-manager.mqh"                   |
//|   CPositionManager posMgr;                                        |
//|   posMgr.Open(ORDER_TYPE_BUY, 0.1, ...);                         |
//+------------------------------------------------------------------+
#ifndef __POSITION_MANAGER_MQH__
#define __POSITION_MANAGER_MQH__

#include <Trade\Trade.mqh>

//+------------------------------------------------------------------+
//| Class: CPositionManager                                           |
//|                                                                   |
//| Manages one-symbol, one-magic positions:                          |
//|   - Open / close / modify                                        |
//|   - Count & aggregate P&L                                        |
//|   - Enforce max-concurrent-positions guard                       |
//+------------------------------------------------------------------+
class CPositionManager {
private:
    //--- configuration (set once via constructor)
    string            m_symbol;
    long              m_magic;
    int               m_slippage;
    int               m_maxPositions;

    //--- internal helper
    CTrade            m_trade;

    //--- state
    int               m_openCount;

    //--- private helper — not exposed outside this file
    bool              IsMyPosition(int index);

public:
    //--- constructor / destructor
                      CPositionManager(string symbol, long magic,
                                       int slippage = 10,
                                       int maxPositions = 5);
                     ~CPositionManager();

    //--- order execution
    bool              Open(ENUM_ORDER_TYPE type, double lots,
                           double price, double sl, double tp,
                           const string comment = "");
    bool              CloseByTicket(ulong ticket);
    bool              CloseAll();
    bool              ModifySL(ulong ticket, double newSL);

    //--- position queries
    int               Count();
    double            TotalProfit();
    double            TotalVolume();

    //--- accessors
    void              SetMaxPositions(int max);
    int               GetMaxPositions();
};

//+------------------------------------------------------------------+
//|                     IMPLEMENTATION BELOW                          |
//+------------------------------------------------------------------+

//+------------------------------------------------------------------+
//| CPositionManager::CPositionManager                                |
//+------------------------------------------------------------------+
CPositionManager::CPositionManager(string symbol, long magic,
                                   int slippage, int maxPositions)
    : m_symbol(symbol),
      m_magic(magic),
      m_slippage(slippage),
      m_maxPositions(maxPositions),
      m_openCount(0) {
    m_trade.SetExpertMagicNumber(m_magic);
    m_trade.SetMarginMode();
    m_trade.SetTypeFillingBySymbol(m_symbol);
    m_trade.SetDeviationInPoints(m_slippage);
}

//+------------------------------------------------------------------+
//| CPositionManager::~CPositionManager                               |
//+------------------------------------------------------------------+
CPositionManager::~CPositionManager() {
    // nothing to release — CTrade owns no handles
}

//+------------------------------------------------------------------+
//| IsMyPosition: check if position belongs to this symbol + magic.   |
//+------------------------------------------------------------------+
bool CPositionManager::IsMyPosition(int index) {
    if (PositionGetSymbol(index) != m_symbol)   return false;
    if (PositionGetInteger(POSITION_MAGIC) != m_magic) return false;
    return true;
}

//+------------------------------------------------------------------+
//| Open: open a position with full retcode check.                    |
//+------------------------------------------------------------------+
bool CPositionManager::Open(ENUM_ORDER_TYPE type, double lots,
                            double price, double sl, double tp,
                            const string comment) {
    //--- guard: max positions
    if (Count() >= m_maxPositions) {
        PrintFormat("Max positions (%d) reached — skipping",
                    m_maxPositions);
        return false;
    }

    bool ok = m_trade.PositionOpen(m_symbol, type, lots,
                                   price, sl, tp, comment);
    if (!ok || m_trade.ResultRetcode() != TRADE_RETCODE_DONE) {
        PrintFormat("Open failed: retcode=%u (%s)",
                    m_trade.ResultRetcode(),
                    m_trade.ResultRetcodeDescription());
        return false;
    }
    return true;
}

//+------------------------------------------------------------------+
//| CloseByTicket: close a single position by ticket.                 |
//+------------------------------------------------------------------+
bool CPositionManager::CloseByTicket(ulong ticket) {
    if (!m_trade.PositionClose(ticket)) {
        PrintFormat("Close ticket %llu failed: retcode=%u",
                    ticket, m_trade.ResultRetcode());
        return false;
    }
    return true;
}

//+------------------------------------------------------------------+
//| CloseAll: close every position on this symbol + magic.            |
//+------------------------------------------------------------------+
bool CPositionManager::CloseAll() {
    bool allClosed = true;
    uint total = PositionsTotal();
    for (uint i = total; i > 0; i--) {   // iterate backwards (safe)
        int idx = (int)i - 1;
        if (!IsMyPosition(idx)) continue;
        ulong ticket = PositionGetInteger(POSITION_TICKET);
        if (!CloseByTicket(ticket)) allClosed = false;
    }
    return allClosed;
}

//+------------------------------------------------------------------+
//| ModifySL: change stop-loss on an existing position.               |
//+------------------------------------------------------------------+
bool CPositionManager::ModifySL(ulong ticket, double newSL) {
    if (!m_trade.PositionModify(ticket, newSL, 0)) {
        PrintFormat("Modify ticket %llu SL→%.5f failed: retcode=%u",
                    ticket, newSL, m_trade.ResultRetcode());
        return false;
    }
    return true;
}

//+------------------------------------------------------------------+
//| Count: number of open positions on this symbol + magic.           |
//+------------------------------------------------------------------+
int CPositionManager::Count() {
    int n = 0;
    uint total = PositionsTotal();
    for (uint i = 0; i < total; i++) {
        if (IsMyPosition((int)i)) n++;
    }
    return n;
}

//+------------------------------------------------------------------+
//| TotalProfit: sum of unrealized profit (incl. swap/commission).    |
//|                                                                   |
//| POSITION_COMMISSION was removed from ENUM_POSITION_PROPERTY_DOUBLE|
//| in recent MT5 builds. Use CPositionInfo::Commission() instead.   |
//+------------------------------------------------------------------+
double CPositionManager::TotalProfit() {
    double sum = 0;
    CPositionInfo posInfo;
    uint total = PositionsTotal();
    for (uint i = 0; i < total; i++) {
        if (!IsMyPosition((int)i)) continue;
        ulong ticket = PositionGetInteger(POSITION_TICKET);
        if (!posInfo.SelectByTicket(ticket)) continue;
        sum += posInfo.Profit() + posInfo.Swap() + posInfo.Commission();
    }
    return sum;
}

//+------------------------------------------------------------------+
//| TotalVolume: sum of lots across open positions.                   |
//+------------------------------------------------------------------+
double CPositionManager::TotalVolume() {
    double vol = 0;
    uint total = PositionsTotal();
    for (uint i = 0; i < total; i++) {
        if (!IsMyPosition((int)i)) continue;
        vol += PositionGetDouble(POSITION_VOLUME);
    }
    return vol;
}

//+------------------------------------------------------------------+
//| SetMaxPositions: update the guard at runtime.                     |
//+------------------------------------------------------------------+
void CPositionManager::SetMaxPositions(int max) {
    m_maxPositions = max;
}

//+------------------------------------------------------------------+
//| GetMaxPositions: read the current guard.                          |
//+------------------------------------------------------------------+
int CPositionManager::GetMaxPositions() {
    return m_maxPositions;
}
//+------------------------------------------------------------------+
#endif // __POSITION_MANAGER_MQH__
