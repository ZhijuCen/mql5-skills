# CiCustom

CiCustom is a class intended for using the custom technical indicators.

### Description

CiCustom class provides the creation, setup, and access to the data of a custom indicator.

### Declaration

```
   class CiCustom: public CIndicator

```

### Title

```
   #include <Indicators\Custom.mqh>

```

### Class Methods by Groups

| Attributes |  |
| --- | --- |
| NumBuffers | Sets the number of buffers |
| NumParams | Gets the number of parameters used when creating an indicator |
| ParamType | Gets the type of the specified parameter |
| ParamLong | Gets the value of the specified parameter of integer type |
| ParamDouble | Gets the value of the specified parameter of double type |
| ParamString | Gets the value of the specified parameter of string type |
| Input/output |  |
| virtual  Type | Virtual identification method |
