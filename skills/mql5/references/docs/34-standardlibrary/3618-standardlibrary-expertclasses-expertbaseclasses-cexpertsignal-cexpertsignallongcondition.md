# LongCondition

Checks conditions to open a long position.

```
virtual int  LongCondition()

```

Return Value

If the conditions are satisfied, it returns the value from 1 to 100 (depending on "strength" of a signal). If there is no signal to open a long position, it returns 0.

Note

The base class has no implementation of checking conditions to open a long position and always returns 0.
