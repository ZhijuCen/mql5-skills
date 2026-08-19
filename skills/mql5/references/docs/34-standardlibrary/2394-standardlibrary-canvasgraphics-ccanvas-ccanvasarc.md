# Arc

Draws an arc of an ellipse inscribed in a rectangle with corners at (x1,y1) and (x2,y2). The arc boundaries are clipped by lines from the center of the ellipse, which extend to two points with coordinates (x3,y3) and (x4,y4).

```
void  Arc(
   int         x1,      // X coordinate of the upper left corner of the rectangle
   int         y1,      // Y coordinate of the upper left corner of the rectangle
   int         x2,      // X coordinate of the bottom right corner of the rectangle
   int         y2,      // Y coordinate of the bottom right corner of the rectangle
   int         x3,      // X coordinate of the first point to find the arc boundaries
   int         y3,      // Y coordinate of the first point to find the arc boundaries
   int         x4,      // X coordinate of the second point to find the arc boundaries
   int         y4,      // Y coordinate of the second point to find the arc boundaries
   const uint  clr      // color
   );

```

Parameters

x1

[in]  X coordinate of the top left corner forming the rectangle.

y1

[in]  Y coordinate of the top left corner forming the rectangle.

x2

[in]  X coordinate of the bottom right corner forming the rectangle.

y2

[in]  Y coordinate of the bottom right corner forming the rectangle.

x3

[in]  X coordinate of the first point, to which a line from the rectangle center is drawn in order to obtain the arc boundary.

y3

[in]  Y coordinate of the first point, to which a line from the rectangle center is drawn in order to obtain the arc boundary.

x4

[in]  X coordinate of the second point, to which a line from the rectangle center is drawn in order to obtain the arc boundary.

y4

[in]  Y coordinate of the second point, to which a line from the rectangle center is drawn in order to obtain the arc boundary.

clr

[in]  Color in ARGB format. Use the [ColorToARGB()](/en/docs/convert/colortoargb) function to convert a color into the ARGB format.

Draws an arc of an ellipse with center at point (x,y), inscribed in rectangle, with radii rx and ry. The arc boundaries are cropped from the ellipse center using rays formed by angles fi3 and fi4.

```
void  Arc(
   int         x,       // X coordinate of the ellipse center
   int         y,       // Y coordinate of the ellipse center
   int         rx,      // ellipse radius on the X axis
   int         ry,      // ellipse radius on the Y axis
   int         fi3,     // angle of ray from ellipse center, which defines the first boundary of the arc
   int         fi4,     // angle of ray from ellipse center, which defines the second boundary of the arc
   const uint  clr      // color
   );

```

Draws an arc of an ellipse with center at point (x,y), inscribed in rectangle, with radii rx and ry, and also returns the coordinates of the arc boundaries. The arc boundaries are cropped from the ellipse center using rays formed by angles fi3 and fi4.

```
void  Arc(
   int         x,       // X coordinate of the ellipse center
   int         y,       // Y coordinate of the ellipse center
   int         rx,      // ellipse radius on the X axis
   int         ry,      // ellipse radius on the Y axis
   int         fi3,     // angle of ray from ellipse center, which defines the first boundary of the arc
   int         fi4,     // angle of ray from ellipse center, which defines the second boundary of the arc
   int&        x3,      // X coordinate of the first arc boundary
   int&        y3,      // Y coordinate of the first arc boundary
   int&        x4,      // X coordinate of the second arc boundary
   int&        y4,      // Y coordinate of the second arc boundary
   const uint  clr      // color
   );

```

Parameters

x

[in]  X coordinate of the ellipse center.

y

[in]  Y coordinate of the ellipse center.

rx

[in]  Ellipse radius on the X axis, in pixels.

ry

[in]  Ellipse radius on the Y axis, in pixels.

fi3

[in]  Angle in radians, which defines the first boundary of the arc.

fi4

[in]  Angle in radians, which defines the second boundary of the arc.

x3

[out] Variable to get the X coordinate of the first arc boundary.

y3

[out] Variable to get the Y coordinate of the first arc boundary.

x4

[out] Variable to get the X coordinate of the second arc boundary.

y4

[out] Variable to get the Y coordinate of the second arc boundary.

clr

[in]  Color in ARGB format. Use the [ColorToARGB()](/en/docs/convert/colortoargb) function to convert a color into the ARGB format.

Examples of calling the class methods:

```
#include <Canvas\Canvas.mqh>
CCanvas canvas;
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
   int      Width=600;
   int      Height=400;
//--- create canvas
   if(!canvas.CreateBitmapLabel(0,0,"CirclesCanvas",30,30,Width,Height))
     {
      Print("Error creating canvas: ",GetLastError());
     }
//--- clear canvas
   canvas.Erase(clrWhite);
//--- draw rectangle
   canvas.Rectangle(215-190,215-120,215+190,215+120,clrGray);
//--- draw first arc
   canvas.Arc(215,215, 190,120,M_PI_4,2*M_PI-M_PI_4,ColorToARGB(clrRed));
   int x1,y1,x2,y2;
//--- draw second arc
   canvas.Arc(215,215, 190,120,2*M_PI-M_PI_4,2*M_PI+M_PI_4,x1,y1,x2,y2,ColorToARGB(clrGreen));
//--- print coordinates of arc 
   PrintFormat("First point of arc at (%G,%G), second point of arc at (%G,%G)",x1,y1,x2,y2);
   canvas.CircleAA(x1,y1,3, ColorToARGB(clrRed));
   canvas.CircleAA(x2,y2,3, ColorToARGB(clrBlue));
//--- show updated canvas
   canvas.Update();   
  }

```
