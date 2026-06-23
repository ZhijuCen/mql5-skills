# Deleting dynamic resources: ResourceFree

The ResourceFree function removes the previously created dynamic resource and frees the memory it occupies. If you don't call ResourceFree, the dynamic resource will remain in memory until the end of the current terminal session. This can be used as a convenient way to store data, but for regular work with images, it is recommended to release them when the need for them disappears.

Graphical objects attached to the resource being deleted will be displayed correctly even after its deletion. However, newly created graphical objects (OBJ_BITMAP and OBJ_BITMAP_LABEL) will no longer be able to use the deleted resource.

bool ResourceFree(const string resource)

The resource name is set in the resource parameter and must start with "::".

The function returns an indicator of success (true) or error (false).

The function deletes only dynamic resources created by the given MQL program, but not "third-party" ones.

In the previous section, we saw an example of the script ARGBbitmap.mq5, which called ResourceFree upon completion of its operation.
