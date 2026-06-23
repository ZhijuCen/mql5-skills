# Operator overloading

In the [Expressions](/en/book/basis/expressions) chapter, we learned about various operations defined for built-in types. For example, for variables of type double, we could evaluate the following expression:

```
double a = 2.0, b = 3.0, c = 5.0;
double d = a * b + c;

```

It would be convenient to use a similar syntax when working with user-defined types, such as matrices:

```
Matrix a(3, 3), b(3, 3), c(3, 3); // creating 3x3 matrices
// ... somehow fill in a, b, c
Matrix d = a * b + c;

```

MQL5 provides such an opportunity due to operator overloading.

This technique is organized by describing methods with a name beginning with the keyword operator and then containing a symbol (or sequence of symbols) of one of the supported operations. In a generalized form, this can be represented as follows:

```
result_type operator@ ( [type parameter_name] );

```

Here @ - operation's symbol(s).

The complete list of MQL5 operations has been provided in the section [Operation Priorities](/en/book/basis/expressions/operators_precedence), however, not all of them are allowed for overloading.

Forbidden for overloading:

- colons '::', context permission;
- parentheses '()', "function call" or "grouping";
- dot '.', "dereference";
- ampersand '&', "taking address", unary operator (however, the ampersand is available as binary operator "bitwise AND");
- conditional ternary '?:';
- comma ','.

All other operators are available for overloading. Overloading operator priorities cannot be changed, they remain equal to the standard precedence, so grouping with parentheses should be used if necessary.

You cannot create an overload for some new character that is not included in the standard list.

All operators are overloaded taking into account their unarity and binarity, that is, the number of required operands is preserved. Like any class method, operator overloading can return a value of some type. In this case, the type itself should be chosen based on the planned logic of using the result of the function in expressions (see further along).

Operator overloading methods have the following form (instead of the '@' symbol, the symbol(s) of the required operator is substituted):

| Name | Method header | Using  
  in an expression | Function 
 is equivalent to |
| --- | --- | --- | --- |
| unary prefix | type operator@() | @object | object.operator@() |
| unary postfix | type operator@(int) | object@ | object.operator@(0) |
| binary | type operator@(type parameter_name) | object@argument | object.operator@(argument) |
| index | type operator[](type index_name) | object[argument] | object.operator[](argument) |

Unary operators do not take parameters. Of the unary operators, only the increment '++' and decrement '--' operators support the postfix form in addition to the prefix form, all other unary operators only support the prefix form. Specifying an anonymous parameter of type int is used to denote the postfix form (to distinguish it from the prefix form), but the parameter itself is ignored.

Binary operators must take one parameter. For the same operator, several overloaded variants are possible with a parameter of a different type, including the same type as the class of the current object. In this case, objects as parameters can only be passed by reference or by pointer (the latter is only for class objects, but not structures).

Overloaded operators can be used both via the syntax of operations as part of expressions (which is the primary reason for overloading) and the syntax of method calls; both options are shown in the table above. The functional equivalent makes it more obvious that technically speaking, an operator is nothing more than a method call on an object, with the object to the right of the prefix operator and to the left of the symbol for all others. The binary operator method will be passed as an argument the value or expression that is to the right of the operator (this can be, in particular, another object or variable of a built-in type).

It follows that overloaded operators do not have the commutativity property: a@b is not generally equal to b@a, because for a the @ operator may be overloaded, but b is not. Moreover, if b is a variable or value of a built-in type, then in principle you cannot overload the standard behavior for it.

As a first example, consider the class Fibo for generating numbers from the Fibonacci series (we have already done one implementation of this task using functions, see [Function definition](/en/book/basis/functions/functions_definition)). In the class, we will provide 2 fields for storing the current and previous number of the row: current and previous, respectively. The default constructor will initialize them with the values ​​1 and 0. We will also provide a copy constructor (FiboMonad.mq5).

```
class Fibo
{
   int previous;
   int current;
public:
   Fibo() : current(1), previous(0) { }
   Fibo(const Fibo &other) : current(other.current), previous(other.previous) { }
   ...
};

```

