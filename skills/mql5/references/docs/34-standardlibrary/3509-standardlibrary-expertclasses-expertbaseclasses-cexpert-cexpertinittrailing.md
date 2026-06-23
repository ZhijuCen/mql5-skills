# InitTrailing

Initializes trailing stop object.

```
virtual bool  InitTrailing(
   CExpertTrailing*     trailing=NULL,        // pointer
   )

```

Parameters

trailing

[in]  Pointer to [CExpertTrailing](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexperttrailing) class object (or its descendant).

Return Value

true - successful, otherwise - false.

Note

If trailing is NULL, the  [ExpertTrailing](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexperttrailing) class will be used for initialization (it does nothing).
