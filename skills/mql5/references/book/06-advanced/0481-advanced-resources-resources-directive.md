# Describing resources using the #resource directive

To include a resource file in the compiled program version, use the #resource directive in the source code. The directive has different forms depending on the file type. In any case, the directive contains the #resource keyword followed by a constant string.

```
#resource "path_file_name"

```

The #resource command instructs the compiler to include (in binary format ex5) a file with the specified name and, optionally, location (at the time of compilation) into the executable program being generated. The path is optional: if the string contains only the file name, it is searched in the directory next to the compiled source code. If there is a path in the string, the rules described below apply.

The compiler looks for the resource at the specified path in the following sequence:

- If the path is preceded by a backslash '\\' (it must be doubled, since a single backslash is a control character; in particular, '\' is used for newlines '\r', '\n' and tabs '\t'), then the resource is searched starting from the MQL5 folder inside the terminal data directory.
- If there is no backslash, then the resource is searched relative to the location of the source file in which this resource is registered.

Note that in constant strings with resource paths, you must use double backslashes as separators. Forward single slashes are not supported here, unlike paths in the file system.

For example:

```
#resource "\\Images\\euro.bmp" // euro.bmp is in /MQL5/Images/
#resource "picture.bmp"        // picture.bmp is in the same directory,
                               // where the source file is (mq5 or mqh)
#resource "Resource\\map.bmp"  // map.bmp is in the Resource subfolder of the directory
                               // where the source file is (mq5 or mqh)

```

If the resource is declared with a relative path in the mqh header file, the path is considered relative to this mqh file and not to the mq5 file of the program being compiled.

The substrings "..\\" and ":\\" are not allowed in the resource path.

Using a few directives, you can, for example, put all the necessary pictures and sounds directly into the ex5 file. Then, to run such a program in another terminal, you do not need to transfer them separately. We will consider programmatic ways of accessing resources from MQL5 in the following sections.

The length of the constant string "path_file_name" must not exceed 63 characters. The resource file size cannot be more than 128 Mb. Resource files are automatically compressed before being included in the executable.

After the resource is declared by the #resource directive, it can be used in any part of the program. The name of the resource becomes the constant string specified in the directive without a slash at the beginning (if any), and a special sign of the resource (two colons, "::") should be added before the contents of the string.

Below we present examples of resources, with their names in the comments.

```
#resource "\\Images\\euro.bmp"          // resource name - ::Images\\euro.bmp
#resource "picture.bmp"                 // resource name - ::picture.bmp
#resource "Resource\\map.bmp"           // resource name - ::Resource\\map.bmp
#resource "\\Files\\Pictures\\good.bmp" // resource name - ::Files\\Pictures\\good.bmp
#resource "\\Files\\demo.wav";          // resource name - ::Files\\demo.wav"
#resource "\\Sounds\\thrill.wav";       // resource name - ::Sounds\\thrill.wav"

```

Further in the MQL code, you can refer to these resources as follows (here, only the [ObjectSetString](/en/book/applications/objects/objects_properties_get_set) and [PlaySound](/en/book/common/output/output_sound) functions are already known to us, but there are other options like [ResourceReadImage](/en/book/advanced/resources/resources_resourcereadimage), which will be described in the following sections).

```
ObjectSetString(0, bitmap_name, OBJPROP_BMPFILE, 0, "::Images\\euro.bmp");
...
ObjectSetString(0, my_bitmap, OBJPROP_BMPFILE, 0, "::picture.bmp");
...
ObjectSetString(0, bitmap_label, OBJPROP_BMPFILE, 0, "::Resource\\map.bmp");
ObjectSetString(0, bitmap_label, OBJPROP_BMPFILE, 1, "::Files\\Pictures\\good.bmp");
...
PlaySound("::Files\\demo.wav");
...
PlaySound("::Sounds\\thrill.wav");

```

It should be noted that when setting an image from a resource to OBJ_BITMAP and OBJ_BITMAP_LABEL objects, the value of the OBJPROP_BMPFILE property cannot be changed manually (in the object's properties dialog).

Note that wav files are set by default for the PlaySound function relative to the Sounds folder (or its subfolders) located in the terminal's data directory. At the same time, resources (including sound ones), if they are described with a leading slash in the path, are searched inside the MQL5 directory. Therefore, in the example above, the "\\Sounds\\thrill.wav" string refers to the file MQL5/Sounds/thrill.wav and not to Sounds/thrill.wav relative to the data directory (there is indeed the Sounds directory with standard terminal sounds).

The simple syntax of the #resource directive discussed above allows the description of only image resources (BMP format) and sound resources (WAV format). Attempting to describe a file of a different type as a resource will result in an "unknown resource type" error.

As a result of #resource directive processing, the files in fact become embedded into the executable binary program and become accessible by the resource name. Moreover, you should pay attention to a special property of such resources which is their public availability from other programs (more on this in the next section).

MQL5 also supports another way of embedding a file in a program:  in the form of a [resource variable](/en/book/advanced/resources/resources_variables). This method uses extended syntax of the #resource directive and allows you to connect not only BMP or WAV files but also others, for example, text or an array of structures.

We will analyze a practical example of connecting resources in a couple of sections.
