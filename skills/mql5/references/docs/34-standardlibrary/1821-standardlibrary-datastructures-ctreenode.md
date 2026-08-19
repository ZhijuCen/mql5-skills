# CTreeNode

CTreeNode is a class of the CTree binary tree node.

Description

CTreeNode provides the ability to work with nodes of the [CTree](/en/docs/standardlibrary/datastructures/ctree) binary tree. Options of navigation through the tree are implemented in the class. Besides, methods of working with the file are implemented.

Declaration

```
   class CTreeNode : public CObject

```

Title

```
   #include <Arrays\TreeNode.mqh>

```

```
Inheritance hierarchy
   CObject
       CTreeNode
Direct descendants
CTree

```

### Class Methods by Groups

| Attributes |  |
| --- | --- |
| Owner | Gets/sets the pointer of the owner node |
| Left | Gets/sets the pointer of the left node |
| Right | Gets/sets the pointer of the right node |
| Balance | Gets the node balance |
| BalanceL | Gets the balance of the left sub-branch of the node |
| BalanceR | Gets the balance of the right sub-branch of the node |
| Creation of a new element |  |
| CreateSample | Creates a new node instance |
| Comparison |  |
| RefreshBalance | Recalculates the node balance |
| Search |  |
| GetNext | Gets the pointer of the next node |
| Input/Output |  |
| SaveNode | Saves the node data to a file |
| LoadNode | Downloads the node data from a file |
| virtual  Type | Gets the identifier of the node type |

```
Methods inherited from class CObject
Prev, Prev, Next, Next, Save, Load, Compare

```

Trees of CTreeNode class descendants have practical application.

A descendant of CTreeNode class should have predefined methods: [CreateSample](/en/docs/standardlibrary/datastructures/ctreenode/ctreenodecreatesample) creates a new instance of the descendant class of CTreeNode, [Compare](/en/docs/standardlibrary/cobject/cobjectcompare) compares values of key fields of the descendant class of CTreeNode, [Type](/en/docs/standardlibrary/cobject/cobjecttype) (if it is necessary to identify a node), [SaveNode](/en/docs/standardlibrary/datastructures/ctreenode/ctreenodesavenode) and [LoadNode](/en/docs/standardlibrary/datastructures/ctreenode/ctreenodeloadnode) (if it is necessary to work with a file).

Let's consider an example of a CTree descendant class.

