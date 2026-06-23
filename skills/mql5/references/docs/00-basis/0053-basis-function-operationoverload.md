# Operation Overloading

For ease of code reading and writing, overloading of some operations is allowed. Overloading operator is written using the keyword operator. The following operators can be overloaded:

- binary +,-,/,*,%,<<,>>,==,!=,<,>,<=,>=,=,+=,-=,/=,*=,%=,&=,|=,^=,<<=,>>=,&&,||,&,|,^
- unary +,-,++,--,!,~
- assignment operator =
- indexing operator []

Operation overloading allows the use of the operating notation (written in the form of simple expressions) for complex objects - structures and classes. Writing expressions using overloaded operations simplifies the view of the source code, because a more complex implementation is hidden.

For example, consider complex numbers, which consist of real and imaginary parts. They are widely used in mathematics. The MQL5 language has no data type to represent complex numbers, but it is possible to create a new data type in the form of a [structure or class](/en/docs/basis/types/classes). Declare the complex structure and define four methods that implement four arithmetic operations:

```
//+------------------------------------------------------------------+
//| A structure for operations with complex numbers                  |
//+------------------------------------------------------------------+
struct complex
  {
   double            re; // Real part
   double            im; // Imaginary part
   //--- Constructors
                     complex():re(0.0),im(0.0) {  }
                     complex(const double r):re(r),im(0.0) {  }
                     complex(const double r,const double i):re(r),im(i) {  }
                     complex(const complex &o):re(o.re),im(o.im) { }
   //--- Arithmetic operations
   complex           Add(const complex &l,const complex &r) const;  // Addition
   complex           Sub(const complex &l,const complex &r) const;  // Subtraction
   complex           Mul(const complex &l,const complex &r) const;  // Multiplication
   complex           Div(const complex &l,const complex &r) const;  // Division
  };

```

Now, in our code we can declare variables representing complex numbers, and work with them.

For example:

```
void OnStart()
  {
//--- Declare and initialize variables of a complex type
   complex a(2,4),b(-4,-2);
   PrintFormat("a=%.2f+i*%.2f,   b=%.2f+i*%.2f",a.re,a.im,b.re,b.im);
//--- Sum up two numbers
   complex z;
   z=a.Add(a,b);
   PrintFormat("a+b=%.2f+i*%.2f",z.re,z.im);
//--- Multiply two numbers
   z=a.Mul(a,b);
   PrintFormat("a*b=%.2f+i*%.2f",z.re,z.im);
//--- Divide two numbers
   z=a.Div(a,b);
   PrintFormat("a/b=%.2f+i*%.2f",z.re,z.im);
//---
  }

```

But it would be more convenient to use usual operators "+", "-", "*" and "/" for ordinary arithmetic operations with complex numbers.

Keyword operator is used for defining a member function that performs type conversion. Unary and binary operations for class object variables can be overloaded as non-static member functions. They implicitly act on the class object.

Most binary operations can be overloaded like regular functions that take one or both arguments as a class variable or a pointer to an object of this class. For our type complex, overloading in the declaration will look like this:

```
   //--- Operators
   complex operator+(const complex &r) const { return(Add(this,r)); }
   complex operator-(const complex &r) const { return(Sub(this,r)); }
   complex operator*(const complex &r) const { return(Mul(this,r)); }
   complex operator/(const complex &r) const { return(Div(this,r)); }

```

The full example of the script:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- Declare and initialize variables of type complex
   complex a(2,4),b(-4,-2);
   PrintFormat("a=%.2f+i*%.2f,   b=%.2f+i*%.2f",a.re,a.im,b.re,b.im);
   //a.re=5;
   //a.im=1;
   //b.re=-1;
   //b.im=-5;
//--- Sum up two numbers
   complex z=a+b;
   PrintFormat("a+b=%.2f+i*%.2f",z.re,z.im);
//--- Multiply two numbers
 
   z=a*b;
   PrintFormat("a*b=%.2f+i*%.2f",z.re,z.im);
//--- Divide two numbers
   z=a/b;
   PrintFormat("a/b=%.2f+i*%.2f",z.re,z.im);
//---
  }
