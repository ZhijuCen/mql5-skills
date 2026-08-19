# LabelMake

Generates a segment label based on its value and the original label.

```
 string  LabelMake(
   const string  text,     // label
   const double  value,    // value
   const bool    to_left,  // flag
   )

```

Parameters

text

[in] Label.

value

[in] Value.

to_left

[in]  Defines the order of the label layout:

- true — label, then value.
- false — value, then label.

Return Value

Label of the segment.
