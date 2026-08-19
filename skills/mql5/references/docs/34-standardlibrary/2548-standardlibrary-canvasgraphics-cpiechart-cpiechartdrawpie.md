# DrawPie

Draws a segment of the pie chart, which corresponds to a specified value.

```
 void  DrawPie(
   double      fi3,   // angle of ray from pie chart center, which defines the first boundary of the arc
   double      fi4,   // angle of ray from pie chart center, which defines the second boundary of the arc
   int         idx,   // index
   CPoint&     p[],  // 
   const uint  clr,   // 
   )

```

Parameters

fi3

[in] Angle in radians, which defines the first boundary of the arc.

fi4

[in] Angle in radians, which defines the second boundary of the arc.

idx

[in] Index of the value the segment corresponds to.

p[]

[in] Array of reference points (x, y) for plotting the segments.

clr

[in]  Color of the segment.
