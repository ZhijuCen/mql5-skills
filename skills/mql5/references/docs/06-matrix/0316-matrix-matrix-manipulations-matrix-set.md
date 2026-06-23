# Set

Sets the value for a vector element by the specified index.

```
bool vector::Set(
  ulong   index,     // element index
  double  value      // value
   );

```

Parameters

index

[in]  Index of the element the value needs to be set for.

value

[in]  Value.

Return Value

Returns true if successful, otherwise - false.

Note

The Set method does the same thing as assigning a value using square brackets, namely: vector[index]=value. The method has been added to simplify transferring a code from languages where this type of notation is used. The example below shows both options for filling the vector with values by the specified index.

Example:

```
void OnStart()
  {
//---
   vector v1(10, VectorAssignValues);
   Print("v1 = ", v1);
 
   vector v2(10, VectorSetValues);
   Print("v2 = ", v2);
  }
 /* Result
  v1 = [1,2,4,8,16,32,64,128,256,512]
  v2 = [1,2,4,8,16,32,64,128,256,512]
  */
//+-------------------------------------------------------------------------+
//| Fill a vector with powers of a number through the assignment operation  |
//+-------------------------------------------------------------------------+
void VectorAssignValues(vector& v, double initial=1)
  {
   double value=initial;
   for(ulong k=0; k<v.Size(); k++)
     {
      v[k]=value;
      value*=2;
     }
  }
//+--------------------------------------------------------------------------+
//| Fill a vector with powers of a number using the Set method               |
//+--------------------------------------------------------------------------+
void VectorSetValues(vector& v, double initial=1)
  {
   double value=initial;
   for(ulong k=0; k<v.Size(); k++)
     {
      v.Set(k, value);
      value*=2;
     }
  }

```
