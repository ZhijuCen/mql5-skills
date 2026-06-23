# Size

Return the size of vector.

```
ulong vector::Size()

```

Return Value

Integer.

Example

```
  matrix m={{1,2,3,4,5,6,7,8,9,10,11,12}};
  m.Reshape(3,4);
  Print("matrix m\n",m);
  vector v=m.Row(1);
  Print("v.Size()=",v.Size());
  Print("v=",v);
 
 
  /*
   matrix m
   [[1,2,3,4]
    [5,6,7,8]
    [9,10,11,12]]
   v.Size()=4
   v=[5,6,7,8]  
  */

```
