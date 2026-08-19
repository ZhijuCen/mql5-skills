# ShortCondition

Checks conditions to open a short position.

```
virtual int  ShortCondition()

```

Return Value

If the conditions are satisfied, it returns the value from 1 to 100 (depending on "strength" of a signal). If there isn't a signal to open short position, it returns 0.

Note

The base class has no implementation of checking conditions to open a short position and always returns 0.
