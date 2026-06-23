# Shared use of resources of different MQL programs

The resource name is unique throughout the terminal. Later we will learn how to create resources not at the compilation stage (by the #resource directive) but dynamically, using the [ResourceCreate](/en/book/advanced/resources/resources_resourcecreate) function. In any case, the resource is declared in the context of the program that creates it, so that the uniqueness of the full name is provided automatically by binding to the file system (path and name of a specific file ex5).

In addition to containing and using resources, an MQL program can also access the resources of another compiled program (ex5 file). This is possible provided that the program using the resource knows the location path and the name of another program containing the required resource, as well as the name of this resource.

Thus, the terminal provides an important property of resources which is their shared use: resources from one ex5 file can be used in many other programs.

In order to use a resource from a third-party ex5 file, it must be specified in the form "path_file_name.ex5::resource_name". For example, let's say the script DrawingScript.mq5 refers to a specified image resource in the file triangle.bmp:

```
#resource "\\Files\\triangle.bmp"

```

Then its name for use in the actual script will look like "::Files\\triangle.bmp".

To use the same resource from another program, for example, an Expert Advisor, the resource name should be preceded by the path of the ex5 script file relative to the MQL5 folder in the terminal data directory, as well as the name of the script itself (in the compiled form, DrawingScript.ex5). Let the script be in the standard MQL5/Scripts/ folder. In this case, the image should be accessed using the "\\Scripts\\DrawingScript.ex5::Files\\triangle.bmp" string. The ".ex5" extension is optional.

If, when accessing the resource of another ex5 file, the path to this file is not specified, then such a file is searched in the same folder where the program requesting the resource is located. For example, if we assume that the same Expert Advisor is in the standard MQL5/Experts/ folder, and it queries a resource without specifying the path (for example, "DrawingScript.ex5::Files\\triangle.bmp"), then DrawingScript.ex5 will be searched in the MQL5/Experts/ folder.

Due to the shared use of resources, their dynamic creation and updating can be used to exchange data between MQL programs. This happens right in memory and is therefore a good alternative to files or global variables.

Please note that to load a resource from an MQL program, you do not need to run it: to read resources, it is enough to have an ex5 file with resources.

An important exception during which report sharing is not possible is when a resource is described in the form of a [resource variable](/en/book/advanced/resources/resources_variables).
