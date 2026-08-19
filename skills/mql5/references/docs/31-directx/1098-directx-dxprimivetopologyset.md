# DXPrimiveTopologySet

Sets the type of primitives for rendering using [DXDrawIndexed()](/en/docs/directx/dxdrawindexed).

```
bool  DXPrimiveTopologySet(
   int                         context,                // graphic context handle
   ENUM_DX_PRIMITIVE_TOPOLOGY  primitive_topology      // primitive type
   );

```

Parameters

context

[in]  Handle for a graphic context created in [DXContextCreate()](/en/docs/directx/dxcontextcreate).

primitive_topology

[in]  The value from the [ENUM_DX_PRIMITIVE_TOPOLOGY](/en/docs/directx/dxprimivetopologyset#enum_dx_primitive_topology) enumeration.

Return Value

In case of successful execution, returns true, otherwise - false. To receive an [error](/en/docs/constants/errorswarnings/errorcodes) code, the [GetLastError()](/en/docs/check/getlasterror) function should be called.

ENUM_DX_PRIMITIVE_TOPOLOGY

| ID | Value | Match in  D3D11_PRIMITIVE_TOPOLOGY |
| --- | --- | --- |
| DX_PRIMITIVE_TOPOLOGY_POINTLIST | 1 | D3D11_PRIMITIVE_TOPOLOGY_POINTLIST |
| DX_PRIMITIVE_TOPOLOGY_LINELIST | 2 | D3D11_PRIMITIVE_TOPOLOGY_LINELIST |
| DX_PRIMITIVE_TOPOLOGY_LINESTRIP | 3 | D3D11_PRIMITIVE_TOPOLOGY_LINESTRIP |
| DX_PRIMITIVE_TOPOLOGY_TRIANGLELIST | 4 | D3D11_PRIMITIVE_TOPOLOGY_TRIANGLELIST |
| DX_PRIMITIVE_TOPOLOGY_TRIANGLESTRIP | 5 | D3D11_PRIMITIVE_TOPOLOGY_TRIANGLESTRIP |
| DX_PRIMITIVE_TOPOLOGY_LINELIST_ADJ | 6 | D3D11_PRIMITIVE_TOPOLOGY_LINELIST_ADJ |
| DX_PRIMITIVE_TOPOLOGY_LINESTRIP_ADJ | 7 | D3D11_PRIMITIVE_TOPOLOGY_LINESTRIP_ADJ |
| DX_PRIMITIVE_TOPOLOGY_TRIANGLELIST_ADJ | 8 | D3D11_PRIMITIVE_TOPOLOGY_TRIANGLELIST_ADJ |
| DX_PRIMITIVE_TOPOLOGY_TRIANGLESTRIP_ADJ | 9 | D3D11_PRIMITIVE_TOPOLOGY_TRIANGLESTRIP_ADJ |
