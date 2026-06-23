# Access rights

If necessary, in the description of the structure, you can use special keywords, which represent access modifiers that limit the visibility of fields from outside the structure. There are three modifiers: public, protected, and private. By default, all structure members are public, which is equivalent to the following entry (using the Result structure as an example):

```
struct Result
{
public:
   double probability;
   double coef[3];
   int direction;
   string status;
   ...
};

```

All members below the modifier receive the appropriate access rights until another modifier is encountered or the structure block ends. There can be many sections with different access rights, however, they can be modified arbitrarily.

Members marked as protected are available only from the code of this structure and descendant structures, i.e., it is assumed that they must have public methods, otherwise, no one will be able to access such fields.

Members marked as private are accessible only from within the structure's code. For example, if you add private before the status field, you will most likely need a method to read the status by external code (getStatus).

```
struct Result
{
public:
   double probability;
   double coef[3];
   int direction;
   
private:
   string status;
   
public:
   string getStatus()
   {
      return status;
   }
   ...
};

```

It will be possible to set the status only through the parameter of the second constructor. Accessing the field directly will result in the error "no access to private member 'status' of structure 'Result'":

```
// error:
// cannot access to private member 'status' declared in structure 'Result'
r.status = "message";

```

In classes, the default access is private. This follows the principle of encapsulation, which we will cover in the [Chapter on Classes](/en/book/oop/classes_and_interfaces).
