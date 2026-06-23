# Basic Class CObject

Class CObject is the base class for constructing a MQL5 Standard Library.

### Description

Class CObject allows all its descendants to be part of a linked list. Also, a number of virtual methods for further implementation in descendant classes are identified.

Declaration

```
   class CObject

```

### Title

```
   #include <Object.mqh>

```

```
Inheritance hierarchy
   CObject
Direct descendants
CAccountInfo, CArray, CChart, CChartObject, CCurve, CDealInfo, CDictionary_Obj_Double, CDictionary_Obj_Obj, CDictionary_String_Obj, CExpertBase, CFile, CHistoryOrderInfo, CList, COrderInfo, CPositionInfo, CString, CSymbolInfo, CTerminalInfo, CTrade, CTreeNode, CWnd, ICondition, IExpression, IMembershipFunction, INamedValue, IParsableRule

```

### Class Methods by Groups

| Attributes |  |
| --- | --- |
| Prev | Gets the value of the previous item |
| Prev | Sets the value of the previous item |
| Next | Gets the value of the subsequent element |
| Next | Sets the next element |
| Compare methods |  |
| virtual  Compare | Returns the result of comparison with another object |
| Input/output |  |
| virtual  Save | Writes object to a file |
| virtual  Load | Reads the object from the file |
| virtual  Type | Returns the type of object |
