# Render

Renders all scene objects in the frame inner buffer for subsequent display.

```
bool  Render(
   uint  flags,                  // combination of flags
   uint  background_color=0      // background color
   );

```

Parameters

flags

[in]  Combination of flags that sets the rendering mode. Possible values:  

DX_CLEAR_COLOR – clear the image buffer using background_color.  

DX_CLEAR_DEPTH – clear the depth buffer.

background_color=0

[in]  3D scene background color.

Return Value

true – if successful, false – if failed to render.

Note

Calling Render() does not update a scene on a chart. Instead, it only updates the inner buffer of the image. The Update() method should be explicitly called to render the updated frame.

Render() features the [RenderBegin](/en/docs/standardlibrary/3dgraphics/ccanvas3d/ccanvas3drenderbegin) and [RenderEnd()](/en/docs/standardlibrary/3dgraphics/ccanvas3d/ccanvas3drenderend) calls.
