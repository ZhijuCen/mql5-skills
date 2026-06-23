# CSugenoVariable

Class for creating fuzzy Sugeno-type variables.

### Description

Fuzzy Sugeno-type variable is different from the general linguistic variable since it is not set by a term set but by a set of linear functions.

### Declaration

```
   class CSugenoVariable : public CNamedVariableImpl

```

### Title

```
   #include <Math\Fuzzy\sugenovariable.mqh>

```

```
Inheritance hierarchy
   CObject
       INamedValue
           INamedVariable
               CNamedVariableImpl
                   CSugenoVariable

```

### Class methods

| Class method | Description |
| --- | --- |
| Functions | Gets the list of linear functions of the fuzzy Sugeno variable. |
| GetFuncByName | Gets the linear function by a specified name. |
| Values | Gets the list of linear functions of the fuzzy Sugeno variable. |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Save ,  Load ,  Type ,  Compare |
| --- |
| Methods inherited from class CNamedVariableImpl 
 Name, Name |
