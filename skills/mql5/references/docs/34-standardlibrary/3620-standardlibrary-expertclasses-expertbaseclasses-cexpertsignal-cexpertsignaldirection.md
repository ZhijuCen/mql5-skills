# Direction

Returns the value of "weighted" price direction.

```
virtual double  Direction()

```

Return Value

It returns the value>0 when upward direction is most probable and <0 in case of a downward direction. The absolute value depends on the "strength" of a signal.

Note

If the built-in filters are used, their results are considered when defining the general direction.
