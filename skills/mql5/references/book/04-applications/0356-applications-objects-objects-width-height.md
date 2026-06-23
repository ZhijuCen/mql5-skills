# Determining object width and height

Some types of objects allow you to set their dimensions in pixels. These include OBJ_BUTTON, OBJ_CHART, OBJ_BITMAP, OBJ_BITMAP_LABEL, OBJ_EDIT, and OBJ_RECTANGLE_LABEL. In addition, OBJ_LABEL objects support reading (but not setting) sizes because labels automatically expand or contract to fit the text they contain. Attempting to access properties on other types of objects will result in an OBJECT_WRONG_PROPERTY (4203) error.

| Identifier | Description |
| --- | --- |
| OBJPROP_XSIZE | Width of the object along the X-axis in pixels |
| OBJPROP_YSIZE | Height of the object along the Y-axis in pixels |

Both sizes are integers and are therefore handled by the ObjectGetInteger/ObjectSetInteger functions.

Special dimension handling is performed for OBJ_BITMAP and OBJ_BITMAP_LABEL objects.

Without assigning an image, these objects allow you to set an arbitrary size. At the same time, they are drawn transparent (only the frame is visible if it is not "hidden" also by setting the color clrNone), but they receive all events, in particular, about mouse movements (with a text description, if any, in a tooltip) and clicks of its buttons on the object.

When an image is assigned, it defaults to the object's height and width. However, an MQL program can set smaller sizes and select a fragment of an image to display; more on this in the section on [framing](/en/book/applications/objects/objects_bitmap_offset). If you try to set the height or width larger than the image size, it stops being displayed, and the object's dimensions do not change.

As an example, let's develop an improved version of the script ObjectAnchorLabel.mq5 from the section titled [Defining anchor point on an object](/en/book/applications/objects/objects_anchor). In that section, we moved the text label around the window and reversed it when it reached any of the window borders, but we did this while only taking into account the anchor point. Because of this, depending on the location of the anchor point on the object, there could be a situation where the label is almost completely traveled beyond the window. For example, if the anchor point was on the right side of the object, moving to the left would cause almost all of the text to go beyond the left border of the window before the anchor point touched the edge.

In the new script ObjectSizeLabel.mq5, we will take into account the size of the object and change the direction of movement as soon as it touches the edge of the window with any of its sides.

For the correct implementation of this mode, it should be taken into account that each window corner used as the center of reference of coordinates to the anchor point on the object determines the characteristic direction of both the X and Y axes. For example, if the user selects the upper left corner in the ENUM_BASE_CORNER Corner input variable, then X increases from left to right and Y increases from top to bottom. If the center is considered to be the lower right corner, then X increases from right to left of it, and Y increases from bottom to top.

A different mutual combination of the anchor corner in the window and the anchor point on the object requires different adjustments of the distances between the object edges and the window borders. In particular, when one of the right corners and one of the anchor points on the right side of the object is selected, then the correction at the right border of the window is not required, and at the opposite side, the left, we must take into account the width of the object (so that its dimensions do not go out of the window to the left).

This rule about correcting for the size of an object can be generalized:

- On the border of the window adjacent to the anchor corner, the correction is needed when the anchor point is on the far side of the object relative to this corner;
- On the border of the window opposite the anchor corner, the correction is needed when the anchor point is on the near side of the object relative to this corner.

In other words, if the name of the corner (in the ENUM_BASE_CORNER element) and the anchor point (in the ENUM_ANCHOR_POINT element) contain a common word (for example, RIGHT), the correction is needed on the far side of the window (that is, far from the selected corner). If opposite directions are found in the combination of ENUM_BASE_CORNER and ENUM_ANCHOR_POINT sides (for example, LEFT and RIGHT), the correction is needed at the nearest side of the window. These rules work the same for the horizontal and vertical axes.

Additionally, it should be taken into account that the anchor point can be in the middle of any side of the object. Then in the perpendicular direction, an indent from the window borders is required, equal to half the size of the object.

A special case is the anchor point at the center of the object. For it, you should always have a margin of distance in any direction, equal to half the size of the object.

