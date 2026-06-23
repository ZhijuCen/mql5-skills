# CTree

CTree is a class of the binary tree of the instances of CTreeNode class and its descendants.

Description

CTree class provides the possibility to work with the binary tree of [CTreeNode](/en/docs/standardlibrary/datastructures/ctreenode) class instances and its descendants. Options of adding/inserting/deleting of tree elements and search in the tree are implemented in the class. Besides that, methods of working with a file are implemented.

Note that mechanism of dynamic memory management is not implemented in class CTree (unlike classes [CList](/en/docs/standardlibrary/datastructures/clist) and [CArrayObj](/en/docs/standardlibrary/datastructures/carrayobj)). All tree nodes are deleted with memory deallocation.

Declaration

```
   class CTree : public CTreeNode

```

Title

```
   #include <Arrays\Tree.mqh>

```

```
Inheritance hierarchy
   CObject
       CTreeNode
           CTree

```

### Class Methods by Groups

| Attributes |  |
| --- | --- |
| Root | Gets the root node of the tree |
| Creation of a new element |  |
| CreateElement | Creates a new instance of the node |
| Filling |  |
| Insert | Adds a node to a tree |
| Deletion |  |
| Detach | Detaches a specified node from a tree |
| Delete | Deletes a specified node from a tree |
| Clear | Deletes all nodes of a tree |
| Search |  |
| Find | Searches for a node in a tree by sample |
| Input/output |  |
| virtual  Save | Saves all the tree data to a file |
| virtual  Load | Downloads tree data from a file |
| virtual  Type | Gets identifier of the tree type |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Compare |
| --- |
| Methods inherited from class CTreeNode 
 Parent, Parent,  Left ,  Left ,  Right ,  Right ,  Balance ,  BalanceL ,  BalanceR ,  RefreshBalance ,  GetNext ,  SaveNode ,  LoadNode |

Trees of CTreeNode class descendants – descendants of class CTree - have practical application.

Descendant of CTree class should have a predefined method [CreateElement](/en/docs/standardlibrary/datastructures/ctree/ctreecreateelement) that creates a new instance of the [CTreeNode](/en/docs/standardlibrary/datastructures/ctreenode) descendant class.

Let's consider an example of the CTree descendant class.

