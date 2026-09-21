# Quick Ref — MQL5 Code Style and Conventions

Companion to `SKILL.md` §1 "MQL5 Fundamentals".
Naming rules derived from MQL5 Book (§basis/identifiers, §oop/classes)
and the MQL5 Standard Library (`CTrade`, `CPositionInfo`, etc.).

## 1. Naming Conventions

### Classes

PascalCase with **`C` prefix** — matches the MQL5 Standard Library:

```mql5
class CPositionManager { ... };
class CMyCustomFilter { ... };
```

Reference: `CTrade`, `CPositionInfo`, `CDealInfo`, `CSymbolInfo`.

### Methods

PascalCase. No prefix:

```mql5
bool   Open(ENUM_ORDER_TYPE type, double lots, ...);
double TotalProfit();
void   SetMaxPositions(int max);
```

### Member Variables

**`m_` prefix** + camelCase. Private by default; no `public:` prefix on data:

```mql5
private:
    string   m_symbol;
    long     m_magic;
    int      m_maxPositions;
```

The `m_` prefix is not mandated by the MQL5 Book but is consistently
used across the Standard Library and is the de-facto MQL5 convention.

### Standalone Functions

PascalCase (same as methods):

```mql5
double PointValue(string symbol);
int    FindFXRate(string from, string to, string &result);
bool   IsNewBar();
```

### Constants and Enums

ALL_CAPS with underscores:

```mql5
#define EA_MAGIC MagicNumber

enum ENUM_RISK_MODE {
    RISK_MODE_FIXED_LOT,    // ALL_CAPS
    RISK_MODE_DYNAMIC
};
```

### Input Variables

PascalCase (no prefix). Matches MetaEditor default:

```mql5
input double RiskPercent = 1.0;
input int    Slippage    = 10;
```

### Local Variables

Flexible — camelCase or snake_case. Be consistent within a file:

```mql5
double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
int    slPts = 500;
double sl_distance = 0;
```

## 2. Class Structure

### Access Modifier Order

**private → protected → public**. Maintain this order across all
classes in the project (MQL5 Book §oop/classes/access-rights):

```mql5
class CMyClass {
private:
    string   m_name;
    int      m_count;

protected:
    CTrade   m_trade;

public:
              CMyClass(string name);
    bool      Open(...);
    int       Count();
};
```

### Declaration vs Definition

For MQH files, prefer **declaration at top, implementation below**
using `ClassName::Method()` syntax. This is the standard pattern
from MQL5 Book §oop/classes/declaration-definition:

```mql5
//--- declaration
class CMyClass {
public:
    void DoSomething(int x);
};

//--- implementation
void CMyClass::DoSomething(int x) {
    // ...
}
```

Benefits:
- Header file shows the full API at a glance.
- Implementation details are hidden below the interface.
- Enables library distribution as `.ex5` + `.mqh` pair.

### Constructor Initialization Lists

Use initializer lists for member setup, not body assignment:

```mql5
CPositionManager::CPositionManager(string symbol, long magic)
    : m_symbol(symbol),
      m_magic(magic),
      m_openCount(0) {
    // body for logic that cannot go in initializer list
}
```

## 3. Formatting

MQL5 is free-form — whitespace is compiler-insensitive. MetaEditor
has a built-in styler (Tools → Settings → Styler).

### Braces

K&R style (opening brace on same line) is the MQL5 community norm
and matches MetaEditor default:

```mql5
void OnTick() {
    if (!IsNewBar()) return;
    // ...
}

if (x > 0) {
    // ...
} else {
    // ...
}
```

### Indentation

4 spaces (MetaEditor default). Do not mix tabs and spaces.

### Comments

Use `//` for inline, `//+------------------------------------------------------------------+`
block separators for function headers (matches MetaEditor auto-generated
header style):

```mql5
//+------------------------------------------------------------------+
//| Open: open a position with full retcode check.                    |
//+------------------------------------------------------------------+
bool CPositionManager::Open(...) {
    // inline comment
}
```

## 4. MQH File Template

```mql5
//+------------------------------------------------------------------+
//| filename.mqh — Brief description.                                 |
//| Companion doc: skills/mql5/SKILL.md §X.                           |
//+------------------------------------------------------------------+
#ifndef __FILENAME_MQH__
#define __FILENAME_MQH__

#include <Trade\Trade.mqh>

class CMyClass {
private:
    //--- members (m_ prefix)
public:
              CMyClass(...);
             ~CMyClass();
    bool      DoWork(...);
};

//+------------------------------------------------------------------+
//|                     IMPLEMENTATION BELOW                          |
//+------------------------------------------------------------------+

CMyClass::CMyClass(...) : m_field(...) { }
CMyClass::~CMyClass() { }
bool CMyClass::DoWork(...) { return true; }

#endif // __FILENAME_MQH__
```

## 5. Common Anti-Patterns

| Anti-Pattern | Why It's Wrong | Fix |
|--------------|----------------|-----|
| `POSITION_COMMISSION` | Removed from `ENUM_POSITION_PROPERTY_DOUBLE` in recent builds | Use `CPositionInfo::Commission()` |
| No `m_` prefix on members | Ambiguous: is `symbol` a local or a field? | Prefix with `m_` |
| Public data members | Breaks encapsulation | Use `private` + getter/setter |
| Inconsistent naming in one file | Harder to read, looks unprofessional | Pick one style, stick to it |
| `trade.Buy()` without retcode check | Silent failures hide bugs | Always check `ResultRetcode()` |

## References

- MQL5 Book: `references/book/01-basis/0015-basis-identifiers.md` (naming styles)
- MQL5 Book: `references/book/02-oop/0109-oop-...-classes-definition.md` (class structure)
- MQL5 Book: `references/book/02-oop/0110-oop-...-access-rights.md` (private/protected/public)
- MQL5 Book: `references/book/02-oop/0120-oop-...-declaration-definition.md` (split pattern)
- MQL5 Standard Library: `Include/Trade/Trade.mqh`, `Include/Trade/PositionInfo.h`
