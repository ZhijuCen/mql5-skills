# Alignment

Sets alignment parameters of the control.

```
void  Alignment(
   const int  flags,      // flags
   const int  left,       // offset
   const int  top,        // offset
   const int  right,      // offset
   const int  bottom      // offset
   )

```

Parameters

flags

[in]  Alignment flags.

left

[in]  Fixed offset from the left border.

top

[in]  Fixed offset from the top border.

right

[in]  Fixed offset from the right border.

bottom

[in]  Fixed offset from the bottom border.

Return Value

None.

Note

Alignement flags:

```
enum WND_ALIGN_FLAGS
{
   WND_ALIGN_NONE=0,                                  // no align
   WND_ALIGN_LEFT=1,                                  // align left
   WND_ALIGN_TOP=2,                                   // align top
   WND_ALIGN_RIGHT=4,                                 // align right
   WND_ALIGN_BOTTOM=8,                                // align bottom
   WND_ALIGN_WIDTH = WND_ALIGN_LEFT|WND_ALIGN_RIGHT,  // align width
   WND_ALIGN_HEIGHT=WND_ALIGN_TOP|WND_ALIGN_BOTTOM,   // align height
   WND_ALIGN_CLIENT=WND_ALIGN_WIDTH|WND_ALIGN_HEIGHT, // align height and width
   }

```
