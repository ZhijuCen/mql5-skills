# Virtual Functions

The virtual keyword is the function specifier, which provides a mechanism to select dynamically at runtime an appropriate function-member among the functions of basic and derived classes. Structures cannot have virtual functions. It can be used to change the [declarations](/en/docs/basis/function#function_declaration) for function-members only.

The virtual function, like an ordinary function, must have an [executable body](/en/docs/basis/function#function_body). When called, its semantic is the same as that of other functions.

A virtual function may be overridden in a derived class. The choice of what [function definition](/en/docs/basis/function#function_definition) should be called for a virtual function is made dynamically (at runtime). A typical case is when a base class contains a virtual function, and derived classes have their own versions of this function.

The pointer to the base class can indicate either a base class object or the object of a derived class. The choice of the member-function to call will be performed at runtime and will depend on the type of the object, not the type of the pointer. If there is no member of a derived type, the virtual function of the base class is used by default.

[Destructors](/en/docs/basis/types/classes#destructor) are always virtual, regardless of whether they are declared with the virtual keyword or not.

Let's consider the use of virtual functions on the example of MT5_Tetris.mq5. The base class CTetrisShape with the virtual function Draw is defined in the included file MT5_TetrisShape.mqh.

```
//+------------------------------------------------------------------+
class CTetrisShape
  {
protected:
   int               m_type;
   int               m_xpos;
   int               m_ypos;
   int               m_xsize;
   int               m_ysize;
   int               m_prev_turn;
   int               m_turn;
   int               m_right_border;
public:
   void              CTetrisShape();
   void              SetRightBorder(int border) { m_right_border=border; }
   void              SetYPos(int ypos)          { m_ypos=ypos;           }
   void              SetXPos(int xpos)          { m_xpos=xpos;           }
   int               GetYPos()                  { return(m_ypos);        }
   int               GetXPos()                  { return(m_xpos);        }
   int               GetYSize()                 { return(m_ysize);       }
   int               GetXSize()                 { return(m_xsize);       }
   int               GetType()                  { return(m_type);        }
   void              Left()                     { m_xpos-=SHAPE_SIZE;    }
   void              Right()                    { m_xpos+=SHAPE_SIZE;    }
   void              Rotate()                   { m_prev_turn=m_turn; if(++m_turn>3) m_turn=0; }
   virtual void      Draw()                     { return;                }
   virtual bool      CheckDown(int& pad_array[]);
   virtual bool      CheckLeft(int& side_row[]);
   virtual bool      CheckRight(int& side_row[]);
  };

```

Further, for each derived class, this function is implemented in accordance with characteristics of a descendant class. For example, the first shape CTetrisShape1 has its own implementation of the Draw() function:

```
class CTetrisShape1 : public CTetrisShape
  {
public:
   //--- shape drawing
   virtual void      Draw()
     {
      int    i;
      string name;
      //---
      if(m_turn==0 || m_turn==2)
        {
         //--- horizontal
         for(i=0; i<4; i++)
           {
            name=SHAPE_NAME+(string)i;
            ObjectSetInteger(0,name,OBJPROP_XDISTANCE,m_xpos+i*SHAPE_SIZE);
            ObjectSetInteger(0,name,OBJPROP_YDISTANCE,m_ypos);
           }
        }
      else
        {
         //--- vertical
         for(i=0; i<4; i++)
           {
            name=SHAPE_NAME+(string)i;
            ObjectSetInteger(0,name,OBJPROP_XDISTANCE,m_xpos);
            ObjectSetInteger(0,name,OBJPROP_YDISTANCE,m_ypos+i*SHAPE_SIZE);
           }
        }
     }
  }

```

The Square shape is described by class CTetrisShape6 and has its own implementation of the Draw() method:

```
class CTetrisShape6 : public CTetrisShape
  {
public:
   //--- Shape drawing
   virtual void      Draw()
     {
      int    i;
      string name;
      //---
      for(i=0; i<2; i++)
        {
         name=SHAPE_NAME+(string)i;
         ObjectSetInteger(0,name,OBJPROP_XDISTANCE,m_xpos+i*SHAPE_SIZE);
         ObjectSetInteger(0,name,OBJPROP_YDISTANCE,m_ypos);
        }
      for(i=2; i<4; i++)
        {
         name=SHAPE_NAME+(string)i;
         ObjectSetInteger(0,name,OBJPROP_XDISTANCE,m_xpos+(i-2)*SHAPE_SIZE);
         ObjectSetInteger(0,name,OBJPROP_YDISTANCE,m_ypos+SHAPE_SIZE);
        }
     }
  };

```

Depending on the class, to which the created object belongs, it calls the virtual function of this or that derived class.

```
void CTetrisField::NewShape()
  {
//--- creating one of the 7 possible shapes randomly
   int nshape=rand()%7;
   switch(nshape)
     {
      case 0: m_shape=new CTetrisShape1; break;
      case 1: m_shape=new CTetrisShape2; break;
      case 2: m_shape=new CTetrisShape3; break;
      case 3: m_shape=new CTetrisShape4; break;
      case 4: m_shape=new CTetrisShape5; break;
      case 5: m_shape=new CTetrisShape6; break;
      case 6: m_shape=new CTetrisShape7; break;
     }
//--- draw
   m_shape.Draw();
//---
  }

```

## Modifier 'override'  #

The 'override' modifier means that the declared function must override the method of a parent class. Use of this method allows you to avoid overriding errors, for example it allows you to avoid accidental modification of the method signature. Suppose, the 'func' method is defined in the base class. The method accepts an int variable as an argument:

```
class CFoo
  {
   void virtual func(int x) const { }
  };

```

Next, the method is overridden in the child class:

```
class CBar : public CFoo
  {
   void func(short x) { }
  };

```

However, the argument type is mistakenly changed from int to short. In fact, this is not method overriding, but it is method overloading. Acting in accordance with the [overloaded function defining algorithm](/en/docs/basis/function/functionoverload), the compiler can in certain situations choose a method defined in the base class instead of the overridden method.

In order to avoid such errors, you should explicitly add the 'override' modifier to the method you want to override.

```
class CBar : public CFoo
  {
   void func(short x) override { }
  };

```

If the method signature is changed during overriding, the compiler will not be able to find a method with the same signature in the parent class, and it will return a compilation error:

```
'CBar::func' method is declared with 'override' specifier but does not override any base class method

```

## Modifier 'final'  #

The 'final' modifier does the opposite — it prohibits method overriding in child classes. If a method implementation is sufficient and fully complete, declare this method with the 'final' modifier so as to make sure that it will not be modified later.

```
class CFoo
  {
   void virtual func(int x) final { }
  };
 
class CBar : public CFoo
  {
   void func(int) { }
  };
 

```

If you try to override a method with the 'final' modifier as shown in the above example, the compiler will return an error:

```
'CFoo::func' method declared as 'final' cannot be overridden by 'CBar::func'
see declaration of 'CFoo::func'

```

See also

[Standard Library](/en/docs/standardlibrary)
