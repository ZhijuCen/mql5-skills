# CCanvas

CCanvas is a class for simplified creation of custom images.

### Description

CCanvas provides creation of a graphical resource (with or without binding to a chart object) and drawing graphic primitives.

### Declaration

```
   class CCanvas

```

### Title

```
   #include <Canvas\Canvas.mqh>

```

```
Inheritance hierarchy
   CCanvas
Direct descendants
CChartCanvas, CFlameCanvas

```

### Class methods by groups

| Creating |  |
| --- | --- |
| Attach | Attaches the OBJ_BITMAP_LABEL object to an instance of the CCanvas class |
| Create | Creates a graphical resource without binding to a chart object |
| CreateBitmap | Create a graphical resource bound to a chart object |
| CreateBitmapLabel | Create a graphical resource bound to a chart object |
| Destroy | Destroys a graphical resource |
| Properties |  |
| ChartObjectName | Gets the name of a bound chart object |
| ResourceName | Gets the name of a graphical resource |
| Width | Gets the width of a graphical resource |
| Height | Gets the height of a graphical resource |
| LineStyleSet | Sets the line style |
| Updates an object on the screen |  |
| Update | Displays changes on the screen |
| Resize | Resizes a graphical resource |
| Erasing/Filling with color |  |
| Erase | Erases or fills with the specified color |
| Data access |  |
| PixelGet | Gets a color of the dot with the specified coordinates |
| PixelSet | Sets color of the dot with the specified coordinates |
| Draws primitives |  |
| LineVertical | Draws a vertical line |
| LineHorizontal | Draws a horizontal line |
| Line | Draws a freehand line |
| Polyline | Draws a polyline |
| Polygon | Draws a polygon |
| Rectangle | Draws a rectangle |
| Circle | Draws a circle |
| Triangle | Draws a triangle |
| Ellipse | Draws an ellipse |
| Arc | Draws an ellipse arc |
| Pie | Draws an ellipse sector |
| Draws filled primitives |  |
| FillRectangle | Draws a filled rectangle |
| FillCircle | Draws a filled circle |
| FillTriangle | Draws a filled triangle |
| FillPolygon | Draws a filled polygon |
| FillEllipse | Draws a filled ellipse |
| Fill | Fills an area |
| Draws primitives with antialiasing |  |
| PixelSetAA | Draws a pixel |
| LineAA | Draws a line |
| PolylineAA | Draws a polyline |
| PolygonAA | Draws a polygon |
| TriangleAA | Draws a triangle |
| CircleAA | Draws a circle |
| EllipseAA | Draws an ellipse |
| LineWu | Draws a line |
| PolylineWu | Draws a polyline |
| PolygonWu | Draws a polygon |
| TriangleWu | Draws a triangle |
| CircleWu | Draws a circle |
| EllipseWu | Draws an ellipse |
| LineThick | Draws a segment of a freehand line having a specified width using antialiasing algorithm. |
| LineThickVertical | Draws a vertical segment of a freehand line having a specified width using antialiasing algorithm. |
| LineThickHorizontal | Draws a horizontal segment of a freehand line having a specified width using antialiasing algorithm. |
| PolygonSmooth | Draws a polygon with a specified width using two antialiasing algorithms |
| PolygonThick | Draws a polygon with a specified width using antialiasing algorithm |
| PolylineSmooth | Draws a polyline with a specified width using two antialiasing algorithms |
| PolylineThick | Draws a polyline with a specified width using antialiasing algorithm |
| Text |  |
| FontSet | Sets font parameters |
| FontNameSet | Sets font name |
| FontSizeSet | Sets font size |
| FontFlagsSet | Sets font flags |
| FontAngleSet | Sets font slope angle |
| FontGet | Gets font parameters |
| FontNameGet | Gets font name |
| FontSizeGet | Gets font size |
| FontFlagsGet | Gets font flags |
| FontAngleGet | Gets font slope angle |
| TextOut | Displays text |
| TextWidth | Gets the text width |
| TextHeight | Gets the text height |
| TextSize | Gets the text size |
| Transparency |  |
| TransparentLevelSet | Sets transparency level |
| Input/output |  |
| LoadFromFile | Reads an image from a BMP file |