The initial state of the object: the current number is 1, and the previous one is 0. To find the next number in the series, we overload the prefix and postfix increment operators.

```
   Fibo *operator++() // prefix
   {
      int temp = current;
      current = current + previous;
      previous = temp;
      return &this;
   }
   
   Fibo operator++(int) // postfix
   {
      Fibo temp = this;
      ++this;
      return temp;
   }

```

Please note that the prefix method does not return a pointer to the current object Fibo after the number has been modified, but the postfix method returns to a new object with the previous counter saved, which corresponds to the principles of postfix increment.

If necessary, the programmer, of course, can overload any operation in an arbitrary way. For example, it is possible to calculate the product, output the number to the log, or do something else in the implementation of the increment. However, it is recommended to stick to the approach where operator overloading performs intuitive actions.

We implement decrement operations in a similar way: they will return the previous number of the series.

```
   Fibo *operator--() // prefix
   {
      int diff = current - previous;
      current = previous;
      previous = diff;
      return &this;
   }
   
   Fibo operator--(int) // postfix
   {
      Fibo temp = this;
      --this;
      return temp;
   }

```

To get a number from a series by a given number, we will overload the index access operation.

```
   Fibo *operator[](int index)
   {
      current = 1;
      previous = 0;
      for(int i = 0; i < index; ++i)
      {
         ++this;
      }
      return &this;
   }

```

To get the current number contained in the current variable, let's overload the '~' operator (since it is rarely used).

```
   int operator~() const
   {
      return current;
   }

```

Without this overload, you would still need to implement some public method to read the private field current. We will use this operator to output numbers with Print.

You should also overload the assignment for convenience.

```
   Fibo *operator=(const Fibo &other)
   {
      current = other.current;
      previous = other.previous;
      return &this;
   }
   
   Fibo *operator=(const Fibo *other)
   {
      current = other.current;
      previous = other.previous;
      return &this;
   }

```

Let's check, how it all works.

```
void OnStart()
{
   Fibo f1, f2, f3, f4;
   for(int i = 0; i < 10; ++i, ++f1) // prefix increment
   {
      f4 = f3++; // postfix increment and assignment overloading
   }
   
   // compare all values ​​obtained by increments and by index [10]
   Print(~f1, " ", ~f2[10], " ", ~f3, " ", ~f4); // 89 89 89 55
   
   // counting in opposite direction, down to 0
   Fibo f0;
   Fibo f = f0[10]; // copy constructor (due to initialization)
   for(int i = 0; i < 10; ++i)
   {
      // prefix decrement
      Print(~--f); // 55, 34, 21, 13, 8, 5, 3, 2, 1, 1
   }
}

```

The results are as expected. Still, we have to consider one detail.

```
   Fibo f5;
   Fibo *pf5 = &f5;
   
   f5 = f4;   // call Fibo *operator=(const Fibo &other) 
   f5 = &f4;  // call Fibo *operator=(const Fibo *other)
   pf5 = &f4; // calls nothing, assigns &f4 to pf5!

```

Overloading the assignment operator for a pointer only works when accessed via an object. If the access goes via a pointer, then there is a standard assignment of one pointer to another.

The return type of an overloaded operator can be one of the built-in types, an object type (of a class or structure), or a pointer (for class objects only).

To return an object (an instance, not a reference), the class must implement a copy constructor. This way will cause instance duplication, which can affect the efficiency of the code. If possible, you should return a pointer.

However, when returning a pointer, you need to make sure that it is not returning a local automatic object (which will be deleted when the function exits, and the pointer will become invalid), but some already existing one - as a rule, &this is returned.

Returning an object or a pointer to an object allows you to "send" the result of one overloaded operator to another, and thereby construct complex expressions in the same way as we are accustomed to doing with built-in types. Returning void will make it impossible to use the operator in expressions. For example, if the '=' operator is defined with type void, then the multiple assignment will stop working:

```
Type x, y, z = 1; // constructors and initialization of variables of a certain class
x = y = z; // assignments, compilation error 

```

