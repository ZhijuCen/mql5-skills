# ViewRotationSet

Sets the direction of a gaze at a 3D scene.

```
void  ViewRotationSet(
   const DXVector3  &rotation      // vector of turning angles 
   );

```

Parameters

&rotation

[in]  Vector setting Euler angles to calculate the direction of a gaze at a 3D scene.

Return Value

None.

Note

Setting the gaze direction using ViewRotationSet() changes the view matrix obtained in [ViewMatrixGet()](/en/docs/standardlibrary/3dgraphics/ccanvas3d/ccanvas3dviewmatrixget).
