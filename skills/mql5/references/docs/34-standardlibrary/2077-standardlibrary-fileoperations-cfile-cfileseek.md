# Seek

Sets file pointer's position.

```
void  Seek(
   long                offset,     // offset
   ENUM_FILE_POSITION  origin      // origin
   )

```

Parameters

offset

[in]  File offset in bytes (can be negative).

origin

[in]  Origin of the offset.

Return Value

true - successful, false - cannot change the file pointer.
