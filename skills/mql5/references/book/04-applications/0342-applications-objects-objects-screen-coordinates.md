# Objects bound to screen coordinates

The following table lists the names and ENUM_OBJECT identifiers of objects positioned based on the screen coordinates. Almost all of them, except for the chart object, are designed to create a user interface for programs. In particular, there are such basic controls as a button and an input field, as well as labels and panels for visual grouping of objects. Based on them, you can create more complex controls (for example, drop-down lists or checkboxes). Together with the terminal, a class library with ready-made controls is supplied as a set of header files (see the MQL5/Include/Controls directory).

| Identifier | Name | Setting  
 anchor point |
| --- | --- | --- |
| OBJ_LABEL | Text label | Yes |
| OBJ_RECTANGLE_LABEL | Rectangular panel |  |
| OBJ_BITMAP_LABEL | Panel with an image | Yes |
| OBJ_BUTTON | Button |  |
| OBJ_EDIT | Input field |  |
| OBJ_CHART | Chart object |  |

All these objects require the [determining of the anchor corner](/en/book/applications/objects/objects_corner_x_y) in the chart window. By default, their coordinates are relative to the upper left corner of the window.

The types in this list also use an anchor point on the object, and only one. It is editable in some objects and is hard-coded in others. For example, a rectangular panel, a button, an input field, and a chart object are always anchored at their top left corner. And for a label or a panel with a picture, many options are available. The choice is made from the ENUM_ANCHOR_POINT enumeration described in the section on [Defining the object anchor point](/en/book/applications/objects/objects_anchor).

The text label (OBJ_LABEL) provides text output without the possibility of editing it. For editing, use the input field (OBJ_EDIT).