The logic described is implemented in a special function called GetMargins. It takes as inputs the selected corner and anchor point, as well as the dimensions of the object (dx and dy). The function returns a structure with 4 fields containing the sizes of additional indents that should be set aside from the anchor point in the direction of the near and far borders of the window so that the object does not go out of view. Indents reserve the distance according to the dimensions and relative position of the object itself.

```
struct Margins
{
   int nearX; // X increment between the object point and the window border adjacent to the corner
   int nearY; // Y increment between the object point and the window border adjacent to the corner
   int farX;  // X increment between the object's point and the opposite corner of the window border
   int farY;  // Y increment between the object's point and the opposite corner of the window border
};
   
Margins GetMargins(const ENUM_BASE_CORNER corner, const ENUM_ANCHOR_POINT anchor,
   int dx, int dy)
{
   Margins margins = {}; // zero corrections by default
   ...
   return margins;
}

```

To unify the algorithm, the following macro definitions of directions (sides) are introduced:

```
   #define LEFT 0x1
   #define LOWER 0x2
   #define RIGHT 0x4
   #define UPPER 0x8
   #define CENTER 0x16

```

With their help, bit masks (combinations) are defined that describe the elements of the ENUM_BASE_CORNER and ENUM_ANCHOR_POINT enumerations.

```
   const int corner_flags[] = // flags for ENUM_BASE_CORNER elements
   {
      LEFT | UPPER,
      LEFT | LOWER,
      RIGHT | LOWER,
      RIGHT | UPPER
   };
   
   const int anchor_flags[] = // flags for ENUM_ANCHOR_POINT elements
   {
      LEFT | UPPER,
      LEFT,
      LEFT | LOWER,
      LOWER,
      RIGHT | LOWER,
      RIGHT,
      RIGHT | UPPER,
      UPPER,
      CENTER
   };

```

Each of the arrays, corner_flags and anchor_flags, contains exactly as many elements as there are in the corresponding enumeration.

Next comes the main function code. First of all, let's deal with the simplest option: the central anchor point.

```
   if(anchor == ANCHOR_CENTER)
   {
      margins.nearX = margins.farX = dx / 2;
      margins.nearY = margins.farY = dy / 2;
   }
   else
   {
      ...
   }

```

To analyze the rest of the situations, we will use the bit masks from the above arrays by directly addressing them by the received values corner and anchor.

```
      const int mask = corner_flags[corner] & anchor_flags[anchor];
      ...

```

If the corner and the anchor point are on the same horizontal side, the following condition will work and the object width at the far edge of the window will be adjusted.

```
      if((mask & (LEFT | RIGHT)) != 0)
      {
         margins.farX = dx;
      }
      ...

```

If they are not on the same side, then they may be on opposite sides, or it may be the case that the anchor point is in the middle of the horizontal side (top or bottom). Checking for an anchor point in the middle is done using the expression (anchor_flags[anchor] & (LEFT | RIGHT)) == 0 - then the correction is equal to half the width of the object.

```
      else
      {
         if((anchor_flags[anchor] & (LEFT | RIGHT)) == 0)
         {
            margins.nearX = dx / 2;
            margins.farX = dx / 2;
         }
         else
         {
            margins.nearX = dx;
         }
      }
      ...

```

Otherwise, with the opposite orientation of the corner and the anchor point, we make an adjustment to the width of the object at the near border of the window.

Similar checks are made for the Y-axis.

```
      if((mask & (UPPER | LOWER)) != 0)
      {
         margins.farY = dy;
      }
      else
      {
         if((anchor_flags[anchor] & (UPPER | LOWER)) == 0)
         {
            margins.farY = dy / 2;
            margins.nearY = dy / 2;
         }
         else
         {
            margins.nearY = dy;
         }
      }

```

Now the GetMargins function is ready, and we can proceed to the main code of the script in the OnStart function. As before, we determine the size of the window, calculate the initial coordinates in the center, create an OBJ_LABEL object, and select it.

```
void OnStart()
{
   const int t = ChartWindowOnDropped();
   Comment(EnumToString(Corner));
   
   const string name = "ObjSizeLabel";
   int h = (int)ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS, t) - 1;
   int w = (int)ChartGetInteger(0, CHART_WIDTH_IN_PIXELS) - 1;
   int x = w / 2;
   int y = h / 2;
      
   ObjectCreate(0, name, OBJ_LABEL, t, 0, 0);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, true);
   ObjectSetInteger(0, name, OBJPROP_SELECTED, true);
   ObjectSetInteger(0, name, OBJPROP_CORNER, Corner);
   ...

```

