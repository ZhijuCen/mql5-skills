# StepsDimension (Get method)

Get the value indicating the dimension used in step-type curve rendering.

```
int  StepsDimension()

```

Return Value

Dimension used in step-type curve rendering.

# StepsDimension (Set method)

Set the value indicating the dimension used in step-type curve rendering.

```
void  StepsDimension(
   const int  dimension      // dimension 
   )

```

Parameters

dimension

[in]  Dimension (0 or 1).

Note

0 — x (the horizontal line is followed by the vertical one).

1 — y (the vertical line is followed by the horizontal one).
