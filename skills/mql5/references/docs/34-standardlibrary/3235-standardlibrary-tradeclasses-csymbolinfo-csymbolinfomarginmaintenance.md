# MarginMaintenance

Gets the value of maintenance margin.

```
double  MarginMaintenance()

```

Return Value

Value of maintenance margin.

Note

It returns the amount of margin (in margin currency of instrument) that is charged from one lot. Used to check client's equity, when the account state is changed. If the maintenance margin is equal to 0, then the initial margin is used.

The symbol should be selected by [Name](/en/docs/standardlibrary/tradeclasses/csymbolinfo/csymbolinfoname) method.
