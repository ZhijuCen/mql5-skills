# GlobalVariableSetOnCondition

Sets the new value of the existing global variable if the current value equals to the third parameter check_value. If there is no global variable, the function will generate an error ERR_GLOBALVARIABLE_NOT_FOUND (4501) and return false.

```
bool  GlobalVariableSetOnCondition(
   string  name,            // Global variable name
   double  value,           // New value for variable if condition is true
   double  check_value      // Check value condition
   );

```

Parameters

name

[in]  The name of a global variable.

value

[in]  New value.

check_value

[in]   The value to check the current value of the global variable.

Return Value

If successful, the function returns true, otherwise it returns false. For details about the [error](/en/docs/constants/errorswarnings/errorcodes) call [GetLastError()](/en/docs/check/getlasterror). If the current value of the global variable is different from check_value, the function returns false.

Note

Function provides atomic access to the global variable, so it can be used for providing of a mutex at interaction of several Expert Advisors working simultaneously within one client terminal.

Example:

```
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
 
#property description   "To test the functionality of the GlobalVariableSetOnCondition function,"
#property description   "it is necessary to run the EA on several charts simultaneously."
 
#define   EXP_NAME      StringSubstr(__FILE__, 0, StringLen(__FILE__)-4)   // program name
#define   MUTEX         EXP_NAME+"_MUTEX"                                  // mutex global variable name
#define   DELAY         5000                                               // number of milliseconds of EA emulation
 
input long  InpExpMagic =  0; /* Expert magic number  */ // EA ID. If 0, the chart ID is used
 
union LongDouble              // union for writing and retrieving long values from double
  {
   long   lvalue;             // long value
   double dvalue;             // double value
  };
  
//--- EA global variables
long  ExtExpMagic;            // EA ID
ulong ExtStart;               // moment the EA "calculations" start
 
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- assign the chart ID to the EA ID if a zero value is specified
   ExtExpMagic=(InpExpMagic==0 ? ChartID() : InpExpMagic);
 
//--- create mutex, if there is an error, return an initialization error
   if(!MutexCreate())
      return(INIT_FAILED);
      
//--- successful initialization
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//--- if mutex is captured by the EA, release mutex
   if(MutexGetExpertID()==ExtExpMagic)
      MutexRelease();
      
//--- clean up
   Comment("");
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//--- if there is no mutex, create it; if there is an error, leave until the next tick
   if(!GlobalVariableCheck(MUTEX) && !MutexCreate())
      return;
      
//--- get the expert ID set in the terminal global variable
   long magic=MutexGetExpertID();
 
//--- if the ID belongs to the EA, simulate its work
   if(magic==ExtExpMagic)
     {
      //--- if the EA "work" is completed, release mutex
      if(EAProgressHandler(ExtStart))
         MutexRelease();
      return;
     }
//--- mutex captured by another EA
   else
     {
      //--- if mutex is already released
      if(magic==0)
        {
         //--- occupy mutex and remember the work access time
         if(MutexOccupy())
           {
            PrintFormat("%s: Mutex is occupied by %s",Symbol(), ExpertIDDescription());
            ExtStart=GetTickCount64();
           }
         return;
        }
      //--- mutex still occupied by another EA - work is prohibited
      else
         return;
     }
   /*
   result of running two identical EAs on EURUSD and AUDUSD charts:
   EURUSD: Mutex is occupied by Expert 133829812107724569
   EURUSD: Expert 133829812107724569 next tick
   EURUSD: Expert 133829812107724569 next tick
   EURUSD: Expert 133829812107724569 next tick
   EURUSD: Expert 133829812107724569 next tick
   EURUSD: Expert 133829812107724569 end
   EURUSD: Mutex is occupied by Expert 133829812107724569
   EURUSD: Expert 133829812107724569 next tick
   EURUSD: Expert 133829812107724569 next tick
   EURUSD: Expert 133829812107724569 next tick
   EURUSD: Expert 133829812107724569 next tick
   EURUSD: Expert 133829812107724569 next tick
   EURUSD: Expert 133829812107724569 end
   AUDUSD: Mutex is occupied by Expert 128968168951083984
   AUDUSD: Expert 128968168951083984 next tick
   AUDUSD: Expert 128968168951083984 next tick
   AUDUSD: Expert 128968168951083984 next tick
   AUDUSD: Expert 128968168951083984 next tick
   AUDUSD: Expert 128968168951083984 next tick
   AUDUSD: Expert 128968168951083984 next tick
   AUDUSD: Expert 128968168951083984 next tick
   AUDUSD: Expert 128968168951083984 end
   AUDUSD: Mutex is occupied by Expert 128968168951083984
   AUDUSD: Expert 128968168951083984 next tick
   AUDUSD: Expert 128968168951083984 next tick
   AUDUSD: Expert 128968168951083984 next tick
   AUDUSD: Expert 128968168951083984 next tick
   AUDUSD: Expert 128968168951083984 next tick
   AUDUSD: Expert 128968168951083984 end
   EURUSD: Mutex is occupied by Expert 133829812107724569
   EURUSD: Expert 133829812107724569 next tick
   EURUSD: Expert 133829812107724569 next tick
   EURUSD: Expert 133829812107724569 next tick
   EURUSD: Expert 133829812107724569 next tick
   EURUSD: Expert 133829812107724569 next tick
   EURUSD: Expert 133829812107724569 next tick
   EURUSD: Expert 133829812107724569 end
   EURUSD: Mutex is occupied by Expert 133829812107724569
   EURUSD: Expert 133829812107724569 next tick
   EURUSD: Expert 133829812107724569 next tick
   EURUSD: Expert 133829812107724569 next tick
   EURUSD: Expert 133829812107724569 next tick
   EURUSD: Expert 133829812107724569 end
   AUDUSD: Mutex is occupied by Expert 128968168951083984
   AUDUSD: Expert 128968168951083984 next tick
   AUDUSD: Expert 128968168951083984 next tick
   AUDUSD: Expert 128968168951083984 next tick
   AUDUSD: Expert 128968168951083984 next tick
   AUDUSD: Expert 128968168951083984 next tick
   AUDUSD: Expert 128968168951083984 next tick
   AUDUSD: Expert 128968168951083984 next tick
   AUDUSD: Expert 128968168951083984 end
   EURUSD: Mutex is occupied by Expert 133829812107724569
   EURUSD: Expert 133829812107724569 next tick
   EURUSD: Expert 133829812107724569 next tick
   EURUSD: Expert 133829812107724569 next tick
   EURUSD: Expert 133829812107724569 next tick
   EURUSD: Expert 133829812107724569 next tick
   EURUSD: Expert 133829812107724569 end
   
  we can see that the first EA to occupy mutex is the one, in which the tick arrived first
  after the completion of the work cycle, if the tick came first again here,
  the same EA occupies mutex again
   */
  }
//+------------------------------------------------------------------+
//| EA operation handler emulator                                    |
//+------------------------------------------------------------------+
bool EAProgressHandler(ulong start)
  {
   //--- if the specified time has passed since the handler started working
   if(GetTickCount64()-start>=DELAY)
     {
      //--- report to the journal about the completion of the handler,
      //--- set a new start time for the handler and return 'true'
      PrintFormat("%s: %s end", Symbol(), ExpertIDDescription());
      start=GetTickCount64();
      return(true);
     }
   //--- operation time of the EA calculation emulator has not yet been completed -
   //--- report the next tick in the journal
   else
     {
      PrintFormat("%s: %s next tick", Symbol(), ExpertIDDescription());
     }
//--- work time has not yet ended - return 'false'
   return(false);
  }
//+------------------------------------------------------------------+
//| Create mutex, set it to the locked state                         |
//+------------------------------------------------------------------+
bool MutexCreate(void)
  {
   if(!GlobalVariableCheck(MUTEX))
     {
      LongDouble magic={};
      magic.lvalue=ExtExpMagic;
      ResetLastError();
      if(!GlobalVariableSet(MUTEX, magic.dvalue))
        {
         PrintFormat("%s: GlobalVariableSet() failed. Error %d",__FUNCTION__, GetLastError());
         return(false);
        }
     }
   return(true);
  }
//+------------------------------------------------------------------+
//| Capture mutex                                                    |
//+------------------------------------------------------------------+
bool MutexOccupy(void)
  {
   if(!GlobalVariableCheck(MUTEX))
     {
      PrintFormat("%s: Error! Mutex is missing. First create it with MutexCreate()",__FUNCTION__);
      return(false);
     }
   LongDouble magic={};
   magic.lvalue=ExtExpMagic;
   ResetLastError();
   if(!GlobalVariableSetOnCondition(MUTEX, magic.dvalue, 0))
     {
      PrintFormat("%s: GlobalVariableSetOnCondition() failed. Error %d",__FUNCTION__, GetLastError());
      return(false);
     }
   return(true);
  }
//+------------------------------------------------------------------+
//| Release mutex                                                    |
//+------------------------------------------------------------------+
bool MutexRelease(void)
  {
   if(!GlobalVariableCheck(MUTEX))
     {
      PrintFormat("%s: Error! Mutex is missing. First create it with MutexCreate()",__FUNCTION__);
      return(false);
     }
   LongDouble magic={};
   magic.lvalue=ExtExpMagic;
   ResetLastError();
   if(!GlobalVariableSetOnCondition(MUTEX, 0, magic.dvalue))
     {
      PrintFormat("%s: GlobalVariableSetOnCondition() failed. Error %d",__FUNCTION__, GetLastError());
      return(false);
     }
   return(true);
  }
//+------------------------------------------------------------------+
//| Return mutex value                                               |
//+------------------------------------------------------------------+
long MutexGetExpertID(void)
  {
   LongDouble magic={};
   ResetLastError();
   if(!GlobalVariableGet(MUTEX, magic.dvalue))
     {
      PrintFormat("%s: GlobalVariableGet() failed. Error %d",__FUNCTION__, GetLastError());
      return(WRONG_VALUE);
     }
   return(magic.lvalue);
  }
//+------------------------------------------------------------------+
//| Return EA ID as a string                                         |
//+------------------------------------------------------------------+
string ExpertIDDescription(void)
  {
   return("Expert "+(string)ExtExpMagic);
  }

```