//+------------------------------------------------------------------+
//| A structure for operations with complex numbers                  |
//+------------------------------------------------------------------+
struct complex
  {
   double            re; // Real part
   double            im; // Imaginary part
   //--- Constructors
                     complex():re(0.0),im(0.0) {  }
                     complex(const double r):re(r),im(0.0) {  }
                     complex(const double r,const double i):re(r),im(i) {  }
                     complex(const complex &o):re(o.re),im(o.im) { }
   //--- Arithmetic operations
   complex           Add(const complex &l,const complex &r) const;  // Addition
   complex           Sub(const complex &l,const complex &r) const;  // Subtraction
   complex           Mul(const complex &l,const complex &r) const;  // Multiplication
   complex           Div(const complex &l,const complex &r) const;  // Division
   //--- Binary operators
   complex operator+(const complex &r) const { return(Add(this,r)); }
   complex operator-(const complex &r) const { return(Sub(this,r)); }
   complex operator*(const complex &r) const { return(Mul(this,r)); }
   complex operator/(const complex &r) const { return(Div(this,r)); }
  };
//+------------------------------------------------------------------+
//| Addition                                                         |
//+------------------------------------------------------------------+
complex complex::Add(const complex &l,const complex &r) const
  {
   complex res;
//---
   res.re=l.re+r.re;
   res.im=l.im+r.im;
//--- Result
   return res;
  }
//+------------------------------------------------------------------+
//| Subtraction                                                      |
//+------------------------------------------------------------------+
complex complex::Sub(const complex &l,const complex &r) const
  {
   complex res;
//---
   res.re=l.re-r.re;
   res.im=l.im-r.im;
//--- Result
   return res;
  }
//+------------------------------------------------------------------+
//| Multiplication                                                   |
//+------------------------------------------------------------------+
complex complex::Mul(const complex &l,const complex &r) const
  {
   complex res;
//---
   res.re=l.re*r.re-l.im*r.im;
   res.im=l.re*r.im+l.im*r.re;
//--- Result
   return res;
  }
//+------------------------------------------------------------------+
//| Division                                                         |
//+------------------------------------------------------------------+
complex complex::Div(const complex &l,const complex &r) const
  {
//--- Empty complex number
   complex res(EMPTY_VALUE,EMPTY_VALUE);
//--- Check for zero
   if(r.re==0 && r.im==0)
     {
      Print(__FUNCTION__+": number is zero");
      return(res);
     }
//--- Auxiliary variables
   double e;
   double f;
//--- Selecting calculation variant
   if(MathAbs(r.im)<MathAbs(r.re))
     {
      e = r.im/r.re;
      f = r.re+r.im*e;
      res.re=(l.re+l.im*e)/f;
      res.im=(l.im-l.re*e)/f;
     }
   else
     {
      e = r.re/r.im;
      f = r.im+r.re*e;
      res.re=(l.im+l.re*e)/f;
      res.im=(-l.re+l.im*e)/f;
     }
//--- Result
   return res;
  }

```

Most unary operations for classes can be overloaded as ordinary functions that accept a single class object argument or a pointer to it. Add overloading of unary operations "-" and "!".

```
//+------------------------------------------------------------------+
//| A structure for operations with complex numbers                  |
//+------------------------------------------------------------------+
struct complex
  {
   double            re;       // Real part
   double            im;       // Imaginary part
...
   //--- Unary operators 
   complex operator-()  const; // Unary minus
   bool    operator!()  const; // Negation
  };
...
//+------------------------------------------------------------------+
//| Overloading the "unary minus" operator                           |
//+------------------------------------------------------------------+
complex complex::operator-() const
  {
   complex res;
//---
   res.re=-re;
   res.im=-im;
//--- Result
   return res;
  }
//+------------------------------------------------------------------+
//| Overloading the "logical negation" operator                      |
//+------------------------------------------------------------------+
bool complex::operator!() const
  {
//--- Are the real and imaginary parts of the complex number equal to zero?
   return (re!=0 && im!=0);
  }

```

Now we can check the value of a complex number for zero and get a negative value:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- Declare and initialize variables of type complex
   complex a(2,4),b(-4,-2);
   PrintFormat("a=%.2f+i*%.2f,   b=%.2f+i*%.2f",a.re,a.im,b.re,b.im);
//--- Divide the two numbers
   complex z=a/b;
   PrintFormat("a/b=%.2f+i*%.2f",z.re,z.im);
//--- A complex number is equal to zero by default (in the default constructor re==0 and im==0)
   complex zero;
   Print("!zero=",!zero);
//--- Assign a negative value
   zero=-z;
   PrintFormat("z=%.2f+i*%.2f,  zero=%.2f+i*%.2f",z.re,z.im, zero.re,zero.im);
   PrintFormat("-zero=%.2f+i*%.2f",-zero.re,-zero.im);
//--- Check for zero once again   
   Print("!zero=",!zero);
//---
  }

```

