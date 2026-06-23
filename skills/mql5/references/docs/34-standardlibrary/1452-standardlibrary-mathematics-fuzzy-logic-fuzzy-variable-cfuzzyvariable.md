# CFuzzyVariable

Class for creating general fuzzy variables.

### Description

Here, a fuzzy variable is created with the following parameters:

- maximum variable value;
- minimum variable value;
- fuzzy variable name;
- term set (set of all possible values, which a linguistic variable is capable of receiving).

### Declaration

```
   class CFuzzyVariable : public CNamedVariableImpl

```

### Title

```
   #include <Math\Fuzzy\fuzzyvariable.mqh>

```

```
Inheritance hierarchy
   CObject
       INamedValue
           INamedVariable
               CNamedVariableImpl
                   CFuzzyVariable

```

### Class methods

| Class method | Description |
| --- | --- |
| AddTerm | Adds a single fuzzy term to a fuzzy variable. |
| GetTermByName | Gets a fuzzy term by a specified name. |
| Max | Gets and sets a maximum value for a fuzzy variable. |
| Min | Gets and sets a minimum value for a fuzzy variable. |
| Terms | Gets and sets a list of fuzzy terms for the given fuzzy variable. |
| Values | Gets and sets a list of fuzzy terms for the given fuzzy variable. |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Save ,  Load ,  Type ,  Compare |
| --- |
| Methods inherited from class CNamedVariableImpl 
 Name, Name |
