# Magic

Sets the Expert Advisor ID (magic).

```
void  Magic(
   ulong  value     // new value
   )

```

Parameters

value

[in]  New value of Expert Advisor ID.

Return Value

None.

Note

If EA's identifier is changed, the same identifier is assigned to all auxiliary objects.

Implementation

```
//+------------------------------------------------------------------+
//| Sets magic number for object and its dependent objects           |
//| INPUT:  value - new value of magic number.                       |
//| OUTPUT: no.                                                      |
//| REMARK: no.                                                      |
//+------------------------------------------------------------------+
void CExpert::Magic(ulong value)
  {
   if(m_trade!=NULL)    m_trade.SetExpertMagicNumber(value);
   if(m_signal!=NULL)   m_signal.Magic(value);
   if(m_money!=NULL)    m_money.Magic(value);
   if(m_trailing!=NULL) m_trailing.Magic(value);
//---
   CExpertBase::Magic(value);
  }

```
