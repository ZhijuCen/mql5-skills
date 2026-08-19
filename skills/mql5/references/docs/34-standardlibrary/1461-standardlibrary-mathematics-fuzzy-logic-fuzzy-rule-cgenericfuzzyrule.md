# CGenericFuzzyRule

Base class for both types of fuzzy rules.

### Declaration

```
   class CGenericFuzzyRule : public IParsableRule

```

### Title

```
   #include <Math\Fuzzy\fuzzyrule.mqh>

```

```
Inheritance hierarchy
   CObject
       IParsableRule
           CGenericFuzzyRule
Direct descendants
CMamdaniFuzzyRule, CSugenoFuzzyRule

```

### Class methods

| Class method | Description |
| --- | --- |
| Conclusion | Gets and sets the fuzzy rule conclusion |
| Condition | Gets and sets the 'if' condition (set of conditions) for a fuzzy rule |
| CreateCondition | Creates a condition for a fuzzy rule by specified parameters |

```
Methods inherited from class CObject
Prev, Prev, Next, Next, Save, Load, Type, Compare

```
