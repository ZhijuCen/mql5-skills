# ViewTargetSet

Sets the coordinates of the point a gaze is directed at.

```
void  ViewTargetSet(
   const DXVector3  &target      // target coordinates
   );

```

Parameters

&target

[in]  Coordinates of the point a gaze is directed at.

Return Value

None.

Note

Used to fix the gaze at one scene point when moving the viewpoint.

Setting a new target coordinate using ViewRotationSet() changes the view matrix obtained in [ViewMatrixGet()](/en/docs/standardlibrary/3dgraphics/ccanvas3d/ccanvas3dviewmatrixget).

ViewTargetSet() is used together with [ViewUpDirectionSet()](/en/docs/standardlibrary/3dgraphics/ccanvas3d/ccanvas3dviewupdirectionset) to define the gaze direction.