Note that we did not have to overload the assignment operator "=", as [structures of simple types](/en/docs/basis/types/classes#simple_structure) can be directly copied one into each other. Thus, we can now write a code for calculations involving complex numbers in the usual manner.

Overloading of the indexing operator allows to obtain the values of the arrays enclosed in an object, in a simple and familiar way, and it also contributes to a better readability of the source code. For example, we need to provide access to a symbol in the string at the specified position. A string in MQL5 is a separate type [string](/en/docs/basis/types/stringconst), which is not an array of symbols, but with the help of an overloaded indexing operation we can provide a simple and transparent work in the generated CString class:

```
//+------------------------------------------------------------------+
//| Class to access symbols in string as in array of symbols         |
//+------------------------------------------------------------------+
class CString
  {
   string            m_string;
  
public:
                     CString(string str=NULL):m_string(str) { }
   ushort operator[] (int x) { return(StringGetCharacter(m_string,x)); }
  };
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()  
  {
//--- An array for receiving symbols from a string
   int     x[]={ 19,4,18,19,27,14,15,4,17,0,19,14,17,27,26,28,27,5,14,
                 17,27,2,11,0,18,18,27,29,30,19,17,8,13,6 };
   CString str("abcdefghijklmnopqrstuvwxyz[ ]CS");
   string  res;
//--- Make up a phrase using symbols from the str variable
   for(int i=0,n=ArraySize(x);i<n;i++)
     {
      res+=ShortToString(str[x[i]]);
     }
//--- Show the result
   Print(res);
  }

```

Another example of overloading of the indexing operation is operations with matrices. The matrix represents a two-dimensional dynamic array, the array size is not defined in advance. Therefore, you cannot declare an array of form array[][] without specifying the size of the second dimension, and then pass this array as a parameter. A possible solution is a special class CMatrix, which contains an array of CRow class objects.

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- Operations of addition and multiplication of matrices
   CMatrix A(3),B(3),C();
//--- Prepare an array for rows
   double a1[3]={1,2,3}, a2[3]={2,3,1}, a3[3]={3,1,2};
   double b1[3]={3,2,1}, b2[3]={1,3,2}, b3[3]={2,1,3};
//--- Fill the matrices
   A[0]=a1; A[1]=a2; A[2]=a3;
   B[0]=b1; B[1]=b2; B[2]=b3;
//--- Output the matrices in the Experts log
   Print("---- Elements of matrix A");
   Print(A.String());
   Print("---- Elements of matrix B");
   Print(B.String());
 
//--- Addition of matrices
   Print("---- Addition of matrices A and B");
   C=A+B;
//--- Output the formatted string representation
   Print(C.String());
 
//--- Multiplication of matrices
   Print("---- Multiplication of matrices A and B");
   C=A*B;
   Print(C.String());
 
//--- Now we show how to get values in the style of dynamic arrays matrix[i][j]
   Print("Output the values of matrix C elementwise");
//--- Go through the matrix rows - CRow objects - in a loop
   for(int i=0;i<3;i++)
     {
      string com="| ";
      //--- Form rows from the matrix for the value
      for(int j=0;j<3;j++)
        {
         //--- Get the matrix element by the number of the row and column
         double element=C[i][j];// [i] - Access to CRow in the array m_rows[] ,
                                // [j] - Overloaded operator of indexing in CRow
         com=com+StringFormat("a(%d,%d)=%G ; ",i,j,element);
        }
      com+="|";
      //--- Output the values of the row
      Print(com);
     }
  }
//+------------------------------------------------------------------+
//| Class "Row"                                                      |
//+------------------------------------------------------------------+
class CRow
  {
private:
   double            m_array[];
public:
   //--- Constructors and a destructor
                     CRow(void)          { ArrayResize(m_array,0);    }
                     CRow(const CRow &r) { this=r;                    }
                     CRow(const double &array[]);
                    ~CRow(void){};
   //--- Number of elements in the row
   int               Size(void) const    { return(ArraySize(m_array));}
   //--- Returns a string with values  
   string            String(void) const;
   //--- Indexing operator
   double            operator[](int i) const  { return(m_array[i]);   }
   //--- Assignment operators
   void              operator=(const double  &array[]); // An array
   void              operator=(const CRow & r);         // Another CRow object
   double            operator*(const CRow &o);          // CRow object for multiplication
  };
