# CColorGenerator

CColorGenerator class is an auxiliary graphics library class for working with the color palette.

### Description

The CColorGenerator class contains the initial color palette used for curves by default (if a color is not specified by a user).

If all colors from the initial palette are used already, new colors are automatically generated and the palette is refilled.

### Declaration

```
   class CColorGenerator

```

### Title

```
   #include <Graphics\ColorGenerator.mqh>

```

### Class methods

| Method | Description |
| --- | --- |
| Next | Returns the next color from the palette |
| Reset | Resets the generator |
