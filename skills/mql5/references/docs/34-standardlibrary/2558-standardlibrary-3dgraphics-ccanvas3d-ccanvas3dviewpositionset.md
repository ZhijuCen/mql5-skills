# ViewPositionSet

Sets a viewpoint on a 3D scene.

```
void  ViewPositionSet(
   const DXVector3  &position      // viewpoint position
   );

```

Parameters

&position

[in]  Setting a viewpoint position on a 3D scene.

Return Value

None.

Note

Setting a viewpoint position using ViewPositionSet() changes the view matrix obtained in [ViewMatrixGet()](/en/docs/standardlibrary/3dgraphics/ccanvas3d/ccanvas3dviewmatrixget).
