# Sort

Sort a matrix or vector in place.

```
void vector::Sort(
  func_name  compare_func=NULL,  // comparison function
  T          context             // parameter for the custom sort function
   );
 
void matrix::Sort(
  func_name  compare_func=NULL   // comparison function
  T          context             // parameter for the custom sort function
   );
 
void matrix::Sort(
  const int  axis,               // axis for sorting
  func_name  compare_func=NULL   // comparison function
  T          context             // parameter for the custom sort function
   );

```

Parameters

axis

[in]  The axing along which to sort: 0 is horizontal, 1 is vertical.

func_name

[in]  Comparator. You can specify one of the values of the [ENUM_SORT_MODE](/en/docs/matrix/matrix_types/matrix_enumerations#enum_sort_mode) enumeration or your own comparison function. If no function is specified, ascending sort is used.  

   

A custom comparison function can be of two types:

- int comparator(T x1,T x2)
- int comparator(T x1,T x2,TContext context)

Here T is the type of matrix or vector, and TContex is the type of the 'context' variable which is passed as an additional parameter to the Sort method.

context

[in] Additional optional parameter that can be passed to a custom sort function.

Return Value

None. Sorting is performed in place, i.e. it is applied to the data of the matrix/vector for which the Sort method is called.

Example

```
//+------------------------------------------------------------------+
//| Sort function                                                    |
//+------------------------------------------------------------------+
int MyDoubleComparator(double x1,double x2,int sort_mode=0)
  {
   int res=x1<x2 ? -1 : (x1>x2 ? 1 : 0);
   return(sort_mode==0 ? res : -res);
  }
//+------------------------------------------------------------------+
//| Script start function                                            |
//+------------------------------------------------------------------+
void OnStart()
  {
   //--- fill the vector
   vector v(100);
   //--- sort ascending
   v.Sort(MyDoubleComparator);   // an additional parameter with the default value '0' is used here
   Print(v);
   // sort descending
   v.Sort(MyDoubleComparator,1); // here the additional parameter '1' is explicitly specified by the user
   Print(v);
  }

```
