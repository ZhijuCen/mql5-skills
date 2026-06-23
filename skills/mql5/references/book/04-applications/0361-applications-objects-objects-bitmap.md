# Adjusting images in bitmap objects

Objects of OBJ_BITMAP_LABEL type (a panel with a picture positioned in screen coordinates) allow displaying bitmap images. Bitmap images mean the BMP graphic format: although in principle there are many other raster formats (for example, PNG or GIF), they are currently not supported in MQL5, just like vector ones.

The string property OBJPROP_BMPFILE allows you to specify an image for an object. It must contain the name of the BMP file or [resource](/en/book/advanced/resources).

Since this object supports the possibility of two-position state switching (see [OBJPROP_STATE](/en/book/applications/objects/objects_pressed_state)), a modifier parameter should be used for it: a picture for the "on"/"pressed" state is set under index 0, and the "off"/"released" state is set under index 1. If you specify only one picture (no modifier, which is equivalent to 0), it will be used for both states. The default state of an object is "off"/"released".

The size of the object becomes equal to the size of the image, but it can be changed by specifying smaller values in the OBJPROP_XSIZE and OBJPROP_YSIZE properties: in this case, only a part of the image is displayed (for details, see the next section on [framing](/en/book/applications/objects/objects_bitmap_offset)).

The length of the OBJPROP_BMPFILE string must not exceed 63 characters. It can contain not only the file name but also the path to it. If the string starts with a path separator character (forward slash '/' or double backslash '\\'), then the file is searched relative to terminal_data_directory/MQL5/. Otherwise, the file is searched relative to the folder where the MQL program is located.

For example, the string "\\Images\\euro.bmp" (or "/Images/euro.bmp") refers to a file in the directory MQL5/Images/euro.bmp. The standard terminal delivery pack includes the Images folder in the MQL5 directory, and there are a couple of test files euro.bmp and dollar.bmp, so the path is working. If you specify the string "Images\\euro.bmp" or ("Images/euro.bmp"), then this will imply, for example, for a script launched from MQL5/Scripts/MQL5Book/, that the Images folder with the euro.bmp file should be located directly there, that is, the whole path will be MQL5/Scripts/MQL5Book/Images/euro.bmp. There is no such file in our book, and this would lead to an error loading the image. However, this arrangement of graphic files next to the program has its advantages: it is easier to control the assembly, and there is no confusion with mixed pictures of different programs.

The ObjectBitmap.mq5 script creates a panel with an image on the chart and assigns two images to it: "\\Images\\dollar.bmp" and "\\Images\\euro.bmp".

```
#include "ObjectPrefix.mqh"
   
void SetupBitmap(const string button, const int x, const int y,
   const string imageOn, const string imageOff = NULL)
{
   // creating a panel
   const string name = ObjNamePrefix + "Bitmap";
   ObjectCreate(0, name, OBJ_BITMAP_LABEL, 0, 0, 0);
   // set position
   ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y);
   // include images
   ObjectSetString(0, name, OBJPROP_BMPFILE, 0, imageOn);
   if(imageOff != NULL) ObjectSetString(0, name, OBJPROP_BMPFILE, 1, imageOff);
}
   
void OnStart()
{
   SetupBitmap("image", 100, 100,
      "\\Images\\dollar.bmp", "\\Images\\euro.bmp");
}

```

As with the result of the script from the previous section, here you can also click on the picture object and see that it switches from the dollar to the euro image and back.
