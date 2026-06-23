# Time and price bound objects

The following table provides objects with their time and price coordinates, their identifiers in the ENUM_OBJECT enumeration, and the number of anchor points.

| Identifier | Name | Anchor points |
| --- | --- | --- |
| Single straight lines |  |  |
| OBJ_VLINE | Vertical (time coordinate only) | 1 |
| OBJ_HLINE | Horizontal (price coordinate only) | 1 |
| OBJ_TREND | Trend | 2 |
| OBJ_ARROWED_LINE | With an arrow at the end | 2 |
| Periodically repeating vertical lines |  |  |
| OBJ_CYCLES | Cyclic | 2 |
| Channels |  |  |
| OBJ_CHANNEL | Equidistant | 3 |
| OBJ_STDDEVCHANNEL | Standard deviation | 2 |
| OBJ_REGRESSION | Linear regression | 2 |
| OBJ_PITCHFORK | Andrews' pitchfork | 3 |
| Fibonacci Tools |  |  |
| OBJ_FIBO | Levels | 2 |
| OBJ_FIBOTIMES | Time zones | 2 |
| OBJ_FIBOFAN | Fan | 2 |
| OBJ_FIBOARC | Arcs | 2 |
| OBJ_FIBOCHANNEL | Channel | 3 |
| OBJ_EXPANSION | Expansion | 3 |
| Gann Tools |  |  |
| OBJ_GANNLINE | Line | 2 |
| OBJ_GANNFAN | Fan | 2 |
| OBJ_GANNGRID | Net | 2 |
| Elliot waves |  |  |
| OBJ_ELLIOTWAVE5 | Impulse | 5 |
| OBJ_ELLIOTWAVE3 | Corrective | 3 |
| Shapes |  |  |
| OBJ_RECTANGLE | Rectangle | 2 |
| OBJ_TRIANGLE | Triangle | 3 |
| OBJ_ELLIPSE | Ellipse | 3 |
| Single marks and labels |  |  |
| OBJ_ARROW_THUMB_UP | Thumbs up | 1* |
| OBJ_ARROW_THUMB_DOWN | Thumbs down | 1* |
| OBJ_ARROW_UP | Up arrow | 1* |
| OBJ_ARROW_DOWN | Down arrow | 1* |
| OBJ_ARROW_STOP | Stop mark | 1* |
| OBJ_ARROW_CHECK | Check mark | 1* |
| OBJ_ARROW_LEFT_PRICE | Left price label | 1 |
| OBJ_ARROW_RIGHT_PRICE | Right price label | 1 |
| OBJ_ARROW_BUY | Buy sign (blue up arrow) | 1 |
| OBJ_ARROW_SELL | Sell sign (red down arrow) | 1 |
| OBJ_ARROW | Arbitrary Wingdings character | 1* |
| Text and graphics |  |  |
| OBJ_TEXT | Text | 1* |
| OBJ_BITMAP | Picture | 1* |
| Events |  |  |
| OBJ_EVENT | Timestamp at the bottom of the main window (time coordinate only) | 1 |

An asterisk marks those objects for which it is allowed to select an anchor point on the object (for example, in one of the corners of the object or in the middle of one of the sides). The selection methods can vary for different object types, and the details will be outlined in the section on [Defining the object anchor point](/en/book/applications/objects/objects_anchor). Anchor points are required because objects have a certain size, and there would be positional ambiguity without them.
