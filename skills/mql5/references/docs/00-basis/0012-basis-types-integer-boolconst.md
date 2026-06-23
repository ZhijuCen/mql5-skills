# Bool Type

The bool type is intended to store the logical values of true or false, numeric representation of them is 1 or 0, respectively.

Examples:

```
bool a = true;
bool b = false;
bool c = 1;

```

The internal representation is a whole number 1 byte large. It should be noted that in logical expressions you can use other integer or real types or expressions of these types - the compiler will not generate any error. In this case, the zero value will be interpreted as false, and all other values - as true.

Examples:

```
   int i=5;
   double d=-2.5;
   if(i) Print("i = ",i," and is set to true");
   else Print("i = ",i," and is set to false");
 
   if(d) Print("d = ",d," and has the true value");
   else Print("d = ",d," and has the false value");
 
   i=0;
   if(i) Print("i = ",i," and has the true value");
   else Print("i = ",i," and has the false value");
 
   d=0.0;
   if(d) Print("d = ",d," and has the true value");
   else Print("d = ",d," and has the false value");
 
//--- Execution results
//   i= 5 and has the true value
//   d= -2.5 and has the true value
//   i= 0 and has the false value
//   d= 0 and has the false value

```

See also

[Boolean Operations](/en/docs/basis/operations/bool), [Precedence Rules](/en/docs/basis/operations/rules)
