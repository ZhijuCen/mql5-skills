# Working with DirectX

DirectX 11 functions and shaders are designed for 3D visualization directly on a price chart.

Creating 3D graphics requires a graphic context ([DXContextCreate](/en/docs/directx/dxcontextcreate)) with the necessary image size. Besides, it is necessary to prepare vertex and index buffers ([DXBufferCreate](/en/docs/directx/dxbuffercreate)), as well as create vertex and pixel shaders ([DXShaderCreate](/en/docs/directx/dxshadercreate)). This is enough to display graphics in color.

The next level of graphics requires the inputs ([DXInputSet](/en/docs/directx/dxinputset)) for passing additional rendering parameters to shaders. This allows setting the camera and 3D object positions, describe light sources and implement mouse and keyboard control.

Thus, the built-in MQL5 functions enable you to create animated 3D charts directly in MetaTrader 5 with no need for third-party tools. A video card should support DX 11 and Shader Model 5.0 for the functions to work.

To start working with the library, simply read the article [How to create 3D graphics using DirectX in MetaTrader 5](https://www.mql5.com/en/articles/7708).

| Function | Action |
| --- | --- |
| DXContextCreate | Creates a graphic context for rendering frames of a specified size |
| DXContextSetSize | Changes a frame size of a graphic context created in DXContextCreate() |
| DXContextSetSize | Gets a frame size of a graphic context created in DXContextCreate() |
| DXContextClearColors | Sets a specified color to all pixels for the rendering buffer |
| DXContextClearDepth | Clears the depth buffer |
| DXContextGetColors | Gets an image of a specified size and offset from a graphic context |
| DXContextGetDepth | Gets the depth buffer of a rendered frame |
| DXBufferCreate | Creates a buffer of a specified type based on a data array |
| DXTextureCreate | Creates a 2D texture out of a rectangle of a specified size cut from a passed image |
| DXInputCreate | Creates shader inputs |
| DXInputSet | Sets shader inputs |
| DXShaderCreate | Creates a shader of a specified type |
| DXShaderSetLayout | Sets vertex layout for the vertex shader |
| DXShaderInputsSet | Sets shader inputs |
| DXShaderTexturesSet | Sets shader textures |
| DXDraw | Renders the vertices of the vertex buffer set in DXBufferSet() |
| DXDrawIndexed | Renders graphic primitives described by the index buffer from DXBufferSet() |
| DXPrimiveTopologySet | Sets the type of primitives for rendering using DXDrawIndexed() |
| DXBufferSet | Sets a buffer for the current rendering |
| DXShaderSet | Sets a shader for rendering |
| DXHandleType | Returns a handle type |
| DXRelease | Releases a handle |