The assignment chain runs from right to left, and y = z will return empty.

If objects contain fields of built-in types only (including arrays), then the assignment/copy operator '=' from objects of the same class does not need to be redefined: MQL5 provides "one-to-one" copying of all fields by default. The assignment/copy operator should not be confused with the copy constructor and initialization.

Now let's turn to the second example: working with matrices(Matrix.mq5).

Note, by the way, that the built-in object types [matrices and vectors](/en/book/common/matrices) have recently appeared in MQL5. Whether to use built-in types or your own (or maybe combine them) is the choice of each developer. Ready-made and fast implementation of many popular methods in built-in types is convenient and eliminates routine coding. On the other hand, custom classes allow you to adapt algorithms to your tasks. Here we provide the class Matrix as a tutorial.

In the matrix class, we will store its elements in a one-dimensional dynamic array m. Under the sizes, select the variables rows and columns.

```
class Matrix
{
protected:
   double m[];
   int rows;
   int columns;
   void assign(const int r, const int c, const double v)
   {
      m[r * columns + c] = v;
   }
      
public:
   Matrix(const Matrix &other) : rows(other.rows), columns(other.columns)
   {
      ArrayCopy(m, other.m);
   }
   
   Matrix(const int r, const int c) : rows(r), columns(c)
   {
      ArrayResize(m, rows * columns);
      ArrayInitialize(m, 0);
   }

```

The main constructor takes two parameters (matrix dimensions) and allocates memory for the array. There is also a copy constructor from the other matrix other. Here and below, built-in functions for working with arrays are massively used (in particular, ArrayCopy, ArrayResize, ArrayInitialize) — they will be considered in a separate [chapter](/en/book/common/arrays).

We organize the filling of elements from an external array by overloading the assignment operator:

```
   Matrix *operator=(const double &a[])
   {
      if(ArraySize(a) == ArraySize(m))
      {
         ArrayCopy(m, a);
      }
      return &this;
   }

```

To implement the addition of two matrices, we overload the operations '+=' and '+':

```
   Matrix *operator+=(const Matrix &other)
   {
      for(int i = 0; i < rows * columns; ++i)
      {
         m[i] += other.m[i];
      }
      return &this;
   }
   
   Matrix operator+(const Matrix &other) const
   {
      Matrix temp(this);
      return temp += other;
   }

```

Note that the operator '+=' returns a pointer to the current object after it has been modified, while the operator '+' returns a new instance by value (the copy constructor will be used), and the operator itself has the const modifier, so how does not change the current object.

The operator '+' is essentially a wrapper that delegates all the work to the operator '+=', having previously created a temporary copy of the current matrix under the name temp to call it. Thus, temp is added to other by an internal call to the operator '+=' (with temp being modified) and then returned as the result of the ' +'.

Matrix multiplication is overloaded similarly, with two operators '*=' and '*'.

```
   Matrix *operator*=(const Matrix &other)
   {
      // multiplication condition: this.columns == other.rows
     // the result will be a matrix of size this.rows by other.columns
      Matrix temp(rows, other.columns);
      
      for(int r = 0; r < temp.rows; ++r)
      {
         for(int c = 0; c < temp.columns; ++c)
         {
            double t = 0;
            //we add up the pairwise products of the i-th elements
           // row 'r' of the current matrix and column 'c' of the matrix other
            for(int i = 0; i < columns; ++i)
            {
               t += m[r * columns + i] * other.m[i * other.columns + c];
            }
            temp.assign(r, c, t);
         }
      }
      // copy the result to the current object of the matrix this
      this = temp; // calling an overloaded assignment operator
      return &this;
   }
   
   Matrix operator*(const Matrix &other) const
   {
      Matrix temp(this);
      return temp *= other;
   }

```

Now, we multiply the matrix by a number:

```
   Matrix *operator*=(const double v)
   {
      for(int i = 0; i < ArraySize(m); ++i)
      {
         m[i] *= v;
      }
      return &this;
   }
   
   Matrix operator*(const double v) const
   {
      Matrix temp(this);
      return temp *= v;
   }

```

