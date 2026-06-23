# Checking Object Pointer

The [CheckPointer()](/en/docs/common/checkpointer) function is used for checking the type of the [object pointer](/en/docs/basis/types/object_pointers). The function returns a value of the ENUM_POINTER_TYPE enumeration. If an incorrect pointer is used, the program execution will be immediately terminated.

Objects created by the [new()](/en/docs/basis/operators/newoperator) operator are of POINTER_DYNAMIC type. The [delete() operator](/en/docs/basis/operators/deleteoperator) can and should be used only for such pointers.

All other pointers are of POINTER_AUTOMATIC type, which means that this object has been created automatically by the mql5 program environment. Such objects are deleted automatically after being used.

ENUM_POINTER_TYPE

| Constant | Description |
| --- | --- |
| POINTER_INVALID | Incorrect pointer |
| POINTER_DYNAMIC | Pointer of the object created by the  new()  operator |
| POINTER_AUTOMATIC | Pointer of any objects created automatically (not using new()) |

See also

[Runtime errors](/en/docs/runtime/errors), [Object Delete Operator delete](/en/docs/basis/operators/deleteoperator), [CheckPointer](/en/docs/common/checkpointer)
