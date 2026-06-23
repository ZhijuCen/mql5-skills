# TransparentLevelSet

Sets transparency level.

```
void  TransparentLevelSet(
   const uchar  value      // value
   );

```

Parameters

value

[in]  New value of the transparency level.

Note

0 stands for full transparency, while 255 - for full opacity.

Setting a transparency level affects all that was previously drawn. The specified transparency level does not affect further constructions.
