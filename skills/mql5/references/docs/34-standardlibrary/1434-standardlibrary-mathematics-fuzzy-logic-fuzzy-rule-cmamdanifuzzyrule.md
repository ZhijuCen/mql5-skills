# CMamdaniFuzzyRule

Mamdani-type fuzzy inference — one of the two basic types of fuzzy systems. Output variable values are set using fuzzy terms.

### Description

Fuzzy logic rule for the Mamdani algorithm can be described as follows:

![where:](pics/fuzzy_mamdani_rule.png)

where:

- X = (X1, X2, X3 ... Xn) — vector of input variables;
- Y — output variable;
- a = (a1, a2, a3 ... an) — vector of input variable values;
- d — output variable value;
- W — rule weight.

### Declaration

```
   class CMamdaniFuzzyRule : public CGenericFuzzyRule

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
               CMamdaniFuzzyRule

```

### Class methods

| Class method | Description |
| --- | --- |
| Conclusion | Gets and sets the Mamdani fuzzy rule conclusion |
| Weight | Gets and sets the Mamdani fuzzy rule weight |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Save ,  Load ,  Type ,  Compare |
| --- |
| Methods inherited from class CGenericFuzzyRule 
 Condition ,  Condition ,  CreateCondition ,  CreateCondition ,  CreateCondition |
