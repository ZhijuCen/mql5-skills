# ViewUpDirectionSet

Sets the direction of the upper frame border in 3D space.

```
void  ViewUpDirectionSet(
   const DXVector3  &up_direction      // top direction
   );

```

Parameters

&up_direction

[in]  Direction of the upper part of the frame in 3D space.

Return Value

None.

Note

Setting a new direction using ViewUpDirectionSet() changes the view matrix obtained in [ViewMatrixGet()](/en/docs/standardlibrary/3dgraphics/ccanvas3d/ccanvas3dviewmatrixget).

ViewUpDirectionSet() is used together with [ViewTargetSet()](/en/docs/standardlibrary/3dgraphics/ccanvas3d/ccanvas3dviewtargetset) to define the gaze direction.
