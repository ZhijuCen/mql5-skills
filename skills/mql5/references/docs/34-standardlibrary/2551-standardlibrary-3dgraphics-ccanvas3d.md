# CCanvas3D

CCanvas3D is a class for simplified creation and visualization of 3D objects on a chart.

### Description

CCanvas3D greatly simplifies creation and visualization of large amounts of data in the form of animated 3D graphics. The class contains the methods for managing camera and lighting, as well as features the resource manager for creating graphic resources: textures, shaders, vertex buffers, indexes, and shader parameters.

Besides, the library contains the classes of the scene base objects, such as a box, a three-dimensional surface on user data, or an arbitrary grid.

A video card should support DX 11 and Shader Model 5.0 for the functions to work.

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
       CCanvas3D

```

### Class methods by groups

| Creating/deleting | Description |
| --- | --- |
| Create | Creates a graphic resource for rendering a 3D scene without binding to a chart object. |
| Attach | Gets a graphical resource from the OBJ_BITMAP_LABEL object and attaches it to an instance of the CCanvas class. |
| ObjectAdd | Adds an object to a 3D scene for subsequent rendering. |
| Destroy | Destroys a graphic resource and releases a graphic 3D context. |
| Light |  |
| AmbientColorSet | Sets the color and intensity of the ambient all-round lighting. |
| AmbientColorGet | Gets the color and intensity of the ambient all-round lighting. |
| LightDirectionSet | Sets the direction of a directed light source. |
| LightDirectionGet | Gets the direction of a directed light source. |
| LightColorSet | Sets the color and intensity of a directed light source. |
| LightColorGet | Gets the color and intensity of a directed light source. |
| Camera |  |
| ProjectionMatrixSet | Calculates and sets a 3D coordinate projection matrix to a 2D frame. |
| ProjectionMatrixGet | Gets a 3D scene projection matrix to a 2D frame. |
| ViewMatrixSet | Sets a 3D scene view matrix. |
| ViewMatrixGet | Returns a 3D scene view matrix. |
| ViewPositionSet | Sets a viewpoint on a 3D scene. |
| ViewRotationSet | Sets the direction of a gaze at a 3D scene. |
| ViewTargetSet | Sets the coordinates of the point a gaze is directed at. |
| ViewUpDirectionSet | Sets the direction of the upper frame border in 3D space. |
| Rendering |  |
| Render | Renders all scene objects in the frame inner buffer for subsequent display. |
| RenderBegin | Prepares a graphic context for rendering a new frame. |
| RenderEnd | Copies a rendered frame to the inner buffer and updates a chart image if necessary. |
| Getting resources |  |
| DXContext | Gets the graphic context handle. |
| DXDispatcher | Gets the resource dispatcher handle. |
| InputScene | Gets the pointer to the buffer of scene parameters. |
