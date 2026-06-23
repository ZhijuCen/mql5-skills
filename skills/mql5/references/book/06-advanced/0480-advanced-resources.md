# Resources

The operation of MQL programs may require many auxiliary resources, which are arrays of application data or files of various types, including images, sounds, and fonts. The MQL development environment allows you to include all such resources in the executable file at the compilation stage. This eliminates the need for their parallel transfer and installation along with the main program and makes it a complete self-sufficient product that is convenient for the end user.

In this chapter, we will learn how to describe different types of resources and built-in functions for subsequent operations with connected resources.

Raster images, represented as arrays of points (pixels) in the widely recognized BMP format, hold a unique position among resources. The MQL5 API allows the creation, manipulation, and dynamic display of these graphic resources on charts.

Earlier, we already discussed graphical objects and, in particular, objects of types [OBJ_BITMAP](/en/book/applications/objects/objects_time_price) and [OBJ_BITMAP_LABEL](/en/book/applications/objects/objects_screen_coordinates) that are useful for designing user interfaces. For these objects, there is the [OBJPROP_BMPFILE](/en/book/applications/objects/objects_bitmap) property that specifies the image as a file or resource. Previously, we only considered examples with files. Now we will learn how to work with resource images.