//+------------------------------------------------------------------+
//| Constructor for initializing a row with an array                 |
//+------------------------------------------------------------------+
void  CRow::CRow(const double &array[])
  {
   int size=ArraySize(array);
//--- If the array is not empty
   if(size>0)
     {
      ArrayResize(m_array,size);
      //--- Fill with values
      for(int i=0;i<size;i++)
         m_array[i]=array[i];
     }
//---
  }
//+------------------------------------------------------------------+
//| Assignment operation for the array                               |
//+------------------------------------------------------------------+
void CRow::operator=(const double &array[])
  {
   int size=ArraySize(array);
   if(size==0) return;
//--- Fill the array with values
   ArrayResize(m_array,size);
   for(int i=0;i<size;i++) m_array[i]=array[i];
//--- 
  }
//+------------------------------------------------------------------+
//| Assignment operation for CRow                                    |
//+------------------------------------------------------------------+
void CRow::operator=(const CRow  &r)
  {
   int size=r.Size();
   if(size==0) return;
//--- Fill the array with values
   ArrayResize(m_array,size);
   for(int i=0;i<size;i++) m_array[i]=r[i];
//--- 
  }
//+------------------------------------------------------------------+
//| Operator of multiplication by another row                        |
//+------------------------------------------------------------------+
double CRow::operator*(const CRow &o)
  {
   double res=0;
//--- Verifications
   int size=Size();
   if(size!=o.Size() || size==0)
     {
      Print(__FUNCSIG__,": Failed to multiply two matrices, their sizes are different");
      return(res);
     }
//--- Multiply arrays elementwise and add the products
   for(int i=0;i<size;i++)
      res+=m_array[i]*o[i];
//--- Result
   return(res);
  }
//+------------------------------------------------------------------+
//| Returns a formatted string representation                        |
//+------------------------------------------------------------------+
string CRow::String(void) const
  {
   string out="";
//--- If the size of the array is greater than zero
   int size=ArraySize(m_array);
//--- We work only with a non-zero number of array elements
   if(size>0)
     {
      out="{";
      for(int i=0;i<size;i++)
        {
         //--- Collect the values to a string
         out+=StringFormat(" %G;",m_array[i]);
        }
      out+=" }";
     }
//--- Result
   return(out);
  }
//+------------------------------------------------------------------+
//| Class "Matrix"                                                   |
//+------------------------------------------------------------------+
class CMatrix
  {
private:
   CRow              m_rows[];
 
public:
   //--- Constructors and a destructor
                     CMatrix(void);
                     CMatrix(int rows)  { ArrayResize(m_rows,rows);             }
                    ~CMatrix(void){};
   //--- Get the matrix sizes
   int               Rows()       const { return(ArraySize(m_rows));            }
   int               Cols()       const { return(Rows()>0? m_rows[0].Size():0); }
   //--- Returns the value of the column in the form of a CRow row
   CRow              GetColumnAsRow(const int col_index) const;
   //--- Returns a string with the matrix values 
   string            String(void) const;
   //--- The indexing operator returns a string by its number
   CRow *operator[](int i) const        { return(GetPointer(m_rows[i]));        }
   //--- Addition operator
   CMatrix           operator+(const CMatrix &m);
   //--- Multiplication operator
   CMatrix           operator*(const CMatrix &m);
   //--- Assignment operator
   CMatrix          *operator=(const CMatrix &m);
  };
//+------------------------------------------------------------------+
//| A default constructor, create an array of rows of zero size      |
//+------------------------------------------------------------------+
CMatrix::CMatrix(void)
  {
//--- The zero number of rows in the matrix
   ArrayResize(m_rows,0);
//---  
  }
