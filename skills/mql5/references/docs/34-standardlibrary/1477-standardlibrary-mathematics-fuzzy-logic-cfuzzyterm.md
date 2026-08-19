# CFuzzyTerm (fuzzy terms)

Class for implementing fuzzy terms.

### Description

A term is any element of a term set.  A term is defined by two components:

- fuzzy term name;
- membership function.

### Declaration

```
   class CFuzzyTerm : public CNamedValueImpl

```

### Title

```
   #include <Math\Fuzzy\fuzzyterm.mqh>

```

```
Inheritance hierarchy
   CObject
       INamedValue
           CNamedValueImpl
               CFuzzyTerm

```

### Class methods

| Class method | Description |
| --- | --- |
| MembershipFunction | Gets a membership function for the fuzzy term. |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Save ,  Load ,  Type ,  Compare |
| --- |
| Methods inherited from class CNamedValueImpl 
 Name, Name |
