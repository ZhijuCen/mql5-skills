# CSingleCondition

The class sets a fuzzy condition expressed by "Fuzzy variable — Fuzzy term" pair.

### Description

According to a fuzzy condition, one variable corresponds to one term. A fuzzy condition can be described by the following expression: X is a,

where:

- X is a fuzzy variable;
- a  is a fuzzy variable value (fuzzy term).

### Declaration

```
   class CSingleCondition : public ICondition

```

### Title

```
   #include <Math\Fuzzy\fuzzyrule.mqh>

```

```
Inheritance hierarchy
   CObject
       ICondition
           CSingleCondition
Direct descendants
CFuzzyCondition

```

### Class methods

| Class method | Description |
| --- | --- |
| Not | Gets and sets the flag indicating whether it is necessary to apply negation to this condition. |
| Term | Gets and sets a fuzzy term for this condition. |
| Var | Gets and sets a fuzzy variable for this condition. |

```
Methods inherited from class CObject
Prev, Prev, Next, Next, Save, Load, Type, Compare

```
