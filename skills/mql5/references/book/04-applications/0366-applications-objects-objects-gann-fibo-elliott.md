# Additional properties of Gann, Fibonacci, and Elliot objects

Gann, Fibonacci, and Elliot objects have specific, unique properties. Depending on the property type, use the ObjectGetInteger/ObjectSetInteger or ObjectGetDouble/ObjectSetDouble functions.

| Identifier | Description | Type |
| --- | --- | --- |
| OBJPROP_DIRECTION | Gann object trend (Fan OBJ_GANNFAN and Grid OBJ_GANNGRID) | ENUM_GANN_DIRECTION |
| OBJPROP_DEGREE | Elliot wave degree levels | ENUM_ELLIOT_WAVE_DEGREE |
| OBJPROP_DRAWLINES | Displaying lines for the Elliot wave levels | bool |
| OBJPROP_SCALE | Scale in points per bar (property of Gann objects and the Fibonacci Arcs object) | double |
| OBJPROP_ELLIPSE | Full ellipse display for the Fibonacci Arcs object (OBJ_FIBOARC) | bool |

The ENUM_GANN_DIRECTION enumeration has the following members:

| Constant | Trend direction |
| --- | --- |
| GANN_UP_TREND | Ascending lines |
| GANN_DOWN_TREND | Descending lines |

ENUM_ELLIOT_WAVE_DEGREE is used to set the size (labeling method) of Elliot waves.

| Constant | Description |
| --- | --- |
| ELLIOTT_GRAND_SUPERCYCLE | Grand Supercycle |
| ELLIOTT_SUPERCYCLE | Supercycle |
| ELLIOTT_CYCLE | Cycle |
| ELLIOTT_PRIMARY | Primary cycle |
| ELLIOTT_INTERMEDIATE | Intermediate link |
| ELLIOTT_MINOR | Minor cycle |
| ELLIOTT_MINUTE | Minute |
| ELLIOTT_MINUETTE | Minuette |
| ELLIOTT_SUBMINUETTE | Subminuette |