```
//+------------------------------------------------------------------+
//|                                                       MyTree.mq5 |
//|                        Copyright 2010, MetaQuotes Software Corp. |
//|                                       https://www.metaquotes.net/ |
//+------------------------------------------------------------------+
#property copyright "2010, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
//---
#include <Arrays\Tree.mqh>
#include "MyTreeNode.mqh"
//---
input int extCountedNodes = 100;
//+------------------------------------------------------------------+
//| Describe class CMyTree derived from CTree.                       |
//+------------------------------------------------------------------+
//| Class CMyTree.                                                   |
//| Purpose: Construction and navigation of a binary search tree.    |
//+------------------------------------------------------------------+
class CMyTree : public CTree
  {
public:
   //--- methods of searching in the tree by custom data
   CMyTreeNode*        FindByLong(long find_long);
   //--- method of creation of the tree element
   virtual CTreeNode *CreateElement();
  };
//---
CMyTree MyTree;
//+------------------------------------------------------------------+
//| Creation of a new tree node.                                     |
//| INPUT:  none.                                                    |
//| OUTPUT: pointer to the new tree node if OK, or NULL.             |
//| REMARK: none.                                                    |
//+------------------------------------------------------------------+
CTreeNode *CMyTree::CreateElement()
  {
   CMyTreeNode *node=new CMyTreeNode;
//---
   return(node);
  }
//+------------------------------------------------------------------+
//| Search of element in a list by value m_long.                     |
//| INPUT:  find_long - searched value.                              |
//| OUTPUT: pointer of a found list element, or NULL.                |
//| REMARK: none.                                                    |
//+------------------------------------------------------------------+
CMyTreeNode* CMyTree::FindByLong(long find_long)
  {
   CMyTreeNode *res=NULL;
   CMyTreeNode *node;
//--- create a tree node to pass the search parameter
   node=new CMyTreeNode;
   if(node==NULL) return(NULL);
   node.SetLong(find_long);
//---
   res=Find(node);
   delete node;
//---
   return(res);
  }
//+------------------------------------------------------------------+
//| script "testing of class CMyTree"                                |
//+------------------------------------------------------------------+
//---  array for string initialization
string str_array[11]={"p","oo","iii","uuuu","yyyyy","ttttt","rrrr","eee","ww","q","999"};
//---
int OnStart() export
  {
   int          i;
   uint         pos;
   int          beg_time,end_time;
   CMyTreeNode *node; //--- temporary pointer to the sample of class CMyTreeNode 
//---  
   printf("Start test %s.",__FILE__);
//--- Fill out MyTree with instances of class MyTreeNode in the amount of extCountedNodes.
   beg_time=GetTickCount();
   for(i=0;i<extCountedNodes;i++)
     {
      node=MyTree.CreateElement();
      if(node==NULL)
        {
         //--- emergency exit
         printf("%s (%4d): create error",__FILE__,__LINE__);
         return(__LINE__);
        }
      NodeSetData(node,i);
      node.SetLong(i);
      MyTree.Insert(node);
     }
   end_time=GetTickCount();
   printf("Filling time of MyTree is %d ms.",end_time-beg_time);
//--- Create a temporary tree TmpMyTree.
   CMyTree TmpMyTree;
//--- Detach 50% of tree elements (all even)
//--- and add them to the temporary tree TmpMyTree.
   beg_time=GetTickCount();
   for(i=0;i<extCountedNodes;i+=2)
     {
      node=MyTree.FindByLong(i);
      if(node!=NULL)
         if(MyTree.Detach(node)) TmpMyTree.Insert(node);
     }
   end_time=GetTickCount();
   printf("Deletion time of %d elements from MyTree is %d ms.",extCountedNodes/2,end_time-beg_time);
//--- Return the detached
   node=TmpMyTree.Root();
   while(node!=NULL)
     {
      if(TmpMyTree.Detach(node)) MyTree.Insert(node);
      node=TmpMyTree.Root();
     }
//--- Check work of method Save(int file_handle);
   int file_handle;
   file_handle=FileOpen("MyTree.bin",FILE_WRITE|FILE_BIN|FILE_ANSI);
   if(file_handle>=0)
     {
      if(!MyTree.Save(file_handle))
        {
         //--- error writing to a file
         //--- emergency exit
         printf("%s: Error %d in %d!",__FILE__,GetLastError(),__LINE__);
         //--- close file before leaving!!!
         FileClose(file_handle);
         return(__LINE__);
        }
      FileClose(file_handle);
     }
//--- Check work of method Load(int file_handle);
   file_handle=FileOpen("MyTree.bin",FILE_READ|FILE_BIN|FILE_ANSI);
   if(file_handle>=0)
     {
      if(!TmpMyTree.Load(file_handle))
        {
         //--- error reading from file
         //--- emergency exit
         printf("%s: Error %d in %d!",__FILE__,GetLastError(),__LINE__);
         //--- close file before leaving!!!
         FileClose(file_handle);
         return(__LINE__);
        }
      FileClose(file_handle);
     }
//---
   MyTree.Clear();
   TmpMyTree.Clear();
//---
   printf("End test %s. OK!",__FILE__);
//---
   return(0);
  }
//+------------------------------------------------------------------+
//| Function to output node contents to journal                      | 
//+------------------------------------------------------------------+
void NodeToLog(CMyTreeNode *node)
  {
   printf("   %I64d,%f,'%s','%s'",
               node.GetLong(),node.GetDouble(),
               node.GetString(),TimeToString(node.GetDateTime()));
  }
//+------------------------------------------------------------------+
//| Function to populate node with random values                     | 
//+------------------------------------------------------------------+
void NodeSetData(CMyTreeNode *node,int mode)
  {
   if(mode%2==0)
     {
      node.SetLong(mode*MathRand());
      node.SetDouble(MathPow(2.02,mode)*MathRand());
     }
   else
     {
      node.SetLong(mode*(long)(-1)*MathRand());
      node.SetDouble(-MathPow(2.02,mode)*MathRand());
     }
   node.SetString(str_array[mode%10]);
   node.SetDateTime(10000*mode);
  }

```