To compare two matrices, we provide the operators '==' and '!=':

```
   bool operator==(const Matrix &other) const
   {
      return ArrayCompare(m, other.m) == 0;
   }
   
   bool operator!=(const Matrix &other) const
   {
      return !(this == other);
   }

```

For debugging purposes, we implement the output of the matrix array to the log.

```
   void print() const
   {
      ArrayPrint(m);
   }

```

In addition to the described overloads, the class Matrix additionally has an overload of the operator []: it returns an object of the nested class MatrixRow, i.e., a row with a given number.

```
   MatrixRow operator[](int r)
   {
      return MatrixRow(this, r);
   }

```

The class MatrixRow itself provides more "deep" access to the elements of the matrix by overloading the same operator [] (that is, for a matrix, it will be possible to naturally specify two indexes m[i][j]).

```
   class MatrixRow
   {
   protected:
      const Matrix *owner;
      const int row;
      
   public:
      class MatrixElement
      {
      protected:
         const MatrixRow *row;
         const int column;
         
      public:
         MatrixElement(const MatrixRow &mr, const int c) : row(&mr), column(c) { }
         MatrixElement(const MatrixElement &other) : row(other.row), column(other.column) { }
         
         double operator~() const
         {
            return row.owner.m[row.row * row.owner.columns + column];
         }
         
         double operator=(const double v)
         {
            row.owner.m[row.row * row.owner.columns + column] = v;
            return v;
         }
      };
   
      MatrixRow(const Matrix &m, const int r) : owner(&m), row(r) { }
      MatrixRow(const MatrixRow &other) : owner(other.owner), row(other.row) { }
      
      MatrixElement operator[](int c)
      {
         return MatrixElement(this, c);
      }
   
      double operator[](uint c)
      {
         return owner.m[row * owner.columns + c];
      }
   };

```

The operator [] for a type parameter int returns an object of class MatrixElement, through which you can write a specific element in the array. To read an element, the operator [] is used with a type parameter uint. This seems like a trick, but this is a language limitation: overloads must differ in the parameter type. As an alternative to reading an element, the class MatrixElement provides an overload of the operator '~'.

When working with matrices, you often need an identity matrix, so let's create a derived class for it:

```
class MatrixIdentity : public Matrix
{
public:
   MatrixIdentity(const int n) : Matrix(n, n)
   {
      for(int i = 0; i < n; ++i)
      {
         m[i * rows + i] = 1;
      }
   }
};

```

Now let's try matrix expressions in action.

```
void OnStart()
{
   Matrix m(2, 3), n(3, 2); // description
   MatrixIdentity p(2);     // identity matrix
   
   double ma[] = {-1,  0, -3,
                   4, -5,  6};
   double na[] = {7,  8,
                  9,  1,
                  2,  3};
   m = ma; // filling in data
   n = na;
   
   //we can read and write elements separately
   m[0][0] = m[0][(uint)0] + 2; // variant 1 
   m[0][1] = ~m[0][1] + 2;      // variant 2 
   
   Matrix r = m * n + p;                    // expression
   Matrix r2 = m.operator*(n).operator+(p); // equivalent
   Print(r == r2); // true
   
   m.print(); // 1.00000  2.00000 -3.00000  4.00000 -5.00000  6.00000
   n.print(); // 7.00000 8.00000 9.00000 1.00000 2.00000 3.00000
   r.print(); // 20.00000  1.00000 -5.00000  46.00000
}

```

Here we have created 2 matrices of 3 by 2 and 2 by 3 dimensions, respectively, then filled them with values ​​from arrays and edited the selective element using the syntax of two indexes [][]. Finally, we calculated the expression m * n + p, where all operands are matrices. The line below shows the same expression in the form of method calls. We've got the same results.

Unlike C++, MQL5 does not support operator overloading at the global level. In MQL5, an operator can only be overloaded in the context of a class or structure, that is, using their method. Also, MQL5 does not support overloading of type casting, operators new and delete.