//+------------------------------------------------------------------+
//| Returns the column value in the form of CRow                     |
//+------------------------------------------------------------------+
CRow  CMatrix::GetColumnAsRow(const int col_index) const
  {
//--- A variable to get the values from the column
   CRow row();
//--- The number of rows in the matrix
   int rows=Rows();
//--- If the number of rows is greater than zero, execute the operation
   if(rows>0)
     {
      //--- An array to receive the values of the column with index col_index
      double array[];
      ArrayResize(array,rows);
      //--- Filling the array
      for(int i=0;i<rows;i++)
        {
         //--- Check the number of the column for row i - it may exceed the boundaries of the array
         if(col_index>=this[i].Size())
           {
            Print(__FUNCSIG__,": Error! Column number ",col_index,"> row size ",i);
            break; // row will be uninitialized object
           }
         array[i]=this[i][col_index];
        }
      //--- Create a CRow row based on the array values
      row=array;
     }
//--- Result
   return(row);
  }
//+------------------------------------------------------------------+
//| Addition of two matrices                                         |
//+------------------------------------------------------------------+
CMatrix CMatrix::operator+(const CMatrix &m)
  {
//--- The number of rows and columns in the passed matrix
   int cols=m.Cols();
   int rows=m.Rows();
//--- The matrix to receive the addition results 
   CMatrix res(rows);
//--- The sizes of the matrix must match
   if(cols!=Cols() || rows!=Rows())
     {
      //--- Addition impossible
      Print(__FUNCSIG__,": Failed to add two matrices, their sizes are different");
      return(res);
     }
//--- Auxiliary array
   double arr[];
   ArrayResize(arr,cols);
//--- Go through rows to add
   for(int i=0;i<rows;i++)
     {
      //--- Write the results of addition of matrix strings in the array
      for(int k=0;k<cols;k++)
        {
         arr[k]=this[i][k]+m[i][k];
        }
      //--- Place the array to the matrix row
      res[i]=arr;
     }
//--- return the result of addition of matrices
   return(res);
  }
//+------------------------------------------------------------------+
//| Multiplication of two matrices                                   |
//+------------------------------------------------------------------+
CMatrix CMatrix::operator*(const CMatrix &m)
  {
//--- Number of columns of the first matrix, number of rows passed in the matrix
   int cols1=Cols();
   int rows2=m.Rows();
   int rows1=Rows();
   int cols2=m.Cols();
//--- Matrix to receive the addition result
   CMatrix res(rows1);
//--- Matrices should be coordinated
   if(cols1!=rows2)
     {
      //--- Multiplication impossible
      Print(__FUNCSIG__,": Failed to multiply two matrices, format is not compatible "
            "- number of columns in the first factor should be equal to the number of rows in the second");
      return(res);
     }
//--- Auxiliary array
   double arr[];
   ArrayResize(arr,cols1);
//--- Fill the rows in the multiplication matrix
   for(int i=0;i<rows1;i++)// Go through rows
     {
      //--- Reset the receiving array
      ArrayInitialize(arr,0);
      //--- Go through elements in the row
      for(int k=0;k<cols1;k++)
        {
         //--- Take values of column k of the matrix m in the for of CRow
         CRow column=m.GetColumnAsRow(k);
         //--- Multiply two rows and write the result of scalar multiplication of vectors in the i-th element
         arr[k]=this[i]*column;
        }
      //--- place array arr[] in the i-th row of the matrix
      res[i]=arr;
     }
//--- Return the product of two matrices
   return(res);
  }
//+------------------------------------------------------------------+
//| Assignment operation                                             |
//+------------------------------------------------------------------+
CMatrix *CMatrix::operator=(const CMatrix &m)
  {
//--- Find and set the number of rows
   int rows=m.Rows();
   ArrayResize(m_rows,rows);
//--- Fill our rows with the values of rows of  the passed matrix
   for(int i=0;i<rows;i++) this[i]=m[i];
//---
   return(GetPointer(this));
  }
//+------------------------------------------------------------------+
//| String representation of the matrix                              |
//+------------------------------------------------------------------+
string CMatrix::String(void) const
  {
   string out="";
   int rows=Rows();
//--- Form string by string
   for(int i=0;i<rows;i++)
     {
      out=out+this[i].String()+"\r\n";
     }
//--- Result
   return(out);
  }

```

See also

[Overloading](/en/docs/basis/oop/overload), [Arithmetic Operations](/en/docs/basis/operations/mathoperation), [Function Overloading](/en/docs/basis/function/functionoverload), [Precedence Rules](/en/docs/basis/operations/rules)
