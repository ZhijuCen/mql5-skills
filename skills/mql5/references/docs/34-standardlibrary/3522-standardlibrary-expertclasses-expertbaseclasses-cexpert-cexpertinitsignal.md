# InitSignal

Initializes trading signal object.

```
virtual bool  InitSignal(
   CExpertSignal*     signal=NULL,        // pointer
   )

```

Parameters

signal

[in]  Pointer to [CExpertSignal](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertsignal) class object (or its descendant).

Return Value

true - successful, otherwise - false.

Note

If signal is NULL, the [CExpertSignal](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertsignal) class will be used for initialization (it does nothing).