```
//+------------------------------------------------------------------+
//|                                                   MyTreeNode.mq5 |
//|                        Copyright 2010, MetaQuotes Software Corp. |
//|                                       https://www.metaquotes.net/ |
//+------------------------------------------------------------------+
#property copyright "2010, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
//---
#include <Arrays\TreeNode.mqh>
//+------------------------------------------------------------------+
//| Describe CMyTreeNode class derived from CTreeNode.               |
//+------------------------------------------------------------------+
//| Class CMyTreeNode.                                               |
//| Purpose: Class of element of a binary tree.                      |
//|             Descendant of class CTreeNode.                       |
//+------------------------------------------------------------------+
class CMyTreeNode : public CTreeNode
  {
protected:
   //--- user's data
   long              m_long;            // key field of long type
   double            m_double;          // custom variable of double type
   string            m_string;          // custom variable of string type
   datetime          m_datetime;        // custom variable of datetime type
 
public:
                     CMyTreeNode();
   //--- methods of accessing user's data
   long              GetLong(void)                { return(m_long); }
   void              SetLong(long value)          { m_long=value;  }
   double            GetDouble(void)              { return(m_double); }
   void              SetDouble(double value)      { m_double=value;  }
   string            GetString(void)              { return(m_string); }
   void              SetString(string value)      { m_string=value;  }
   datetime          GetDateTime(void)            { return(m_datetime); }
   void              SetDateTime(datetime value)  { m_datetime=value;  }
   //--- methods for working with files
   virtual bool      Save(int file_handle);
   virtual bool      Load(int file_handle);
protected:
   virtual int       Compare(const CObject *node,int mode);
   //--- method of creating class instances
   virtual CTreeNode* CreateSample();
  };
//+------------------------------------------------------------------+
//| CMyTreeNode class constructor.                                   |
//| INPUT:  none.                                                    |
//| OUTPUT: none.                                                    |
//| REMARK: none.                                                    |
//+------------------------------------------------------------------+
void CMyTreeNode::CMyTreeNode()
  {
//--- initialization of user's data
   m_long        =0;
   m_double      =0.0;
   m_string      ="";
   m_datetime    =0;
  }
//+------------------------------------------------------------------+
//| Comparison with another tree node by the specified algorithm.    |
//| INPUT:  node - tree element to compare,                          |
//|         mode - identifier of comparison algorithm.               |
//| OUTPUT: result of comparison (>0,0,<0).                          |
//| REMARK: none.                                                    |
//+------------------------------------------------------------------+
int CMyTreeNode::Compare(const CObject *node,int mode)
  {
//--- mode parameter is ignored, because tree construction algorithm is the only one
   int res=0;
//--- explicit type casting
   CMyTreeNode *n=node;
   res=(int)(m_long-n.m_long);
//---
   return(res);
  }
//+------------------------------------------------------------------+
//| Creation of a new class instance.                                |
//| INPUT:  none.                                                    |
//| OUTPUT: pointer to a new instance of CMyTreeNode class.          |
//| REMARK: none.                                                    |
//+------------------------------------------------------------------+
CTreeNode* CMyTreeNode::CreateSample()
  {
   CMyTreeNode *result=new CMyTreeNode;
//---
   return(result);
  }
//+------------------------------------------------------------------+
//| Write tree node data to a file.                                  |
//| INPUT:  file_handle -handle of a file pre-opened for writing.    |
//| OUTPUT: true if OK, otherwise false.                             |
//| REMARK: none.                                                    |
//+------------------------------------------------------------------+
bool CMyTreeNode::Save(int file_handle)
  {
   uint i=0,len;
//--- checks
   if(file_handle<0) return(false);
//--- writing user data
//--- writing custom variable of long type
   if(FileWriteLong(file_handle,m_long)!=sizeof(long))          return(false);
//--- writing custom variable of double type
   if(FileWriteDouble(file_handle,m_double)!=sizeof(double))    return(false);
//--- writing custom variable of string type
   len=StringLen(m_string);
//--- write string length
   if(FileWriteInteger(file_handle,len,INT_VALUE)!=INT_VALUE)   return(false);
//--- write the string
   if(len!=0 && FileWriteString(file_handle,m_string,len)!=len) return(false);
//--- writing custom variable of datetime type
   if(FileWriteLong(file_handle,m_datetime)!=sizeof(long))      return(false);
//---
   return(true);
  }
//+------------------------------------------------------------------+
//| Read tree node data from a file.                                 |
//| INPUT:  file_handle -handle of a file pre-opened for reading.    |
//| OUTPUT: true if OK, otherwise false.                             |
//| REMARK: none.                                                    |
//+------------------------------------------------------------------+
bool CMyTreeNode::Load(int file_handle)
  {
   uint i=0,len;
//--- checks
   if(file_handle<0) return(false);
//--- reading
   if(FileIsEnding(file_handle)) return(false);
//--- reading custom variable of char type
//--- reading custom variable of long type
   m_long=FileReadLong(file_handle);
//--- reading custom variable of double type
   m_double=FileReadDouble(file_handle);
//--- reading custom variable of string type
//--- read the string length
   len=FileReadInteger(file_handle,INT_VALUE);
//--- read the string
   if(len!=0) m_string=FileReadString(file_handle,len);
   else       m_string="";
//--- reading custom variable of datetime type
   m_datetime=FileReadLong(file_handle);
//---
   return(true);
  }

```