For animation, an infinite loop provides variables pass (iteration counter) and anchor (the anchor point, which will be periodically chosen randomly).

```
   int pass = 0;
   ENUM_ANCHOR_POINT anchor = 0;
   ...

```

But there are some changes compared to ObjectAnchorLabel.mq5.

We will not generate random movements of the object. Instead, let's set a constant speed of 5 pixels diagonally.

```
   int px = 5, py = 5;

```

To store the size of the text label, we will reserve two new variables.

```
   int dx = 0, dy = 0;

```

The result of counting additional indents will be stored in a variable m of type Margins.

```
   Margins m = {};

```

This is followed directly by the loop of moving and modifying the object. In it, at every 75th iteration (one iteration of 100 ms, see further), we randomly select a new anchor point, form a new text (the contents of the object) from it, and wait for the changes to be applied to the object (calling ChartRedraw). The latter is necessary because the size of the inscription is automatically adjusted to the content, and the new size is important for us in order to correctly calculate the indents in the GetMargins call.

We get the dimensions using calls ObjectGetInteger with properties OBJPROP_XSIZE and OBJPROP_YSIZE.

```
   for( ;!IsStopped(); ++pass)
   {
      if(pass % 75 == 0)
      {
         // ENUM_ANCHOR_POINT consists of 9 elements: randomly choose one
         const int r = rand() * 8 / 32768 + 1;
         anchor = (ENUM_ANCHOR_POINT)((anchor + r) % 9);
         ObjectSetInteger(0, name, OBJPROP_ANCHOR, anchor);
         ObjectSetString(0, name, OBJPROP_TEXT, " " + EnumToString(anchor)
            + StringFormat("[%3d,%3d] ", x, y));
         ChartRedraw();
         Sleep(1);
   
         dx = (int)ObjectGetInteger(0, name, OBJPROP_XSIZE);
         dy = (int)ObjectGetInteger(0, name, OBJPROP_YSIZE);
         
         m = GetMargins(Corner, anchor, dx, dy);
      }
      ...

```

Once we know the anchor point and all distances, we move the object. If it "bumps" against the wall, we change the direction of movement to the opposite (px to -px or py to -py, depending on the side).

```
      // bounce off window borders, object fully visible
      if(x + px >= w - m.farX)
      {
         x = w - m.farX + px - 1;
         px = -px;
      }
      else if(x + px < m.nearX)
      {
         x = m.nearX + px;
         px = -px;
      }
      
      if(y + py >= h - m.farY)
      {
         y = h - m.farY + py - 1;
         py = -py;
      }
      else if(y + py < m.nearY)
      {
         y = m.nearY + py;
         py = -py;
      }
      
      // calculate the new label position
      x += px;
      y += py;
      ...

```

It remains to update the state of the object itself: display the current coordinates in the text label and assign them to the OBJPROP_XDISTANCE and OBJPROP_YDISTANCE properties.

```
      ObjectSetString(0, name, OBJPROP_TEXT, " " + EnumToString(anchor)
         + StringFormat("[%3d,%3d] ", x, y));
      ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x);
      ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y);
      ...

```

After changing the object, we call ChartRedraw and wait 100ms to ensure a reasonably smooth animation.

```
      ChartRedraw();
      Sleep(100);
      ...

```

At the end of the loop, we check the window size again, since the user can change it while the script is running, and we also repeat the size request.

```
      h = (int)ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS, t) - 1;
      w = (int)ChartGetInteger(0, CHART_WIDTH_IN_PIXELS) - 1;
      
      dx = (int)ObjectGetInteger(0, name, OBJPROP_XSIZE);
      dy = (int)ObjectGetInteger(0, name, OBJPROP_YSIZE);
      m = GetMargins(Corner, anchor, dx, dy);
   }

```

We omitted some other innovations of the ObjectSizeLabel.mq5 script in order to keep the explanation concise. Those who wish can refer to the code. In particular, distinctive colors were used for the inscription: each specific color corresponds to its own anchor point, which makes the switching points more noticeable. Also, you can click Delete while the script is running: this will remove the selected object from the chart and the script will automatically end.
